import { useState } from "react";
import { FiCopy, FiCheck } from "react-icons/fi";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

export default function CodeBlock({
  language,
  children,
}) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    await navigator.clipboard.writeText(children);

    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 2000);
  }

  return (
    <div className="rounded-xl overflow-hidden border border-slate-700 my-4">

      <div className="flex items-center justify-between bg-slate-900 px-4 py-2">

        <span className="text-xs uppercase text-slate-400">
          {language || "text"}
        </span>

        <button
          onClick={handleCopy}
          className="flex items-center gap-2 text-sm text-slate-300 hover:text-white"
        >
          {copied ? (
            <>
              <FiCheck />
              Copied
            </>
          ) : (
            <>
              <FiCopy />
              Copy
            </>
          )}
        </button>

      </div>

      <SyntaxHighlighter
        language={language}
        style={oneDark}
        customStyle={{
          margin: 0,
          borderRadius: 0,
        }}
      >
        {children}
      </SyntaxHighlighter>

    </div>
  );
}