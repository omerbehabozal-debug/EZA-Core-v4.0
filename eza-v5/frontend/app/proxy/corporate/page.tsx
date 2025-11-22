/**
 * Corporate Portal Page - Multi-Tenant
 */

'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import useSWR from 'swr';
import DashboardLayout from '@/components/Layout/DashboardLayout';
import AiAuditList from './components/AiAuditList';
import PolicyConfig from './components/PolicyConfig';
import WorkflowBuilder from './components/WorkflowBuilder';
import StatusBadge, { StatusType } from '@/components/StatusBadge';
import { useTenantStore } from '@/lib/tenantStore';
import { fetchCorporateAudit, fetchCorporatePolicy, updateCorporatePolicy } from '@/api/corporate';
import { MOCK_CORPORATE_AUDIT, MOCK_CORPORATE_POLICY } from '@/mock/corporate';
import type { PolicyConfig as PolicyConfigType, CorporateAudit } from '@/lib/types';

function getStatusType(isLoading: boolean, error: any, data: any, fallback: any): StatusType {
  if (isLoading) return 'loading';
  if (error || !data || data === fallback) return 'preview';
  return 'live';
}

export default function CorporatePage() {
  const searchParams = useSearchParams();
  const { setTenant, getTenant } = useTenantStore();
  const tenant = getTenant();

  useEffect(() => {
    const tenantParam = searchParams.get('tenant');
    if (tenantParam && tenantParam !== tenant.id) {
      setTenant(tenantParam);
    }
  }, [searchParams, tenant.id, setTenant]);

  const { data: auditItems, error: auditError, isLoading: auditLoading } = useSWR(
    ['corporate-audit', tenant.id],
    () => fetchCorporateAudit(100, 0),
    {
      fallbackData: MOCK_CORPORATE_AUDIT,
      revalidateOnMount: true,
      shouldRetryOnError: false,
      errorRetryCount: 0,
      onError: () => {
        console.info('[Preview Mode] Backend unavailable for corporate audit');
      },
    }
  );

  const { data: policyConfig, error: policyError, isLoading: policyLoading, mutate: mutatePolicy } = useSWR(
    ['corporate-policy', tenant.id],
    () => fetchCorporatePolicy(tenant.id),
    {
      fallbackData: MOCK_CORPORATE_POLICY,
      revalidateOnMount: true,
      shouldRetryOnError: false,
      errorRetryCount: 0,
      onError: () => {
        console.info('[Preview Mode] Backend unavailable for corporate policy');
      },
    }
  );

  const auditStatus = getStatusType(auditLoading, auditError, auditItems, MOCK_CORPORATE_AUDIT);
  const policyStatus = getStatusType(policyLoading, policyError, policyConfig, MOCK_CORPORATE_POLICY);

  const handleSavePolicy = async (config: PolicyConfigType) => {
    try {
      await updateCorporatePolicy(tenant.id, config);
      mutatePolicy(config, false);
    } catch (error) {
      console.info('[Preview Mode] Policy save failed, using local state');
      mutatePolicy(config, false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-semibold text-gray-900 mb-2">
              Kurumsal AI Uyum Paneli
            </h1>
            <p className="text-gray-600">
              {tenant.description}
            </p>
          </div>
          <StatusBadge status={auditStatus} />
        </div>

        <div>
          <div className="flex justify-end mb-2">
            <StatusBadge status={auditStatus} />
          </div>
          <AiAuditList items={auditItems || MOCK_CORPORATE_AUDIT} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <div className="flex justify-end mb-2">
              <StatusBadge status={policyStatus} />
            </div>
            <PolicyConfig 
              config={policyConfig || MOCK_CORPORATE_POLICY} 
              onSave={handleSavePolicy} 
            />
          </div>
          <WorkflowBuilder />
        </div>
      </div>
    </DashboardLayout>
  );
}
