"use client";

import React from "react";
import { theme } from "@/theme/eza-theme";

interface EzaBadgeProps {
  children: React.ReactNode;
  variant?: "default" | "safe" | "caution" | "high" | "critical" | "primary";
  className?: string;
}

export default function EzaBadge({
  children,
  variant = "default",
  className = ""
}: EzaBadgeProps) {
  const baseStyles = "inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium";
  
  const variantStyles = {
    default: "bg-neutral-800 text-neutral-300 border border-neutral-700",
    primary: "bg-blue-600/20 text-blue-400 border border-blue-600/30",
    safe: "bg-[#3DE3B6]/20 text-[#3DE3B6] border border-[#3DE3B6]/30",
    caution: "bg-[#FFCB47]/20 text-[#FFCB47] border border-[#FFCB47]/30",
    high: "bg-[#FF6A5C]/20 text-[#FF6A5C] border border-[#FF6A5C]/30",
    critical: "bg-[#D91E18]/20 text-[#D91E18] border border-[#D91E18]/30"
  };

  return (
    <span className={`${baseStyles} ${variantStyles[variant]} ${className}`}>
      {children}
    </span>
  );
}

