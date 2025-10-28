import React from "react";
import { Message, Artifact } from "../services/api";

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const formatTime = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  const renderArtifacts = (artifacts: Artifact[]) => {
    return artifacts.map((artifact, index) => {
      if (artifact.mimeType?.startsWith("image/")) {
        return (
          <div key={index} className="artifact-image">
            <img
              src={artifact.uri}
              alt={artifact.filename || "Generated image"}
              className="max-w-full h-auto rounded-lg"
            />
          </div>
        );
      }
      return null;
    });
  };

  const renderMapLinks = (content: string) => {
    const mapUrlRegex = /https:\/\/www\.google\.com\/maps\/[^\s]+/g;
    const parts = content.split(mapUrlRegex);
    const urls = content.match(mapUrlRegex) || [];

    if (urls.length === 0) {
      return content;
    }

    return parts.map((part, index) => (
      <React.Fragment key={index}>
        {part}
        {urls[index] && (
          <a href={urls[index]} target="_blank" rel="noopener noreferrer" className="map-link">
            🗺️ Open in Maps
          </a>
        )}
      </React.Fragment>
    ));
  };

  return (
    <div className={`message ${message.type}`}>
      <div className="message-content">
        <div className="message-text">{renderMapLinks(message.content)}</div>
        {message.artifacts && message.artifacts.length > 0 && (
          <div className="message-artifacts">{renderArtifacts(message.artifacts)}</div>
        )}
        <div className="message-time">{formatTime(message.timestamp)}</div>
      </div>
    </div>
  );
};

export default ChatMessage;
