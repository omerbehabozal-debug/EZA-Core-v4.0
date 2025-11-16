"use client";

import { useChatStore } from "@/stores/chatStore";

const engineLabels = {
  standalone: "EZA Standalone",
  proxy: "EZA Proxy (LLM)"
};

export default function TopBar() {
  const {
    engineMode,
    depthMode,
    provider,
    setEngineMode,
    setDepthMode,
    setProvider,
    reset
  } = useChatStore();

  return (
    <div className="flex items-center justify-between px-4 py-3 border-b border-neutral-800 bg-neutral-950">
      <div className="flex items-center gap-3 text-sm">
        <span className="font-semibold text-neutral-100">EZA Portal</span>
        <span className="text-xs text-neutral-500">
          {engineLabels[engineMode]}
        </span>
      </div>

      <div className="flex items-center gap-3 text-xs">
        {/* Engine mode */}
        <div className="flex items-center gap-1 bg-neutral-900 px-2 py-1 rounded-lg">
          <button
            onClick={() => {
              setEngineMode("standalone");
              reset();
            }}
            className={`px-2 py-1 rounded-md ${
              engineMode === "standalone"
                ? "bg-blue-600 text-white"
                : "text-neutral-300"
            }`}
          >
            Standalone
          </button>
          <button
            onClick={() => {
              setEngineMode("proxy");
              reset();
            }}
            className={`px-2 py-1 rounded-md ${
              engineMode === "proxy"
                ? "bg-emerald-600 text-white"
                : "text-neutral-300"
            }`}
          >
            Proxy
          </button>
        </div>

        {/* Depth mode */}
        <div className="flex items-center gap-1 bg-neutral-900 px-2 py-1 rounded-lg">
          <span className="text-neutral-400 mr-1">Mode</span>
          <button
            onClick={() => setDepthMode("fast")}
            className={`px-2 py-1 rounded-md ${
              depthMode === "fast"
                ? "bg-neutral-700 text-white"
                : "text-neutral-300"
            }`}
          >
            Fast
          </button>
          <button
            onClick={() => setDepthMode("deep")}
            className={`px-2 py-1 rounded-md ${
              depthMode === "deep"
                ? "bg-neutral-700 text-white"
                : "text-neutral-300"
            }`}
          >
            Deep
          </button>
        </div>

        {/* Provider select */}
        <div className="flex items-center gap-1 bg-neutral-900 px-2 py-1 rounded-lg">
          <span className="text-neutral-400 mr-1">LLM</span>
          <select
            value={provider}
            onChange={(e) => setProvider(e.target.value as any)}
            className="bg-neutral-900 text-neutral-100 text-xs outline-none"
          >
            <option value="openai">OpenAI</option>
            <option value="anthropic">Anthropic</option>
            <option value="mistral">Mistral</option>
            <option value="llama">Llama</option>
          </select>
        </div>
      </div>
    </div>
  );
}

