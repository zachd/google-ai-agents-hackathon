from google.adk import Agent
from dotenv import load_dotenv

load_dotenv()

class UserPersonaAgent(Agent):
    """Interviews the user to build a persona."""
    def __init__(self):
        super().__init__(
            model="gemini-2.5-flash",
            name="user_persona",
            description="Interviews the user to build a persona.",
            instruction="You are a friendly assistant that interviews a user to understand their travel preferences."
        )

root_agent = UserPersonaAgent()
