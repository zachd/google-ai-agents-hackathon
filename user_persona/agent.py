from google.adk import Agent
from tools.time import get_current_time
from dotenv import load_dotenv

load_dotenv()

class UserPersonaAgent(Agent):
    """Interviews the user to build a persona."""
    def __init__(self):
        super().__init__(
            model="gemini-2.5-flash",
            name="user_persona",
            description="Interviews the user to understand their travel preferences.",
            instruction="""You are a friendly assistant that interviews a user to understand their travel preferences.

Ask only 2-3 quick questions:
1. Vibe: a question similar to: local secrets/iconic landmarks? adventurous/relaxed?
2. Trip duration: afternoon, weekend, or longer?
3. Current location, like what city (use get_current_time for time)

Keep responses SHORT (1-2 sentences max). When you have enough info, say "Got it! Transferring you back to plan your adventure." and you'll be transferred back.""",
            tools=[get_current_time]
        )

root_agent = UserPersonaAgent()
