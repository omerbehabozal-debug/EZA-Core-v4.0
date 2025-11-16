"use client";

import { useState } from "react";
import { useChatStore } from "@/stores/chatStore";

export default function ChatInput() {
  const [message, setMessage] = useState("");
  const addMessage = useChatStore(s => s.addMessage);
  const setAnalysis = useChatStore(s => s.setAnalysis);

  async function send() {
    if (!message.trim()) return;

    addMessage({ role: "user", text: message });

    const r = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const j = await r.json();

    if (j.ok) {
      const analyzed = j.data;
      const assistant = analyzed.cleaned_output || analyzed.output || "EZA bir yanıt üretti.";

      addMessage({ role: "assistant", text: assistant });
      setAnalysis(analyzed);

    } else {
      addMessage({ role: "assistant", text: "Hata: API erişilemedi."});
    }

    setMessage("");
  }

  return (
    <div className="flex gap-2 p-4 border-t border-neutral-800">
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && send()}
        className="flex-1 p-3 bg-neutral-900 text-neutral-100 rounded-lg outline-none"
        placeholder="Mesaj yaz..."
      />

      <button onClick={send} className="bg-blue-600 px-4 rounded-lg">
        Gönder
      </button>
    </div>
  );
}

