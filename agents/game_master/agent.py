from google.adk import Agent
from agents.user_persona.agent import root_agent as user_persona_agent
from agents.planning.agent import root_agent as planning_agent
from dotenv import load_dotenv

load_dotenv()

class GameMasterAgent(Agent):
    """The main orchestrator of the trip."""
    def __init__(self):
        super().__init__(
            model="gemini-2.5-flash",
            name="game_master",
            description="The main orchestrator of the trip.",
            instruction="You are the game master of a choose-your-own-adventure trip. Your goal is to guide the user through a series of mystery locations. You can use the user_persona agent to understand the user and the planning agent to plan the trip.",
            tools=[user_persona_agent, planning_agent]
        )

    def run(self):
        """Runs the agent."""
        pass

root_agent = GameMasterAgent()