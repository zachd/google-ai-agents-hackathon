import os
from google.genai import types
from google.adk.tools import ToolContext
from google import genai

async def generate_welcome_avatar(location: str, adventure_type: str, tool_context: ToolContext) -> dict:
    """
    Generate a welcome avatar image using Gemini image generation (Nano Banana).
    
    Args:
        location: The user's location (e.g., "Rotterdam")
        adventure_type: Type of adventure (e.g., "adventurous", "chill")
        tool_context: The ADK tool context
    
    Returns:
        Dictionary with avatar info and URI
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_API_KEY not set"}
    
    try:
        client = genai.Client(api_key=api_key)
        
        # Create a prompt for the welcome avatar
        prompt = f"""Create a realistic, atmospheric welcome avatar image for a choose-your-own-adventure mystery trip.

Setting: {location}
Adventure style: {adventure_type}

The image should be:
- Photorealistic or realistic digital art, NOT cartoonish
- Feature a clearly visible person as the central subject (full or upper body visible)
- The person should be in the foreground, clearly visible
- Subtly reference the location vibe without showing the location name
- Match the adventure type ({adventure_type} style)
- Colorful, atmospheric, and engaging
- Suitable as a welcome greeting image
- Professional travel/adventure photography style
- No abstract symbols, question marks, or icons
- Clean, focused composition with the person as the main element"""
        
        # Call Gemini to generate the image using gemini-2.5-flash-image model
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[prompt],
            config=types.GenerateContentConfig(
                image_config=types.ImageConfig(
                    aspect_ratio="1:1"
                )
            )
        )
        
        # Extract the image data and save as artifact
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                # Save as ADK artifact using the Blob data directly
                filename = f"welcome_avatar_{location}_{adventure_type}.png"
                artifact_part = types.Part(
                    inline_data=types.Blob(
                        data=part.inline_data.data,
                        mime_type=part.inline_data.mime_type or "image/png"
                    )
                )
                
                # Save the artifact (await for async method)
                artifact_version = await tool_context.save_artifact(
                    filename=filename,
                    artifact=artifact_part
                )
                
                return {
                    "status": "Avatar generated successfully",
                    "filename": filename,
                    "version": artifact_version,
                    "location": location,
                    "adventure_type": adventure_type,
                    "message": f"Welcome to your {adventure_type} mystery adventure in {location}!"
                }
        
        return {"error": "No image data generated"}
        
    except Exception as e:
        return {"error": f"Error generating image: {str(e)}"}
