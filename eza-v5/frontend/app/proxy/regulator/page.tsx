/**
 * Regulator Portal Page
 */

'use client';

import { useState } from 'react';
import Layout from '@/components/Layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/Card';
import CaseTable from './components/CaseTable';
import RiskMatrix from './components/RiskMatrix';
import ScreeningPanel from './components/ScreeningPanel';
import { CaseItem } from '@/lib/types';

const tabs = [
  { id: 'risk', label: 'Risk Sınıflandırma' },
  { id: 'review', label: 'İçerik İnceleme Masası' },
  { id: 'reports', label: 'Uygunluk Raporları' },
  { id: 'audit', label: 'Audit Log' },
];

// Mock data
const mockCases: CaseItem[] = [
  {
    id: '1',
    content_id: 'CONT-001',
    risk_score: 0.85,
    eu_ai_class: 'High Risk',
    status: 'pending',
    created_at: new Date().toISOString(),
  },
  {
    id: '2',
    content_id: 'CONT-002',
    risk_score: 0.45,
    eu_ai_class: 'Limited Risk',
    status: 'reviewed',
    created_at: new Date().toISOString(),
  },
];

const mockRiskData = [
  { x: 0, y: 0, value: 0.9, label: 'High Risk Content' },
  { x: 0, y: 1, value: 0.7, label: 'Medium-High Risk' },
  { x: 1, y: 0, value: 0.5, label: 'Medium Risk' },
  { x: 2, y: 2, value: 0.2, label: 'Low Risk' },
];

export default function RegulatorPage() {
  const [activeTab, setActiveTab] = useState('risk');
  const [selectedCase, setSelectedCase] = useState<CaseItem | null>(null);

  const handleReview = (caseId: string) => {
    const caseItem = mockCases.find(c => c.id === caseId);
    setSelectedCase(caseItem || null);
  };

  const handleClose = () => setSelectedCase(null);

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-semibold text-gray-900 mb-2">
            Regulator Compliance Panel
          </h1>
          <p className="text-gray-600">
            EU AI Act, RTÜK, BTK uyumluluk değerlendirmesi
          </p>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200">
          <nav className="flex gap-6">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        {activeTab === 'risk' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <RiskMatrix data={mockRiskData} />
            <Card>
              <CardHeader>
                <CardTitle>Risk İstatistikleri</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Toplam İçerik</span>
                    <span className="font-semibold">1,234</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Yüksek Risk</span>
                    <span className="font-semibold text-red-600">45</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Orta Risk</span>
                    <span className="font-semibold text-yellow-600">123</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === 'review' && (
          <Card>
            <CardHeader>
              <CardTitle>İçerik İnceleme Masası</CardTitle>
            </CardHeader>
            <CardContent>
              <CaseTable cases={mockCases} onReview={handleReview} />
            </CardContent>
          </Card>
        )}

        {activeTab === 'reports' && (
          <Card>
            <CardHeader>
              <CardTitle>Uygunluk Raporları</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">Raporlar burada görüntülenecek</p>
            </CardContent>
          </Card>
        )}

        {activeTab === 'audit' && (
          <Card>
            <CardHeader>
              <CardTitle>Audit Log</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">Audit log kayıtları burada görüntülenecek</p>
            </CardContent>
          </Card>
        )}

        {/* Screening Panel */}
        <ScreeningPanel
          caseItem={selectedCase}
          onClose={handleClose}
          onApprove={(id) => {
            console.log('Approve:', id);
            handleClose();
          }}
          onWarning={(id) => {
            console.log('Warning:', id);
            handleClose();
          }}
          onRemove={(id) => {
            console.log('Remove:', id);
            handleClose();
          }}
          onReport={(id) => {
            console.log('Report:', id);
            handleClose();
          }}
        />
      </div>
    </Layout>
  );
}

