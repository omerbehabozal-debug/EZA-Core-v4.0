import { create } from "zustand";

interface Msg {
  role: "user" | "assistant";
  text: string;
}

interface Analysis {
  eza_score?: number;
  intent?: any;
  critical_bias?: any;
  abuse?: any;
  moral?: any;
  memory_consistency?: any;
}

interface ChatState {
  messages: Msg[];
  analysis: Analysis | null;
  addMessage: (m: Msg) => void;
  setAnalysis: (a: Analysis | null) => void;
  reset: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  analysis: null,
  addMessage: (m) => set((s) => ({ messages: [...s.messages, m] })),
  setAnalysis: (a) => set(() => ({ analysis: a })),
  reset: () => set({ messages: [], analysis: null })
}));

