"use client";

import React, { useState } from "react";
import { Alert } from "@/types";
import { AlertCircle, AlertTriangle, CheckCircle, ShieldAlert, Clock } from "lucide-react";
import { apiClient } from "@/lib/api";

interface AlertListProps {
  alerts: Alert[];
  patientId: string;
  onRefresh: () => void;
}

export const AlertList: React.FC<AlertListProps> = ({ alerts, patientId, onRefresh }) => {
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);
  const [resolutionNote, setResolutionNote] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleAcknowledge = async (alertId: string) => {
    try {
      await apiClient.post(`/patients/${patientId}/alerts/${alertId}/acknowledge`);
      onRefresh();
    } catch (e) {
      console.error("Failed to acknowledge alert:", e);
    }
  };

  const handleResolve = async () => {
    if (!selectedAlert) return;
    setIsSubmitting(true);
    try {
      await apiClient.post(`/patients/${patientId}/alerts/${selectedAlert.id}/resolve`, {
        note: resolutionNote || "Resolved after verification.",
      });
      setSelectedAlert(null);
      setResolutionNote("");
      onRefresh();
    } catch (e) {
      console.error("Failed to resolve alert:", e);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (alerts.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-center text-slate-400">
        <CheckCircle className="w-12 h-12 text-emerald-400 mx-auto mb-3" />
        <h3 className="text-lg font-bold text-white mb-1">All Clear</h3>
        <p className="text-sm">No safety alerts or emergency events on record.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {alerts.map((alert) => {
        const isCritical = alert.severity === "CRITICAL";
        const isOpen = alert.status === "OPEN" || alert.status === "ESCALATED";
        const isAcknowledged = alert.status === "ACKNOWLEDGED";

        return (
          <div
            key={alert.id}
            className={`p-4 rounded-xl border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 transition-all ${
              isOpen
                ? isCritical
                  ? "bg-rose-950/40 border-rose-600/70 shadow-lg shadow-rose-950/30"
                  : "bg-amber-950/30 border-amber-500/50"
                : "bg-slate-900/60 border-slate-800 opacity-80"
            }`}
          >
            <div className="flex items-start gap-3.5">
              <div
                className={`p-2.5 rounded-xl flex-shrink-0 mt-0.5 ${
                  isOpen
                    ? isCritical
                      ? "bg-rose-600 text-white"
                      : "bg-amber-600 text-white"
                    : "bg-slate-800 text-slate-400"
                }`}
              >
                {isCritical ? (
                  <ShieldAlert className="w-5 h-5" />
                ) : (
                  <AlertTriangle className="w-5 h-5" />
                )}
              </div>

              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-base font-bold text-white leading-tight">
                    {alert.summary}
                  </span>
                  <span
                    className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full uppercase tracking-wider ${
                      isOpen
                        ? isCritical
                          ? "bg-rose-500/30 text-rose-300 border border-rose-500/50"
                          : "bg-amber-500/30 text-amber-300 border border-amber-500/50"
                        : "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                    }`}
                  >
                    {alert.status}
                  </span>
                </div>

                <div className="flex items-center gap-3 text-xs text-slate-400">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    {new Date(alert.created_at).toLocaleTimeString([], {
                      month: "short",
                      day: "numeric",
                      hour: "numeric",
                      minute: "2-digit",
                    })}
                  </span>
                  <span>Type: {alert.alert_type}</span>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-2 self-end sm:self-center">
              {isOpen && (
                <button
                  onClick={() => handleAcknowledge(alert.id)}
                  className="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 cursor-pointer"
                >
                  Acknowledge
                </button>
              )}

              {(isOpen || isAcknowledged) && (
                <button
                  onClick={() => setSelectedAlert(alert)}
                  className="px-3.5 py-1.5 rounded-lg bg-emerald-700 hover:bg-emerald-600 text-xs font-bold text-white shadow cursor-pointer"
                >
                  Resolve
                </button>
              )}
            </div>
          </div>
        );
      })}

      {/* Resolution Modal */}
      {selectedAlert && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 shadow-2xl">
            <h3 className="text-xl font-bold text-white mb-2">Resolve Alert</h3>
            <p className="text-sm text-slate-400 mb-4">{selectedAlert.summary}</p>

            <label className="block text-xs font-semibold text-slate-300 mb-2">
              Clinical / Caregiver Note:
            </label>
            <textarea
              rows={3}
              value={resolutionNote}
              onChange={(e) => setResolutionNote(e.target.value)}
              placeholder="e.g. Spoke with patient, verified they are safe and comfortable..."
              className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white placeholder-slate-500 mb-5 focus:outline-none focus:border-sky-400"
            />

            <div className="flex justify-end gap-3">
              <button
                onClick={() => setSelectedAlert(null)}
                className="px-4 py-2 rounded-xl text-sm font-semibold text-slate-300 hover:bg-slate-800"
              >
                Cancel
              </button>
              <button
                onClick={handleResolve}
                disabled={isSubmitting}
                className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-bold shadow"
              >
                {isSubmitting ? "Saving..." : "Confirm Resolution"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
