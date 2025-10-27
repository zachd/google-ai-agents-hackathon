from google.adk import Agent
from tools.time import get_current_time
from dotenv import load_dotenv

load_dotenv()

class PlanningAgent(Agent):
    """Plans the trip based on the user's persona."""
    def __init__(self):
        super().__init__(
            model="gemini-2.5-flash",
            name="planning",
            description="Plans mystery trip locations based on the user's persona and preferences.",
            instruction="""You are a creative trip planner that finds interesting mystery locations based on a user's persona.

When the game master asks you to plan a location, consider:
- The user's vibe preferences (from the conversation history)
- Their location and radius
- The current time of day (use get_current_time to check)
- Any other preferences they've shared

Return a unique, interesting location nearby that matches their preferences. Generate a poetic hint about the location that doesn't give it away too easily (like 'A place where mirrors reflect the city's soul').""",
            tools=[get_current_time]
        )

root_agent = PlanningAgent()
