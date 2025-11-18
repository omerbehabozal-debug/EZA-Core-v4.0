import { MessageAnalysis } from "@/stores/chatStore";

export interface Message {
  id: string;
  role: "user" | "assistant";
  text: string;
  timestamp: number;
  analysis?: MessageAnalysis;
}

export interface Analysis {
  eza_score?: number;
  intent?: {
    level?: string;
    summary?: string;
  };
  critical_bias?: {
    level?: string;
  };
  abuse?: {
    level?: string;
  };
  moral?: {
    level?: string;
  };
  memory_consistency?: {
    level?: string;
  };
  cleaned_output?: string;
  output?: string;
}

