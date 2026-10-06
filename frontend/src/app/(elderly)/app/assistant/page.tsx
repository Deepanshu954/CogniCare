"use client";

import React, { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import { Navbar } from "@/components/ui/Navbar";
import { VoiceButton } from "@/components/elderly/VoiceButton";
import { Message, Conversation } from "@/types";
import { apiClient } from "@/lib/api";
import {
  Send,
  Volume2,
  Bot,
  User,
  Sparkles,
  Zap,
  Brain,
  ShieldCheck,
  ChevronDown,
  ChevronUp,
  Mic,
  X,
  Radio,
} from "lucide-react";

export default function AssistantPage() {
  const { user } = useAuth();
  const router = useRouter();

  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [activeMode, setActiveMode] = useState<"normal" | "extended">("normal");
  const [showContextDetails, setShowContextDetails] = useState(false);
  const [isLiveTalkOpen, setIsLiveTalkOpen] = useState(false);
  const [liveTalkStatus, setLiveTalkStatus] = useState<"idle" | "listening" | "thinking" | "speaking">("idle");

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const patientId = user?.patient_profile?.id;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    const initConversation = async () => {
      if (!patientId) return;
      try {
        const res = await apiClient.post<Conversation>(`/patients/${patientId}/conversations`);
        setConversation(res.data);
        setMessages(res.data.messages || []);
      } catch (e) {
        console.error("Failed to load conversation:", e);
      }
    };
    initConversation();
  }, [patientId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (textToSend?: string) => {
    const text = textToSend || inputText;
    if (!text.trim() || !conversation || !patientId || isSending) return;

    setIsSending(true);
    setInputText("");
    if (isLiveTalkOpen) setLiveTalkStatus("thinking");

    // Optimistic user message bubble
    const tempUserMsg: Message = {
      id: `temp_${Date.now()}`,
      conversation_id: conversation.id,
      role: "USER",
      content: text,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    try {
      const res = await apiClient.post<Message>(
        `/patients/${patientId}/conversations/${conversation.id}/messages`,
        { content: text, mode: activeMode }
      );
      setMessages((prev) => [...prev, res.data]);

      // Speech synthesis for live talk or voice response
      if (isLiveTalkOpen) {
        setLiveTalkStatus("speaking");
      }
      speakText(res.data.content, () => {
        if (isLiveTalkOpen) setLiveTalkStatus("idle");
      });
    } catch (e: any) {
      console.error("Message send error:", e);
      if (isLiveTalkOpen) setLiveTalkStatus("idle");
    } finally {
      setIsSending(false);
    }
  };

  const speakText = (text: string, onEnd?: () => void) => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.95; // Gentle pace for senior comfort
      if (onEnd) {
        utterance.onend = onEnd;
      }
      window.speechSynthesis.speak(utterance);
    } else if (onEnd) {
      onEnd();
    }
  };

  const startLiveTalkSpeech = () => {
    if (typeof window === "undefined") return;
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Voice recognition is not supported in this browser. Please use text input.");
      return;
    }

    setLiveTalkStatus("listening");
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      handleSendMessage(transcript);
    };

    recognition.onerror = () => {
      setLiveTalkStatus("idle");
    };

    recognition.onend = () => {
      if (liveTalkStatus === "listening") {
        setLiveTalkStatus("idle");
      }
    };

    recognition.start();
  };

  const quickPrompts = [
    "What do I have today?",
    "Did I take my morning pills?",
    "Tell me a calm story",
    "Where is Sarah?",
  ];

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-6 flex flex-col">
        {/* Model Mode Switcher & Live Talk Banner */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-4 sm:p-6 mb-6 shadow-xl">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pb-4 border-b border-slate-800">
            {/* Mode Selector */}
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400 mr-1">
                AI Mode:
              </span>
              <div className="flex items-center bg-slate-950 p-1 rounded-2xl border border-slate-800">
                <button
                  type="button"
                  onClick={() => setActiveMode("normal")}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs sm:text-sm font-black transition cursor-pointer ${
                    activeMode === "normal"
                      ? "bg-emerald-600 text-white shadow-md shadow-emerald-900/40"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  <Zap className="w-4 h-4" />
                  <span>Gemini 3.8 Live</span>
                </button>
                <button
                  type="button"
                  onClick={() => setActiveMode("extended")}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs sm:text-sm font-black transition cursor-pointer ${
                    activeMode === "extended"
                      ? "bg-purple-600 text-white shadow-md shadow-purple-900/40"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  <Brain className="w-4 h-4 text-purple-200" />
                  <span>Extended Thinking</span>
                </button>
              </div>
            </div>

            {/* Live Talk Button */}
            <button
              onClick={() => {
                setIsLiveTalkOpen(true);
                startLiveTalkSpeech();
              }}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 text-white font-bold rounded-2xl text-sm shadow-lg shadow-sky-900/30 transition transform hover:scale-102 cursor-pointer"
            >
              <Radio className="w-4 h-4 text-emerald-300 animate-pulse" />
              <span>Open Live Talk Mode</span>
            </button>
          </div>

          {/* Context Disclosure Bar */}
          <div className="mt-3">
            <button
              type="button"
              onClick={() => setShowContextDetails(!showContextDetails)}
              className="flex items-center justify-between w-full text-xs font-semibold text-slate-400 hover:text-slate-200 transition"
            >
              <span className="flex items-center gap-1.5 text-sky-400 font-bold">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Dual Grounding Active: Public Geriatric Knowledge + Private Care Profile</span>
              </span>
              {showContextDetails ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>

            {showContextDetails && (
              <div className="mt-3 p-3.5 rounded-2xl bg-slate-950 border border-slate-800 text-xs text-slate-300 space-y-2">
                <p>
                  <strong className="text-sky-300">Public Knowledge:</strong> Naomi Feil validation therapy, cognitive load minimization, non-clinical boundaries, and patient orientation cues.
                </p>
                <p>
                  <strong className="text-emerald-300">Private Records Grounding:</strong> Margaret Vance (78), Lisinopril (10mg, 9am), Donepezil (5mg, 8pm), Emergency Contacts (Sarah Vance, Dr. Watson), and rolling adherence statistics.
                </p>
              </div>
            )}
          </div>

          {/* Voice Microphone Tile */}
          <div className="mt-5 text-center">
            <VoiceButton
              onTranscript={(transcript) => handleSendMessage(transcript)}
              isProcessing={isSending}
            />

            {/* Quick Prompt Chips */}
            <div className="flex flex-wrap items-center justify-center gap-2 mt-4">
              {quickPrompts.map((prompt, i) => (
                <button
                  key={i}
                  onClick={() => handleSendMessage(prompt)}
                  disabled={isSending}
                  className="px-3.5 py-1.5 rounded-full bg-slate-800/80 hover:bg-slate-700 text-sky-300 border border-slate-700 hover:border-sky-400 text-xs sm:text-sm font-bold transition cursor-pointer"
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Message Stream */}
        <div className="flex-1 overflow-y-auto space-y-4 mb-6 min-h-[300px]">
          {messages.length === 0 ? (
            <div className="text-center py-12 text-slate-400">
              <Bot className="w-12 h-12 text-sky-400 mx-auto mb-3" />
              <p className="text-xl font-bold text-white">Hello! How can I help you today?</p>
              <p className="text-base text-slate-400 mt-1">Tap the microphone or choose a quick question above.</p>
            </div>
          ) : (
            messages.map((m) => {
              const isUser = m.role === "USER";
              const modelLabel =
                m.active_model ||
                m.tool_calls?.active_model ||
                (activeMode === "extended" ? "Gemini 3.8 Live Extended Thinking" : "Gemini 3.8 Live");
              const thinkingTrace = m.thinking_trace || m.tool_calls?.thinking_trace;

              return (
                <div
                  key={m.id}
                  className={`flex items-start gap-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}
                >
                  <div
                    className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 text-white font-bold ${
                      isUser ? "bg-indigo-600" : activeMode === "extended" ? "bg-purple-600" : "bg-sky-600"
                    }`}
                  >
                    {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
                  </div>

                  <div
                    className={`max-w-[85%] rounded-2xl p-4 sm:p-5 text-base sm:text-lg font-medium leading-relaxed ${
                      isUser
                        ? "bg-indigo-600 text-white rounded-tr-none"
                        : "bg-slate-800 text-slate-100 border border-slate-700 rounded-tl-none shadow"
                    }`}
                  >
                    {/* Model Badge */}
                    {!isUser && (
                      <div className="flex items-center gap-1.5 text-[11px] font-extrabold uppercase tracking-wider mb-2 text-sky-300">
                        <Sparkles className="w-3.5 h-3.5" />
                        <span>{modelLabel}</span>
                      </div>
                    )}

                    {/* Thinking Trace (if Extended Thinking) */}
                    {!isUser && thinkingTrace && (
                      <div className="mb-3 p-3 rounded-xl bg-purple-950/40 border border-purple-800/60 text-xs text-purple-200">
                        <div className="font-bold flex items-center gap-1.5 mb-1 text-purple-300">
                          <Brain className="w-3.5 h-3.5" />
                          <span>Extended Reasoning Trace:</span>
                        </div>
                        <p className="whitespace-pre-line leading-relaxed">{thinkingTrace}</p>
                      </div>
                    )}

                    <p className="whitespace-pre-line">{m.content}</p>

                    {!isUser && (
                      <button
                        onClick={() => speakText(m.content)}
                        className="mt-3 inline-flex items-center gap-1.5 text-xs text-sky-300 hover:text-sky-200 font-bold bg-slate-700/60 hover:bg-slate-700 px-3 py-1.5 rounded-lg border border-slate-600 cursor-pointer"
                      >
                        <Volume2 className="w-4 h-4" />
                        <span>Read Out Loud</span>
                      </button>
                    )}
                  </div>
                </div>
              );
            })
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Text Input Fallback Bar */}
        <div className="bg-slate-900 border border-slate-800 p-2 sm:p-3 rounded-2xl flex items-center gap-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
            placeholder="Type your question or request..."
            className="flex-1 bg-transparent px-4 py-2.5 text-white text-base sm:text-lg placeholder-slate-500 focus:outline-none"
          />
          <button
            onClick={() => handleSendMessage()}
            disabled={!inputText.trim() || isSending}
            className="p-3.5 bg-sky-600 hover:bg-sky-500 disabled:opacity-50 text-white rounded-xl shadow cursor-pointer transition"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </main>

      {/* Full-Screen Live Talk Overlay */}
      {isLiveTalkOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/95 backdrop-blur-md flex flex-col items-center justify-between p-6 sm:p-10 animate-fade-in">
          {/* Header */}
          <div className="w-full max-w-xl flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-emerald-400 animate-ping" />
              <span className="text-sm font-bold uppercase tracking-wider text-emerald-400">
                Gemini Live Voice Active
              </span>
            </div>
            <button
              onClick={() => {
                if (typeof window !== "undefined" && "speechSynthesis" in window) {
                  window.speechSynthesis.cancel();
                }
                setIsLiveTalkOpen(false);
              }}
              className="p-2 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 cursor-pointer"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Central Animated Visualizer */}
          <div className="flex flex-col items-center justify-center my-auto text-center">
            <div className="relative mb-8">
              <div
                className={`w-40 h-40 rounded-full flex items-center justify-center text-white transition-all duration-300 ${
                  liveTalkStatus === "listening"
                    ? "bg-gradient-to-tr from-sky-500 to-emerald-500 shadow-2xl shadow-emerald-500/50 scale-105"
                    : liveTalkStatus === "thinking"
                    ? "bg-gradient-to-tr from-purple-600 to-indigo-600 shadow-2xl shadow-purple-500/50 animate-pulse"
                    : liveTalkStatus === "speaking"
                    ? "bg-gradient-to-tr from-sky-500 to-indigo-500 shadow-2xl shadow-sky-500/50 scale-105"
                    : "bg-slate-800 border-2 border-slate-700"
                }`}
              >
                {liveTalkStatus === "listening" ? (
                  <Mic className="w-20 h-20 animate-bounce" />
                ) : liveTalkStatus === "thinking" ? (
                  <Brain className="w-20 h-20 animate-spin" />
                ) : liveTalkStatus === "speaking" ? (
                  <Volume2 className="w-20 h-20 animate-pulse" />
                ) : (
                  <Bot className="w-20 h-20 text-slate-400" />
                )}
              </div>

              {/* Pulsing Outer Rings */}
              {liveTalkStatus === "listening" && (
                <div className="absolute inset-0 rounded-full border-4 border-emerald-400/50 animate-ping pointer-events-none" />
              )}
            </div>

            <h3 className="text-2xl sm:text-3xl font-black text-white mb-2">
              {liveTalkStatus === "listening"
                ? "Listening to you..."
                : liveTalkStatus === "thinking"
                ? "Reasoning with care context..."
                : liveTalkStatus === "speaking"
                ? "Speaking with Margaret..."
                : "Tap the button below to speak"}
            </h3>
            <p className="text-slate-400 text-sm max-w-sm mx-auto">
              {activeMode === "extended"
                ? "Operating in Extended Thinking mode with longitudinal clinical grounding."
                : "Operating in Live Conversational mode."}
            </p>
          </div>

          {/* Bottom Voice Triggers */}
          <div className="w-full max-w-md flex flex-col items-center gap-4">
            <button
              onClick={startLiveTalkSpeech}
              disabled={liveTalkStatus === "thinking"}
              className="w-full min-h-[64px] bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white text-xl font-black rounded-2xl shadow-xl flex items-center justify-center gap-3 cursor-pointer"
            >
              <Mic className="w-7 h-7" />
              <span>{liveTalkStatus === "listening" ? "Listening..." : "Tap to Speak"}</span>
            </button>

            <button
              onClick={() => {
                if (typeof window !== "undefined" && "speechSynthesis" in window) {
                  window.speechSynthesis.cancel();
                }
                setIsLiveTalkOpen(false);
              }}
              className="text-slate-400 hover:text-white text-sm font-bold"
            >
              Return to Text Chat
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
