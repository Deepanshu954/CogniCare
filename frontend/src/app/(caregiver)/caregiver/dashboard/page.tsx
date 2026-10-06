"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import { Navbar } from "@/components/ui/Navbar";
import { PatientHeader } from "@/components/caregiver/PatientHeader";
import { TrendChart } from "@/components/caregiver/TrendChart";
import { AdherenceGauge } from "@/components/caregiver/AdherenceGauge";
import { AlertList } from "@/components/caregiver/AlertList";
import {
  PatientDetail,
  PatientSummary,
  CognitiveOverview,
  CognitiveTrendPoint,
  Alert,
  Medication,
} from "@/types";
import { apiClient } from "@/lib/api";
import {
  Activity,
  Brain,
  ShieldAlert,
  Pill,
  Plus,
  Users,
  CheckCircle2,
  Calendar,
} from "lucide-react";

export default function CaregiverDashboardPage() {
  const { user, isLoading: isAuthLoading } = useAuth();
  const router = useRouter();

  const [patients, setPatients] = useState<PatientDetail[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string>("");
  const [summary, setSummary] = useState<PatientSummary | null>(null);
  const [overview, setOverview] = useState<CognitiveOverview | null>(null);
  const [trends, setTrends] = useState<CognitiveTrendPoint[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [medications, setMedications] = useState<Medication[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // New Medication Modal state
  const [showAddMed, setShowAddMed] = useState(false);
  const [medName, setMedName] = useState("");
  const [medDose, setMedDose] = useState("");
  const [medTime, setMedTime] = useState("09:00");

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
        loadPatientData(initialId);
      } else {
        setIsLoading(false);
      }
    } catch (e) {
      console.error("Failed to load patients list:", e);
      setIsLoading(false);
    }
  };

  const loadPatientData = async (patId: string) => {
    setIsLoading(true);
    try {
      const [sumRes, overRes, trendRes, alertRes, medRes] = await Promise.all([
        apiClient.get<PatientSummary>(`/patients/${patId}/summary`),
        apiClient.get<CognitiveOverview>(`/patients/${patId}/cognition/overview`),
        apiClient.get<CognitiveTrendPoint[]>(`/patients/${patId}/cognition/trends`),
        apiClient.get<Alert[]>(`/patients/${patId}/alerts`),
        apiClient.get<Medication[]>(`/patients/${patId}/medications`),
      ]);

      setSummary(sumRes.data);
      setOverview(overRes.data);
      setTrends(trendRes.data);
      setAlerts(alertRes.data);
      setMedications(medRes.data);
    } catch (e) {
      console.error("Error loading patient data:", e);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePatientSwitch = (patId: string) => {
    setSelectedPatientId(patId);
    loadPatientData(patId);
  };

  const handleCreateMedication = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPatientId || !medName.trim()) return;

    try {
      await apiClient.post(`/patients/${selectedPatientId}/medications`, {
        name: medName,
        dosage_text: medDose || "1 tablet",
        instructions: "Take with water as prescribed.",
        schedules: [
          {
            schedule_type: "DAILY",
            time_of_day: medTime,
            criticality: "HIGH",
          },
        ],
      });
      setShowAddMed(false);
      setMedName("");
      setMedDose("");
      loadPatientData(selectedPatientId);
    } catch (e) {
      console.error("Failed to create medication:", e);
    }
  };

  if (isAuthLoading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white">
        Loading Caregiver Console...
      </div>
    );
  }

  const selectedPatient = patients.find((p) => p.id === selectedPatientId);

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-8 py-8">
        {/* Top Controls: Patient Switcher */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-3">
            <Users className="w-5 h-5 text-indigo-400" />
            <label className="text-sm font-semibold text-slate-300">Monitored Patient:</label>
            <select
              value={selectedPatientId}
              onChange={(e) => handlePatientSwitch(e.target.value)}
              className="bg-slate-900 border border-slate-700 text-white font-bold rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-indigo-500 cursor-pointer"
            >
              {patients.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.display_name} ({p.email})
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowAddMed(true)}
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow cursor-pointer"
            >
              <Plus className="w-4 h-4" />
              <span>Add Medication</span>
            </button>
          </div>
        </div>

        {/* Patient Status Ribbon */}
        {selectedPatient && <PatientHeader patient={selectedPatient} summary={summary || undefined} />}

        {/* Grid: Adherence Gauge + Cognitive Trends Chart */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Adherence Gauge Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-md flex flex-col justify-between">
            <div>
              <h3 className="text-lg font-bold text-white mb-1 flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                <span>Today&apos;s Care Adherence</span>
              </h3>
              <p className="text-xs text-slate-400">
                Percentage of scheduled morning, afternoon, and evening care items completed.
              </p>
            </div>

            <AdherenceGauge
              percentage={summary?.adherence_percentage || 100}
              completed={summary?.today_completed_reminders || 0}
              total={summary?.today_reminders_count || 0}
            />

            <div className="text-center pt-2 border-t border-slate-800/80">
              <span className="text-xs text-slate-400">
                Missed critical care triggers automated caregiver escalation.
              </span>
            </div>
          </div>

          {/* 14-Day Cognitive Trend Curve */}
          <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-md">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Brain className="w-5 h-5 text-sky-400" />
                  <span>Cognitive Performance Trends</span>
                </h3>
                <p className="text-xs text-slate-400">
                  Longitudinal composite score (0-100) compared with 30-day baseline.
                </p>
              </div>

              {overview && (
                <span
                  className={`text-xs font-bold px-3 py-1 rounded-full uppercase ${
                    overview.trend_direction === "IMPROVING"
                      ? "bg-emerald-500/20 text-emerald-400"
                      : overview.trend_direction === "VARIABLE"
                      ? "bg-amber-500/20 text-amber-400"
                      : "bg-sky-500/20 text-sky-400"
                  }`}
                >
                  {overview.trend_direction}
                </span>
              )}
            </div>

            <TrendChart data={trends} />
          </div>
        </div>

        {/* Domain Scores & Prescriptions Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Cognitive Domain Breakdown */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-md">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <Activity className="w-5 h-5 text-indigo-400" />
              <span>Cognitive Domain Breakdown</span>
            </h3>

            <div className="space-y-3">
              {overview &&
                Object.entries(overview.category_scores).map(([cat, score]) => (
                  <div key={cat} className="space-y-1">
                    <div className="flex justify-between text-xs font-semibold">
                      <span className="text-slate-300">{cat}</span>
                      <span className="text-sky-400 font-bold">{score}/100</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-sky-500 to-indigo-500 h-2.5 rounded-full"
                        style={{ width: `${Math.min(100, score)}%` }}
                      />
                    </div>
                  </div>
                ))}
            </div>
          </div>

          {/* Active Prescriptions */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-md">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <Pill className="w-5 h-5 text-sky-400" />
                <span>Active Prescriptions & Schedule</span>
              </h3>
              <span className="text-xs text-slate-400">{medications.length} active</span>
            </div>

            <div className="space-y-2.5 max-h-56 overflow-y-auto">
              {medications.map((m) => (
                <div
                  key={m.id}
                  className="p-3 rounded-xl bg-slate-800/60 border border-slate-700/60 flex items-center justify-between text-xs"
                >
                  <div>
                    <span className="font-bold text-white block text-sm">{m.name}</span>
                    <span className="text-slate-400 font-medium">Dosage: {m.dosage_text}</span>
                  </div>

                  <div className="text-right">
                    {m.schedules.map((s, idx) => (
                      <span
                        key={idx}
                        className="inline-block px-2.5 py-1 rounded-md bg-indigo-950 text-indigo-300 font-bold border border-indigo-800/60 ml-1"
                      >
                        {s.time_of_day}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Safety Alerts Feed */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-md">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-rose-400" />
              <span>Safety & Incident Log</span>
            </h3>
            <span className="text-xs text-slate-400">
              Emergency SOS and Missed Care Events
            </span>
          </div>

          {selectedPatientId && (
            <AlertList
              alerts={alerts}
              patientId={selectedPatientId}
              onRefresh={() => loadPatientData(selectedPatientId)}
            />
          )}
        </section>

        {/* Add Medication Modal */}
        {showAddMed && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 shadow-2xl">
              <h3 className="text-xl font-bold text-white mb-4">Add Prescription</h3>

              <form onSubmit={handleCreateMedication} className="space-y-4 text-sm">
                <div>
                  <label className="block text-xs font-bold text-slate-300 mb-1">
                    Medication Name
                  </label>
                  <input
                    type="text"
                    required
                    value={medName}
                    onChange={(e) => setMedName(e.target.value)}
                    placeholder="e.g. Donepezil"
                    className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-indigo-400"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-300 mb-1">
                    Dosage
                  </label>
                  <input
                    type="text"
                    required
                    value={medDose}
                    onChange={(e) => setMedDose(e.target.value)}
                    placeholder="e.g. 10mg"
                    className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-indigo-400"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-300 mb-1">
                    Daily Scheduled Time
                  </label>
                  <input
                    type="time"
                    required
                    value={medTime}
                    onChange={(e) => setMedTime(e.target.value)}
                    className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-indigo-400"
                  />
                </div>

                <div className="flex justify-end gap-3 pt-3">
                  <button
                    type="button"
                    onClick={() => setShowAddMed(false)}
                    className="px-4 py-2 rounded-xl text-slate-300 hover:bg-slate-800"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold shadow"
                  >
                    Save Prescription
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
