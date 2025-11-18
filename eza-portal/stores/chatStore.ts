import { create } from "zustand";

export type Role = "user" | "assistant";

export interface MessageAnalysis {
  eza_score?: number;
  risk_level?: string;
  intent?: string;
  intent_score?: number;
  bias?: string;
  safety?: string;
  rationale?: string;
  flags?: string[];
}

export interface Msg {
  id: string;
  role: Role;
  text: string;
  timestamp: number;
  analysis?: MessageAnalysis;
}

export type EngineMode = "standalone" | "proxy" | "fast" | "deep" | "openai";
export type DepthMode = "fast" | "deep";

export type Provider = "openai" | "anthropic" | "mistral" | "llama";

interface ChatState {
  messages: Msg[];
  analysis: any | null;
  selectedMessageIndex: number | null;
  selectedMessageId: string | null;
  engineMode: EngineMode;
  depthMode: DepthMode;
  provider: Provider;
  audit: Array<{
    timestamp: string;
    message_id: string;
    analysis_snapshot: any;
  }>;
  auditLog: MessageAnalysis[];
  addMessage: (m: Msg) => void;
  updateMessage: (id: string, updates: Partial<Msg>) => void;
  setAnalysis: (a: any | null) => void;
  setSelectedMessageIndex: (idx: number | null) => void;
  setSelectedMessageId: (id: string | null) => void;
  setEngineMode: (m: EngineMode) => void;
  setDepthMode: (m: DepthMode) => void;
  setProvider: (p: Provider) => void;
  addAuditEntry: (entry: { timestamp: string; message_id: string; analysis_snapshot: any }) => void;
  addAuditLogEntry: (analysis: MessageAnalysis) => void;
  reset: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  analysis: null,
  selectedMessageIndex: null,
  selectedMessageId: null,
  engineMode: "standalone",
  depthMode: "fast",
  provider: "openai",
  audit: [],
  auditLog: [],
  addMessage: (m) =>
    set((s) => ({
      messages: [...s.messages, m]
    })),
  updateMessage: (id, updates) =>
    set((s) => ({
      messages: s.messages.map((msg) =>
        msg.id === id ? { ...msg, ...updates } : msg
      )
    })),
  setAnalysis: (a) => set(() => ({ analysis: a })),
  setSelectedMessageIndex: (idx) => set(() => ({ selectedMessageIndex: idx })),
  setSelectedMessageId: (id) => set(() => ({ selectedMessageId: id })),
  setEngineMode: (m) => set(() => ({ engineMode: m })),
  setDepthMode: (m) => set(() => ({ depthMode: m })),
  setProvider: (p) => set(() => ({ provider: p })),
  addAuditEntry: (entry) =>
    set((s) => ({
      audit: [...s.audit, entry]
    })),
  addAuditLogEntry: (analysis) =>
    set((s) => ({
      auditLog: [...s.auditLog, analysis]
    })),
  reset: () =>
    set({
      messages: [],
      analysis: null,
      selectedMessageIndex: null,
      selectedMessageId: null,
      engineMode: "standalone",
      depthMode: "fast",
      provider: "openai",
      audit: [],
      auditLog: []
    })
}));
