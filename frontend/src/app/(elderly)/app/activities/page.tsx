"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import { Navbar } from "@/components/ui/Navbar";
import { CognitiveActivity } from "@/types";
import { apiClient } from "@/lib/api";
import { Brain, Sparkles, Clock, Eye, Layers, ArrowLeft } from "lucide-react";

export default function ActivitiesCatalogPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [activities, setActivities] = useState<CognitiveActivity[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const res = await apiClient.get<CognitiveActivity[]>("/activities");
        setActivities(res.data);
      } catch (e) {
        console.error("Failed to load activities catalog:", e);
      } finally {
        setIsLoading(false);
      }
    };
    fetchActivities();
  }, []);

  const getIcon = (type: string) => {
    switch (type) {
      case "ATTENTION_STROOP":
        return <Eye className="w-8 h-8 text-sky-400" />;
      case "WORD_SEQUENCE":
        return <Layers className="w-8 h-8 text-indigo-400" />;
      case "ORIENTATION_MATCH":
        return <Clock className="w-8 h-8 text-amber-400" />;
      case "MEMORY_RECALL":
      default:
        return <Brain className="w-8 h-8 text-rose-400" />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-8 py-8 space-y-6">
        <div className="flex items-center gap-4">
          <button
            onClick={() => router.push("/app/my-day")}
            className="p-3 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-2xl border border-slate-700 cursor-pointer"
          >
            <ArrowLeft className="w-6 h-6" />
          </button>
          <div>
            <h1 className="text-3xl sm:text-4xl font-black text-white">Daily Brain Games</h1>
            <p className="text-slate-300 text-lg">
              Fun, calm exercises designed to stimulate your memory and attention.
            </p>
          </div>
        </div>

        {isLoading ? (
          <div className="text-center py-16 text-slate-400 text-xl font-bold">
            Loading exercises...
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-5">
            {activities.map((act) => (
              <div
                key={act.id}
                onClick={() => router.push(`/app/activities/${act.id}`)}
                className="bg-slate-900 hover:bg-slate-800/80 border-2 border-slate-800 hover:border-sky-500/70 p-6 sm:p-8 rounded-3xl flex items-center justify-between gap-6 cursor-pointer transition-all transform active:scale-98 shadow-xl"
              >
                <div className="flex items-start gap-5">
                  <div className="w-16 h-16 rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center flex-shrink-0 mt-1">
                    {getIcon(act.activity_type)}
                  </div>
                  <div>
                    <span className="text-xs uppercase font-extrabold tracking-wider text-sky-400 block mb-1">
                      {act.category}
                    </span>
                    <h2 className="text-2xl sm:text-3xl font-extrabold text-white mb-2">
                      {act.title}
                    </h2>
                    <p className="text-slate-300 text-base sm:text-lg max-w-xl">
                      {act.description}
                    </p>
                  </div>
                </div>

                <div className="hidden sm:flex items-center gap-2 px-5 py-3 rounded-2xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-lg flex-shrink-0 shadow">
                  <span>Play</span>
                  <span>➔</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
