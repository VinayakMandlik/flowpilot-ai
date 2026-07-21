import { useState } from "react";
import { ArrowUp } from "lucide-react";

export default function ChatInput({
  selectedDocument,
  selectedSession,
  messages,
  setMessages,
  loading,
  setLoading,
}) {
  const [question, setQuestion] = useState("");

  const askQuestion = async () => {
    if (!question.trim()) return;

    if (!selectedDocument) {
      alert("Please select a document.");
      return;
    }

    if (!selectedSession) {
      alert("Please create a chat first.");
      return;
    }

    const userQuestion = question;

    setQuestion("");
    setLoading(true);

    // Add user's question with an empty AI response
    setMessages((prev) => [
      ...prev,
      {
        question: userQuestion,
        answer: "",
        sources: [],
      },
    ]);

    try {
      const response = await fetch(
        "http://localhost:8000/api/v1/chat/document",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: userQuestion,
            document_id: selectedDocument.id,
            session_id: selectedSession.id,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to connect to server.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();

        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        const events = buffer.split("\n\n");
        buffer = events.pop() || "";

        for (const event of events) {
          if (!event.startsWith("data: ")) continue;

          const json = JSON.parse(event.substring(6));

          if (json.type === "token") {
            setMessages((prev) => {
              const updated = [...prev];

              updated[updated.length - 1] = {
                ...updated[updated.length - 1],
                answer:
                  updated[updated.length - 1].answer + json.content,
              };

              return updated;
            });
          }

          if (json.type === "sources") {
            setMessages((prev) => {
              const updated = [...prev];

              updated[updated.length - 1] = {
                ...updated[updated.length - 1],
                sources: json.content,
              };

              return updated;
            });
          }

          if (json.type === "done") {
            setLoading(false);
          }
        }
      }
    } catch (error) {
      console.error(error);
      alert("Failed to get response.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="border-t border-zinc-800 p-6">
      <div className="mx-auto flex max-w-4xl rounded-3xl border border-zinc-700 bg-zinc-900 p-2">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              askQuestion();
            }
          }}
          placeholder={
            selectedSession
              ? "Ask anything..."
              : "Create a chat first..."
          }
          disabled={!selectedSession || loading}
          className="flex-1 bg-transparent px-4 outline-none disabled:opacity-50"
        />

        <button
          onClick={askQuestion}
          disabled={!selectedSession || loading}
          className="rounded-2xl bg-white p-3 text-black hover:bg-zinc-200 disabled:opacity-50"
        >
          <ArrowUp size={18} />
        </button>
      </div>
    </div>
  );
}