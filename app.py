"""
Main entry point for Cloud Run deployment
"""
import sys
import os

# Add current directory to Python path for Cloud Run
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_master.agent import root_agent

# Cloud Run will look for this
def app():
    return root_agent

if __name__ == "__main__":
    app()

