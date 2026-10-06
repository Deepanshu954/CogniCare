"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import { Navbar } from "@/components/ui/Navbar";
import { TodayCard } from "@/components/elderly/TodayCard";
import { BigActionButton } from "@/components/elderly/BigActionButton";
import { SosButton } from "@/components/elderly/SosButton";
import { Reminder } from "@/types";
import { apiClient } from "@/lib/api";
import { Brain, MessageSquare, AlertCircle, Calendar, CheckCircle2, Pill } from "lucide-react";

export default function MyDayPage() {
  const { user, isLoading: isAuthLoading } = useAuth();
  const router = useRouter();

  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const patientId = user?.patient_profile?.id;

  const fetchReminders = async () => {
    if (!patientId) return;
    try {
      const res = await apiClient.get<Reminder[]>(`/patients/${patientId}/reminders/today`);
      setReminders(res.data);
    } catch (e) {
      console.error("Failed to load reminders:", e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!isAuthLoading) {
      if (!user) {
        router.push("/login");
      } else if (patientId) {
        fetchReminders();
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, isAuthLoading, patientId]);

  const handleAcknowledge = async (reminderId: string) => {
    try {
      await apiClient.post(`/patients/${patientId}/reminders/${reminderId}/acknowledge`);
      fetchReminders();
    } catch (e) {
      console.error("Acknowledge failed:", e);
    }
  };

  const handleSnooze = async (reminderId: string) => {
    try {
      await apiClient.post(`/patients/${patientId}/reminders/${reminderId}/snooze`, {
        snooze_minutes: 15,
      });
      fetchReminders();
    } catch (e) {
      console.error("Snooze failed:", e);
    }
  };

  if (isAuthLoading || !user) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white text-2xl font-bold">
        Loading CogniCare...
      </div>
    );
  }

  const name = user.profile?.display_name?.split(" ")[0] || "Friend";
  const nextReminder = reminders.find((r) => r.status === "SCHEDULED" || r.status === "SNOOZED");
  const todayFormatted = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  });

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-8 py-8 space-y-8">
        {/* Big Greeting Banner */}
        <div className="bg-gradient-to-r from-sky-950/60 to-indigo-950/40 border-2 border-sky-500/30 rounded-3xl p-6 sm:p-8">
          <div className="flex items-center gap-2 text-sky-400 text-lg font-bold uppercase tracking-wider mb-1">
            <Calendar className="w-5 h-5" />
            <span>{todayFormatted}</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-black text-white">
            Good day, {name}!
          </h1>
          <p className="text-lg sm:text-xl text-slate-300 mt-2">
            Here is your daily care schedule. Take your time with each activity.
          </p>
        </div>

        {/* Hero "Next Up" Card */}
        <section>
          <TodayCard
            reminder={nextReminder}
            onAcknowledge={handleAcknowledge}
            onSnooze={handleSnooze}
            isLoading={isLoading}
          />
        </section>

        {/* Big Primary Action Grid */}
        <section className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <BigActionButton
            icon={<Brain className="w-8 h-8" />}
            title="Play Brain Game"
            subtitle="Card matching & memory exercises"
            variant="primary"
            onClick={() => router.push("/app/activities")}
          />

          <BigActionButton
            icon={<MessageSquare className="w-8 h-8" />}
            title="Talk with Assistant"
            subtitle="Ask about your routine or medicine"
            variant="success"
            onClick={() => router.push("/app/assistant")}
          />
        </section>

        {/* Today's Schedule Timeline */}
        <section className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8">
          <h2 className="text-2xl sm:text-3xl font-black text-white mb-6">
            Today&apos;s Schedule
          </h2>

          <div className="space-y-4">
            {reminders.map((rem) => {
              const isDone = rem.status === "ACKNOWLEDGED";
              const timeStr = new Date(rem.scheduled_for).toLocaleTimeString([], {
                hour: "numeric",
                minute: "2-digit",
              });

              return (
                <div
                  key={rem.id}
                  className={`p-5 rounded-2xl border-2 flex items-center justify-between gap-4 transition-all ${
                    isDone
                      ? "bg-slate-900/60 border-slate-800 text-slate-400"
                      : "bg-slate-800 border-slate-700 text-white"
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <div
                      className={`w-12 h-12 rounded-xl flex items-center justify-center font-bold text-lg ${
                        isDone
                          ? "bg-emerald-500/20 text-emerald-400"
                          : "bg-sky-500/20 text-sky-400"
                      }`}
                    >
                      {isDone ? <CheckCircle2 className="w-6 h-6" /> : <Pill className="w-6 h-6" />}
                    </div>

                    <div>
                      <span className="text-sm font-semibold opacity-80 block">{timeStr}</span>
                      <span className="text-xl sm:text-2xl font-bold">{rem.title}</span>
                    </div>
                  </div>

                  {!isDone && (
                    <button
                      onClick={() => handleAcknowledge(rem.id)}
                      className="px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-base font-extrabold cursor-pointer"
                    >
                      Done
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* Emergency SOS Bar */}
        {patientId && (
          <section className="pt-4">
            <SosButton patientId={patientId} />
          </section>
        )}
      </main>
    </div>
  );
}
