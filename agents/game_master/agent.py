from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from agents.user_persona.agent import root_agent as user_persona_agent
from agents.planning.agent import root_agent as planning_agent
from dotenv import load_dotenv

load_dotenv()

class GameMasterAgent(Agent):
    """The main orchestrator of the trip."""
    def __init__(self):
        # Planning agent as a tool (background processing)
        planning_tool = AgentTool(agent=planning_agent)
        
        super().__init__(
            model="gemini-2.5-flash",
            name="game_master",
            description="The main orchestrator of the trip.",
            instruction="""You are the game master of a choose-your-own-adventure trip. Your goal is to guide the user through a series of mystery locations.

You have access to:
1. user_persona (sub-agent) - Can interview the user to understand their travel preferences (transfers to them for conversation)
2. planning (tool) - Finds mystery trip locations based on user preferences (runs in background)

Your workflow:
1. Greet the user warmly and explain the adventure
2. Transfer to user_persona agent - they will interview the user about preferences (takes over conversation)
3. Once user_persona is done, you'll get control back with their preferences
4. Use the planning tool to find interesting mystery locations (this runs in background while you stay engaged)
5. Give the user hints and clues about the location
6. Guide them through the adventure!

When the user says they're done at a location, ask for feedback and use planning again for the next location.""",
            sub_agents=[user_persona_agent],
            tools=[planning_tool]
        )

    def run(self):
        """Runs the agent."""
        pass

root_agent = GameMasterAgent()