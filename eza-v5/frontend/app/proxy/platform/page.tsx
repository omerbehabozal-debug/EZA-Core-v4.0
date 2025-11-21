/**
 * Platform Portal Page
 */

'use client';

import { useState } from 'react';
import Layout from '@/components/Layout';
import ApiKeyCard from './components/ApiKeyCard';
import ContentStream from './components/ContentStream';
import TrendHeatmap from './components/TrendHeatmap';
import { ApiKey, ContentItem } from '@/lib/types';

// Mock data
const mockApiKeys: ApiKey[] = [
  {
    id: '1',
    name: 'Production Key',
    key: 'eza_live_sk_test_1234567890abcdef',
    created_at: new Date().toISOString(),
    last_used: new Date().toISOString(),
    status: 'active',
  },
];

const mockContent: ContentItem[] = [
  {
    id: '1',
    content: 'Sample content for moderation...',
    score: 75,
    risk_level: 'medium',
    timestamp: new Date().toISOString(),
  },
];

const mockTrendData = [
  { hour: 0, risk: 0.3 },
  { hour: 8, risk: 0.6 },
  { hour: 12, risk: 0.8 },
  { hour: 18, risk: 0.5 },
];

export default function PlatformPage() {
  const [apiKeys, setApiKeys] = useState(mockApiKeys);
  const [contentItems, setContentItems] = useState(mockContent);

  const handleGenerateKey = () => {
    const newKey: ApiKey = {
      id: Date.now().toString(),
      name: `Key ${apiKeys.length + 1}`,
      key: `eza_live_sk_${Math.random().toString(36).substring(7)}`,
      created_at: new Date().toISOString(),
      status: 'active',
    };
    setApiKeys([...apiKeys, newKey]);
  };

  const handleRevoke = (id: string) => {
    setApiKeys(apiKeys.map(k => k.id === id ? { ...k, status: 'revoked' as const } : k));
  };

  const handleCopy = (key: string) => {
    navigator.clipboard.writeText(key);
  };

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-semibold text-gray-900 mb-2">
            Platform Portal
          </h1>
          <p className="text-gray-600">
            İçerik platformları ve API entegrasyonları
          </p>
        </div>

        <ApiKeyCard
          apiKeys={apiKeys}
          onGenerate={handleGenerateKey}
          onRevoke={handleRevoke}
          onCopy={handleCopy}
        />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ContentStream
            items={contentItems}
            onAnalyze={(id) => console.log('Analyze:', id)}
            onLoadMore={() => console.log('Load more')}
            hasMore={true}
          />
          <TrendHeatmap data={mockTrendData} />
        </div>
      </div>
    </Layout>
  );
}

