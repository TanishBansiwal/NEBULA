import api from "../api/axios";

export async function getMessages(conversationId) {
  const response = await api.get(
    `/conversations/${conversationId}/messages`
  );

  return response.data;
}

export async function streamChat(conversationId, content, onChunk,signal) {
  const token = localStorage.getItem("token");

  const response = await fetch(
    `http://127.0.0.1:8000/chat/${conversationId}/stream`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({content}),
      signal,
    }
  );

  if (!response.ok) {
    throw new Error("Streaming failed.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();

    if (done) break;

    const chunk = decoder.decode(value);

    chunk
      .split("\n")
      .filter((line) => line.startsWith("data: "))
      .forEach((line) => {
        const text = line.replace("data: ", "");

        if (text !== "[DONE]") {
          onChunk(text);
        }
      });
  }
}