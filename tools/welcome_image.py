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
    # Check if running in Cloud Run
    is_cloud_run = os.getenv("K_SERVICE") is not None
    
    try:
        if is_cloud_run:
            # Always use default credentials in Cloud Run
            client = genai.Client()
        else:
            # Use API key for local development
            api_key = os.getenv("GOOGLE_API_KEY")
            client = genai.Client(api_key=api_key)
        
        # Create a prompt for the welcome avatar
        prompt = f"""Create a realistic, atmospheric welcome avatar image for a choose-your-own-adventure mystery trip.

Setting: {location}
Adventure style: {adventure_type}

The image should be:
- Photorealistic or realistic digital art, NOT cartoonish
- Show a person from behind (back turned), showing their silhouette/outline - NO FACE visible, NO gender identifiable
- The person should be dressed appropriately for the adventure type ({adventure_type}):
  * adventurous: hiking gear, backpack, outdoor clothing
  * chill: casual, comfortable clothing for urban exploration
- The person should be looking at the location/setting shown in the background
- Subtly show the location vibe in the background without revealing the name
- Match the adventure style in clothing and pose
- Colorful, atmospheric, and engaging
- Professional travel/adventure photography style
- No abstract symbols, question marks, or icons
- No text on the image
- Clean, focused composition showing a mysterious silhouette person (back to camera) looking at the destination"""
        
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
