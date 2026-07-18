export default function TypingIndicator() {
  return (
    <div className="flex items-center gap-2 py-2">
      <div className="h-2 w-2 rounded-full bg-slate-400 animate-bounce"></div>

      <div
        className="h-2 w-2 rounded-full bg-slate-400 animate-bounce"
        style={{ animationDelay: "0.15s" }}
      ></div>

      <div
        className="h-2 w-2 rounded-full bg-slate-400 animate-bounce"
        style={{ animationDelay: "0.3s" }}
      ></div>
    </div>
  );
}