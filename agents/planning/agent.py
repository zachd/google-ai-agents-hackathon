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
            description="Plans the trip based on the user's persona.",
            instruction="You are a creative trip planner that suggests mystery locations based on a user's persona.",
            tools=[get_current_time]
        )

root_agent = PlanningAgent()
