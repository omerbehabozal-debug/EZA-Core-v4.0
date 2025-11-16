"use client";

import ChatInput from "@/components/ChatInput";
import ChatMessage from "@/components/ChatMessage";
import AnalysisPanel from "@/components/AnalysisPanel";
import TopBar from "@/components/TopBar";
import { useChatStore } from "@/stores/chatStore";

export default function ChatPage() {
  const messages = useChatStore((s) => s.messages);

  return (
    <div className="flex flex-col h-screen">
      <TopBar />

      <div className="flex flex-1">
        <div className="flex flex-col flex-1">
          <div className="flex-1 overflow-y-auto p-6">
            {messages.map((m, i) => (
              <ChatMessage key={i} role={m.role} text={m.text} />
            ))}
          </div>

          <ChatInput />
        </div>

        <div className="w-[350px] border-l border-neutral-800 bg-neutral-950 overflow-y-auto">
          <AnalysisPanel />
        </div>
      </div>
    </div>
  );
}
