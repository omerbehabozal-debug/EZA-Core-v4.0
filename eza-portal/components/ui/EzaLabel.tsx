"use client";

import React from "react";

interface EzaLabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  children: React.ReactNode;
  required?: boolean;
}

export default function EzaLabel({
  children,
  required = false,
  className = "",
  ...props
}: EzaLabelProps) {
  return (
    <label
      className={`block text-sm text-neutral-300 font-medium ${className}`}
      {...props}
    >
      {children}
      {required && <span className="text-[#FF6A5C] ml-1">*</span>}
    </label>
  );
}

