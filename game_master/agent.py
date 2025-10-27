from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from user_persona.agent import root_agent as user_persona_agent
from planning.agent import root_agent as planning_agent
from tools.tracking import track_suggested_place
from tools.welcome_image import generate_welcome_avatar
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
1. Welcome briefly ("Hello! Let's plan your mystery adventure.")
2. Transfer to user_persona to interview
3. After interview returns, extract: location (e.g. "Rotterdam"), adventure_type (e.g. "adventurous" or "chill")
4. Call generate_welcome_avatar(location, adventure_type) to create welcome image artifact
5. Let the user see it, then call planning tool to get first hint
6. Planning returns: place_id, name, hint, map_url, photos[]
7. Call track_suggested_place(place_id, name)
8. Show hint: ![Hint](photos[0]) + hint + map link

When user asks for new place, call planning again (it filters suggested_places).

IMPORTANT: Show the avatar BEFORE starting the planning tool.

Keep responses under 2 sentences.""",
            sub_agents=[user_persona_agent],
            tools=[planning_tool, track_suggested_place, generate_welcome_avatar]
        )

    def run(self):
        """Runs the agent."""
        pass

root_agent = GameMasterAgent()
