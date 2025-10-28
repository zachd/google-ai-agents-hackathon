# Mystery Trip Planner 🗺️

A choose-your-own-adventure mystery trip planner powered by Google AI Agents. Chat with AI agents that interview you, then reveal personalized mystery destinations with AI-generated images and map links.

**Built with:** [Google ADK](https://github.com/google/adk-python) • Gemini • Google Places API • React

---

## 🚀 Quick Start (3 Steps)

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

```bash
make run-all        # Start backend + frontend together
make run-backend    # Backend only (port 8080)
make run-frontend   # Frontend only (port 8082)
make clean          # Clean and start fresh
python test_integration.py  # Test everything works
```

---

## 🏗️ Architecture

```
React Frontend (8082) → FastAPI (8080) → ADK Agents → Gemini + Places API
```

**Agents:**
- 🎮 Game Master - Orchestrates the experience
- 👤 User Persona - Interviews about preferences
- 🗺️ Planning - Finds mystery locations

---

## 🛠️ Troubleshooting

**Backend won't start?**
```bash
# Check API key is set
cat .env

# Restart backend
lsof -ti:8080 | xargs kill -9
make run-backend
```

**Frontend errors?**
```bash
cd frontend && npm install
```

**Test the connection:**
```bash
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
