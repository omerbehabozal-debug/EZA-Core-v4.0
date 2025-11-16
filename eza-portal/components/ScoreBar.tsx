"use client";

import React from "react";

interface ScoreBarProps {
  score: number;
  label: string;
  maxScore?: number;
}

export default function ScoreBar({ score, label, maxScore = 100 }: ScoreBarProps) {
  const percentage = Math.min((score / maxScore) * 100, 100);
  const getColor = () => {
    if (score >= 80) return "bg-green-500";
    if (score >= 60) return "bg-yellow-500";
    if (score >= 40) return "bg-orange-500";
    return "bg-red-500";
  };

  return (
    <div className="w-full">
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium">{label}</span>
        <span className="text-sm">{score}/{maxScore}</span>
      </div>
      <div className="w-full bg-neutral-800 rounded-full h-2">
        <div
          className={`h-2 rounded-full transition-all duration-300 ${getColor()}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

