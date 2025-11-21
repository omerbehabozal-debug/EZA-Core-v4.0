/**
 * Proxy-Lite Page - Audit Panel
 */

import { useState } from 'react';
import AuthGuard from '@/components/AuthGuard';
import ProxyLiteLayout from '@/components/proxy-lite/ProxyLiteLayout';
import QuickCheckForm from '@/components/proxy-lite/QuickCheckForm';
import RiskResultCard from '@/components/proxy-lite/RiskResultCard';
import RecommendationCard from '@/components/proxy-lite/RecommendationCard';
import RiskDistributionChart from '@/components/proxy-lite/RiskDistributionChart';
import apiClient from '@/lib/api';

export default function ProxyLitePage() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (message: string, outputText: string) => {
    console.log('Proxy-Lite: handleSubmit called', { message, outputText });
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      console.log('Proxy-Lite: Making API call to /api/proxy-lite/report');
      const res = await apiClient.post('/api/proxy-lite/report', {
        message,
        output_text: outputText,
      });

      console.log('Proxy-Lite: API response received', res.data);
      setResult(res.data);
    } catch (err: any) {
      console.error('Proxy-Lite: API error', err);
      console.error('Proxy-Lite: Error response', err.response);
      console.error('Proxy-Lite: Error data', err.response?.data);
      
      let errorMessage = 'Teknik bir sorun oluştu, lütfen tekrar deneyin.';
      
      if (err.response) {
        // Server responded with error
        errorMessage = err.response.data?.detail || 
                      err.response.data?.message || 
                      `Sunucu hatası: ${err.response.status} ${err.response.statusText}`;
      } else if (err.request) {
        // Request made but no response
        errorMessage = 'Sunucuya bağlanılamadı. Backend çalışıyor mu kontrol edin.';
      } else {
        // Error in request setup
        errorMessage = err.message || 'İstek hazırlanırken hata oluştu.';
      }
      
      console.error('Proxy-Lite: Final error message', errorMessage);
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthGuard allowedRoles={['institution_auditor', 'admin']}>
      <ProxyLiteLayout>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column - Form */}
          <div>
            <QuickCheckForm onSubmit={handleSubmit} isLoading={isLoading} />
          </div>

          {/* Right Column - Results */}
          <div className="space-y-6">
            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-4">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            {/* Risk Result */}
            {result && (
              <>
                <RiskResultCard
                  riskLevel={result.risk_level}
                  riskCategory={result.risk_category}
                  violatedRuleCount={result.violated_rule_count}
                  summary={result.summary}
                />

                <RecommendationCard recommendation={result.recommendation} />
              </>
            )}

            {/* Risk Distribution Chart */}
            <RiskDistributionChart />
          </div>
        </div>
      </ProxyLiteLayout>
    </AuthGuard>
  );
}
