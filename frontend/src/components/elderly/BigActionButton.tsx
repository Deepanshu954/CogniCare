"use client";

import React from "react";

interface BigActionButtonProps {
  icon: React.ReactNode;
  title: string;
  subtitle?: string;
  onClick: () => void;
  variant?: "primary" | "success" | "warning" | "danger" | "neutral";
  className?: string;
  disabled?: boolean;
}

export const BigActionButton: React.FC<BigActionButtonProps> = ({
  icon,
  title,
  subtitle,
  onClick,
  variant = "primary",
  className = "",
  disabled = false,
}) => {
  const variantStyles = {
    primary: "bg-sky-600 hover:bg-sky-500 text-white border-sky-400 shadow-sky-900/40",
    success: "bg-emerald-600 hover:bg-emerald-500 text-white border-emerald-400 shadow-emerald-900/40",
    warning: "bg-amber-600 hover:bg-amber-500 text-white border-amber-400 shadow-amber-900/40",
    danger: "bg-rose-700 hover:bg-rose-600 text-white border-rose-400 shadow-rose-900/40",
    neutral: "bg-slate-800 hover:bg-slate-700 text-slate-100 border-slate-600 shadow-slate-900/40",
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`w-full min-h-[72px] sm:min-h-[84px] px-6 py-4 rounded-2xl border-2 flex items-center justify-between gap-4 text-left font-bold transition-all transform active:scale-[0.98] shadow-lg ${variantStyles[variant]} ${
        disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"
      } ${className}`}
    >
      <div className="flex items-center gap-4 sm:gap-5">
        <div className="p-3 bg-white/15 rounded-xl flex-shrink-0 text-white">
          {icon}
        </div>
        <div>
          <div className="text-xl sm:text-2xl font-extrabold tracking-wide leading-tight">
            {title}
          </div>
          {subtitle && (
            <div className="text-base sm:text-lg font-medium opacity-90 mt-0.5">
              {subtitle}
            </div>
          )}
        </div>
      </div>
      <div className="text-2xl font-bold opacity-80">➔</div>
    </button>
  );
};
