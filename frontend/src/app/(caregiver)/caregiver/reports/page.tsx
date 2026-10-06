"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import { Navbar } from "@/components/ui/Navbar";
import { WeeklySummaryCard } from "@/components/caregiver/WeeklySummaryCard";
import { Report, PatientDetail } from "@/types";
import { apiClient } from "@/lib/api";
import { FileText, ArrowLeft, Sparkles, Users } from "lucide-react";

export default function CaregiverReportsPage() {
  const { user, isLoading: isAuthLoading } = useAuth();
  const router = useRouter();

  const [patients, setPatients] = useState<PatientDetail[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string>("");
  const [reports, setReports] = useState<Report[]>([]);
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!isAuthLoading) {
      if (!user) {
        router.push("/login");
      } else {
        loadPatients();
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, isAuthLoading]);

  const loadPatients = async () => {
    try {
      const res = await apiClient.get<PatientDetail[]>("/patients");
      setPatients(res.data);
      if (res.data.length > 0) {
        const initialId = res.data[0].id;
        setSelectedPatientId(initialId);
        loadReports(initialId);
      } else {
        setIsLoading(false);
      }
    } catch (e) {
      console.error("Failed to load patients:", e);
      setIsLoading(false);
    }
  };

  const loadReports = async (patientId: string) => {
    setIsLoading(true);
    try {
      const res = await apiClient.get<Report[]>(`/patients/${patientId}/reports`);
      setReports(res.data);
      if (res.data.length > 0) {
        setSelectedReport(res.data[0]);
      } else {
        setSelectedReport(null);
      }
    } catch (e) {
      console.error("Failed to load reports:", e);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePatientSwitch = (patId: string) => {
    setSelectedPatientId(patId);
    loadReports(patId);
  };

  const handleGenerateReport = async () => {
    if (!selectedPatientId) return;
    setIsGenerating(true);
    try {
      const res = await apiClient.post<Report>(`/patients/${selectedPatientId}/reports/generate`);
      setReports((prev) => [res.data, ...prev]);
      setSelectedReport(res.data);
    } catch (e) {
      console.error("Failed to generate report:", e);
    } finally {
      setIsGenerating(false);
    }
  };

  if (isAuthLoading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white">
        Loading Reports...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-8 py-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-black text-white">Clinical & Weekly Reports</h1>
            <p className="text-sm text-slate-400 mt-1">
              Evidence-based longitudinal care summaries and cognitive engagement analytics.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Users className="w-5 h-5 text-indigo-400" />
            <select
              value={selectedPatientId}
              onChange={(e) => handlePatientSwitch(e.target.value)}
              className="bg-slate-900 border border-slate-700 text-white font-bold rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-indigo-500 cursor-pointer"
            >
              {patients.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.display_name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* History Sidebar */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 h-fit">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400">
                Report Archive
              </h3>
              <button
                onClick={handleGenerateReport}
                disabled={isGenerating}
                className="text-xs font-bold text-indigo-400 hover:text-indigo-300"
              >
                + New
              </button>
            </div>

            <div className="space-y-2">
              {reports.map((r) => (
                <button
                  key={r.id}
                  onClick={() => setSelectedReport(r)}
                  className={`w-full text-left p-3 rounded-xl border text-xs font-semibold transition ${
                    selectedReport?.id === r.id
                      ? "bg-indigo-600/30 border-indigo-400 text-white"
                      : "bg-slate-800/60 border-slate-700/60 text-slate-300 hover:bg-slate-800"
                  }`}
                >
                  <span className="block font-bold">
                    Week of {r.period_start}
                  </span>
                  <span className="text-[11px] text-slate-400 block mt-0.5">
                    Adherence: {r.metrics_snapshot?.adherence_percentage || 100}%
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Active Report Viewer */}
          <div className="lg:col-span-3">
            <WeeklySummaryCard
              report={selectedReport || undefined}
              onGenerateNew={handleGenerateReport}
              isGenerating={isGenerating}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
