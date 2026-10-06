"use client";

import React from "react";
import { PatientDetail, PatientSummary } from "@/types";
import { User, Activity, AlertCircle, ShieldCheck } from "lucide-react";

interface PatientHeaderProps {
  patient?: PatientDetail;
  summary?: PatientSummary;
}

export const PatientHeader: React.FC<PatientHeaderProps> = ({ patient, summary }) => {
  const name = patient?.display_name || summary?.display_name || "Patient";
  const status = summary?.status || "EXCELLENT";

  const statusConfig = {
    EXCELLENT: {
      label: "All Systems Normal",
      color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
      icon: <ShieldCheck className="w-4 h-4 text-emerald-400" />,
    },
    ATTENTION_NEEDED: {
      label: "Attention Needed",
      color: "bg-amber-500/20 text-amber-400 border-amber-500/30",
      icon: <Activity className="w-4 h-4 text-amber-400" />,
    },
    CRITICAL_ALERT: {
      label: "Active Alert",
      color: "bg-rose-500/20 text-rose-400 border-rose-500/30",
      icon: <AlertCircle className="w-4 h-4 text-rose-400" />,
    },
  }[status];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 sm:p-6 mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-md">
      <div className="flex items-center gap-4">
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-indigo-600 to-sky-500 flex items-center justify-center text-white text-2xl font-black shadow-md shadow-indigo-600/20">
          {name.charAt(0)}
        </div>
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-white tracking-tight">{name}</h1>
            <span
              className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${statusConfig.color}`}
            >
              {statusConfig.icon}
              {statusConfig.label}
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Active Care Monitoring • Emergency Contacts On File: {patient?.emergency_contacts?.length || 2}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-6 border-t md:border-t-0 md:border-l border-slate-800 pt-3 md:pt-0 md:pl-6 text-sm">
        <div>
          <span className="block text-slate-400 text-xs">Today&apos;s Adherence</span>
          <span className="text-xl font-bold text-white">
            {summary ? `${summary.adherence_percentage}%` : "100%"}
          </span>
        </div>
        <div>
          <span className="block text-slate-400 text-xs">Active Prescriptions</span>
          <span className="text-xl font-bold text-indigo-400">
            {summary?.total_medications || 3}
          </span>
        </div>
        <div>
          <span className="block text-slate-400 text-xs">Open Alerts</span>
          <span className={`text-xl font-bold ${summary?.open_alerts_count ? "text-rose-400" : "text-emerald-400"}`}>
            {summary?.open_alerts_count || 0}
          </span>
        </div>
      </div>
    </div>
  );
};
