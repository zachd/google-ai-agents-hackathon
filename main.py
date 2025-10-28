from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import json
import os
import base64
import traceback
from dotenv import load_dotenv
import uuid

from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google import genai
from google.genai import types

from game_master.agent import root_agent

load_dotenv()

# Initialize ADK services
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()

# Configuration for conversation history management
MAX_HISTORY_MESSAGES = 20  # Keep last 20 messages to prevent token overflow

app = FastAPI(title="Mystery Trip Planner API", version="1.0.0")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    message: str
    artifacts: Optional[Dict[str, Any]] = None

async def truncate_session_history(session, max_messages: int = MAX_HISTORY_MESSAGES):
    """
    Truncate session history to prevent token overflow.
    Keeps only the most recent messages and a system message if present.
    """
    if not session or not hasattr(session, 'history') or not session.history:
        return session
    
    history = session.history
    
    # If history is within limits, return as-is
    if len(history) <= max_messages:
        return session
    
    print(f"Truncating history from {len(history)} to {max_messages} messages")
    
    # Keep the first message if it's a system message, then keep the last N messages
    new_history = []
    
    # Check if first message is system/important context
    if history and hasattr(history[0], 'role') and history[0].role == 'system':
        new_history.append(history[0])
        # Keep last (max_messages - 1) messages
        new_history.extend(history[-(max_messages - 1):])
    else:
        # Just keep last max_messages
        new_history = history[-max_messages:]
    
    # Update session history
    session.history = new_history
    
    # Update session in service
    await session_service.update_session(session)
    
    return session

@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
    return {"status": "healthy", "service": "mystery-trip-planner"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint that streams responses from the ADK agent"""
    
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        user_id = "web-user"
        
        async def generate_response():
            """Generator function for streaming responses"""
            try:
                # Get or create session
                session = None
                try:
                    session = await session_service.get_session(
                        app_name="mystery-trip-planner",
                        user_id=user_id,
                        session_id=session_id
                    )
                except Exception as e:
                    print(f"Session not found, creating new: {e}")
                
                if session is None:
                    # Session doesn't exist, create it
                    session = await session_service.create_session(
                        state={},
                        app_name="mystery-trip-planner",
                        user_id=user_id,
                        session_id=session_id
                    )
                
                if session is None:
                    raise Exception("Failed to create or retrieve session")
                
                # Truncate session history to prevent token overflow
                session = await truncate_session_history(session)
                
                # Create message content
                content = types.Content(
                    role="user",
                    parts=[types.Part(text=request.message)]
                )
                
                # Create runner
                runner = Runner(
                    app_name="mystery-trip-planner",
                    agent=root_agent,
                    artifact_service=artifact_service,
                    session_service=session_service,
                )
                
                # Stream events from the agent
                events = runner.run_async(
                    session_id=session.id,
                    user_id=user_id,
                    new_message=content
                )
                
                event_count = 0
                async for event in events:
                    event_count += 1
                    try:
                        # Handle different event types
                        # Check if event has content
                        if hasattr(event, 'content') and event.content:
                            # Process content parts
                            if hasattr(event.content, 'parts') and event.content.parts:
                                for part in event.content.parts:
                                    # Handle text parts
                                    if hasattr(part, 'text') and part.text:
                                        response_data = {
                                            "session_id": session_id,
                                            "message": part.text,
                                            "type": "message"
                                        }
                                        yield f"data: {json.dumps(response_data)}\n\n"
                                    
                                    # Handle inline_data artifacts (images)
                                    if hasattr(part, 'inline_data') and part.inline_data:
                                        try:
                                            mime_type = part.inline_data.mime_type or "image/png"
                                            data_b64 = base64.b64encode(part.inline_data.data).decode('utf-8')
                                            data_uri = f"data:{mime_type};base64,{data_b64}"
                                            
                                            artifact_data = {
                                                "session_id": session_id,
                                                "type": "artifact",
                                                "artifact": {
                                                    "filename": f"artifact_{session_id}_{int(asyncio.get_event_loop().time())}.png",
                                                    "mime_type": mime_type,
                                                    "uri": data_uri
                                                }
                                            }
                                            yield f"data: {json.dumps(artifact_data)}\n\n"
                                        except Exception as artifact_error:
                                            print(f"Error processing artifact: {artifact_error}")
                                    
                                    # Handle function responses that might contain image data
                                    if hasattr(part, 'function_response') and part.function_response:
                                        try:
                                            response_data = part.function_response.response
                                            # Check if this is a tool response with image data
                                            if isinstance(response_data, dict) and 'image_data' in response_data:
                                                mime_type = response_data.get('mime_type', 'image/png')
                                                image_data = response_data['image_data']
                                                filename = response_data.get('filename', f"image_{session_id}_{int(asyncio.get_event_loop().time())}.png")
                                                
                                                data_b64 = base64.b64encode(image_data).decode('utf-8')
                                                data_uri = f"data:{mime_type};base64,{data_b64}"
                                                
                                                artifact_data = {
                                                    "session_id": session_id,
                                                    "type": "artifact",
                                                    "artifact": {
                                                        "filename": filename,
                                                        "mime_type": mime_type,
                                                        "uri": data_uri
                                                    }
                                                }
                                                yield f"data: {json.dumps(artifact_data)}\n\n"
                                        except Exception as function_error:
                                            print(f"Error processing function response: {function_error}")
                    except Exception as event_error:
                        print(f"Error processing event {event_count}: {event_error}")
                        traceback.print_exc()
                
                print(f"Processed {event_count} events successfully")
                
                # Send completion signal AFTER all events are processed
                yield f"data: {json.dumps({'type': 'done', 'session_id': session_id})}\n\n"
                
            except Exception as e:
                error_msg = f"Error processing request: {str(e)}\n{traceback.format_exc()}"
                print(error_msg)  # Log to console
                error_data = {
                    "session_id": session_id,
                    "type": "error",
                    "message": str(e)
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear-session")
async def clear_session(session_id: str):
    """Clear conversation history for a session"""
    try:
        user_id = "web-user"
        
        # Try to get the session
        try:
            session = await session_service.get_session(
                app_name="mystery-trip-planner",
                user_id=user_id,
                session_id=session_id
            )
            
            if session:
                # Clear the history
                session.history = []
                await session_service.update_session(session)
                return {"status": "success", "message": "Session history cleared"}
            else:
                return {"status": "not_found", "message": "Session not found"}
                
        except Exception as e:
            return {"status": "not_found", "message": "Session not found"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Mystery Trip Planner API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat (POST)",
            "clear-session": "/clear-session (POST)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
