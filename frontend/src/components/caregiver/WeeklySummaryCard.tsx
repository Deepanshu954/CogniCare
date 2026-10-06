"use client";

import React from "react";
import { Report } from "@/types";
import { FileText, Printer, Sparkles, CheckCircle2 } from "lucide-react";

interface WeeklySummaryCardProps {
  report?: Report;
  onGenerateNew: () => void;
  isGenerating?: boolean;
}

export const WeeklySummaryCard: React.FC<WeeklySummaryCardProps> = ({
  report,
  onGenerateNew,
  isGenerating = false,
}) => {
  const handlePrint = () => {
    if (typeof window !== "undefined") {
      window.print();
    }
  };

  if (!report) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-center">
        <FileText className="w-12 h-12 text-slate-500 mx-auto mb-3" />
        <h3 className="text-xl font-bold text-white mb-2">No Reports Generated Yet</h3>
        <p className="text-sm text-slate-400 mb-6 max-w-md mx-auto">
          Generate an AI-assisted weekly report compiling routine adherence, cognitive trends,
          and safety events into an executive clinical summary.
        </p>
        <button
          onClick={onGenerateNew}
          disabled={isGenerating}
          className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-6 py-2.5 rounded-xl shadow cursor-pointer"
        >
          <Sparkles className="w-4 h-4" />
          <span>{isGenerating ? "Compiling..." : "Generate Weekly Report"}</span>
        </button>
      </div>
    );
  }

  const metrics = report.metrics_snapshot || {};

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-xl print:border-none print:shadow-none">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-800 gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 text-xs font-bold uppercase tracking-wider mb-1">
            <Sparkles className="w-4 h-4" />
            <span>AI Caregiver Weekly Summary</span>
          </div>
          <h2 className="text-2xl font-bold text-white">
            Report: {report.period_start} to {report.period_end}
          </h2>
        </div>

        <div className="flex items-center gap-3 print:hidden">
          <button
            onClick={handlePrint}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 cursor-pointer"
          >
            <Printer className="w-4 h-4" />
            <span>Print / PDF</span>
          </button>
          <button
            onClick={onGenerateNew}
            disabled={isGenerating}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow cursor-pointer"
          >
            <Sparkles className="w-4 h-4" />
            <span>{isGenerating ? "Generating..." : "Regenerate"}</span>
          </button>
        </div>
      </div>

      {/* Structured Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700/60">
          <span className="block text-xs text-slate-400 font-medium">Adherence Rate</span>
          <span className="text-2xl font-black text-emerald-400">
            {metrics.adherence_percentage || 100}%
          </span>
          <span className="text-[11px] text-slate-500 block mt-0.5">
            {metrics.reminders_acknowledged || 0} / {metrics.total_reminders_scheduled || 0} on time
          </span>
        </div>

        <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700/60">
          <span className="block text-xs text-slate-400 font-medium">Cognitive Score</span>
          <span className="text-2xl font-black text-sky-400">
            {metrics.cognitive_composite_score || 85}/100
          </span>
          <span className="text-[11px] text-slate-500 block mt-0.5">
            {metrics.cognitive_sessions_completed || 0} exercises completed
          </span>
        </div>

        <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700/60">
          <span className="block text-xs text-slate-400 font-medium">Reaction Latency</span>
          <span className="text-2xl font-black text-indigo-300">
            {metrics.average_latency_ms || 1700}ms
          </span>
          <span className="text-[11px] text-slate-500 block mt-0.5">
            Accuracy: {metrics.average_accuracy_percentage || 85}%
          </span>
        </div>

        <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700/60">
          <span className="block text-xs text-slate-400 font-medium">Safety Incidents</span>
          <span className="text-2xl font-black text-white">
            {metrics.alerts_triggered_count || 0}
          </span>
          <span className="text-[11px] text-slate-500 block mt-0.5">
            {metrics.sos_events_count || 0} emergency SOS triggers
          </span>
        </div>
      </div>

      {/* AI Narrative Section */}
      <div className="bg-slate-800/40 p-6 rounded-2xl border border-slate-700/60">
        <h4 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-3">
          Clinical Insights & Narrative Evaluation
        </h4>
        <div className="text-slate-200 text-sm leading-relaxed whitespace-pre-line space-y-2">
          {report.ai_narrative_summary}
        </div>
      </div>
    </div>
  );
};
