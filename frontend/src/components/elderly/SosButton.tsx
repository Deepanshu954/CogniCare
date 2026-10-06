"use client";

import React, { useState, useEffect } from "react";
import { AlertTriangle, PhoneCall, XCircle, CheckCircle } from "lucide-react";
import { apiClient } from "@/lib/api";

interface SosButtonProps {
  patientId: string;
}

export const SosButton: React.FC<SosButtonProps> = ({ patientId }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [countdown, setCountdown] = useState(5);
  const [isTriggered, setIsTriggered] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    let timer: any = null;
    if (isOpen && countdown > 0 && !isTriggered) {
      timer = setTimeout(() => setCountdown(countdown - 1), 1000);
    } else if (isOpen && countdown === 0 && !isTriggered) {
      dispatchSos();
    }
    return () => clearTimeout(timer);
  }, [isOpen, countdown, isTriggered]);

  const startSosFlow = () => {
    setCountdown(5);
    setIsTriggered(false);
    setErrorMsg(null);
    setIsOpen(true);
  };

  const cancelSos = () => {
    setIsOpen(false);
    setCountdown(5);
    setIsTriggered(false);
  };

  const dispatchSos = async () => {
    setIsTriggered(true);
    try {
      await apiClient.post(`/patients/${patientId}/sos`, {
        message: "Emergency SOS triggered by elderly user from safety button.",
        location_note: "User app screen",
      });
    } catch (e: any) {
      setErrorMsg(e.message || "Failed to transmit SOS signal.");
    }
  };

  return (
    <>
      <button
        onClick={startSosFlow}
        className="w-full min-h-[76px] bg-rose-700 hover:bg-rose-600 text-white text-2xl sm:text-3xl font-black py-4 px-6 rounded-3xl border-4 border-rose-400 shadow-2xl animate-sos-pulse flex items-center justify-center gap-4 transition-transform active:scale-95 cursor-pointer"
      >
        <AlertTriangle className="w-10 h-10 sm:w-12 sm:h-12" />
        <span>PRESS FOR HELP (SOS)</span>
      </button>

      {/* Fullscreen Emergency Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-slate-900 border-4 border-rose-500 rounded-3xl max-w-xl w-full p-6 sm:p-10 text-center shadow-2xl">
            {!isTriggered ? (
              <>
                <div className="w-24 h-24 bg-rose-600 text-white rounded-full flex items-center justify-center mx-auto mb-6 animate-ping">
                  <span className="text-5xl font-black">{countdown}</span>
                </div>

                <h2 className="text-3xl sm:text-4xl font-black text-rose-400 mb-3">
                  Sending Emergency Alert!
                </h2>
                <p className="text-xl text-slate-200 mb-8">
                  Notifying your caregivers and emergency contacts in {countdown} seconds...
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <button
                    onClick={cancelSos}
                    className="w-full min-h-[64px] bg-slate-800 hover:bg-slate-700 text-slate-200 border-2 border-slate-600 rounded-2xl text-xl font-bold flex items-center justify-center gap-2 cursor-pointer"
                  >
                    <XCircle className="w-7 h-7 text-slate-400" />
                    <span>Cancel (I am OK)</span>
                  </button>

                  <button
                    onClick={dispatchSos}
                    className="w-full min-h-[64px] bg-rose-600 hover:bg-rose-500 text-white border-2 border-rose-300 rounded-2xl text-xl font-black flex items-center justify-center gap-2 cursor-pointer"
                  >
                    <PhoneCall className="w-7 h-7" />
                    <span>Send Now</span>
                  </button>
                </div>
              </>
            ) : (
              <>
                <div className="w-20 h-20 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-6">
                  <CheckCircle className="w-14 h-14" />
                </div>

                <h2 className="text-3xl sm:text-4xl font-black text-emerald-400 mb-3">
                  Help is on the Way!
                </h2>
                <p className="text-xl text-slate-200 mb-6">
                  Your family and caregivers have received an urgent alert on their phones.
                  Please stay calm and remain in a safe, comfortable spot.
                </p>

                {errorMsg && (
                  <p className="text-sm text-rose-300 bg-rose-950/60 p-3 rounded-lg mb-6 border border-rose-800">
                    {errorMsg}
                  </p>
                )}

                <button
                  onClick={cancelSos}
                  className="w-full min-h-[56px] bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-600 rounded-xl text-lg font-bold cursor-pointer"
                >
                  Close Window
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </>
  );
};
