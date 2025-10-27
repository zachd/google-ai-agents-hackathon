from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from user_persona.agent import root_agent as user_persona_agent
from planning.agent import root_agent as planning_agent
from tools.tracking import track_suggested_place
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
            instruction="""Game master for mystery trips. SHORT responses.

Workflow:
1. Welcome briefly
2. Transfer to user_persona to interview
3. After interview, call planning tool
4. Planning returns: place_id, name, hint, map_url
5. Call track_suggested_place(place_id, name) to track it
6. Give user the hint + map link

When user asks for new place, call planning again (it filters suggested_places).

Keep responses under 2 sentences.""",
            sub_agents=[user_persona_agent],
            tools=[planning_tool, track_suggested_place]
        )

    def run(self):
        """Runs the agent."""
        pass

root_agent = GameMasterAgent()
