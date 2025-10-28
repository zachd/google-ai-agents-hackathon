"""
Alternative entry point for Cloud Run
"""
from game_master.agent import root_agent

# For Cloud Run deployment
if __name__ == "__main__":
    from google.adk.runners import Runner
    runner = Runner(app_name="mystery-trip", agent=root_agent)
    runner.run()

