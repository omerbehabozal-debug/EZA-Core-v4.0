"use client";

import { useState } from "react";
import { useChatStore, EngineMode, ProxySubMode } from "@/stores/chatStore";

export default function ModeSelector() {
  const engineMode = useChatStore((s) => s.engineMode);
  const proxySubMode = useChatStore((s) => s.proxySubMode);
  const setEngineMode = useChatStore((s) => s.setEngineMode);
  const setProxySubMode = useChatStore((s) => s.setProxySubMode);
  const reset = useChatStore((s) => s.reset);
  
  const [showProxySubModes, setShowProxySubModes] = useState(false);

  const handleMainModeClick = (mode: EngineMode) => {
    if (mode === "proxy") {
      setShowProxySubModes(!showProxySubModes);
      setEngineMode("proxy");
    } else {
      setShowProxySubModes(false);
      setEngineMode(mode);
    }
    reset();
  };

  const handleProxySubModeClick = (subMode: ProxySubMode) => {
    setEngineMode(subMode);
    setProxySubMode(subMode);
    setShowProxySubModes(false);
    reset();
  };

  return (
    <div className="relative">
      {/* Main Mode Buttons */}
      <div className="flex items-center gap-1 glass rounded-full p-1">
        <button
          onClick={() => handleMainModeClick("standalone")}
          className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200 ${
            engineMode === "standalone"
              ? "bg-accent text-bg shadow-accent-glow"
              : "text-text-dim hover:text-text hover:bg-panel/30"
          }`}
        >
          Standalone
        </button>
        <button
          onClick={() => handleMainModeClick("proxy")}
          className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200 ${
            engineMode.startsWith("proxy")
              ? "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30"
              : "text-text-dim hover:text-text hover:bg-panel/30"
          }`}
        >
          Proxy
        </button>
      </div>

      {/* Proxy Sub-Mode Buttons (Dropdown) */}
      {showProxySubModes && (
        <div className="absolute top-full right-0 mt-2 glass rounded-lg p-2 shadow-lg z-50 min-w-[200px]">
          <div className="flex flex-col gap-1">
            <button
              onClick={() => handleProxySubModeClick("proxy")}
              className={`px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200 text-left ${
                proxySubMode === "proxy"
                  ? "bg-accent text-bg"
                  : "text-text-dim hover:text-text hover:bg-panel/30"
              }`}
            >
              Normal
            </button>
            <button
              onClick={() => handleProxySubModeClick("proxy_fast")}
              className={`px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200 text-left ${
                proxySubMode === "proxy_fast"
                  ? "bg-green-500/20 text-green-400 border border-green-500/30"
                  : "text-text-dim hover:text-text hover:bg-panel/30"
              }`}
            >
              Fast
            </button>
            <button
              onClick={() => handleProxySubModeClick("proxy_deep")}
              className={`px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200 text-left ${
                proxySubMode === "proxy_deep"
                  ? "bg-blue-500/20 text-blue-400 border border-blue-500/30"
                  : "text-text-dim hover:text-text hover:bg-panel/30"
              }`}
            >
              Deep
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

