import { useRef, useState } from "react";
import { FiSend, FiSquare } from "react-icons/fi";

import { useChat } from "../../hooks/useChat";
import {streamChat, getMessages,} from "../../services/messageService";

export default function ChatInput() {
  const {
    selectedConversation,
    messages,
    setMessages,
    thinking,
    setThinking,
  } = useChat();

  const [content, setContent] = useState("");
  const [sending, setSending] = useState(false);
  const controllerRef = useRef(null);

  async function handleSend() {
    if (!selectedConversation) return;

    if (!content.trim()) return;

    const userText = content;

    // Show user message immediately
    const tempUser = {
      id: Date.now(),
      role: "user",
      content: userText,
    };

    // Empty assistant bubble
    const tempAssistant = {
      id: Date.now() + 1,
      role: "assistant",
      content: "",
    };

    setMessages([
      ...messages,
      tempUser,
      tempAssistant,
    ]);

    setContent("");
    setSending(true);
    setThinking(true);
    controllerRef.current = new AbortController();

    try {
      await streamChat(
        selectedConversation.id,
        userText,
        (chunk) => {
          setThinking(false);
          tempAssistant.content += chunk;

          setMessages((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = {
              ...tempAssistant,
            };
            return updated;
          });
        },
        controllerRef.current.signal
     );

      // Refresh from database
      const updated = await getMessages(
        selectedConversation.id
      );

      setMessages(updated);
    } catch (err) {
      if (err.name === "AbortError") {
        console.log("Generation stopped.");
      } else {
        console.error(err);
      }
      } finally {
      setSending(false);
      setThinking(false);
    }
  }

  function handleStop() {
  controllerRef.current?.abort();

  setSending(false);
  setThinking(false);
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="border-t border-slate-800 bg-slate-900 p-5">
      <div className="max-w-4xl mx-auto flex gap-3">

        <input
          value={content}
          onChange={(e) => setContent(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={!selectedConversation || sending}
          placeholder={
            selectedConversation
              ? "Ask Nebula anything..."
              : "Select a conversation first..."
          }
          className="flex-1 rounded-xl bg-slate-800 px-5 py-4 text-white outline-none disabled:opacity-50"
        />

        <button
          onClick={sending ? handleStop : handleSend}
          disabled={!selectedConversation || sending}
          className="rounded-xl bg-blue-600 px-5 hover:bg-blue-700 disabled:opacity-50 transition"
        >
          {sending ? <FiSquare size={20} /> : <FiSend size={20} />}
        </button>

      </div>
    </div>
  );
}