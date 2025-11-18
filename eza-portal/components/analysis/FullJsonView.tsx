"use client";

import { useState } from "react";
import { useChatStore } from "@/stores/chatStore";

interface FullJsonViewProps {
  data: any;
  messageId: string;
}

export default function FullJsonView({ data, messageId }: FullJsonViewProps) {
  const [isOpen, setIsOpen] = useState(false);

  if (!data) return null;

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="text-xs text-text-dim hover:text-accent transition-colors px-2 py-1 rounded hover:bg-panel/30"
      >
        📄 Full JSON
      </button>

      {isOpen && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
          onClick={() => setIsOpen(false)}
        >
          <div
            className="bg-panel border border-panel-border rounded-lg shadow-2xl max-w-4xl w-full mx-4 max-h-[90vh] flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-panel-border">
              <h3 className="text-lg font-semibold text-text">
                Full JSON View - Message {messageId}
              </h3>
              <button
                onClick={() => setIsOpen(false)}
                className="text-text-dim hover:text-text transition-colors"
              >
                ✕
              </button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-auto p-4">
              <pre className="text-xs text-text-dim font-mono bg-bg/50 p-4 rounded border border-panel-border overflow-auto">
                {JSON.stringify(fullData, null, 2)}
              </pre>
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-panel-border flex justify-end gap-2">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(JSON.stringify(fullData, null, 2));
                }}
                className="px-3 py-1.5 text-xs bg-accent/20 text-accent rounded hover:bg-accent/30 transition-colors"
              >
                📋 Copy JSON
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="px-3 py-1.5 text-xs bg-panel-border text-text rounded hover:bg-panel-border/80 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

