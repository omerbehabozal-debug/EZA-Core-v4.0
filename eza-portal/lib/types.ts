export interface Message {
  role: "user" | "assistant";
  text: string;
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

