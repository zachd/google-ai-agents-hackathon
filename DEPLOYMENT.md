# Mystery Trip Planner - Cloud Run Deployment

This project deploys a Google ADK-based mystery trip planner to Google Cloud Run with a React TypeScript frontend.

## 🚀 Quick Start

### Prerequisites
- Google Cloud Project with billing enabled
- Google API Key for Places API
- Docker installed locally
- Node.js 18+ and npm

### 1. Backend Setup

1. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

2. **Test locally:**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the FastAPI server
   python main.py
   ```

3. **Deploy to Cloud Run:**
   ```bash
   # Set your project ID
   export GOOGLE_CLOUD_PROJECT=your-project-id
   
   # Run deployment script
   ./deploy.sh
   ```

### 2. Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure API URL:**
   ```bash
   # Update .env.production with your Cloud Run URL
   echo "VITE_API_URL=https://your-service-url.run.app" > .env.production
   ```

3. **Run locally:**
   ```bash
   npm run dev
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

## 📁 Project Structure

```
google-ai-agents-hackathon/
├── main.py                    # FastAPI server
├── Dockerfile                 # Container config
├── .gcloudignore             # GCP ignore file
├── .env.example              # Environment template
├── deploy.sh                 # Deployment script
├── requirements.txt          # Python dependencies
├── game_master/              # ADK agents
├── planning/
├── user_persona/
├── tools/
└── frontend/                 # React app
    ├── src/
    │   ├── App.tsx
    │   ├── components/
    │   ├── services/
    │   └── styles/
    ├── package.json
    └── .env.production
```

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
- `GOOGLE_API_KEY`: Google Places API key
- `PORT`: Server port (default: 8080)

**Frontend (.env.production):**
- `VITE_API_URL`: Cloud Run backend URL

### Cloud Run Settings
- Memory: 512Mi
- Timeout: 300s
- Max instances: 10
- Public access enabled

## 🧪 Testing

### Backend Health Check
```bash
curl https://your-service-url.run.app/health
```

### Chat API Test
```bash
curl -X POST https://your-service-url.run.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to explore hidden gems in San Francisco"}'
```

### Frontend Local Development
```bash
cd frontend
npm run dev
# Open http://localhost:5173
```

## 🚀 Deployment Options

### Option 1: Manual Deployment
Use the provided `deploy.sh` script for one-time deployment.

### Option 2: GitHub Integration
1. Push code to GitHub repository
2. Connect Cloud Run to GitHub for automatic deployments
3. Set environment variables in Cloud Run console

### Option 3: CI/CD Pipeline
Add GitHub Actions workflow for automated testing and deployment.

## 🔍 Troubleshooting

### Common Issues

1. **API Key not working:**
   - Verify GOOGLE_API_KEY is set correctly
   - Check Places API is enabled in Google Cloud Console

2. **CORS errors:**
   - Ensure backend CORS is configured for your frontend domain
   - Check Cloud Run allows unauthenticated requests

3. **Session issues:**
   - Verify session service is properly initialized
   - Check session ID is being passed correctly

4. **Build failures:**
   - Ensure all dependencies are in requirements.txt
   - Check Dockerfile copies all necessary files

### Logs
```bash
# View Cloud Run logs
gcloud logs read --service=mystery-trip-planner --limit=50
```

## 📚 API Documentation

### Endpoints

- `GET /health` - Health check
- `POST /chat` - Chat with the agent (streaming response)
- `GET /` - API information

### Chat Request Format
```json
{
  "message": "string",
  "session_id": "string (optional)"
}
```

### Chat Response Format (Server-Sent Events)
```
data: {"type": "message", "message": "response text", "session_id": "..."}
data: {"type": "artifact", "artifact": {...}, "session_id": "..."}
data: {"type": "done", "session_id": "..."}
```

## 🎯 Features

- **Multi-agent system** with Game Master, User Persona, and Planning agents
- **Real-time streaming** responses
- **Image artifacts** support for visual hints
- **Session management** for conversation continuity
- **Google Maps integration** for navigation
- **Responsive chat UI** with modern design
- **Cloud Run deployment** with auto-scaling

## 🔐 Security Considerations

- API keys stored as environment variables
- CORS configured for specific origins in production
- Consider adding authentication for production use
- Rate limiting recommended for public APIs

## 📈 Monitoring

- Cloud Run provides built-in metrics
- Consider adding custom logging for agent interactions
- Monitor API usage and costs
- Set up alerts for service health
