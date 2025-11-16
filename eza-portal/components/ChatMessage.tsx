"use client";

import React from "react";

interface ChatMessageProps {
  role: "user" | "assistant";
  text: string;
}

export default function ChatMessage({ role, text }: ChatMessageProps) {
  const isUser = role === "user";
  return (
    <div className={`p-3 my-2 rounded-lg max-w-[70%] ${isUser ? "bg-blue-600 ml-auto" : "bg-neutral-800 mr-auto"}`}>
      {text}
    </div>
  );
}

