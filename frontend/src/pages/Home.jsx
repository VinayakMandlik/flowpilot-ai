import { useEffect, useState } from "react";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import ChatArea from "@/components/chat/ChatArea";
import ChatInput from "@/components/layout/ChatInput";

export default function Home() {
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [selectedSession, setSelectedSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedDocument) {
      localStorage.setItem("selectedDocumentId", selectedDocument.id);
    }
  }, [selectedDocument]);

  useEffect(() => {
    if (selectedSession) {
      localStorage.setItem("selectedSessionId", selectedSession.id);
    }
  }, [selectedSession]);

  return (
    <div className="flex h-screen overflow-hidden bg-[#0A0A0A] text-white">
      <Sidebar
        selectedDocument={selectedDocument}
        setSelectedDocument={setSelectedDocument}
        selectedSession={selectedSession}
        setSelectedSession={setSelectedSession}
        setMessages={setMessages}
      />

      <div className="flex flex-1 flex-col">
        <Header />

        <ChatArea
          selectedDocument={selectedDocument}
          selectedSession={selectedSession}
          messages={messages}
          loading={loading}
        />

        <ChatInput
          selectedDocument={selectedDocument}
          selectedSession={selectedSession}
          messages={messages}
          setMessages={setMessages}
          loading={loading}
          setLoading={setLoading}
        />
      </div>
    </div>
  );
}