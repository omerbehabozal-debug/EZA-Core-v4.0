"use client";

import { useState } from "react";
import { useChatStore } from "@/stores/chatStore";

export default function ChatInput() {
  const [message, setMessage] = useState("");
  const addMessage = useChatStore((s) => s.addMessage);
  const setAnalysis = useChatStore((s) => s.setAnalysis);
  const engineMode = useChatStore((s) => s.engineMode);
  const depthMode = useChatStore((s) => s.depthMode);
  const provider = useChatStore((s) => s.provider);

  const [loading, setLoading] = useState(false);

  async function send() {
    if (!message.trim() || loading) return;

    const text = message.trim();
    addMessage({ role: "user", text });
    setMessage("");
    setLoading(true);

    try {
      if (engineMode === "standalone") {
        // Eski /api/analyze akışı
        const r = await fetch("/api/analyze", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text })
        });
        const j = await r.json();

        if (j.ok) {
          const analyzed = j.data;
          const assistant =
            analyzed.cleaned_output ||
            analyzed.output ||
            "EZA bir yanıt üretti.";

          addMessage({ role: "assistant", text: assistant });
          setAnalysis(analyzed);
        } else {
          addMessage({
            role: "assistant",
            text: "Hata: EZA-Core analiz API yanıt vermedi."
          });
        }
      } else {
        // Proxy Mode: /api/proxy_chat
        const r = await fetch("/api/proxy_chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: text,
            mode: depthMode,
            provider
          })
        });

        const j = await r.json();

        if (!j.ok) {
          addMessage({
            role: "assistant",
            text: `Proxy hata: ${j.error ?? "bilinmeyen hata"}`
          });
        } else {
          const { data } = j;
          const assistantText = data.llm_output ?? "LLM cevabı alınamadı.";
          addMessage({ role: "assistant", text: assistantText });
          setAnalysis(data);
        }
      }
    } catch (err: any) {
      addMessage({
        role: "assistant",
        text: `İstek sırasında hata oluştu: ${err?.message ?? "bilinmiyor"}`
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-4 border-t border-neutral-800 flex gap-3 items-center bg-[#0F1418]">
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && message && send()}
        placeholder="Mesaj yaz..."
        className="flex-1 px-4 py-3 rounded-xl bg-[#13171D] border border-neutral-700 outline-none focus:border-blue-500 transition"
        disabled={loading}
      />

      <button
        onClick={() => message && send()}
        disabled={loading || !message.trim()}
        className="px-5 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 transition shadow disabled:opacity-60 disabled:cursor-not-allowed"
      >
        {loading ? "Gönderiliyor..." : "Gönder"}
      </button>
    </div>
  );
}
