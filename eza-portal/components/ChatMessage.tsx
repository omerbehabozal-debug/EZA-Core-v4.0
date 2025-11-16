"use client";

import React from "react";

interface ChatMessageProps {
  role: "user" | "assistant";
  text: string;
}

export default function ChatMessage({ role, text }: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div
      className={`w-full flex mb-4 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-[75%] px-4 py-3 rounded-xl text-sm leading-relaxed`}
        style={{
          background: isUser ? "#1A1E23" : "rgba(17,20,24,0.55)",
          backdropFilter: isUser ? "none" : "blur(4px)",
          border: "1px solid #1F2226",
          boxShadow: "0 4px 12px rgba(0,0,0,0.25)"
        }}
      >
        {text}
      </div>
    </div>
  );
}

