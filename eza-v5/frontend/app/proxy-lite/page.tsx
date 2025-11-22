/**
 * Proxy-Lite Page - Hybrid Mock + Real Backend System
 */

"use client";

import { useState } from "react";
import useSWR from "swr";
import { analyzeLiteReal, ProxyLiteRealResult } from "@/api/proxy_lite";
import { MOCK_LITE_RESULT } from "@/mock/proxy_lite";
import StatusBadge from "@/components/StatusBadge";

export default function ProxyLitePage() {
  const [text, setText] = useState("");
  const [analyzeKey, setAnalyzeKey] = useState<string | null>(null);

  const { data, isValidating, mutate } = useSWR<ProxyLiteRealResult>(
    analyzeKey ? ["proxy-lite", analyzeKey] : null,
    async () => {
      const realResult = await analyzeLiteReal(analyzeKey!);
      return realResult ?? MOCK_LITE_RESULT;
    },
    {
      fallbackData: MOCK_LITE_RESULT,
      revalidateOnFocus: false,
      shouldRetryOnError: false,
    }
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      // Önce mock göster, sonra gerçek API isteğini tetikle
      setAnalyzeKey(text.trim());
      mutate(); // gerçek API isteğini tetikle
    }
  };

  const result = data ?? MOCK_LITE_RESULT;

  return (
    <div className="px-4 md:px-10 py-10 max-w-4xl mx-auto">
      <h1 className="text-center text-3xl font-bold">EZA Proxy-Lite</h1>
      <p className="text-center text-gray-500 mb-8">Hızlı ve temel etik kontrol.</p>

      <form onSubmit={handleSubmit}>
        <textarea 
          className="w-full border rounded-lg p-4"
          placeholder="Analiz etmek istediğiniz içeriği yazın..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button 
          type="submit"
          className="mt-4 w-full bg-blue-600 text-white font-semibold rounded-lg p-3"
          disabled={!text.trim() || isValidating}
        >
          {isValidating ? "Analiz Ediliyor..." : "Analiz Et"}
        </button>
      </form>

      {/* Status - Only show when analysis is triggered */}
      {analyzeKey && (
        <div className="mt-6">
          <StatusBadge
            loading={isValidating}
            live={data?.live}
          />
        </div>
      )}

      {/* Result - Only show when analysis is triggered */}
      {analyzeKey && (
        <div className="mt-6 bg-white shadow p-6 rounded-xl">
          <h2 className="font-semibold mb-4 text-lg">Analiz Sonucu</h2>

          <p className="text-4xl font-bold">{result.risk_score}</p>
          <p className="text-gray-600 capitalize">{result.risk_level} risk</p>

          <p className="mt-4 text-gray-700">{result.output}</p>

          {result.flags && result.flags.length > 0 && (
            <div className="mt-4">
              <h3 className="font-semibold text-sm mb-2">Risk Flags:</h3>
              <ul className="list-disc list-inside text-sm text-gray-600">
                {result.flags.map((flag, idx) => (
                  <li key={idx}>{flag}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

