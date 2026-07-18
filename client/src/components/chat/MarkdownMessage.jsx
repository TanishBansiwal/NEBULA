import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import CodeBlock from "./CodeBlock";

export default function MarkdownMessage({ content }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        code({ inline, className, children }) {
        const match = /language-(\w+)/.exec(className || "");

        if (!inline) {
          return (
            <CodeBlock
              language={match?.[1]}
            >
              {String(children).replace(/\n$/, "")}
            </CodeBlock>
          );
        }

        return (
          <code className={className}>
            {children}
          </code>
        );
        }
      }}
    >
      {content}
    </ReactMarkdown>
  );
}