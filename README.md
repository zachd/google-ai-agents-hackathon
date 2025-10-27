# Google AI Agents Hackathon

This project is a submission for the Google AI Agents Hackathon, built with [Google ADK](https://github.com/google/adk-python) (Agent Development Kit).

## Features

- **Game Master Agent**: Orchestrates the multi-agent system
- **User Persona Agent**: Manages user profiles and preferences
- **Planning Agent**: Handles trip planning logic
- **Custom Tools**: Specialized tools for agent interactions

## Prerequisites

- Python 3.9+
- A Google API Key ([Get one here](https://aistudio.google.com/app/apikey))

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd google-ai-agents-hackathon
```

### 2. Run setup

```bash
make setup
```

This will:
- Create a virtual environment
- Install all dependencies
- Create a `.env` file from `.env.example`

### 3. Configure your API key

Edit the `.env` file and add your Google API key:

```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

### 4. Run the server

```bash
make run
```

The ADK web interface will be available at `http://localhost:8081`

## Manual Installation (Alternative)

If you prefer manual setup:

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key
   ```

4. **Run the server:**
   ```bash
   ./venv/bin/adk web --port 8081 .
   ```

## Available Make Commands

- `make setup` - Complete setup (venv + dependencies + .env)
- `make venv` - Create virtual environment only
- `make install` - Install dependencies
- `make run` - Start the ADK server
- `make clean` - Remove virtual environment
- `make help` - Show available commands

## Project Structure

```
.
├── game_master/       # Game master agent implementation
├── user_persona/      # User persona agent
├── planning/          # Planning agent
├── tools/             # Custom tools
├── requirements.txt   # Python dependencies
├── Makefile          # Build automation
└── .env              # Environment variables (not in git)
```

## Security Note

⚠️ **Never commit your `.env` file or API keys to git.** The `.env` file is already in `.gitignore` to prevent accidental commits.
