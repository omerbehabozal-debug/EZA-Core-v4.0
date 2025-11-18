"use client";

import { useChatStore } from "@/stores/chatStore";

interface RiskDotProps {
  messageId: string;
  riskLevel?: string | null;
}

const RISK_COLORS: Record<string, string> = {
  none: "#6b7280",      // stone/gray
  low: "#22c55e",       // green
  medium: "#fbbf24",    // yellow
  high: "#fb923c",      // orange
  critical: "#ef4444",  // red
};

export default function RiskDot({ messageId, riskLevel = "none" }: RiskDotProps) {
  const setSelectedMessageId = useChatStore((s) => s.setSelectedMessageId);
  const color = RISK_COLORS[riskLevel?.toLowerCase() || "none"] || RISK_COLORS.none;
  const displayLevel = riskLevel || "none";

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    e.preventDefault();
    setSelectedMessageId(messageId);
  };

  return (
    <div
      className="relative group"
      onClick={handleClick}
      style={{ zIndex: 10 }}
    >
      <div
        className="w-[10px] h-[10px] rounded-full cursor-pointer transition-all hover:scale-125"
        style={{ backgroundColor: color, pointerEvents: "auto" }}
      />
      {/* Tooltip */}
      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-neutral-900 text-neutral-300 text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50 border border-neutral-700">
        Risk: {displayLevel}
        <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1">
          <div className="w-2 h-2 bg-neutral-900 border-r border-b border-neutral-700 transform rotate-45"></div>
        </div>
      </div>
    </div>
  );
}

