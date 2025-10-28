// Simple API client for the Mystery Trip Planner
export interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  artifacts?: Artifact[];
}

export interface Artifact {
  filename?: string;
  mimeType?: string;
  uri: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

export async function sendMessage(message: string, sessionId?: string | null): Promise<Response> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      session_id: sessionId || undefined
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response;
}