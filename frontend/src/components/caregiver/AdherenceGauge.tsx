"use client";

import React from "react";
import { CheckCircle, Clock } from "lucide-react";

interface AdherenceGaugeProps {
  percentage: number;
  completed: number;
  total: number;
}

export const AdherenceGauge: React.FC<AdherenceGaugeProps> = ({
  percentage,
  completed,
  total,
}) => {
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  const colorClass =
    percentage >= 85
      ? "text-emerald-400 stroke-emerald-400"
      : percentage >= 60
      ? "text-amber-400 stroke-amber-400"
      : "text-rose-400 stroke-rose-400";

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div className="relative w-36 h-36 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r={radius}
            className="stroke-slate-800"
            strokeWidth="10"
            fill="transparent"
          />
          <circle
            cx="50"
            cy="50"
            r={radius}
            className={`${colorClass} transition-all duration-1000 ease-out`}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-3xl font-black text-white">{Math.round(percentage)}%</span>
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Adherence
          </span>
        </div>
      </div>

      <div className="mt-4 flex items-center gap-4 text-xs font-semibold text-slate-300">
        <div className="flex items-center gap-1.5">
          <CheckCircle className="w-4 h-4 text-emerald-400" />
          <span>{completed} Taken</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Clock className="w-4 h-4 text-slate-400" />
          <span>{total - completed} Pending</span>
        </div>
      </div>
    </div>
  );
};
