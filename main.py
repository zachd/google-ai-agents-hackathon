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

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Mystery Trip Planner API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat (POST)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
