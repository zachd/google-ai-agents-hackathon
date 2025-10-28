import React, { useState } from "react";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, disabled = false }) => {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-input">
      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-container">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Tell me what kind of adventure you're looking for..."
            disabled={disabled}
            className="message-input"
            rows={1}
          />
          <button type="submit" disabled={disabled || !message.trim()} className="send-button">
            {disabled ? "⏳" : "🚀"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInput;
