"use client";

import { useState } from "react";
import ChatInput from "@/components/ChatInput";
import ChatMessage from "@/components/ChatMessage";
import AnalysisPanel from "@/components/AnalysisPanel";
import TopBar from "@/components/TopBar";
import { useChatStore } from "@/stores/chatStore";

export default function ChatPage() {
  const messages = useChatStore((s) => s.messages);
  const analysis = useChatStore((s) => s.analysis);
  const [showAnalysisPanel, setShowAnalysisPanel] = useState(false);

  return (
    <div className="flex flex-col h-screen bg-[#0D0F12]">
      <TopBar />

      <div className="flex flex-1 overflow-hidden">
        {/* Main Chat Area */}
        <div className="flex flex-col flex-1 min-w-0">
          <div className="flex-1 overflow-y-auto p-4 md:p-6">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full text-neutral-500 text-sm">
                Mesaj göndermek için aşağıdaki alanı kullanın
              </div>
            ) : (
              messages.map((m, i) => (
                <ChatMessage key={i} role={m.role} text={m.text} />
              ))
            )}
          </div>

          <ChatInput />
        </div>

        {/* Desktop Analysis Panel */}
        <div className="hidden lg:block w-[350px] border-l border-neutral-800 bg-[#0D0F12] overflow-y-auto">
          <AnalysisPanel />
        </div>
      </div>

      {/* Mobile Analysis Panel - Bottom Sheet */}
      {analysis && (
        <>
          {/* Overlay */}
          <div
            className={`lg:hidden fixed inset-0 bg-black/50 z-40 transition-opacity ${
              showAnalysisPanel ? "opacity-100" : "opacity-0 pointer-events-none"
            }`}
            onClick={() => setShowAnalysisPanel(false)}
          />

          {/* Bottom Sheet */}
          <div
            className={`lg:hidden fixed bottom-0 left-0 right-0 bg-[#111418] border-t border-neutral-800 rounded-t-2xl z-50 transition-transform duration-300 ${
              showAnalysisPanel ? "translate-y-0" : "translate-y-full"
            }`}
            style={{
              maxHeight: "80vh",
              boxShadow: "0 -8px 20px rgba(0,0,0,0.25)"
            }}
          >
            {/* Handle */}
            <div className="flex justify-center pt-3 pb-2">
              <div className="w-12 h-1 bg-neutral-700 rounded-full" />
            </div>

            {/* Header */}
            <div className="flex items-center justify-between px-4 pb-3 border-b border-neutral-800">
              <h2 className="text-lg font-semibold">Etik Analiz</h2>
              <button
                onClick={() => setShowAnalysisPanel(false)}
                className="text-neutral-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            {/* Content */}
            <div className="overflow-y-auto" style={{ maxHeight: "calc(80vh - 80px)" }}>
              <AnalysisPanel />
            </div>
          </div>

          {/* Mobile Toggle Button */}
          <button
            onClick={() => setShowAnalysisPanel(!showAnalysisPanel)}
            className="lg:hidden fixed bottom-20 right-4 bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-full shadow-lg z-30 transition"
          >
            {showAnalysisPanel ? "✕" : "📊"}
          </button>
        </>
      )}
    </div>
  );
}
