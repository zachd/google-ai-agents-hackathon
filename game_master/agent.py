from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from user_persona.agent import root_agent as user_persona_agent
from planning.agent import root_agent as planning_agent
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
            instruction="""You are the game master. Keep responses SHORT.

Workflow:
1. Welcome briefly
2. Transfer to user_persona for interview
3. After interview, call planning tool (gets location from interview)
4. Planning returns: hint, place_id, name, map_url
5. Add place_id to state['visited_places'] list (initialize if needed)
6. Give user hint and map link

When user asks for new place, call planning again.

Keep responses under 2 sentences.""",
            sub_agents=[user_persona_agent],
            tools=[planning_tool]
        )

    def run(self):
        """Runs the agent."""
        pass

root_agent = GameMasterAgent()
