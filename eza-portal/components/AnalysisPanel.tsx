"use client";

import { useChatStore } from "@/stores/chatStore";

export default function AnalysisPanel() {
  const analysis = useChatStore((s) => s.analysis);
  const engineMode = useChatStore((s) => s.engineMode);
  const depthMode = useChatStore((s) => s.depthMode);

  if (!analysis) {
    return (
      <div className="w-full p-4">
        <div className="text-neutral-500 text-sm">
          ⓘ Analiz sonuçları burada görünecek.
        </div>
      </div>
    );
  }

  // Standalone mod: eski /analyze response
  if (engineMode === "standalone") {
    return (
      <div className="w-full p-4 space-y-4">
        {/* EZA Score */}
        <div className="bg-[#111418] border border-neutral-800 p-4 rounded-xl shadow">
          <h3 className="text-neutral-300 text-sm">EZA Skoru</h3>
          <p className="text-2xl font-semibold mt-1">
            {analysis.eza_score?.eza_score ?? analysis.eza_score ?? "—"}
          </p>
        </div>

        {/* Intent */}
        {analysis.intent && (
          <div className="bg-[#111418] border border-neutral-800 p-4 rounded-xl shadow">
            <h3 className="text-neutral-300 text-sm">Niyet Analizi</h3>
            <p className="text-lg font-medium mt-1">
              {analysis.intent.level ?? "—"}
            </p>
            <p className="text-neutral-400 text-xs mt-1">
              {analysis.intent.summary ?? "—"}
            </p>
          </div>
        )}

        {/* Bias */}
        {analysis.critical_bias && (
          <div className="bg-[#111418] border border-neutral-800 p-4 rounded-xl shadow">
            <h3 className="text-neutral-300 text-sm">Bias Analizi</h3>
            <p className="text-lg font-medium mt-1">
              {analysis.critical_bias.level ?? "—"}
            </p>
            <p className="text-neutral-400 text-xs mt-1">
              Skor: {analysis.critical_bias.bias_score ?? "—"}
            </p>
          </div>
        )}

        {/* Abuse */}
        {analysis.abuse && (
          <div className="bg-[#111418] border border-neutral-800 p-4 rounded-xl shadow">
            <h3 className="text-neutral-300 text-sm">Abuse Analizi</h3>
            <p className="text-lg font-medium mt-1">
              {analysis.abuse.level ?? "—"}
            </p>
          </div>
        )}

        {/* Moral Compass */}
        {analysis.moral_compass && (
          <div className="bg-[#111418] border border-neutral-800 p-4 rounded-xl shadow">
            <h3 className="text-neutral-300 text-sm">Moral Compass</h3>
            <p className="text-lg font-medium mt-1">
              {analysis.moral_compass.level ?? "—"}
            </p>
          </div>
        )}

        {/* Memory Consistency */}
        {analysis.memory_consistency && (
          <div className="bg-[#111418] border border-neutral-800 p-4 rounded-xl shadow">
            <h3 className="text-neutral-300 text-sm">Memory Consistency</h3>
            <p className="text-lg font-medium mt-1">
              {analysis.memory_consistency.level ?? "—"}
            </p>
          </div>
        )}
      </div>
    );
  }

  // Proxy mode analizi: input + output
  const input = analysis.input_analysis;
  const output = analysis.output_analysis;

  return (
    <div className="w-full p-4 space-y-4">
      <h2 className="text-lg font-semibold mb-2">
        Etik Analiz (Proxy — {depthMode.toUpperCase()})
      </h2>

      {/* Input analizi */}
      {input && (
        <div className="bg-[#111418] border border-neutral-800 p-4 rounded-xl shadow space-y-2">
          <h3 className="text-neutral-300 text-sm font-semibold">Input Analizi</h3>
          <div>
            <p className="text-xs text-neutral-400">EZA Skoru</p>
            <p className="text-lg font-medium">
              {input.eza_score?.eza_score ?? input.eza_score ?? "—"}
            </p>
          </div>
          {input.intent && (
            <div>
              <p className="text-xs text-neutral-400">Niyet</p>
              <p className="text-sm">{input.intent.level ?? "—"}</p>
            </div>
          )}
          {input.abuse && (
            <div>
              <p className="text-xs text-neutral-400">Abuse</p>
              <p className="text-sm">{input.abuse.level ?? "—"}</p>
            </div>
          )}
          {input.critical_bias && (
            <div>
              <p className="text-xs text-neutral-400">Bias</p>
              <p className="text-sm">{input.critical_bias.level ?? "—"}</p>
            </div>
          )}
        </div>
      )}

      {/* Output analizi */}
      {output ? (
        <div className="bg-[#111418] border border-neutral-800 p-4 rounded-xl shadow space-y-2">
          <h3 className="text-neutral-300 text-sm font-semibold">Output Analizi</h3>
          <div>
            <p className="text-xs text-neutral-400">EZA Skoru</p>
            <p className="text-lg font-medium">
              {output.eza_score?.eza_score ?? output.eza_score ?? "—"}
            </p>
          </div>
          {output.intent && (
            <div>
              <p className="text-xs text-neutral-400">Niyet</p>
              <p className="text-sm">{output.intent.level ?? "—"}</p>
            </div>
          )}
          {output.abuse && (
            <div>
              <p className="text-xs text-neutral-400">Abuse</p>
              <p className="text-sm">{output.abuse.level ?? "—"}</p>
            </div>
          )}
          {output.critical_bias && (
            <div>
              <p className="text-xs text-neutral-400">Bias</p>
              <p className="text-sm">{output.critical_bias.level ?? "—"}</p>
            </div>
          )}
        </div>
      ) : (
        <div className="bg-[#111418] border border-neutral-800 p-4 rounded-xl shadow text-neutral-400 text-xs">
          {depthMode === "fast"
            ? "Fast Mode: Çıkış analizi minimal veya atlanmış olabilir."
            : "Output analizi mevcut değil."}
        </div>
      )}
    </div>
  );
}
