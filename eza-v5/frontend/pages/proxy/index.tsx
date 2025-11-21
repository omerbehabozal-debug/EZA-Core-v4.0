/**
 * Proxy Lab Page - EZA AR-GE Panel
 */

import { useState } from 'react';
import AuthGuard from '@/components/AuthGuard';
import ProxyLayout from '@/components/proxy/ProxyLayout';
import RequestPanel from '@/components/proxy/RequestPanel';
import OutputCompare from '@/components/proxy/OutputCompare';
import RiskSummary from '@/components/proxy/RiskSummary';
import ScoreCards from '@/components/proxy/ScoreCards';
import RiskHeatmap from '@/components/proxy/RiskHeatmap';
import AlignmentGraph from '@/components/proxy/AlignmentGraph';
import EngineTabs from '@/components/proxy/EngineTabs';
import { evaluateProxy } from '@/api/proxy';

export default function ProxyPage() {
  const [mode, setMode] = useState<'fast' | 'deep'>('fast');
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (message: string, model: string, depth: 'fast' | 'deep') => {
    setIsLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await evaluateProxy(message, model, depth);

      if (res.ok === false) {
        setError(res.error?.message || res.error?.detail || 'Bir hata oluştu');
      } else {
        setResponse(res);
      }
    } catch (err: any) {
      setError(err.message || 'Teknik bir sorun oluştu, lütfen tekrar deneyin.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthGuard allowedRoles={['eza_internal', 'admin']}>
      <ProxyLayout mode={mode} onModeChange={setMode}>
        {/* Request Panel */}
        <RequestPanel onSubmit={handleSubmit} isLoading={isLoading} mode={mode} />

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Results */}
        {response && (
          <div className="space-y-6">
            {/* Output Compare - Full Width */}
            <OutputCompare
              rawOutput={response.raw_output}
              safeOutput={response.safe_output}
            />

            {/* Two Column Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left Column */}
              <div className="space-y-6">
                <RiskSummary
                  inputAnalysis={response.analysis?.input}
                  outputAnalysis={response.analysis?.output}
                  alignment={response.analysis?.alignment}
                  scoreBreakdown={response.analysis?.eza_score}
                />
                <ScoreCards
                  scoreBreakdown={response.analysis?.eza_score}
                  alignment={response.analysis?.alignment}
                  deception={response.analysis?.deception}
                  psychPressure={response.analysis?.psychological_pressure}
                />
              </div>

              {/* Right Column */}
              <div className="space-y-6">
                <RiskHeatmap
                  inputAnalysis={response.analysis?.input}
                  outputAnalysis={response.analysis?.output}
                  deception={response.analysis?.deception}
                  psychPressure={response.analysis?.psychological_pressure}
                  legalRisk={response.analysis?.legal_risk}
                />
                <AlignmentGraph
                  alignment={response.analysis?.alignment}
                  scoreBreakdown={response.analysis?.eza_score}
                  deception={response.analysis?.deception}
                />
              </div>
            </div>

            {/* Engine Tabs - Full Width */}
            {mode === 'deep' && (
              <EngineTabs
                deception={response.analysis?.deception}
                psychPressure={response.analysis?.psychological_pressure}
                legalRisk={response.analysis?.legal_risk}
                rawResponse={response}
              />
            )}
          </div>
        )}
      </ProxyLayout>
    </AuthGuard>
  );
}
