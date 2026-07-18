import { useEffect, useRef } from "react";
import MarkdownMessage from "./MarkdownMessage";

import { useChat } from "../../hooks/useChat";
import { getMessages } from "../../services/messageService";
import TypingIndicator from "./TypingIndicator";

export default function ChatWindow() {
  const {
    selectedConversation,
    messages,
    setMessages,
    loadingMessages,
    setLoadingMessages,
    thinking,
    setThinking,
  } = useChat();

  const bottomRef = useRef(null);


  useEffect(() => {
  bottomRef.current?.scrollIntoView({
    behavior: "smooth",
  });
}, [messages]);  

  useEffect(() => {
    if (selectedConversation) {
      loadMessages();
    } else {
      setMessages([]);
    }
  }, [selectedConversation]);

  async function loadMessages() {
    try {
      setLoadingMessages(true);

      const data = await getMessages(selectedConversation.id);

      setMessages(data);
    } catch (err) {
      console.error("Failed to load messages:", err);
    } finally {
      setLoadingMessages(false);
    }
  }

  if (!selectedConversation) {
    return (
      <main className="flex-1 flex items-center justify-center bg-slate-950">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-white mb-3">
            Welcome to Nebula 🚀
          </h2>

          <p className="text-slate-400">
            Select a conversation or create a new one.
          </p>
        </div>
      </main>
    );
  }

  if (loadingMessages) {
    return (
      <main className="flex-1 flex items-center justify-center bg-slate-950">
        <p className="text-slate-400">
          Loading messages...
        </p>
      </main>
    );
  }

  return (
    <main className="flex-1 overflow-y-auto bg-slate-950 px-8 py-6">
      <div className="max-w-4xl mx-auto space-y-4">

        {messages.length === 0 ? (
          <p className="text-slate-500 text-center">
            No messages yet.
          </p>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`rounded-xl p-4 ${
                message.role === "user"
                  ? "bg-blue-600 ml-20"
                  : "bg-slate-800 mr-20"
              }`}
            >
              <p className="text-sm text-slate-300 mb-1">
                {message.role === "user" ? "You" : "Nebula"}
              </p>

              <div className="text-white prose prose-invert max-w-none">
               <MarkdownMessage content={message.content} />
              </div>
              
            </div>
          ))
        )}
           
           {thinking && (
            <div className="bg-slate-800 mr-20 rounded-xl p-4 animate-pulse">
              <p className="text-slate-300">
                <TypingIndicator />
              </p>
            </div>
            )}
            <div ref={bottomRef} />

      </div>
    </main>
  );
}