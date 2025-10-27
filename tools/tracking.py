from google.adk.tools import ToolContext

def track_suggested_place(place_id: str, name: str, tool_context: ToolContext) -> dict:
    """
    Track a suggested place by adding it to the suggested_places dict in state.
    
    Args:
        place_id: The Google Places place_id to track
        name: The name of the place
        tool_context: The ADK tool context
    """
    # Use .get() with default to safely access state
    suggested = tool_context.state.get('suggested_places', {})
    
    # Add the place info
    suggested[place_id] = name
    tool_context.state['suggested_places'] = suggested
    
    return {"message": f"Tracked suggested place: {name}"}

