"use client";

import { useChatStore } from "@/stores/chatStore";
import { theme } from "@/theme/eza-theme";

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
    <div
      className="w-full flex flex-col md:flex-row items-start md:items-center justify-between px-4 md:px-6 py-3 border-b gap-3 md:gap-0"
      style={{
        background: theme.glass.background,
        backdropFilter: theme.glass.blur,
        borderColor: theme.colors.border
      }}
    >
      <div className="flex items-center gap-2 md:gap-3">
        <span className="text-base md:text-lg font-semibold tracking-wide">EZA Portal</span>
        <span className="hidden sm:inline text-xs text-neutral-400">
          {engineMode === "standalone" ? "Standalone Engine" : "Proxy Engine"}
        </span>
      </div>

      <div className="flex items-center gap-2 md:gap-4 flex-wrap">
        {/* Mode Selection */}
        <div className="flex items-center gap-1">
          <button
            onClick={() => {
              setEngineMode("standalone");
              reset();
            }}
            className={`px-2 md:px-3 py-1 rounded-lg text-xs transition ${
              engineMode === "standalone"
                ? "bg-blue-600 shadow-md"
                : "bg-neutral-900 text-neutral-300"
            }`}
          >
            Standalone
          </button>

          <button
            onClick={() => {
              setEngineMode("proxy");
              reset();
            }}
            className={`px-2 md:px-3 py-1 rounded-lg text-xs transition ${
              engineMode === "proxy"
                ? "bg-emerald-600 shadow-md"
                : "bg-neutral-900 text-neutral-300"
            }`}
          >
            Proxy
          </button>
        </div>

        {/* Depth Mode */}
        <div className="flex items-center gap-1">
          <button
            onClick={() => setDepthMode("fast")}
            className={`px-2 md:px-3 py-1 rounded-lg text-xs ${
              depthMode === "fast"
                ? "bg-neutral-700 shadow"
                : "bg-neutral-900 text-neutral-300"
            }`}
          >
            Fast
          </button>

          <button
            onClick={() => setDepthMode("deep")}
            className={`px-2 md:px-3 py-1 rounded-lg text-xs ${
              depthMode === "deep"
                ? "bg-purple-700 shadow"
                : "bg-neutral-900 text-neutral-300"
            }`}
          >
            Deep
          </button>
        </div>

        {/* Provider */}
        <select
          value={provider}
          onChange={(e) => setProvider(e.target.value as any)}
          className="bg-neutral-900 px-2 md:px-3 py-1 rounded-lg text-xs outline-none border border-neutral-700"
        >
          <option value="openai">OpenAI</option>
          <option value="anthropic">Anthropic</option>
          <option value="mistral">Mistral</option>
          <option value="llama">Llama</option>
        </select>
      </div>
    </div>
  );
}

