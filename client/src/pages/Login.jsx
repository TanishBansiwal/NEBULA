import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    setLoading(true);
    setError("");

    try {
      await login(email, password);
      navigate("/chat");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Invalid email or password."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">

      <div className="w-full max-w-md bg-slate-900 rounded-xl p-8 shadow-xl">

        <h1 className="text-3xl font-bold text-white mb-6">
          Login to Nebula
        </h1>

        {error && (
          <p className="mb-4 text-red-400">
            {error}
          </p>
        )}

        <form
          onSubmit={handleSubmit}
          className="space-y-4"
        >

          <input
            type="email"
            placeholder="Email"
            className="w-full rounded bg-slate-800 p-3 text-white"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full rounded bg-slate-800 p-3 text-white"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
          />

          <button
            disabled={loading}
            className="w-full rounded bg-blue-600 p-3 font-semibold hover:bg-blue-700"
          >
            {loading ? "Signing in..." : "Login"}
          </button>

        </form>

        <p className="mt-6 text-slate-400">

          Don't have an account?

          <Link
            to="/register"
            className="ml-2 text-blue-400"
          >
            Register
          </Link>

        </p>

      </div>

    </div>
  );
}