"use client";

import { useState, useRef, useEffect } from "react";
import { useChatStore } from "@/stores/chatStore";

export default function ChatInput() {
  const [message, setMessage] = useState("");
  const [placeholder, setPlaceholder] = useState("Mesaj yaz...");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const addMessage = useChatStore((s) => s.addMessage);
  const updateMessage = useChatStore((s) => s.updateMessage);
  const setAnalysis = useChatStore((s) => s.setAnalysis);
  const engineMode = useChatStore((s) => s.engineMode);
  const depthMode = useChatStore((s) => s.depthMode);
  const provider = useChatStore((s) => s.provider);
  const [loading, setLoading] = useState(false);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  }, [message]);

  // Animated placeholder
  useEffect(() => {
    const placeholders = [
      "Mesaj yaz...",
      "EZA'ya sor...",
      "Etik analiz için metin girin...",
    ];
    let index = 0;
    const interval = setInterval(() => {
      index = (index + 1) % placeholders.length;
      setPlaceholder(placeholders[index]);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  async function send() {
    if (!message.trim() || loading) return;

    const text = message.trim();
    const userMessageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    addMessage({ 
      id: userMessageId,
      role: "user", 
      text,
      timestamp: Date.now()
    });
    setMessage("");
    setLoading(true);

    try {
      if (engineMode === "standalone" || engineMode === "fast" || engineMode === "deep" || engineMode === "openai") {
        const r = await fetch("/api/analyze", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            message: text,
            mode: engineMode === "standalone" ? "standalone" : engineMode
          })
        });
        const j = await r.json();

        if (j.ok) {
          const analyzed = j.data;
          const fullAnalysis = {
            ...analyzed,
            _raw: analyzed._raw || analyzed
          };
          
          // Extract analysis data for messages (both user and assistant)
          const messageAnalysis = {
            eza_score: analyzed.eza_score,
            risk_level: analyzed.risk_level || analyzed._raw?.risk_level,
            intent: analyzed.intent?.level || analyzed._raw?.intent?.primary,
            intent_score: analyzed.intent?.score || analyzed._raw?.intent_score,
            bias: analyzed.bias,
            safety: analyzed.safety,
            rationale: analyzed._raw?.alignment_meta?.rationale || analyzed._raw?.final_verdict?.explanation,
            flags: analyzed._raw?.risk_flags || []
          };

          // Update user message with analysis
          updateMessage(userMessageId, {
            analysis: messageAnalysis
          });

          // Add audit log entry for user message
          useChatStore.getState().addAuditLogEntry(messageAnalysis);
          
          const assistant =
            analyzed.cleaned_output ||
            analyzed.output ||
            analyzed._raw?.rewritten_text ||
            analyzed._raw?.model_outputs?.chatgpt ||
            "EZA bir yanıt üretti.";

          const assistantMessageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
          addMessage({ 
            id: assistantMessageId,
            role: "assistant", 
            text: assistant,
            timestamp: Date.now(),
            analysis: messageAnalysis
          });
          setAnalysis(fullAnalysis);
          
          // Add audit entry
          useChatStore.getState().addAuditEntry({
            timestamp: new Date().toISOString(),
            message_id: assistantMessageId,
            analysis_snapshot: fullAnalysis
          });
          
          // Add audit log entry for assistant message
          useChatStore.getState().addAuditLogEntry(messageAnalysis);
          
          // Auto-select last assistant message
          useChatStore.getState().setSelectedMessageId(assistantMessageId);
        } else {
          const errorMessageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
          addMessage({
            id: errorMessageId,
            role: "assistant",
            text: `Hata: ${j.error || "EZA-Core analiz API yanıt vermedi."}`,
            timestamp: Date.now()
          });
        }
      } else {
        // Proxy Mode
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
          const errorMessageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
          addMessage({
            id: errorMessageId,
            role: "assistant",
            text: `Proxy hata: ${j.error ?? "bilinmeyen hata"}`,
            timestamp: Date.now()
          });
        } else {
          const { data } = j;
          const proxyAnalysis = data.analysis || undefined;
          
          // Update user message with analysis if available
          if (proxyAnalysis) {
            updateMessage(userMessageId, {
              analysis: proxyAnalysis
            });
            // Add audit log entry for user message
            useChatStore.getState().addAuditLogEntry(proxyAnalysis);
          }
          
          const assistantText = data.llm_output ?? "LLM cevabı alınamadı.";
          const assistantMessageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
          addMessage({ 
            id: assistantMessageId,
            role: "assistant", 
            text: assistantText,
            timestamp: Date.now(),
            analysis: proxyAnalysis
          });
          setAnalysis(data);
          
          // Add audit log entry for assistant message if analysis exists
          if (proxyAnalysis) {
            useChatStore.getState().addAuditLogEntry(proxyAnalysis);
          }
          
          // Auto-select last assistant message
          useChatStore.getState().setSelectedMessageId(assistantMessageId);
        }
      }
    } catch (err: any) {
      const errorMessageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      addMessage({
        id: errorMessageId,
        role: "assistant",
        text: `İstek sırasında hata oluştu: ${err?.message ?? "bilinmiyor"}`,
        timestamp: Date.now()
      });
    } finally {
      setLoading(false);
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (message.trim() && !loading) {
        send();
      }
    }
  };

  return (
    <div className="p-4 border-t border-panel/50 glass-strong">
      <div className="flex items-end gap-3 max-w-6xl mx-auto">
        {/* Mode Indicator (Left) */}
        <div className="hidden md:flex flex-col items-center gap-1 text-xs text-text-dim">
          <div className="w-8 h-8 rounded-full bg-panel/50 flex items-center justify-center">
            {engineMode === "deep" && "🔵"}
            {engineMode === "proxy" && "🟡"}
            {engineMode === "standalone" && "⚪"}
            {engineMode === "fast" && "⚡"}
            {engineMode === "openai" && "🤖"}
          </div>
          <span className="text-[10px]">{engineMode}</span>
        </div>

        {/* Input Area */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            rows={1}
            className="w-full px-4 py-3 pr-12 rounded-2xl bg-panel/50 border border-panel/50 text-text placeholder:text-text-dim resize-none outline-none focus:border-accent/50 focus:ring-2 focus:ring-accent/20 transition-all duration-200"
            disabled={loading}
            style={{
              minHeight: "48px",
              maxHeight: "120px",
            }}
          />
        </div>

        {/* Send Button */}
        <button
          onClick={send}
          disabled={loading || !message.trim()}
          className={`px-6 py-3 rounded-2xl font-medium text-sm transition-all duration-200 ${
            message.trim() && !loading
              ? "bg-accent text-bg shadow-accent-glow hover:shadow-accent-glow/80"
              : "bg-panel/50 text-text-dim cursor-not-allowed"
          }`}
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
              Gönderiliyor...
            </span>
          ) : (
            "Gönder"
          )}
        </button>
      </div>
    </div>
  );
}

