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

- `make all` or `make` - Complete setup and show next steps (default)
- `make setup` - Create venv, install dependencies, and create .env
- `make venv` - Create virtual environment only
- `make install` - Install dependencies in existing venv
- `make run` - Start the ADK server on port 8081
- `make clean` - Remove virtual environment
- `make help` - Show all available commands

## Project Structure

```
.
├── game_master/       # Game master agent implementation
│   ├── __init__.py
│   └── agent.py       # Main orchestrator agent
├── user_persona/      # User persona agent
│   ├── __init__.py
│   └── agent.py       # User interview agent
├── planning/          # Planning agent
│   ├── __init__.py
│   └── agent.py       # Trip planning agent
├── tools/             # Custom tools
│   ├── __init__.py
│   ├── time.py        # Time-related tools
│   └── places.py      # Google Places API integration
├── evals/             # Evaluation scenarios
│   ├── README.md                    # Evaluation documentation
│   ├── game_master_scenarios.json   # Game master tests
│   ├── user_persona_scenarios.json  # User persona tests
│   ├── planning_scenarios.json      # Planning tests
│   └── integrated_scenarios.json    # End-to-end tests
├── requirements.txt   # Python dependencies
├── Makefile          # Build automation
├── .env              # Environment variables (not in git)
└── .env.example      # Environment template
```

## Agent Evaluation & Testing

This project includes a comprehensive evaluation framework with **26 detailed test scenarios** documenting expected agent behaviors.

### Test Documentation

The `evals/` directory contains detailed test scenarios for:

- **Game Master Agent** (5 scenarios) - Orchestration, guidance, error handling
- **User Persona Agent** (7 scenarios) - Interview flow, preference gathering
- **Planning Agent** (8 scenarios) - Location search, hint generation, tool usage
- **Integrated System** (6 scenarios) - End-to-end user journeys

### Using the Test Scenarios

#### Game Master Agent
- Initial greeting and adventure explanation
- Multi-agent workflow orchestration
- Location completion handling
- Adventure guidance and hints
- Error recovery

#### User Persona Agent
- Friendly interview initiation
- Vibe preference gathering
- Location and duration collection
- Time awareness
- Proper conversation pacing
- Handoff back to game master

#### Planning Agent
- Location search using Google Places API
- Mysterious hint generation
- Time-aware recommendations
- Preference matching
- GPS coordinate inclusion
- Local vs tourist differentiation
- Distance constraint handling

#### Integrated System
- Complete user journey flows
- Multi-location adventures
- Preference refinement based on feedback
- Help during location search
- Time-based suggestions
- System-wide error recovery

Each test scenario provides:
- **Test name** and description
- **Sample conversation** to simulate
- **Expected behaviors** to validate
- **Coverage** of edge cases and error scenarios

### Manual Testing Guide

Use the test scenarios as a checklist when testing your agents:

1. **Start the web interface**: `make run`
2. **Open** `evals/game_master_scenarios.json` (or other test files)
3. **Test each scenario** by simulating the conversations
4. **Verify** the expected behaviors are present
5. **Document** any issues found

For complete evaluation documentation, see [`evals/README.md`](evals/README.md).

## Development Workflow

1. **Make changes** to agent code
2. **Test manually** using the evaluation scenarios as a guide:
   ```bash
   make run
   # Follow test scenarios in evals/ directory
   ```
3. **Verify** expected behaviors from the test documentation
4. **Add new test scenarios** for new features
5. **Commit** your changes

## Security Note

⚠️ **Never commit your `.env` file or API keys to git.** The `.env` file is already in `.gitignore` to prevent accidental commits.
