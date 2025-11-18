"use client";

import { useChatStore } from "@/stores/chatStore";
import FullJsonView from "./analysis/FullJsonView";

const RISK_COLORS: Record<string, string> = {
  none: "#6b7280",      // stone/gray
  low: "#22c55e",       // green
  medium: "#fbbf24",    // yellow
  high: "#fb923c",      // orange
  critical: "#ef4444",  // red
};

export default function AnalysisPanel() {
  const selectedMessageId = useChatStore((s) => s.selectedMessageId);
  const messages = useChatStore((s) => s.messages);

  // Find selected message
  let selectedMessage = selectedMessageId 
    ? messages.find(m => m.id === selectedMessageId)
    : null;

  // Fallback: if no message selected, use last message with analysis
  if (!selectedMessage) {
    const messagesWithAnalysis = messages.filter(m => m.analysis);
    selectedMessage = messagesWithAnalysis.at(-1) || null;
  }

  // If no message with analysis found, show placeholder
  if (!selectedMessage || !selectedMessage.analysis) {
    return (
      <div className="w-full h-full p-6 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 rounded-full bg-panel/30 flex items-center justify-center mb-4 mx-auto">
            <span className="text-2xl">⚖</span>
          </div>
          <p className="text-neutral-400 text-sm">
            Bir mesajın risk noktasına tıklayarak analiz detaylarını görüntüleyin.
          </p>
        </div>
      </div>
    );
  }

  const analysis = selectedMessage.analysis;
  const riskColor = RISK_COLORS[analysis.risk_level?.toLowerCase() || "none"] || RISK_COLORS.none;

  return (
    <div className="w-full h-full overflow-y-auto p-6 space-y-6">
      {/* EZA Score - Circular with colored border */}
      <div className="flex flex-col items-center">
        <div className="relative w-32 h-32">
          {/* Outer circle with risk color */}
          <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 120 120">
            {/* Background circle */}
            <circle
              cx="60"
              cy="60"
              r="54"
              fill="none"
              stroke="rgba(107, 114, 128, 0.2)"
              strokeWidth="8"
            />
            {/* Progress circle with risk color */}
            <circle
              cx="60"
              cy="60"
              r="54"
              fill="none"
              stroke={riskColor}
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={`${2 * Math.PI * 54}`}
              strokeDashoffset={`${2 * Math.PI * 54 * (1 - (analysis.eza_score || 0) / 100)}`}
              style={{ transition: "stroke-dashoffset 0.5s ease" }}
            />
          </svg>
          {/* Center content */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className="text-3xl font-bold" style={{ color: riskColor }}>
                {analysis.eza_score?.toFixed(0) || "—"}
              </div>
              <div className="text-xs text-neutral-400 mt-1">EZA Score</div>
            </div>
          </div>
        </div>
      </div>

      {/* Risk Level */}
      <div className="bg-neutral-900 border border-neutral-700 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <span className="text-neutral-400 text-sm">Risk Level</span>
          <span 
            className="px-3 py-1 rounded-full text-sm font-medium"
            style={{ 
              backgroundColor: `${riskColor}20`,
              color: riskColor,
              border: `1px solid ${riskColor}40`
            }}
          >
            {analysis.risk_level || "none"}
          </span>
        </div>
      </div>

      {/* Intent + Score */}
      {analysis.intent && (
        <div className="bg-neutral-900 border border-neutral-700 rounded-lg p-4">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-neutral-400 text-sm">Intent</span>
              <span className="text-neutral-300 font-medium">{analysis.intent}</span>
            </div>
            {analysis.intent_score !== undefined && (
              <div className="flex items-center justify-between">
                <span className="text-neutral-400 text-sm">Intent Score</span>
                <span className="text-neutral-300">{analysis.intent_score.toFixed(2)}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Safety */}
      {analysis.safety && (
        <div className="bg-neutral-900 border border-neutral-700 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <span className="text-neutral-400 text-sm">Safety</span>
            <span className="text-neutral-300 font-medium">{analysis.safety}</span>
          </div>
        </div>
      )}

      {/* Bias */}
      {analysis.bias && (
        <div className="bg-neutral-900 border border-neutral-700 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <span className="text-neutral-400 text-sm">Bias</span>
            <span className="text-neutral-300 font-medium">{analysis.bias}</span>
          </div>
        </div>
      )}

      {/* Flags */}
      {analysis.flags && analysis.flags.length > 0 && (
        <div className="bg-neutral-900 border border-neutral-700 rounded-lg p-4">
          <div className="space-y-2">
            <span className="text-neutral-400 text-sm block mb-2">Flags</span>
            <div className="flex flex-wrap gap-2">
              {analysis.flags.map((flag: string, index: number) => (
                <span
                  key={index}
                  className="px-2 py-1 rounded bg-red-500/20 text-red-400 text-xs border border-red-500/30"
                >
                  {flag}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Why This Score? */}
      {analysis.rationale && (
        <div className="bg-neutral-900 border border-neutral-700 rounded-lg p-4">
          <h3 className="text-neutral-300 text-sm font-medium mb-2">Why this score?</h3>
          <p className="text-neutral-400 text-sm leading-relaxed">{analysis.rationale}</p>
        </div>
      )}

      {/* Full JSON View Button */}
      <div className="flex justify-center">
        <FullJsonView 
          data={selectedMessage.analysis} 
          messageId={selectedMessage.id}
        />
      </div>
    </div>
  );
}
