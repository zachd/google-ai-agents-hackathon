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
        
        # Load the images from artifacts (await async load)
        avatar_part = await tool_context.load_artifact(avatar_artifact)
        place_part = await tool_context.load_artifact(place_image_artifact)
        
        if not avatar_part:
            return {"error": f"Failed to load avatar artifact: {avatar_artifact}"}
        if not place_part:
            return {"error": f"Failed to load place image artifact: {place_image_artifact}"}
        
        # Create the prompt
        prompt = f"""Create an artistic, interpretive hint image inspired by the person in the first image and the location in the second image.

The hint is: "{hint}"

Transform these images into a mysterious visual clue that:
- Takes inspiration from the person's style and appearance but shows them in a more poetic, mysterious way
- Captures the essence and atmosphere of the location from the second image
- Uses artistic interpretation rather than literal photo combination
- Creates a dream-like, enigmatic atmosphere that hints at the destination
- Shows abstract clues like shadows, silhouettes, reflections, or partial views of architecture
- Suggests the journey or destination through visual metaphor
- Has a magical, quest-like quality that entices exploration
- NO TEXT on the image - just the visual mystery

The result should be an artistic, interpretive image with NO TEXT that gives visual clues about the mystery location without being too obvious or literal."""
        
        # Call Gemini to generate the combined hint image using the Parts directly
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[prompt, avatar_part, place_part],
        )
        
        # Extract the image data and save as artifact
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                # Save as ADK artifact
                filename = f"hint_image_{hint[:20].replace(' ', '_')}.png"
                artifact_part = types.Part(
                    inline_data=types.Blob(
                        data=part.inline_data.data,
                        mime_type=part.inline_data.mime_type or "image/png"
                    )
                )
                
                artifact_version = await tool_context.save_artifact(
                    filename=filename,
                    artifact=artifact_part
                )
                
                return {
                    "status": "Hint image generated successfully",
                    "filename": filename,
                    "version": artifact_version,
                    "hint": hint
                }
        
        return {"error": "No image data generated"}
        
    except Exception as e:
        return {"error": f"Error generating hint image: {str(e)}"}

