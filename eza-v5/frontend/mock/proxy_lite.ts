/**
 * Mock Proxy-Lite Data
 */

import { ProxyLiteRealResult } from '@/api/proxy_lite';

export const MOCK_LITE_RESULT: ProxyLiteRealResult = {
  live: false,
  risk_score: 85,
  risk_level: "low",
  output: "Content appears safe. Standard monitoring recommended.",
  flags: [],
};

