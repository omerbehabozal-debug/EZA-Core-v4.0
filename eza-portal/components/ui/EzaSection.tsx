"use client";

import React from "react";

interface EzaSectionProps {
  title?: string;
  children: React.ReactNode;
  className?: string;
  headerClassName?: string;
}

export default function EzaSection({
  title,
  children,
  className = "",
  headerClassName = ""
}: EzaSectionProps) {
  return (
    <div className={`space-y-3 ${className}`}>
      {title && (
        <h3 className={`text-sm font-semibold text-neutral-300 ${headerClassName}`}>
          {title}
        </h3>
      )}
      <div>{children}</div>
    </div>
  );
}

