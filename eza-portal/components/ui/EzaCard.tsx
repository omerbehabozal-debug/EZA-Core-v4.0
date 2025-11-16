"use client";

import React from "react";
import { theme } from "@/theme/eza-theme";

interface EzaCardProps {
  children: React.ReactNode;
  className?: string;
  variant?: "default" | "glass" | "elevated";
}

export default function EzaCard({
  children,
  className = "",
  variant = "default"
}: EzaCardProps) {
  const baseStyles = "rounded-xl border p-4";
  
  const variantStyles = {
    default: "bg-[#111418] border-neutral-800",
    glass: "bg-[rgba(17,20,24,0.55)] border-neutral-800 backdrop-blur-[4px]",
    elevated: "bg-[#111418] border-neutral-800 shadow-[0_8px_20px_rgba(0,0,0,0.25)]"
  };

  return (
    <div className={`${baseStyles} ${variantStyles[variant]} ${className}`}>
      {children}
    </div>
  );
}

