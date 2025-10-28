"""
Root agent for Cloud Run deployment.
This file must exist at the root level with 'root_agent' variable.
"""
import sys
import os

# Ensure the current directory is in the path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from game_master.agent import root_agent

