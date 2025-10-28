import { useState, useRef, useEffect } from "react";
import ChatMessage from "./components/ChatMessage";
import ChatInput from "./components/ChatInput";
import { sendMessage, Message, Artifact } from "./services/api";
import "./styles/chat.css";

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    if (!message.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: message,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage(message, sessionId);
      const reader = response.body?.getReader();
      if (!reader) throw new Error("No response body");

      let assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: "",
        timestamp: new Date(),
        artifacts: [],
      };

      setMessages((prev) => [...prev, assistantMessage]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = new TextDecoder().decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6));

              if (data.type === "message") {
                assistantMessage.content += data.message;
                setMessages((prev) =>
                  prev.map((msg) =>
                    msg.id === assistantMessage.id ? { ...msg, content: assistantMessage.content } : msg
                  )
                );
                setSessionId(data.session_id);
              } else if (data.type === "artifact") {
                const artifact: Artifact = {
                  filename: data.artifact.filename,
                  mimeType: data.artifact.mime_type,
                  uri: data.artifact.uri,
                };
                assistantMessage.artifacts?.push(artifact);
                setMessages((prev) =>
                  prev.map((msg) =>
                    msg.id === assistantMessage.id ? { ...msg, artifacts: [...(msg.artifacts || []), artifact] } : msg
                  )
                );
              } else if (data.type === "error") {
                throw new Error(data.message);
              }
            } catch (e) {
              console.error("Error parsing SSE data:", e);
            }
          }
        }
      }
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : "Unknown error"}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>🗺️ Mystery Trip Planner</h1>
        <p>Discover hidden gems and local secrets!</p>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <p>Welcome! I'll help you plan an amazing mystery adventure.</p>
            <p>Just tell me what you're looking for and I'll guide you to some incredible places!</p>
          </div>
        )}

        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}

        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  );
}

export default App;
