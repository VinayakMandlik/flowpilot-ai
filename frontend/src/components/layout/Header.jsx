import { Sparkles } from "lucide-react";

export default function Header() {
  return (
    <header className="flex h-16 items-center justify-center border-b border-zinc-800">
      <div className="flex items-center gap-3">

        <Sparkles className="text-blue-500" size={22} />

        <h1 className="text-xl font-semibold tracking-tight">
          FlowPilot AI
        </h1>

      </div>
    </header>
  );
}