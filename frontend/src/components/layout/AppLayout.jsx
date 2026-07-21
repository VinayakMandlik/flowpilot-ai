import { useState } from "react";

import Sidebar from "./Sidebar";
import ChatWindow from "../chat/ChatWindow";
import ChatInput from "../chat/ChatInput";
import DocumentPanel from "../document/DocumentPanel";

export default function AppLayout() {

    const [selectedDocument, setSelectedDocument] = useState(null);

    return (
        <div className="h-screen bg-zinc-950 text-white flex overflow-hidden">

            <aside className="w-72 border-r border-zinc-800">

                <Sidebar
                    selectedDocument={selectedDocument}
                    setSelectedDocument={setSelectedDocument}
                />

            </aside>

            <main className="flex-1 flex flex-col">

                <section className="flex-1 overflow-auto">

                    <ChatWindow
                        selectedDocument={selectedDocument}
                    />

                </section>

                <section className="border-t border-zinc-800">

                    <ChatInput
                        selectedDocument={selectedDocument}
                    />

                </section>

            </main>

            <aside className="w-80 border-l border-zinc-800">

                <DocumentPanel
                    selectedDocument={selectedDocument}
                />

            </aside>

        </div>
    );
}