/**
 * Proxy-Lite API Client
 */

import { apiRequest } from "./api_client";
import { API_BASE_URL } from "./config";

export interface ProxyLiteAnalyzeRequest {
  message: string;
  output_text: string;
}

export interface ProxyLiteAnalyzeResponse {
  risk_level: string;
  risk_category: string;
  violated_rule_count: number;
  summary: string;
  recommendation: string;
}

export interface ProxyLiteRealResult {
  live: boolean;
  risk_score: number;
  risk_level: string;
  output: string;
  flags: string[];
  raw?: any;
}

export function analyzeProxyLite(
  message: string,
  outputText: string
): Promise<ProxyLiteAnalyzeResponse> {
  return apiRequest<ProxyLiteAnalyzeResponse>(
    "/api/proxy-lite/report",
    "POST",
    {
      message,
      output_text: outputText,
    }
  );
}

/**
 * Analyze Lite - SWR compatible fetcher function
 * Used for hybrid mock + live backend mode
 */
export async function analyzeLite(
  message: string,
  outputText: string
): Promise<ProxyLiteAnalyzeResponse> {
  return analyzeProxyLite(message, outputText);
}

/**
 * Real Backend Integration - EZA Gateway test-call endpoint
 * Returns null on error (for fallback to mock)
 */
export async function analyzeLiteReal(text: string): Promise<ProxyLiteRealResult | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/gateway/test-call`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, provider: "openai" }),
    });

    if (!res.ok) throw new Error("Backend error");

    const data = await res.json();

    return {
      live: true,
      risk_score: data.analysis?.risk_score ?? 50,
      risk_level: data.analysis?.risk_level ?? "medium",
      output: data.gateway?.output ?? data.analysis?.output?.summary ?? "",
      flags: data.analysis?.risk_flags ?? [],
      raw: data,
    };
  } catch (e) {
    console.info("Proxy-Lite: Backend offline, using fallback.");
    return null; // fallback için sinyal
  }
}

