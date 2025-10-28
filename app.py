"""
Main entry point for Cloud Run deployment
"""
from game_master.agent import root_agent

# Cloud Run will look for this
def app():
    return root_agent

if __name__ == "__main__":
    app()

