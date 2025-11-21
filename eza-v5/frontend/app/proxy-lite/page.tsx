/**
 * Proxy-Lite Page
 */

'use client';

import { useState } from 'react';
import { analyzeProxyLite } from '@/api/proxy_lite';
import InputBox from './components/InputBox';
import ResultCard from './components/ResultCard';
import { ProxyLiteResult } from '@/lib/types';

export default function ProxyLitePage() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ProxyLiteResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (text: string) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      // For proxy-lite, we need both input and output
      // For now, using the same text for both (can be improved)
      const response = await analyzeProxyLite(text, text);
      
      // Calculate score from risk level
      const scoreMap = {
        low: 85,
        medium: 65,
        high: 40,
        critical: 20,
      };
      
      setResult({
        ...response,
        score: scoreMap[response.risk_level as keyof typeof scoreMap] || 50,
      });
    } catch (err: any) {
      setError(err.message || 'Analiz sırasında bir hata oluştu.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-semibold text-gray-900 mb-4">
            EZA Proxy-Lite
          </h1>
          <p className="text-lg text-gray-600">
            Hızlı ve temel etik kontrol.
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 mb-8">
          <InputBox onSubmit={handleAnalyze} isLoading={isLoading} />
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-8">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Result Section */}
        {result && <ResultCard result={result} />}
      </div>
    </div>
  );
}

