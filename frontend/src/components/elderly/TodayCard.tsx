"use client";

import React from "react";
import { Reminder } from "@/types";
import { CheckCircle2, Clock, AlertCircle } from "lucide-react";

interface TodayCardProps {
  reminder?: Reminder;
  onAcknowledge: (id: string) => void;
  onSnooze: (id: string) => void;
  isLoading?: boolean;
}

export const TodayCard: React.FC<TodayCardProps> = ({
  reminder,
  onAcknowledge,
  onSnooze,
  isLoading = false,
}) => {
  if (!reminder) {
    return (
      <div className="bg-slate-800/80 border-2 border-emerald-500/50 rounded-3xl p-6 sm:p-8 text-center shadow-xl">
        <div className="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckCircle2 className="w-10 h-10" />
        </div>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-white mb-2">
          You are all caught up!
        </h2>
        <p className="text-lg text-slate-300 max-w-md mx-auto">
          No pending tasks or medicines due right now. Enjoy your day!
        </p>
      </div>
    );
  }

  const isCompleted = reminder.status === "ACKNOWLEDGED";
  const formattedTime = new Date(reminder.scheduled_for).toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
  });

  return (
    <div className="bg-gradient-to-b from-slate-800 to-slate-900 border-2 border-sky-400/60 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
      <div className="flex items-center justify-between gap-4 mb-4">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-sky-500/20 text-sky-300 border border-sky-400/40 text-base font-bold">
          <Clock className="w-5 h-5" />
          <span>Scheduled for {formattedTime}</span>
        </div>
        {reminder.priority === "HIGH" && (
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/40 text-sm font-semibold">
            <AlertCircle className="w-4 h-4" />
            <span>Important</span>
          </div>
        )}
      </div>

      <h2 className="text-2xl sm:text-4xl font-extrabold text-white mb-3 tracking-wide leading-tight">
        {reminder.title}
      </h2>

      {reminder.description && (
        <p className="text-lg sm:text-xl text-slate-300 mb-6">
          {reminder.description}
        </p>
      )}

      {isCompleted ? (
        <div className="flex items-center justify-center gap-3 bg-emerald-950/60 border border-emerald-500/50 text-emerald-300 p-5 rounded-2xl text-xl font-bold">
          <CheckCircle2 className="w-8 h-8 text-emerald-400" />
          <span>Marked as completed for today</span>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          <button
            onClick={() => onAcknowledge(reminder.id)}
            disabled={isLoading}
            className="w-full min-h-[64px] bg-emerald-600 hover:bg-emerald-500 text-white text-xl sm:text-2xl font-black py-4 px-6 rounded-2xl border-2 border-emerald-400 shadow-lg shadow-emerald-900/40 transition-transform active:scale-[0.98] flex items-center justify-center gap-3 cursor-pointer"
          >
            <CheckCircle2 className="w-8 h-8" />
            <span>I Did This!</span>
          </button>

          <button
            onClick={() => onSnooze(reminder.id)}
            disabled={isLoading}
            className="w-full min-h-[64px] bg-slate-700 hover:bg-slate-600 text-slate-200 text-lg sm:text-xl font-bold py-4 px-6 rounded-2xl border-2 border-slate-500 shadow transition-transform active:scale-[0.98] flex items-center justify-center gap-2 cursor-pointer"
          >
            <Clock className="w-6 h-6" />
            <span>Remind in 15 Min</span>
          </button>
        </div>
      )}
    </div>
  );
};
