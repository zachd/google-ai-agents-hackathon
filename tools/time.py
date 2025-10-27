from datetime import datetime

def get_current_time() -> str:
    """Gets the current time."""
    return datetime.now().strftime("%H:%M:%S")
