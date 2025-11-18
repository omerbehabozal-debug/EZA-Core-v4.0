"use client";

import { useState } from "react";
import { useChatStore, Msg } from "@/stores/chatStore";
import RiskDot from "@/components/analysis/RiskDot";

interface MessageBubbleProps {
  message: Msg;
  index: number;
}

export default function MessageBubble({ message, index }: MessageBubbleProps) {
  const [showActions, setShowActions] = useState(false);
  const selectedMessageId = useChatStore((s) => s.selectedMessageId);

  const isUser = message.role === "user";
  const isSelected = selectedMessageId === message.id;
  const analysis = message.analysis;

  return (
    <div
      className={`w-full flex mb-4 animate-slide-in ${
        isUser ? "justify-end" : "justify-start"
      }`}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      <div className="max-w-[75%] relative group">
        {/* Message Bubble */}
        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed transition-all duration-200 relative ${
            isUser
              ? "bg-gradient-to-br from-blue-600 to-blue-700 text-white"
              : "glass text-text border border-panel/50"
          } ${
            isSelected ? "ring-2 ring-accent ring-offset-2 ring-offset-bg" : ""
          }`}
          style={{
            boxShadow: isUser
              ? "0 4px 12px rgba(59, 130, 246, 0.3)"
              : "0 4px 12px rgba(0, 0, 0, 0.25)",
          }}
        >
          {message.text}
          
          {/* Risk Dot - Bottom Right Corner (for both user and assistant if analysis exists) */}
          {analysis && (
            <div className="absolute bottom-2 right-2" style={{ zIndex: 10, pointerEvents: "auto" }}>
              <RiskDot
                messageId={message.id}
                riskLevel={analysis.risk_level}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

