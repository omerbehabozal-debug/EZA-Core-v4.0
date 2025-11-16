"use client";

import { useChatStore } from "@/stores/chatStore";

export default function AnalysisPanel() {
  const analysis = useChatStore((s) => s.analysis);
  const engineMode = useChatStore((s) => s.engineMode);
  const depthMode = useChatStore((s) => s.depthMode);

  if (!analysis) {
    return (
      <div className="p-4 text-neutral-400 text-sm">
        ⓘ Mesaj gönderdikçe EZA analizleri burada görünecek.
      </div>
    );
  }

  // Standalone mod: eski /analyze response
  if (engineMode === "standalone") {
    return (
      <div className="p-4 space-y-4 text-sm">
        <h2 className="text-lg font-semibold">Etik Analiz (Standalone)</h2>

        <div className="bg-neutral-900 p-3 rounded-lg">
          <p>
            <b>EZA Skoru:</b>{" "}
            {analysis.eza_score?.eza_score ?? analysis.eza_score ?? "—"}
          </p>
        </div>

        {analysis.intent && (
          <div className="bg-neutral-900 p-3 rounded-lg">
            <p>
              <b>Niyet seviyesi:</b> {analysis.intent.level ?? "—"}
            </p>
            <p>
              <b>Özet:</b> {analysis.intent.summary ?? "—"}
            </p>
          </div>
        )}

        {analysis.critical_bias && (
          <div className="bg-neutral-900 p-3 rounded-lg">
            <p>
              <b>Bias seviyesi:</b> {analysis.critical_bias.level ?? "—"}
            </p>
            <p>
              <b>Bias skor:</b> {analysis.critical_bias.bias_score ?? "—"}
            </p>
          </div>
        )}

        {analysis.abuse && (
          <div className="bg-neutral-900 p-3 rounded-lg">
            <p>
              <b>Abuse seviyesi:</b> {analysis.abuse.level ?? "—"}
            </p>
          </div>
        )}

        {analysis.moral_compass && (
          <div className="bg-neutral-900 p-3 rounded-lg">
            <p>
              <b>Moral Compass:</b> {analysis.moral_compass.level ?? "—"}
            </p>
          </div>
        )}

        {analysis.memory_consistency && (
          <div className="bg-neutral-900 p-3 rounded-lg">
            <p>
              <b>Memory Consistency:</b>{" "}
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
    <div className="p-4 space-y-4 text-sm">
      <h2 className="text-lg font-semibold">
        Etik Analiz (Proxy Mode — {depthMode.toUpperCase()})
      </h2>

      {/* Input analizi */}
      {input && (
        <div className="bg-neutral-900 p-3 rounded-lg space-y-1">
          <p className="font-semibold text-neutral-200">Input Analizi</p>
          <p>
            <b>EZA Skoru:</b>{" "}
            {input.eza_score?.eza_score ?? input.eza_score ?? "—"}
          </p>
          {input.intent && (
            <p>
              <b>Niyet:</b> {input.intent.level ?? "—"}
            </p>
          )}
          {input.abuse && (
            <p>
              <b>Abuse:</b> {input.abuse.level ?? "—"}
            </p>
          )}
          {input.critical_bias && (
            <p>
              <b>Bias:</b> {input.critical_bias.level ?? "—"}
            </p>
          )}
        </div>
      )}

      {/* Output analizi (sadece deep ise dolu olabilir) */}
      {output ? (
        <div className="bg-neutral-900 p-3 rounded-lg space-y-1">
          <p className="font-semibold text-neutral-200">Output Analizi</p>
          <p>
            <b>EZA Skoru:</b>{" "}
            {output.eza_score?.eza_score ?? output.eza_score ?? "—"}
          </p>
          {output.intent && (
            <p>
              <b>Niyet:</b> {output.intent.level ?? "—"}
            </p>
          )}
          {output.abuse && (
            <p>
              <b>Abuse:</b> {output.abuse.level ?? "—"}
            </p>
          )}
          {output.critical_bias && (
            <p>
              <b>Bias:</b> {output.critical_bias.level ?? "—"}
            </p>
          )}
        </div>
      ) : (
        <div className="bg-neutral-900 p-3 rounded-lg text-neutral-400">
          {depthMode === "fast"
            ? "Fast Mode: Çıkış analizi minimal veya atlanmış olabilir."
            : "Output analizi mevcut değil."}
        </div>
      )}

      <div className="bg-neutral-900 p-3 rounded-lg text-xs text-neutral-400">
        <p>
          Not: Proxy Mode'da EZA hem kullanıcı input'unu hem de seçilen LLM'in
          cevabını analiz eder. Deep Mode'da çift taraflı analiz tam kapsamlı
          çalışır.
        </p>
      </div>
    </div>
  );
}
