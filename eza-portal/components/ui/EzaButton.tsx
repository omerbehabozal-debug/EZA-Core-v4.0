"use client";

import React from "react";
import { theme } from "@/theme/eza-theme";

interface EzaButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "safe" | "caution" | "danger" | "ghost";
  size?: "sm" | "md" | "lg";
  children: React.ReactNode;
}

export default function EzaButton({
  variant = "primary",
  size = "md",
  children,
  className = "",
  ...props
}: EzaButtonProps) {
  const baseStyles = "rounded-lg font-medium transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed";
  
  const variantStyles = {
    primary: "bg-blue-600 hover:bg-blue-700 text-white shadow-md",
    secondary: "bg-neutral-900 hover:bg-neutral-800 text-neutral-300 border border-neutral-700",
    safe: "bg-[#3DE3B6] hover:bg-[#2DD4A5] text-white shadow-md",
    caution: "bg-[#FFCB47] hover:bg-[#FFB800] text-white shadow-md",
    danger: "bg-[#FF6A5C] hover:bg-[#FF5545] text-white shadow-md",
    ghost: "bg-transparent hover:bg-neutral-900 text-neutral-300"
  };

  const sizeStyles = {
    sm: "px-3 py-1 text-xs",
    md: "px-4 py-2 text-sm",
    lg: "px-6 py-3 text-base"
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

