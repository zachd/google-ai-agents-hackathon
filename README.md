# Mystery Trip Planner 🗺️

A choose-your-own-adventure mystery trip planner powered by Google AI Agents. Chat with AI agents that interview you, then reveal personalized mystery destinations with AI-generated images and map links.

**Built with:** [Google ADK](https://github.com/google/adk-python) • Gemini • Google Places API • React

---

## 🚀 Quick Start

### Option A: Docker (Easiest) 🐳

```bash
# Just run it!
make docker
```

**Open:** http://localhost:8082 🎉

> Make sure you have `.env` with your `GOOGLE_API_KEY`

### Option B: Local Development

```bash
# 1. Setup
make setup

# 2. Add your Google API key to .env
# Get key from: https://aistudio.google.com/app/apikey

# 3. Run everything
make run-all
```

**Open:** http://localhost:8082 🎉

---

## ✨ What It Does

1. **Game Master** welcomes you and transfers to User Persona
2. **User Persona** asks 2-3 quick questions about your travel vibe
3. **Planning Agent** finds mystery locations using Google Places API
4. **AI generates** personalized avatar + hint images with Gemini
5. **You explore** with cryptic hints and map links!

---

## 📋 Common Commands

**Docker:**
```bash
make docker         # Build and start (backend + frontend)
make docker-debug   # Start with ADK web interface (3 services)
make docker-up      # Start containers
make docker-down    # Stop containers
make docker-logs    # View logs
```

**Local Development:**
```bash
make run-all        # Start backend + frontend together
make run-backend    # Backend only (port 8080)
make run-frontend   # Frontend only (port 8082)
make clean          # Clean and start fresh
python test_integration.py  # Test everything works
```

---

## 🏗️ Architecture

**Docker Services:**
- Port 8082: React Frontend (chat UI)
- Port 8080: FastAPI Backend (ADK agents via Python)
- Port 8081: ADK Web Interface (optional, for debugging)

**Flow:**
```
Browser → Frontend (8082) → Backend API (8080) → ADK Agents → Gemini + Places
```

**Agents:**
- 🎮 Game Master - Orchestrates the experience
- 👤 User Persona - Interviews about preferences
- 🗺️ Planning - Finds mystery locations

---

## 🛠️ Troubleshooting

**Docker Issues:**
```bash
# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up

# View logs
docker-compose logs backend
docker-compose logs frontend
```

**Local Development Issues:**
```bash
# Backend won't start?
cat .env  # Check API key is set
lsof -ti:8080 | xargs kill -9
make run-backend

# Frontend errors?
cd frontend && npm install

# Test connection
curl http://localhost:8080/health
# Should return: {"status":"healthy","service":"mystery-trip-planner"}
```

---

## 📁 Project Structure

```
├── game_master/      # Orchestrator agent
├── user_persona/     # Interview agent
├── planning/         # Location finding agent
├── tools/            # Places API, image gen, tracking
├── frontend/         # React UI
├── main.py           # FastAPI backend
└── .env              # Your API key (never commit!)
```

---

## 📚 More Docs

- Full technical details: `INTEGRATION_SUMMARY.md`
- Deployment guide: `DEPLOYMENT.md`

---

**Prerequisites:** Python 3.9+ • Node.js • Google API Key  
**Security:** Never commit `.env` to git (already in `.gitignore`)
