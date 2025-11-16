"use client";

import React from "react";

interface EzaInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export default function EzaInput({
  label,
  error,
  className = "",
  ...props
}: EzaInputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm text-neutral-300 mb-1.5">
          {label}
        </label>
      )}
      <input
        className={`w-full px-4 py-3 rounded-xl bg-[#13171D] border border-neutral-700 outline-none focus:border-blue-500 transition text-white placeholder:text-neutral-500 ${className}`}
        {...props}
      />
      {error && (
        <p className="mt-1 text-xs text-[#FF6A5C]">{error}</p>
      )}
    </div>
  );
}

