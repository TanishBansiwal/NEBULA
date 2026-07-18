import { createContext, useState } from "react";

export const ChatContext = createContext();

export function ChatProvider({ children }) {
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [thinking, setThinking] = useState(false);

  return (
    <ChatContext.Provider
      value={{
        selectedConversation,
        setSelectedConversation,
        messages,
        setMessages,
        loadingMessages,
        setLoadingMessages,
        thinking,
        setThinking,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}