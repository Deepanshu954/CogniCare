"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import { Navbar } from "@/components/ui/Navbar";
import { ActivityPlayer } from "@/components/elderly/ActivityPlayer";
import { CognitiveActivity } from "@/types";
import { apiClient } from "@/lib/api";
import { ArrowLeft } from "lucide-react";

export default function PlayActivityPage() {
  const { id } = useParams();
  const { user, isLoading: isAuthLoading } = useAuth();
  const router = useRouter();

  const [activity, setActivity] = useState<CognitiveActivity | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const patientId = user?.patient_profile?.id;

  useEffect(() => {
    if (!isAuthLoading && !user) {
      router.push("/login");
    }
  }, [user, isAuthLoading, router]);

  useEffect(() => {
    const fetchActivity = async () => {
      try {
        const res = await apiClient.get<CognitiveActivity[]>("/activities");
        const found = res.data.find((a) => a.id === id);
        if (found) {
          setActivity(found);
        }
      } catch (e) {
        console.error("Failed to fetch activity:", e);
      } finally {
        setIsLoading(false);
      }
    };
    if (id) {
      fetchActivity();
    }
  }, [id]);

  if (isLoading || !activity || !patientId) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white text-xl font-bold">
        Loading exercise...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-8 py-8 space-y-6">
        <button
          onClick={() => router.push("/app/activities")}
          className="flex items-center gap-2 text-slate-300 hover:text-white font-bold text-lg mb-2"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back to Catalog</span>
        </button>

        <ActivityPlayer
          activity={activity}
          patientId={patientId}
          onFinish={() => router.push("/app/activities")}
        />
      </main>
    </div>
  );
}
