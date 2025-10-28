import os
from google.genai import types
from google.adk.tools import ToolContext
from google import genai

async def generate_hint_image(hint: str, avatar_artifact: str, place_image_artifact: str, tool_context: ToolContext) -> dict:
    """
    Generate a combined hint image using avatar image and place image with Gemini image generation.
    
    Args:
        hint: The poetic hint text about the mystery location
        avatar_artifact: Filename of the avatar artifact to load
        place_image_artifact: Filename of the place photo artifact to load
        tool_context: The ADK tool context
    
    Returns:
        Dictionary with the generated hint image artifact info
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_API_KEY not set"}
    
    try:
        client = genai.Client(api_key=api_key)
        
        # Load the images from artifacts (await async load)
        avatar_part = await tool_context.load_artifact(avatar_artifact)
        place_part = await tool_context.load_artifact(place_image_artifact)
        
        if not avatar_part:
            return {"error": f"Failed to load avatar artifact: {avatar_artifact}"}
        if not place_part:
            return {"error": f"Failed to load place image artifact: {place_image_artifact}"}
        
        # Create the prompt
        prompt = f"""Create a realistic hint image showing the same person from the first image standing in or near the location shown in the second image.

The hint is: "{hint}"

Combine these images to create a visual hint that:
- Keeps the same person from the first image (avatar) - their exact appearance and clothing
- Places this person in or near the actual location/setting from the second image (place photo)
- Shows the specific details, architecture, or landmarks from the second image as the background
- Uses the same realistic, photographic style as the first image
- Creates a mysterious atmosphere by showing where the person is heading
- Gives visual clues about the destination without being too obvious
- NO TEXT on the image - just the visual scene

The result should be a realistic, cohesive image with NO TEXT, showing the avatar person at the mystery location."""
        
        # Call Gemini to generate the combined hint image using the Parts directly
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[prompt, avatar_part, place_part],
        )
        
        # Extract the image data and return it directly as inline_data
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                # Return the image data directly so it appears in the agent response
                filename = f"hint_image_{hint[:20].replace(' ', '_')}.png"
                
                return {
                    "status": "Hint image generated successfully",
                    "filename": filename,
                    "hint": hint,
                    "image_data": part.inline_data.data,
                    "mime_type": part.inline_data.mime_type or "image/png"
                }
        
        return {"error": "No image data generated"}
        
    except Exception as e:
        return {"error": f"Error generating hint image: {str(e)}"}

