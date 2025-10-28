#!/usr/bin/env python3
"""
Simple integration test for the Mystery Trip Planner
Tests the full stack: Frontend API -> Backend -> ADK Agents
"""
import asyncio
import sys
from main import app, session_service, artifact_service
from game_master.agent import root_agent
from google.adk.runners import Runner
from google.genai import types

async def test_agent():
    """Test that the agent can respond to a simple query"""
    print("🧪 Testing ADK agent integration...")
    
    try:
        session_id = "test-session-123"
        user_id = "test-user"
        message = "Hi!"
        
        print(f"   Sending message: '{message}'")
        
        # Create session
        session = await session_service.create_session(
            state={},
            app_name="mystery-trip-planner",
            user_id=user_id,
            session_id=session_id
        )
        
        # Create message content
        content = types.Content(
            role="user",
            parts=[types.Part(text=message)]
        )
        
        # Create runner
        runner = Runner(
            app_name="mystery-trip-planner",
            agent=root_agent,
            artifact_service=artifact_service,
            session_service=session_service,
        )
        
        # Run and collect events
        events = runner.run_async(
            session_id=session.id,
            user_id=user_id,
            new_message=content
        )
        
        response_text = None
        event_count = 0
        async for event in events:
            event_count += 1
            # Check if event has content with text
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts') and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text = part.text
                            print(f"   ✅ Received text event: {response_text[:100]}...")
                            break
                    if response_text:
                        break
        
        print(f"   Total events received: {event_count}")
        
        if response_text:
            print("   ✅ Agent is responding correctly!")
            return True
        else:
            print(f"   ⚠️  No text response received")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_imports():
    """Test that all necessary modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from fastapi import FastAPI
        from google.adk import Agent
        from game_master.agent import root_agent
        from planning.agent import root_agent as planning_agent
        from user_persona.agent import root_agent as persona_agent
        
        print("   ✅ All imports successful!")
        print(f"   - Game Master: {root_agent.name}")
        print(f"   - Planning: {planning_agent.name}")
        print(f"   - User Persona: {persona_agent.name}")
        return True
    except Exception as e:
        print(f"   ❌ Import error: {str(e)}")
        return False

def test_env():
    """Test that environment variables are set"""
    print("🧪 Testing environment configuration...")
    
    import os
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if api_key and api_key != "your_google_api_key_here":
        print(f"   ✅ GOOGLE_API_KEY is set (length: {len(api_key)})")
        return True
    else:
        print("   ⚠️  GOOGLE_API_KEY not set or using placeholder")
        print("   Please set your API key in .env file")
        return False

async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Mystery Trip Planner - Integration Test")
    print("="*60 + "\n")
    
    results = []
    
    # Test 1: Imports
    results.append(("Imports", test_imports()))
    print()
    
    # Test 2: Environment
    results.append(("Environment", test_env()))
    print()
    
    # Test 3: Agent (only if env is set)
    if results[1][1]:  # If environment test passed
        results.append(("Agent Response", await test_agent()))
        print()
    else:
        print("⏭️  Skipping agent test (API key not configured)\n")
    
    # Summary
    print("="*60)
    print("  Test Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("🎉 All tests passed! Your setup is ready to go!")
        print("\nNext steps:")
        print("  1. Run: make run-all")
        print("  2. Open: http://localhost:8082")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

