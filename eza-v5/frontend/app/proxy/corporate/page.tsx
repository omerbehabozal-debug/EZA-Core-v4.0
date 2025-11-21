/**
 * Corporate Portal Page
 */

'use client';

import { useState } from 'react';
import Layout from '@/components/Layout';
import AiAuditList from './components/AiAuditList';
import PolicyConfig from './components/PolicyConfig';
import WorkflowBuilder from './components/WorkflowBuilder';
import { PolicyConfig as PolicyConfigType } from '@/lib/types';

// Mock data
const mockAuditItems = [
  {
    id: '1',
    ai_agent: 'Customer Support Bot',
    risk_score: 0.35,
    flags: ['sensitive_data'],
    reviewer: 'John Doe',
    status: 'approved' as const,
    timestamp: new Date().toISOString(),
  },
  {
    id: '2',
    ai_agent: 'Sales Assistant',
    risk_score: 0.75,
    flags: ['high_risk', 'needs_review'],
    reviewer: 'Jane Smith',
    status: 'flagged' as const,
    timestamp: new Date().toISOString(),
  },
];

const mockPolicyConfig: PolicyConfigType = {
  high_risk_topics: ['Financial advice', 'Medical diagnosis'],
  illegal_use_cases: ['Discrimination', 'Fraud'],
  custom_rules: [],
};

export default function CorporatePage() {
  const [policyConfig, setPolicyConfig] = useState(mockPolicyConfig);

  const handleSavePolicy = (config: PolicyConfigType) => {
    setPolicyConfig(config);
    console.log('Policy saved:', config);
  };

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-semibold text-gray-900 mb-2">
            Corporate Portal
          </h1>
          <p className="text-gray-600">
            Şirket içi AI denetimi ve güvenlik
          </p>
        </div>

        <AiAuditList items={mockAuditItems} />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <PolicyConfig config={policyConfig} onSave={handleSavePolicy} />
          <WorkflowBuilder />
        </div>
      </div>
    </Layout>
  );
}

