"use client";

import React, { useState, useEffect } from "react";
import { Mic, MicOff, Volume2 } from "lucide-react";

interface VoiceButtonProps {
  onTranscript: (text: string) => void;
  isProcessing?: boolean;
}

export const VoiceButton: React.FC<VoiceButtonProps> = ({
  onTranscript,
  isProcessing = false,
}) => {
  const [isListening, setIsListening] = useState(false);
  const [hasSpeechSupport, setHasSpeechSupport] = useState(true);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (!SpeechRecognition) {
        setHasSpeechSupport(false);
      }
    }
  }, []);

  const toggleListening = () => {
    if (typeof window === "undefined") return;

    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Voice speech recognition is not supported in this browser. Please type your message.");
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.lang = "en-US";
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event: any) => {
        const speechText = event.results[0][0].transcript;
        if (speechText) {
          onTranscript(speechText);
        }
        setIsListening(false);
      };

      recognition.onerror = () => {
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
    } catch (e) {
      console.error("Speech recognition error:", e);
      setIsListening(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <button
        onClick={toggleListening}
        disabled={isProcessing}
        aria-label={isListening ? "Listening... Tap to stop" : "Tap to talk"}
        className={`w-28 h-28 sm:w-36 sm:h-36 rounded-full flex flex-col items-center justify-center gap-2 border-4 transition-all transform active:scale-95 shadow-2xl ${
          isListening
            ? "bg-rose-600 border-rose-300 text-white animate-pulse-ring scale-105"
            : isProcessing
            ? "bg-amber-600 border-amber-300 text-white animate-pulse"
            : "bg-sky-600 hover:bg-sky-500 border-sky-300 text-white hover:scale-105"
        }`}
      >
        {isListening ? (
          <>
            <Mic className="w-12 h-12 sm:w-16 sm:h-16 animate-bounce" />
            <span className="text-sm font-extrabold uppercase tracking-wider">Listening</span>
          </>
        ) : isProcessing ? (
          <>
            <Volume2 className="w-12 h-12 sm:w-16 sm:h-16 animate-spin" />
            <span className="text-sm font-extrabold uppercase tracking-wider">Thinking</span>
          </>
        ) : (
          <>
            <Mic className="w-12 h-12 sm:w-16 sm:h-16" />
            <span className="text-sm font-extrabold uppercase tracking-wider">Tap to Talk</span>
          </>
        )}
      </button>

      <p className="mt-4 text-base sm:text-lg font-bold text-slate-300 text-center">
        {isListening
          ? "I am listening... say something like 'What do I have today?'"
          : "Tap the microphone anytime to speak with your assistant"}
      </p>
    </div>
  );
};
