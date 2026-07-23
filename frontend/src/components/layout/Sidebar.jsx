import { useState, useEffect, useRef } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { Plus, FileText, MessageSquare, Pencil, Trash2 } from "lucide-react";
import { deleteDocument } from "@/services/documentService";
import useDocuments from "@/hooks/useDocuments";
import useSessions from "@/hooks/useSessions";

import UploadDialog from "@/components/upload/UploadDialog";

import {
  createSession,
  getMessages,
  renameSession,
  deleteSession
} from "@/services/chatSessionService";

export default function Sidebar({
  selectedDocument,
  setSelectedDocument,

  selectedSession,
  setSelectedSession,

  setMessages,
}) {
  const [openUpload, setOpenUpload] = useState(false);
  const [editingSessionId, setEditingSessionId] = useState(null);
  const [editedTitle, setEditedTitle] = useState(""); 
  const [searchQuery, setSearchQuery] = useState("");
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
  const filteredSessions = sessions.filter((session) =>
  session.title.toLowerCase().includes(searchQuery.toLowerCase())
);
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

const handleRenameSession = async (sessionId) => {

  const title = editedTitle.trim();

  if (!title) {
    return;
  }

  const session = sessions.find((s) => s.id === sessionId);

  if (session?.title === title) {
    setEditingSessionId(null);
    setEditedTitle("");
    return;
  }

  await renameSession(sessionId, title);

  await queryClient.invalidateQueries({
    queryKey: ["sessions"],
  });

  setEditingSessionId(null);
  setEditedTitle("");
};

const handleDeleteSession = async (sessionId) => {

  const confirmed = window.confirm(
    "Delete this chat?"
  );

  if (!confirmed) {
    return;
  }

  await deleteSession(sessionId);

  await queryClient.invalidateQueries({
    queryKey: ["sessions"],
  });

  if (selectedSession?.id === sessionId) {
    setSelectedSession(null);
    setMessages([]);
    localStorage.removeItem("selectedSessionId");
  }
};

const handleDeleteDocument = async (document) => {

  const confirmed = window.confirm(
    `Delete "${document.filename}"?`
  );

  if (!confirmed) return;

  await deleteDocument(document.id);

  await queryClient.invalidateQueries({
    queryKey: ["documents"],
  });

  if (selectedDocument?.id === document.id) {
    setSelectedDocument(null);
  }
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

              <div className="flex items-center justify-between">

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

  <Trash2
    size={16}
    className="cursor-pointer text-red-400 hover:text-red-300"
    onClick={(e) => {
      e.stopPropagation();
      handleDeleteDocument(doc);
    }}
  />

</div>

            </div>

          ))}

          <hr className="my-6 border-zinc-800" />

          <input
  type="text"
  placeholder="Search chats..."
  value={searchQuery}
  onChange={(e) => setSearchQuery(e.target.value)}
  className="mb-4 w-full rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-white outline-none focus:border-blue-500"
/>

          <p className="mb-4 text-xs uppercase tracking-widest text-zinc-500">
            Chats
          </p>

          {filteredSessions.map((session) => (

            <div
              key={session.id}
              onClick={() => handleSelectSession(session)}
              className={`mb-2 cursor-pointer rounded-xl p-3 transition ${
                selectedSession?.id === session.id
                  ? "bg-green-700"
                  : "hover:bg-zinc-900"
              }`}
            >

              <div className="flex items-center justify-between">

  <div className="flex items-center gap-3 flex-1">

    <MessageSquare size={18} />

    {editingSessionId === session.id ? (
      <input
        autoFocus
        value={editedTitle}
        onChange={(e) => setEditedTitle(e.target.value)}
        onClick={(e) => e.stopPropagation()}
       onKeyDown={(e) => {
  e.stopPropagation();

  if (e.key === "Enter") {
    handleRenameSession(session.id);
  }

  if (e.key === "Escape") {
    setEditingSessionId(null);
    setEditedTitle("");
  }
}}
        className="w-full rounded bg-zinc-800 px-2 py-1 text-sm outline-none"
      />
    ) : (
      <p className="truncate text-sm">
        {session.title}
      </p>
    )}

  </div>

<div className="flex items-center gap-2">

  <Pencil
    size={16}
    className="cursor-pointer text-zinc-400 hover:text-white"
    onClick={(e) => {
      e.stopPropagation();
      setEditingSessionId(session.id);
      setEditedTitle(session.title);
    }}
  />

  <Trash2
    size={16}
    className="cursor-pointer text-red-400 hover:text-red-300"
    onClick={(e) => {
      e.stopPropagation();
      handleDeleteSession(session.id);
    }}
  />

</div>

</div>


            </div>

          ))}

            {filteredSessions.length === 0 && (
            <p className="mt-2 text-center text-sm text-zinc-500">
              No chats found.
            </p>
          )}

        </div>

      </aside>
      

      <UploadDialog
        open={openUpload}
        onClose={() => setOpenUpload(false)}
      />

    </>
  );
}