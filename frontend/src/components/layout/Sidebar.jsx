import { useState, useEffect, useRef } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { Plus, FileText, MessageSquare } from "lucide-react";

import useDocuments from "@/hooks/useDocuments";
import useSessions from "@/hooks/useSessions";

import UploadDialog from "@/components/upload/UploadDialog";

import {
  createSession,
  getMessages,
} from "@/services/chatSessionService";

export default function Sidebar({
  selectedDocument,
  setSelectedDocument,

  selectedSession,
  setSelectedSession,

  setMessages,
}) {
  const [openUpload, setOpenUpload] = useState(false);
  const restoredRef = useRef(false);
  const queryClient = useQueryClient();

  const {
    data: documents = [],
    isLoading,
    isError,
    error,
  } = useDocuments();

  const {
    data: sessions = [],
  } = useSessions();
useEffect(() => {
  if (restoredRef.current) return;
  if (!documents.length || !sessions.length) return;

  restoredRef.current = true;

  const savedDocumentId = localStorage.getItem("selectedDocumentId");
  const savedSessionId = localStorage.getItem("selectedSessionId");

  if (savedDocumentId && !selectedDocument) {
    const doc = documents.find(
      (d) => String(d.id) === String(savedDocumentId)
    );

    if (doc) {
      setSelectedDocument(doc);
    }
  }

  if (savedSessionId && !selectedSession) {
    const session = sessions.find(
      (s) => String(s.id) === String(savedSessionId)
    );

    if (session) {
      handleSelectSession(session);
    }
  }
}, [documents, sessions]);

const handleNewChat = async () => {

  if (!selectedDocument) {
    alert("Please select a document first.");
    return;
  }

  const session = await createSession(
    selectedDocument.filename,
    selectedDocument.id
  );

  queryClient.invalidateQueries({
    queryKey: ["sessions"],
  });

  setSelectedSession(session);

  // Save the newly created session as the active one
  localStorage.setItem("selectedSessionId", session.id);
  localStorage.setItem("selectedDocumentId", selectedDocument.id);

  setMessages([]);
};

  const handleSelectSession = async (session) => {

  const matchedDocument = documents.find(
    (doc) => doc.id === session.document_id
  );

  if (matchedDocument) {
    setSelectedDocument(matchedDocument);
  }

  setSelectedSession(session);

  // Save current selection
  localStorage.setItem("selectedDocumentId", session.document_id);
  localStorage.setItem("selectedSessionId", session.id);

  const history = await getMessages(session.id);

  const formatted = [];

  for (let i = 0; i < history.length; i += 2) {
    formatted.push({
      question: history[i]?.content || "",
      answer: history[i + 1]?.content || "",
      sources: history[i + 1]?.sources || [],
    });
  }

  setMessages(formatted);
};


  return (
    <>
      <aside className="flex w-72 flex-col border-r border-zinc-800 bg-[#050505]">

        <div className="p-5">

          <button
            onClick={() => setOpenUpload(true)}
            className="mb-3 flex w-full items-center justify-center gap-2 rounded-xl bg-white py-3 font-medium text-black hover:bg-zinc-200"
          >
            <Plus size={18} />
            Upload
          </button>

          <button
            onClick={handleNewChat}
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 py-3 text-white hover:bg-blue-700"
          >
            <MessageSquare size={18} />
            New Chat
          </button>

        </div>

        <div className="flex-1 overflow-y-auto px-4">

          <p className="mb-4 text-xs uppercase tracking-widest text-zinc-500">
            Documents
          </p>

          {isLoading && (
            <p className="text-zinc-500">
              Loading...
            </p>
          )}

          {isError && (
            <p className="text-red-500">
              {error?.message}
            </p>
          )}

          {documents.map((doc) => (

            <div
              key={doc.id}
              onClick={() => {
  setSelectedDocument(doc);
  localStorage.setItem("selectedDocumentId", doc.id);
}}
              className={`mb-2 cursor-pointer rounded-xl p-3 transition ${
                selectedDocument?.id === doc.id
                  ? "bg-blue-600"
                  : "hover:bg-zinc-900"
              }`}
            >

              <div className="flex items-center gap-3">

                <FileText size={18} />

                <div className="min-w-0">

                  <p className="truncate text-sm">
                    {doc.filename}
                  </p>

                  <p className="text-xs text-zinc-400">
                    {doc.total_chunks} chunks
                  </p>

                </div>

              </div>

            </div>

          ))}

          <hr className="my-6 border-zinc-800" />

          <p className="mb-4 text-xs uppercase tracking-widest text-zinc-500">
            Chats
          </p>

          {sessions.map((session) => (

            <div
              key={session.id}
              onClick={() => handleSelectSession(session)}
              className={`mb-2 cursor-pointer rounded-xl p-3 transition ${
                selectedSession?.id === session.id
                  ? "bg-green-700"
                  : "hover:bg-zinc-900"
              }`}
            >

              <div className="flex items-center gap-3">

                <MessageSquare size={18} />

                <p className="truncate text-sm">
                  {session.title}
                </p>

              </div>

            </div>

          ))}

        </div>

      </aside>

      <UploadDialog
        open={openUpload}
        onClose={() => setOpenUpload(false)}
      />

    </>
  );
}