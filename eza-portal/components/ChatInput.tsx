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
    <div className="flex gap-2 p-4 border-t border-neutral-800">
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && send()}
        className="flex-1 p-3 bg-neutral-900 text-neutral-100 rounded-lg outline-none"
        placeholder={
          engineMode === "proxy"
            ? "Mesaj yaz (EZA Proxy + LLM)..."
            : "Mesaj yaz (sadece EZA-Core)..."
        }
      />

      <button
        onClick={send}
        disabled={loading}
        className="bg-blue-600 disabled:opacity-60 px-4 rounded-lg"
      >
        {loading ? "Gönderiliyor..." : "Gönder"}
      </button>
    </div>
  );
}
