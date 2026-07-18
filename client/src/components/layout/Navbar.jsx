import { FiUser, FiLogOut } from "react-icons/fi";

export default function Navbar() {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900 flex items-center justify-between px-6">

      <div>
        <h1 className="text-xl font-semibold text-white">
          Nebula
        </h1>

        <p className="text-xs text-slate-400">
          AI Workspace
        </p>
      </div>

      <div className="flex items-center gap-4">

        <button className="hover:text-blue-400 transition">
          <FiUser size={20} />
        </button>

        <button className="hover:text-red-400 transition">
          <FiLogOut size={20} />
        </button>

      </div>

    </header>
  );
}