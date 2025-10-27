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
            instruction="""You plan mystery trips. Keep it SHORT - just return hint + map link.

1. Use find_nearby_places (query, location, max_results=10)
2. Filter results - skip places already in state['visited_places']  
3. Pick the first available place
4. Generate ONE poetic hint about it
5. Return: hint, place_id, name, map_url

No greetings, just results.""",
            tools=[get_current_time, find_nearby_places]
        )

root_agent = PlanningAgent()
