"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import { Navbar } from "@/components/ui/Navbar";
import { SosButton } from "@/components/elderly/SosButton";
import { PatientDetail } from "@/types";
import { apiClient } from "@/lib/api";
import { Phone, Shield, ArrowLeft, HeartPulse, User } from "lucide-react";

export default function SafetyPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [patient, setPatient] = useState<PatientDetail | null>(null);

  const patientId = user?.patient_profile?.id;

  useEffect(() => {
    const fetchPatient = async () => {
      if (!patientId) return;
      try {
        const res = await apiClient.get<PatientDetail>(`/patients/${patientId}`);
        setPatient(res.data);
      } catch (e) {
        console.error("Failed to load emergency contacts:", e);
      }
    };
    fetchPatient();
  }, [patientId]);

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-2xl w-full mx-auto px-4 sm:px-8 py-8 space-y-8">
        <button
          onClick={() => router.push("/app/my-day")}
          className="flex items-center gap-2 text-slate-300 hover:text-white font-bold text-lg mb-2"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back to My Day</span>
        </button>

        <div className="text-center">
          <h1 className="text-3xl sm:text-4xl font-black text-white mb-2">Emergency & Safety</h1>
          <p className="text-lg text-slate-300">
            Press the red button below if you need immediate assistance or feel unwell.
          </p>
        </div>

        {patientId && (
          <div className="py-4">
            <SosButton patientId={patientId} />
          </div>
        )}

        {/* Emergency Contacts List */}
        <section className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8">
          <h2 className="text-2xl font-black text-white mb-4 flex items-center gap-2">
            <Phone className="w-6 h-6 text-sky-400" />
            <span>Designated Emergency Contacts</span>
          </h2>

          <div className="space-y-3">
            {patient?.emergency_contacts && patient.emergency_contacts.length > 0 ? (
              patient.emergency_contacts.map((contact) => (
                <div
                  key={contact.id}
                  className="bg-slate-800 p-5 rounded-2xl border border-slate-700 flex items-center justify-between gap-4"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-xl bg-sky-500/20 text-sky-400 flex items-center justify-center font-bold">
                      <User className="w-6 h-6" />
                    </div>
                    <div>
                      <span className="text-xl font-bold text-white block">
                        {contact.name}
                      </span>
                      <span className="text-sm font-semibold text-slate-400">
                        {contact.relationship_type}
                      </span>
                    </div>
                  </div>

                  <a
                    href={`tel:${contact.phone}`}
                    className="px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold text-base flex items-center gap-2 cursor-pointer shadow"
                  >
                    <Phone className="w-5 h-5" />
                    <span>Call</span>
                  </a>
                </div>
              ))
            ) : (
              <p className="text-slate-400 text-base">
                Your family and doctor are registered to receive all urgent signals.
              </p>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
