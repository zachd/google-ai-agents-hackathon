from google.adk import Agent
from dotenv import load_dotenv

load_dotenv()

class UserPersonaAgent(Agent):
    """Interviews the user to build a persona."""
    def __init__(self):
        super().__init__(
            model="gemini-2.5-flash",
            name="user_persona",
            description="Interviews the user to understand their travel preferences including vibe, duration, location, and current time.",
            instruction="""You are a friendly assistant that interviews a user to understand their travel preferences.

Ask the user about:
- Vibe preferences (local secrets vs iconic landmarks, adventurous vs relaxed)
- Trip duration (afternoon, weekend, etc.)
- Current location and preferred radius
- Current time of day
- Any other preferences that would help plan a mystery trip

Be conversational and friendly. Only ask one or two questions at a time.

When you have gathered enough information to understand their preferences (vibe, duration, location, time), let the user know and you'll be transferred back to the game master who will plan their adventure."""
        )

root_agent = UserPersonaAgent()
