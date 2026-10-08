"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import { Navbar } from "@/components/ui/Navbar";
import { Brain, Heart, Shield, Activity, Users, Sparkles, CheckCircle2 } from "lucide-react";

export default function LandingPage() {
  const { user, quickLogin } = useAuth();
  const router = useRouter();
  const [loadingAccount, setLoadingAccount] = useState<"margaret" | "sarah" | null>(null);

  useEffect(() => {
    if (user) {
      if (user.role === "ELDERLY") {
        router.push("/app/my-day");
      } else {
        router.push("/caregiver/dashboard");
      }
    }
  }, [user, router]);

  const handleQuickLogin = async (account: "margaret" | "sarah") => {
    setLoadingAccount(account);
    try {
      const loggedUser = await quickLogin(account);
      if (loggedUser.role === "ELDERLY") {
        router.push("/app/my-day");
      } else {
        router.push("/caregiver/dashboard");
      }
    } catch (e) {
      console.error("Quick login error:", e);
      setLoadingAccount(null);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar />

      {/* Hero Section */}
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-8 py-12 sm:py-20 flex flex-col items-center text-center justify-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sky-500/10 border border-sky-400/30 text-sky-400 text-sm font-bold mb-6">
          <Sparkles className="w-4 h-4" />
          <span>Independent Capstone • AI-Powered Cognitive Care Platform</span>
        </div>

        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-black text-white tracking-tight max-w-4xl leading-tight mb-6">
          Dignified Cognitive Support.{" "}
          <span className="bg-gradient-to-r from-sky-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
            Peace of Mind for Families.
          </span>
        </h1>

        <p className="text-lg sm:text-2xl text-slate-300 max-w-3xl mb-10 leading-relaxed font-normal">
          A unified, accessibility-first web assistant bridging low-complexity daily routines
          and voice guidance for seniors with an intelligent, longitudinal monitoring control tower for caregivers.
        </p>

        {/* 1-Click Interactive Demo Buttons */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 max-w-2xl w-full shadow-2xl mb-12">
          <h2 className="text-lg font-bold text-slate-200 uppercase tracking-wider mb-4">
            🚀 1-Click Instant Demo Experience
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <button
              type="button"
              disabled={loadingAccount !== null}
              onClick={() => handleQuickLogin("margaret")}
              className={`min-h-[72px] bg-sky-600 hover:bg-sky-500 text-white font-extrabold text-lg px-6 py-4 rounded-2xl border-2 border-sky-300 shadow-lg shadow-sky-900/40 transition-transform active:scale-95 flex items-center justify-center gap-3 cursor-pointer ${
                loadingAccount !== null ? "opacity-75 cursor-not-allowed" : ""
              }`}
            >
              <Heart className="w-6 h-6 text-rose-300" />
              <span>
                {loadingAccount === "margaret" ? "Opening Senior Portal..." : "Enter as Margaret (Senior)"}
              </span>
            </button>

            <button
              type="button"
              disabled={loadingAccount !== null}
              onClick={() => handleQuickLogin("sarah")}
              className={`min-h-[72px] bg-indigo-600 hover:bg-indigo-500 text-white font-extrabold text-lg px-6 py-4 rounded-2xl border-2 border-indigo-300 shadow-lg shadow-indigo-900/40 transition-transform active:scale-95 flex items-center justify-center gap-3 cursor-pointer ${
                loadingAccount !== null ? "opacity-75 cursor-not-allowed" : ""
              }`}
            >
              <Users className="w-6 h-6 text-sky-300" />
              <span>
                {loadingAccount === "sarah" ? "Opening Caregiver Tower..." : "Enter as Sarah (Caregiver)"}
              </span>
            </button>
          </div>
          <p className="text-xs text-slate-500 mt-3">
            Pre-loaded with verified demo data, active medication schedules, and 14 days of cognitive trends.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl w-full text-left">
          <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
            <div className="w-12 h-12 rounded-xl bg-sky-500/20 text-sky-400 flex items-center justify-center mb-4">
              <Brain className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Cognitive Games & Scoring</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              4 engaging, accessible mini-games in memory, working sequence, Stroop attention, and spatial orientation with mathematical, reproducible scoring.
            </p>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center mb-4">
              <Activity className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Care & Adherence Automation</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Automated daily medication schedules, hydration prompts, and instant escalation rules that notify family if critical care is unacknowledged.
            </p>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
            <div className="w-12 h-12 rounded-xl bg-rose-500/20 text-rose-400 flex items-center justify-center mb-4">
              <Shield className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Emergency SOS & Grounded AI</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              1-tap emergency safety trigger paired with a compassionate assistant grounded in application facts, strictly guarded against medical hallucination.
            </p>
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        CogniCare — AI-Powered Cognitive Health & Care Platform • WCAG 2.2 AA Aligned
      </footer>
    </div>
  );
}
