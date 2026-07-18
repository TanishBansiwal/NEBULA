import api from "../api/axios";

export const login = async (email, password) => {
  const formData = new URLSearchParams();

  formData.append("username", email); // OAuth2 expects "username"
  formData.append("password", password);

  const response = await api.post(
    "/auth/login",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data;
};

export const register = async (email, username, password) => {
  const response = await api.post("/auth/register", {
    email,
    username,
    password,
  });

  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get("/users/me");
  return response.data;
};