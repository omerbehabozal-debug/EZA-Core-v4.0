"use client";

import { useChatStore } from "@/stores/chatStore";

export default function AnalysisPanel() {
  const analysis = useChatStore(s => s.analysis);

  if (!analysis) return (
    <div className="p-4 text-neutral-400">
      ⓘ Mesaj gönderdikçe etik analiz burada görünecek.
    </div>
  );

  return (
    <div className="p-4 space-y-4 text-sm">
      <h2 className="text-lg font-semibold">Etik Analiz</h2>

      <div className="bg-neutral-900 p-3 rounded-lg">
        <p><b>EZA Skoru:</b> {analysis.eza_score}</p>
      </div>

      <div className="bg-neutral-900 p-3 rounded-lg">
        <p><b>Niyet:</b> {analysis.intent?.level}</p>
        <p><b>Özet:</b> {analysis.intent?.summary}</p>
      </div>

      <div className="bg-neutral-900 p-3 rounded-lg">
        <p><b>Bias:</b> {analysis.critical_bias?.level}</p>
      </div>

      <div className="bg-neutral-900 p-3 rounded-lg">
        <p><b>Abuse/Coercion:</b> {analysis.abuse?.level}</p>
      </div>

      <div className="bg-neutral-900 p-3 rounded-lg">
        <p><b>Moral Compass:</b> {analysis.moral?.level}</p>
      </div>

      <div className="bg-neutral-900 p-3 rounded-lg">
        <p><b>Memory Consistency:</b> {analysis.memory_consistency?.level}</p>
      </div>
    </div>
  );
}

