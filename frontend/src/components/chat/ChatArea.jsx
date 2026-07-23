import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";

import "highlight.js/styles/github-dark.css";

export default function ChatArea({
  selectedDocument,
  selectedSession,
  messages,
  loading,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  if (!selectedDocument) {
    return (
      <main className="flex flex-1 items-center justify-center">
        <div className="text-center">
          <h2 className="mb-3 text-4xl font-bold">
            Welcome to FlowPilot
          </h2>

          <p className="text-zinc-400">
            Select a document to begin.
          </p>
        </div>
      </main>
    );
  }

  if (!selectedSession) {
    return (
      <main className="flex flex-1 items-center justify-center">
        <div className="text-center">
          <h2 className="mb-3 text-3xl font-bold">
            {selectedDocument.filename}
          </h2>

          <p className="text-zinc-400">
            Create a new chat to start asking questions.
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="flex-1 overflow-y-auto bg-[#0A0A0A]">
      <div className="mx-auto flex max-w-5xl flex-col p-8">

        <div className="sticky top-0 z-10 mb-8 rounded-xl border border-zinc-800 bg-[#0A0A0A]/90 p-4 backdrop-blur">
          <p className="text-xs uppercase tracking-widest text-zinc-500">
            Current Chat
          </p>

          <h2 className="mt-1 text-xl font-semibold">
            {selectedSession.title}
          </h2>

          <p className="mt-1 text-sm text-zinc-400">
            {selectedDocument.filename}
          </p>
        </div>

        {messages.length === 0 && (
          <div className="mt-20 text-center text-zinc-500">
            Ask your first question.
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className="mb-10">

            {/* USER */}

            <div className="mb-5 flex justify-end">
              <div className="max-w-3xl rounded-2xl bg-blue-600 px-5 py-4 text-white shadow">
                {msg.question}
              </div>
            </div>

            {/* AI */}

            <div className="flex justify-start">
              <div className="prose prose-invert max-w-4xl rounded-2xl border border-zinc-800 bg-zinc-900 px-6 py-5 shadow">

                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeHighlight]}
                >
                  {msg.answer}
                </ReactMarkdown>

                {msg.sources?.length > 0 && (
                  <>
                    <div className="my-5 border-t border-zinc-700" />

                    <p className="mb-3 text-xs font-semibold uppercase tracking-widest text-zinc-400">
                      Sources
                    </p>

                    <div className="space-y-3">
                      {msg.sources.map((source, idx) => (
                        <div
                          key={idx}
                          className="rounded-xl border border-zinc-700 bg-zinc-950 p-4"
                        >
                          <p className="font-medium">
                            📄 {source.filename}
                          </p>

                          <p className="mt-1 text-sm text-zinc-400">
  📄 Page {source.page}
</p>

                        <p className="mt-1 text-sm text-zinc-400">
                          Chunk #{source.chunk_number}
                        </p>

                        <p className="mt-1 text-sm text-green-400">
                          {(source.score * 100).toFixed(1)}% Similarity
                        </p>
                        </div>
                      ))}
                    </div>
                  </>
                )}

              </div>
            </div>

          </div>
        ))}

        {loading && (
          <div className="mb-10 flex">
            <div className="rounded-2xl border border-zinc-700 bg-zinc-900 px-5 py-4 text-zinc-400">
              <span className="animate-pulse">
                FlowPilot is thinking...
              </span>
            </div>
          </div>
        )}

        <div ref={bottomRef} />

      </div>
    </main>
  );
}