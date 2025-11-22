/**
 * Corporate API Client
 */

import { apiRequest } from './api_client';
import { MOCK_CORPORATE_AUDIT, MOCK_CORPORATE_POLICY } from '@/mock/corporate';
import type { CorporateAudit, PolicyConfig } from '@/lib/types';

export interface CorporateAuditApiResponse {
  id: number;
  endpoint: string;
  method: string;
  risk_score: number | null;
  eza_score: number | null;
  action_taken: string | null;
  created_at: string;
}

export interface CorporatePolicyApiResponse {
  id: number;
  tenant: string;
  rules: Record<string, any>;
  policy_type: string;
  is_active: string;
  created_at: string;
  updated_at: string;
}

export interface PolicyUpdateRequest {
  rules: Record<string, any>;
  policy_type?: string;
}

const fetcher = async <T>(url: string, fallback: T, method: string = 'GET', body?: any): Promise<T> => {
  try {
    const response = await apiRequest<T>(url, method, body);
    return response;
  } catch (error) {
    console.info(`[Preview Mode] Backend unavailable for ${url}, using fallback data`);
    return fallback;
  }
};

export async function fetchCorporateAudit(limit: number = 100, offset: number = 0): Promise<CorporateAudit[]> {
  const url = `/api/corporate/audit?limit=${limit}&offset=${offset}`;
  const response = await fetcher<CorporateAuditApiResponse[]>(url, MOCK_CORPORATE_AUDIT);
  return response.map(audit => ({
    id: audit.id.toString(),
    ai_agent: audit.endpoint,
    risk_score: audit.risk_score || 0,
    flags: audit.action_taken ? [audit.action_taken] : [],
    reviewer: 'System',
    status: audit.action_taken === 'blocked' ? 'flagged' : 'approved' as const,
    timestamp: audit.created_at,
  }));
}

export async function fetchCorporatePolicy(tenant: string): Promise<PolicyConfig> {
  const url = `/api/corporate/policy?tenant=${tenant}`;
  const response = await fetcher<CorporatePolicyApiResponse>(url, MOCK_CORPORATE_POLICY);
  return {
    high_risk_topics: response.rules.high_risk_topics || [],
    illegal_use_cases: response.rules.illegal_use_cases || [],
    custom_rules: response.rules.custom_rules || [],
  };
}

export async function updateCorporatePolicy(
  tenant: string,
  rules: Record<string, any>,
  policy_type: string = 'default'
): Promise<PolicyConfig> {
  const url = `/api/corporate/policy?tenant=${tenant}`;
  const requestBody: PolicyUpdateRequest = { rules, policy_type };
  const response = await fetcher<CorporatePolicyApiResponse>(url, MOCK_CORPORATE_POLICY, 'POST', requestBody);
  return {
    high_risk_topics: response.rules.high_risk_topics || [],
    illegal_use_cases: response.rules.illegal_use_cases || [],
    custom_rules: response.rules.custom_rules || [],
  };
}
