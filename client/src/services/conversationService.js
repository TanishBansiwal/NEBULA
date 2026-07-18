import api from "../api/axios";

export async function getConversations() {
  const response = await api.get("/conversations");
  return response.data;
}

export async function createConversation(title = "New Chat") {
  const response = await api.post("/conversations", {
    title,
  });

  return response.data;
}

export async function deleteConversation(id) {
  await api.delete(`/conversations/${id}`);
}