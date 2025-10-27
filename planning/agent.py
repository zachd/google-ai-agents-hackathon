from google.adk import Agent
from tools.time import get_current_time
from tools.places import find_nearby_places
from dotenv import load_dotenv

load_dotenv()

class PlanningAgent(Agent):
    """Plans the trip based on the user's persona."""
    def __init__(self):
        super().__init__(
            model="gemini-2.5-flash",
            name="planning",
            description="Plans mystery trip locations based on the user's persona and preferences using Google Places API.",
            instruction="""You are a creative trip planner that finds interesting mystery locations based on a user's persona.

When the game master asks you to plan a location, consider:
- The user's vibe preferences (from the conversation history)
- Their location and radius
- The current time of day (use get_current_time to check)
- Any other preferences they've shared

Use the find_nearby_places tool to search for real places nearby that match their preferences.

Then:
1. Select the best matching place from the results
2. Generate a poetic, mysterious hint about the location that doesn't give it away too easily (like 'A place where mirrors reflect the city's soul')
3. Return the place details with GPS coordinates for navigation

The hint should be poetic and mysterious - make the user curious but not obvious what it is.""",
            tools=[get_current_time, find_nearby_places]
        )

root_agent = PlanningAgent()
