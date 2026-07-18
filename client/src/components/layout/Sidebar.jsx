import { useEffect, useState } from "react";
import { FiPlus, FiMessageSquare } from "react-icons/fi";
import { useChat } from "../../hooks/useChat";

import {
  getConversations,
  createConversation,
} from "../../services/conversationService";

export default function Sidebar() {
  const [conversations, setConversations] = useState([]);
  const { selectedConversation, setSelectedConversation } = useChat();

  useEffect(() => {
    loadConversations();
  }, []);

  async function loadConversations() {
    try {
      const data = await getConversations();
      setConversations(data);
    } catch (err) {
      console.error("Failed to load conversations:", err);
    }
  }

  async function handleNewChat() {
    try {
      const chat = await createConversation("New Chat");

      setConversations((prev) => [chat, ...prev]);
setSelectedConversation(chat);
    } catch (err) {
      console.error("Failed to create conversation:", err);
    }
  }

  return (
    <aside className="w-72 bg-slate-900 border-r border-slate-800 flex flex-col">

      {/* Logo */}
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-blue-400">
          Nebula
        </h1>

        <p className="text-sm text-slate-400 mt-1">
          AI Workspace
        </p>
      </div>

      {/* New Chat */}
      <div className="p-4">
        <button
          onClick={handleNewChat}
          className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 rounded-lg py-3 transition"
        >
          <FiPlus />
          New Chat
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto px-3">
        {conversations.length === 0 ? (
          <p className="text-slate-500 text-sm text-center mt-6">
            No conversations yet
          </p>
        ) : (
          conversations.map((chat) => (
              <button
              key={chat.id}
              onClick={() => setSelectedConversation(chat)}
              className={`w-full flex items-center gap-3 rounded-lg px-3 py-3 mb-2 text-left transition ${
                selectedConversation?.id === chat.id
                  ? "bg-blue-600"
                  : "hover:bg-slate-800"
              }`}
            >
              <FiMessageSquare />

              <span className="truncate">
                {chat.title}
              </span>
            </button>
          ))
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-slate-800 p-4">
        <p className="text-xs text-slate-500">
          Nebula v0.1
        </p>
      </div>

    </aside>
  );
}