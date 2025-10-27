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
            instruction="""You plan mystery trips. NO GREETINGS - just results.

Already suggested places: {suggested_places?}

When called:
1. Use find_nearby_places(query, location, max_results=10)
2. Filter OUT any place_ids already in suggested_places dict above
3. Pick the BEST remaining place
4. Generate ONE poetic hint (1 sentence)
5. Return format: place_id, name, hint, map_url, photos (include photo URLs if available)

The photos array contains Google Places photos that can be shown as visual hints.

No manual state calls needed.""",
            tools=[get_current_time, find_nearby_places]
        )

root_agent = PlanningAgent()
