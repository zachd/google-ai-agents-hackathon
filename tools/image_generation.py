from google.adk.tools import ToolContext

def show_hint_image(image_url: str, hint: str, tool_context: ToolContext) -> dict:
    """
    Display a visual hint image.
    
    Args:
        image_url: The URL of the image to display
        hint: The poetic hint text
        tool_context: The ADK tool context
    
    Returns:
        Dictionary with the image URL formatted for display
    """
    return {
        "image_url": image_url,
        "hint": hint,
        "message": f"Mystery hint: {hint}"
    }

