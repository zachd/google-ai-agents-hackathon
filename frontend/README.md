# Mystery Trip Planner Frontend

A simple React TypeScript chat interface for the Mystery Trip Planner.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server (port 8082)
npm run dev

# Build for production
npm run build
```

## Environment Variables

Create `.env.development` for local development:
```
VITE_API_URL=http://localhost:8080
```

Create `.env.production` for production:
```
VITE_API_URL=https://your-service-url.run.app
```

## Features

- Real-time chat interface
- Streaming responses from backend
- Image artifact support
- Google Maps integration
- Responsive design
- TypeScript support

## Project Structure

```
src/
├── App.tsx              # Main chat application
├── components/
│   ├── ChatMessage.tsx  # Message display component
│   └── ChatInput.tsx    # Input component
├── services/
│   └── api.ts           # API client
└── styles/
    └── chat.css         # Chat styling
```