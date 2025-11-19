"use client";

import { useState, useEffect, useRef } from "react";
import { useChatStore, EngineMode, ProxySubMode } from "@/stores/chatStore";

export default function ModeSelector() {
  const engineMode = useChatStore((s) => s.engineMode);
  const proxySubMode = useChatStore((s) => s.proxySubMode);
  const setEngineMode = useChatStore((s) => s.setEngineMode);
  const setProxySubMode = useChatStore((s) => s.setProxySubMode);
  const reset = useChatStore((s) => s.reset);
  
  const [showProxySubModes, setShowProxySubModes] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowProxySubModes(false);
      }
    };

    if (showProxySubModes) {
      // Use setTimeout to avoid immediate closure
      setTimeout(() => {
        document.addEventListener("click", handleClickOutside, true);
      }, 0);
    }

    return () => {
      document.removeEventListener("click", handleClickOutside, true);
    };
  }, [showProxySubModes]);

  const handleMainModeClick = (mode: EngineMode) => {
    if (mode === "proxy") {
      setShowProxySubModes(!showProxySubModes);
      // Don't reset when just opening dropdown
      if (!showProxySubModes) {
        setEngineMode("proxy");
      }
    } else {
      setShowProxySubModes(false);
      setEngineMode(mode);
      reset(); // Only reset when switching to standalone
    }
  };

  const handleProxySubModeClick = (e: React.MouseEvent, subMode: ProxySubMode) => {
    e.preventDefault();
    e.stopPropagation();
    setEngineMode(subMode);
    setProxySubMode(subMode);
    setShowProxySubModes(false);
    reset(); // Reset messages but keep mode (reset now preserves mode)
  };

  return (
    <div className="relative" ref={dropdownRef}>
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
          Proxy {showProxySubModes ? "▼" : "▶"}
        </button>
      </div>

      {/* Proxy Sub-Mode Buttons (Dropdown) */}
      {showProxySubModes && (
        <div 
          className="absolute top-full right-0 mt-2 glass rounded-lg p-2 shadow-lg z-[100] min-w-[200px] border border-panel-border"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex flex-col gap-1">
            <button
              type="button"
              onClick={(e) => handleProxySubModeClick(e, "proxy")}
              className={`px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200 text-left cursor-pointer ${
                engineMode === "proxy"
                  ? "bg-accent text-bg"
                  : "text-text-dim hover:text-text hover:bg-panel/30"
              }`}
            >
              Normal
            </button>
            <button
              type="button"
              onClick={(e) => handleProxySubModeClick(e, "proxy_fast")}
              className={`px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200 text-left cursor-pointer ${
                engineMode === "proxy_fast"
                  ? "bg-green-500/20 text-green-400 border border-green-500/30"
                  : "text-text-dim hover:text-text hover:bg-panel/30"
              }`}
            >
              Fast
            </button>
            <button
              type="button"
              onClick={(e) => handleProxySubModeClick(e, "proxy_deep")}
              className={`px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200 text-left cursor-pointer ${
                engineMode === "proxy_deep"
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

