/* eslint-disable @next/next/no-img-element */
"use client";

import React, { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import { Navbar } from "@/components/ui/Navbar";
import { VoiceButton } from "@/components/elderly/VoiceButton";
import { Message, Conversation, ApiKeyStatus } from "@/types";
import { apiClient } from "@/lib/api";
import {
  Send,
  Volume2,
  VolumeX,
  Square,
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
  Paperclip,
  FileText,
  Key,
  CheckCircle2,
  AlertCircle,
  UploadCloud,
  ImageIcon,
} from "lucide-react";

export default function AssistantPage() {
  const { user, isLoading: isAuthLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthLoading && !user) {
      router.push("/login");
    }
  }, [user, isAuthLoading, router]);

  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [activeMode, setActiveMode] = useState<"normal" | "extended">("normal");
  const [showContextDetails, setShowContextDetails] = useState(false);
  const [isLiveTalkOpen, setIsLiveTalkOpen] = useState(false);
  const [liveTalkStatus, setLiveTalkStatus] = useState<"idle" | "listening" | "thinking" | "speaking">("idle");
  const [talkAloud, setTalkAloud] = useState<boolean>(false);
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);
  const [speakingMessageId, setSpeakingMessageId] = useState<string | null>(null);

  // File Attachment & Drag and Drop State
  const [pendingAttachment, setPendingAttachment] = useState<{
    name: string;
    type: string;
    size: number;
    data_url: string;
  } | null>(null);
  const [isDraggingOver, setIsDraggingOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Gemini API Key State
  const [apiKeyStatus, setApiKeyStatus] = useState<ApiKeyStatus | null>(null);
  const [apiKeyModalOpen, setApiKeyModalOpen] = useState(false);
  const [apiKeyInput, setApiKeyInput] = useState("");
  const [isSavingKey, setIsSavingKey] = useState(false);
  const [keyMessage, setKeyMessage] = useState<{ text: string; isError: boolean } | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const patientId = user?.patient_profile?.id;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedTalkAloud = localStorage.getItem("cognicare_talk_aloud");
      if (savedTalkAloud !== null) {
        setTalkAloud(savedTalkAloud === "true");
      }
    }
  }, []);

  const toggleTalkAloud = () => {
    const nextVal = !talkAloud;
    setTalkAloud(nextVal);
    if (typeof window !== "undefined") {
      localStorage.setItem("cognicare_talk_aloud", String(nextVal));
    }
    if (!nextVal) {
      stopSpeaking();
    }
  };

  const stopSpeaking = () => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    setIsSpeaking(false);
    setSpeakingMessageId(null);
    if (liveTalkStatus === "speaking") {
      setLiveTalkStatus("idle");
    }
  };

  // Load Conversation & API Key Status
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
      try {
        const keyRes = await apiClient.get<ApiKeyStatus>(`/patients/${patientId}/assistant/api-key`);
        setApiKeyStatus(keyRes.data);
      } catch (e) {
        console.error("Failed to fetch API key status:", e);
      }
    };
    initConversation();
  }, [patientId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileSelected = (file: File) => {
    if (!file) return;
    if (file.size > 15 * 1024 * 1024) {
      alert("File size exceeds 15MB limit.");
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      setPendingAttachment({
        name: file.name,
        type: file.type || (file.name.endsWith(".pdf") ? "application/pdf" : "image/png"),
        size: file.size,
        data_url: result,
      });
    };
    reader.readAsDataURL(file);
  };

  const handleSaveApiKey = async () => {
    if (!apiKeyInput.trim() || !patientId) return;
    setIsSavingKey(true);
    setKeyMessage(null);
    try {
      const res = await apiClient.post<ApiKeyStatus>(
        `/patients/${patientId}/assistant/api-key`,
        { api_key: apiKeyInput.trim() }
      );
      setApiKeyStatus(res.data);
      if (res.data.is_valid) {
        setKeyMessage({ text: "API Key verified successfully! Gemini 2.0 Live is connected.", isError: false });
        setTimeout(() => setApiKeyModalOpen(false), 1600);
      } else {
        setKeyMessage({ text: res.data.status_detail || "Google rejected this key. Check that it starts with AIzaSy...", isError: true });
      }
    } catch (e: any) {
      setKeyMessage({ text: e.response?.data?.message || "Failed to configure key.", isError: true });
    } finally {
      setIsSavingKey(false);
    }
  };

  const handleSendMessage = async (textToSend?: string) => {
    const text = textToSend !== undefined ? textToSend : inputText;
    if ((!text.trim() && !pendingAttachment) || !conversation || !patientId || isSending) return;

    // Stop any ongoing speech before processing new request
    stopSpeaking();

    setIsSending(true);
    setInputText("");
    if (isLiveTalkOpen) setLiveTalkStatus("thinking");

    const currentAttachment = pendingAttachment;
    setPendingAttachment(null);

    // Optimistic user message bubble
    const tempUserMsg: Message = {
      id: `temp_${Date.now()}`,
      conversation_id: conversation.id,
      role: "USER",
      content: text.trim() || (currentAttachment ? `Attached: ${currentAttachment.name}` : ""),
      attachment_name: currentAttachment?.name,
      attachment_type: currentAttachment?.type,
      attachment_data_url: currentAttachment?.data_url,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    try {
      const payload: any = {
        content: text.trim() || (currentAttachment ? `Please explain this ${currentAttachment.name}` : ""),
        mode: activeMode,
      };
      if (currentAttachment) {
        payload.attachment_name = currentAttachment.name;
        payload.attachment_type = currentAttachment.type;
        payload.attachment_data_url = currentAttachment.data_url;
      }
      const res = await apiClient.post<Message>(
        `/patients/${patientId}/conversations/${conversation.id}/messages`,
        payload
      );
      setMessages((prev) => [...prev, res.data]);

      // Only speak aloud if user has explicitly enabled Talk Aloud OR is in Live Talk mode
      if (talkAloud || isLiveTalkOpen) {
        if (isLiveTalkOpen) {
          setLiveTalkStatus("speaking");
        }
        speakText(res.data.content, res.data.id, () => {
          if (isLiveTalkOpen) setLiveTalkStatus("idle");
        });
      } else {
        if (isLiveTalkOpen) setLiveTalkStatus("idle");
      }
    } catch (e: any) {
      console.error("Message send error:", e);
      if (isLiveTalkOpen) setLiveTalkStatus("idle");
    } finally {
      setIsSending(false);
    }
  };

  const speakText = (text: string, messageId?: string, onEnd?: () => void) => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(true);
      if (messageId) setSpeakingMessageId(messageId);
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.95; // Gentle pace for senior comfort
      utterance.onend = () => {
        setIsSpeaking(false);
        setSpeakingMessageId(null);
        if (onEnd) onEnd();
      };
      utterance.onerror = () => {
        setIsSpeaking(false);
        setSpeakingMessageId(null);
        if (onEnd) onEnd();
      };
      window.speechSynthesis.speak(utterance);
    } else {
      setIsSpeaking(false);
      setSpeakingMessageId(null);
      if (onEnd) onEnd();
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

  const quickPrompts = pendingAttachment
    ? [
        "Explain this prescription",
        "What are the dosage instructions?",
        "Save to my medical records",
        "Is this document normal?",
      ]
    : [
        "What do I have today?",
        "Did I take my morning pills?",
        "What is the speed of light?",
        "Tell me a calm story",
      ];

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-6 flex flex-col">
        {/* Model Mode Switcher & Live Talk Banner */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-4 sm:p-6 mb-6 shadow-xl">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pb-4 border-b border-slate-800">
            {/* Controls Bar: AI Mode + Talk Aloud Toggle + Stop Speaking + Live Talk */}
            <div className="flex flex-wrap items-center gap-3">
              {/* Mode Selector */}
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400 mr-1 hidden sm:inline">
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

              {/* Talk Aloud Toggle Button */}
              <button
                type="button"
                onClick={toggleTalkAloud}
                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-2xl text-xs sm:text-sm font-bold border transition cursor-pointer ${
                  talkAloud
                    ? "bg-emerald-950/80 border-emerald-500 text-emerald-300 shadow-sm"
                    : "bg-slate-950 border-slate-800 text-slate-400 hover:text-white"
                }`}
                title="Toggle automatic spoken voice responses"
                aria-label={talkAloud ? "Voice read aloud is enabled. Tap to mute." : "Voice read aloud is disabled. Tap to enable."}
              >
                {talkAloud ? (
                  <Volume2 className="w-4 h-4 text-emerald-400" />
                ) : (
                  <VolumeX className="w-4 h-4 text-slate-500" />
                )}
                <span>{talkAloud ? "Talk Aloud: ON" : "Talk Aloud: OFF"}</span>
              </button>

              {/* Gemini API Key Configuration Pill */}
              <button
                type="button"
                onClick={() => {
                  setKeyMessage(null);
                  setApiKeyModalOpen(true);
                }}
                className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-2xl text-xs sm:text-sm font-bold border transition cursor-pointer ${
                  apiKeyStatus?.is_valid
                    ? "bg-emerald-950/80 border-emerald-500 text-emerald-300"
                    : "bg-amber-950/80 border-amber-500 text-amber-300 hover:bg-amber-900"
                }`}
                title={apiKeyStatus?.status_detail || "Configure Google Gemini API Key"}
              >
                <Key className="w-4 h-4" />
                <span>{apiKeyStatus?.is_valid ? "API Connected" : "Set Gemini Key"}</span>
              </button>

              {/* Global Stop Speaking Button (Shown when TTS is active) */}
              {isSpeaking && (
                <button
                  type="button"
                  onClick={stopSpeaking}
                  className="flex items-center gap-2 px-3.5 py-1.5 bg-rose-600 hover:bg-rose-500 text-white text-xs sm:text-sm font-black rounded-2xl shadow-lg shadow-rose-900/50 animate-pulse cursor-pointer transition"
                  title="Stop assistant speech immediately"
                  aria-label="Stop speaking"
                >
                  <Square className="w-4 h-4 fill-current" />
                  <span>Stop Speaking</span>
                </button>
              )}
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
              <span>Live Talk Mode</span>
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

        {/* Message Stream with Drag & Drop Zone */}
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setIsDraggingOver(true);
          }}
          onDragLeave={() => setIsDraggingOver(false)}
          onDrop={(e) => {
            e.preventDefault();
            setIsDraggingOver(false);
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
              handleFileSelected(e.dataTransfer.files[0]);
            }
          }}
          className={`flex-1 overflow-y-auto space-y-4 mb-4 min-h-[320px] p-4 rounded-3xl transition relative ${
            isDraggingOver
              ? "bg-emerald-950/40 border-2 border-dashed border-emerald-400"
              : "bg-slate-950/40 border border-slate-900"
          }`}
        >
          {isDraggingOver && (
            <div className="absolute inset-0 z-30 bg-slate-950/90 backdrop-blur-sm flex flex-col items-center justify-center text-center p-6 rounded-3xl animate-fade-in pointer-events-none">
              <UploadCloud className="w-16 h-16 text-emerald-400 mb-3 animate-bounce" />
              <h3 className="text-xl font-bold text-white mb-1">Drop Medical File Here</h3>
              <p className="text-slate-300 text-sm max-w-sm">
                Drop your prescription PDF or medical image to inspect with CogniCare AI
              </p>
            </div>
          )}

          {messages.length === 0 ? (
            <div className="text-center py-12 text-slate-400">
              <Bot className="w-12 h-12 text-sky-400 mx-auto mb-3" />
              <p className="text-xl font-bold text-white">Hello! How can I help you today?</p>
              <p className="text-base text-slate-400 mt-1">Tap the microphone, type a question, or attach a prescription.</p>
            </div>
          ) : (
            messages.map((m) => {
              const isUser = m.role === "USER";
              const modelLabel =
                m.active_model ||
                m.tool_calls?.active_model ||
                (activeMode === "extended" ? "Gemini 3.8 Live Extended Thinking" : "Gemini 3.8 Live");
              const thinkingTrace = m.thinking_trace || m.tool_calls?.thinking_trace;
              const attachmentDataUrl = m.attachment_data_url || m.tool_calls?.attachment?.data_url;
              const attachmentName = m.attachment_name || m.tool_calls?.attachment?.name;
              const attachmentType = m.attachment_type || m.tool_calls?.attachment?.type;

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

                    {/* Attached File Card inside User Message */}
                    {isUser && (attachmentDataUrl || attachmentName) && (
                      <div className="mb-3">
                        {attachmentDataUrl && (attachmentType?.startsWith("image/") || attachmentDataUrl.startsWith("data:image")) ? (
                          <div className="overflow-hidden rounded-xl border border-white/20 shadow-md max-w-xs">
                            <img
                              src={attachmentDataUrl}
                              alt={attachmentName || "Uploaded medical image"}
                              className="w-full max-h-48 object-cover"
                            />
                            <div className="bg-black/60 p-1.5 px-2.5 text-[11px] text-slate-200 flex items-center justify-between">
                              <span className="truncate">{attachmentName || "Prescription Scan"}</span>
                              <span className="text-[10px] text-emerald-300 uppercase font-bold">Image</span>
                            </div>
                          </div>
                        ) : (
                          <div className="flex items-center gap-2.5 p-3 rounded-xl bg-indigo-700/90 border border-indigo-400/40 text-xs text-white max-w-xs">
                            <FileText className="w-6 h-6 text-indigo-200 flex-shrink-0" />
                            <div className="min-w-0 flex-1">
                              <span className="font-bold truncate block">{attachmentName || "Medical_Document.pdf"}</span>
                              <span className="text-[10px] text-indigo-200">PDF Document</span>
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    <p className="whitespace-pre-line">{m.content}</p>

                    {!isUser && (
                      <div className="mt-3 flex items-center gap-2">
                        {isSpeaking && speakingMessageId === m.id ? (
                          <button
                            type="button"
                            onClick={stopSpeaking}
                            className="inline-flex items-center gap-1.5 text-xs text-rose-300 hover:text-white font-bold bg-rose-950/80 hover:bg-rose-900 px-3 py-1.5 rounded-lg border border-rose-600 cursor-pointer animate-pulse"
                            aria-label="Stop reading response aloud"
                          >
                            <Square className="w-3.5 h-3.5 fill-current" />
                            <span>Stop Speaking</span>
                          </button>
                        ) : (
                          <button
                            type="button"
                            onClick={() => speakText(m.content, m.id)}
                            className="inline-flex items-center gap-1.5 text-xs text-sky-300 hover:text-sky-200 font-bold bg-slate-700/60 hover:bg-slate-700 px-3 py-1.5 rounded-lg border border-slate-600 cursor-pointer"
                            aria-label="Read response aloud"
                          >
                            <Volume2 className="w-3.5 h-3.5" />
                            <span>Read Out Loud</span>
                          </button>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              );
            })
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Attachment Pending Preview Bar */}
        {pendingAttachment && (
          <div className="mb-2 p-2.5 px-3.5 rounded-2xl bg-slate-900 border border-slate-700 flex items-center justify-between gap-3 animate-fade-in shadow-lg">
            <div className="flex items-center gap-3 min-w-0">
              {pendingAttachment.type.startsWith("image/") ? (
                <img
                  src={pendingAttachment.data_url}
                  alt="Attachment preview"
                  className="w-10 h-10 rounded-xl object-cover border border-slate-600 shadow-sm"
                />
              ) : (
                <div className="w-10 h-10 rounded-xl bg-red-950/80 border border-red-700 flex items-center justify-center text-red-300">
                  <FileText className="w-6 h-6" />
                </div>
              )}
              <div className="min-w-0">
                <span className="font-bold text-white text-sm block truncate">
                  {pendingAttachment.name}
                </span>
                <span className="text-xs text-emerald-400 font-semibold">
                  Ready to send • {(pendingAttachment.size / 1024).toFixed(1)} KB
                </span>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setPendingAttachment(null)}
              className="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition"
              title="Remove attached file"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Text Input Bar with Paperclip File Ingestion */}
        <div className="bg-slate-900 border border-slate-800 p-2 sm:p-3 rounded-2xl flex items-center gap-2">
          {/* Hidden File Picker Input */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => {
              if (e.target.files && e.target.files[0]) {
                handleFileSelected(e.target.files[0]);
              }
            }}
            accept=".pdf,image/png,image/jpeg,image/jpg,image/webp"
            className="hidden"
          />

          {/* Paperclip Button */}
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="p-3 text-slate-400 hover:text-sky-300 hover:bg-slate-800 rounded-xl transition cursor-pointer flex-shrink-0"
            title="Attach doctor prescription or medical image"
            aria-label="Upload file"
          >
            <Paperclip className="w-5 h-5" />
          </button>

          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
            placeholder={
              pendingAttachment
                ? `Ask about ${pendingAttachment.name}... (or tap send)`
                : "Type your question or request..."
            }
            className="flex-1 bg-transparent px-2 sm:px-3 py-2.5 text-white text-base sm:text-lg placeholder-slate-500 focus:outline-none"
          />

          {isSpeaking && (
            <button
              type="button"
              onClick={stopSpeaking}
              className="p-3 bg-rose-600 hover:bg-rose-500 text-white rounded-xl shadow cursor-pointer transition flex items-center gap-1.5 px-3.5 font-bold text-sm animate-pulse"
              title="Stop assistant speaking"
              aria-label="Stop assistant speaking"
            >
              <Square className="w-4 h-4 fill-current" />
              <span className="hidden sm:inline">Stop</span>
            </button>
          )}

          <button
            onClick={() => handleSendMessage()}
            disabled={(!inputText.trim() && !pendingAttachment) || isSending}
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
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={toggleTalkAloud}
                className="px-3 py-1.5 rounded-xl bg-slate-800 text-xs font-bold text-slate-300 hover:text-white flex items-center gap-1.5 transition"
                aria-label="Toggle voice output"
              >
                {talkAloud ? <Volume2 className="w-4 h-4 text-emerald-400" /> : <VolumeX className="w-4 h-4 text-slate-400" />}
                <span>{talkAloud ? "Voice ON" : "Voice Muted"}</span>
              </button>
              <button
                onClick={() => {
                  stopSpeaking();
                  setIsLiveTalkOpen(false);
                }}
                className="p-2 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 cursor-pointer"
                aria-label="Close Live Talk"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
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
                    ? "bg-gradient-to-tr from-rose-500 to-amber-500 shadow-2xl shadow-rose-500/50 scale-105"
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
              {liveTalkStatus === "speaking" && (
                <div className="absolute inset-0 rounded-full border-4 border-rose-400/50 animate-ping pointer-events-none" />
              )}
            </div>

            <h3 className="text-2xl sm:text-3xl font-black text-white mb-2">
              {liveTalkStatus === "listening"
                ? "Listening to you..."
                : liveTalkStatus === "thinking"
                ? "Thinking calmly..."
                : liveTalkStatus === "speaking"
                ? "Speaking aloud..."
                : "Tap the button below to speak"}
            </h3>
            <p className="text-slate-400 text-sm max-w-sm mx-auto">
              {activeMode === "extended"
                ? "Extended Thinking mode active."
                : "Live Conversational mode active."}
            </p>
          </div>

          {/* Bottom Voice Triggers & Stop Speaking Controls */}
          <div className="w-full max-w-md flex flex-col items-center gap-3">
            {liveTalkStatus === "speaking" ? (
              <button
                onClick={stopSpeaking}
                className="w-full min-h-[64px] bg-rose-600 hover:bg-rose-500 text-white text-xl font-black rounded-2xl shadow-xl shadow-rose-900/50 flex items-center justify-center gap-3 cursor-pointer animate-pulse transition"
                aria-label="Stop speaking response"
              >
                <Square className="w-7 h-7 fill-current" />
                <span>Stop Speaking</span>
              </button>
            ) : (
              <button
                onClick={startLiveTalkSpeech}
                disabled={liveTalkStatus === "thinking"}
                className="w-full min-h-[64px] bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white text-xl font-black rounded-2xl shadow-xl flex items-center justify-center gap-3 cursor-pointer transition"
              >
                <Mic className="w-7 h-7" />
                <span>{liveTalkStatus === "listening" ? "Listening..." : "Tap to Speak"}</span>
              </button>
            )}

            <button
              onClick={() => {
                stopSpeaking();
                setIsLiveTalkOpen(false);
              }}
              className="text-slate-400 hover:text-white text-sm font-bold transition py-2"
            >
              Close & Return to Chat
            </button>
          </div>
        </div>
      )}

      {/* Gemini API Key Configuration Modal */}
      {apiKeyModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-lg w-full p-6 shadow-2xl animate-fade-in">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
              <div className="flex items-center gap-2.5 text-white font-black text-lg">
                <Key className="w-5 h-5 text-sky-400" />
                <span>Google Gemini API Configuration</span>
              </div>
              <button
                type="button"
                onClick={() => setApiKeyModalOpen(false)}
                className="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-slate-300 text-sm mb-4 leading-relaxed">
              Connect CogniCare to live <strong>Google Gemini 2.0 Flash</strong> for real-time generative responses.
            </p>

            <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 mb-4 text-xs space-y-2 text-slate-300">
              <div className="flex items-center justify-between font-bold">
                <span className="text-slate-400">Current Status:</span>
                <span className={apiKeyStatus?.is_valid ? "text-emerald-400" : "text-amber-400"}>
                  {apiKeyStatus?.is_valid ? "● Live AI Connected" : "○ Local Offline Engine"}
                </span>
              </div>
              {apiKeyStatus?.masked_key && (
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Key:</span>
                  <span className="font-mono text-slate-300">{apiKeyStatus.masked_key}</span>
                </div>
              )}
              <div className="text-[11px] text-slate-400 pt-1 border-t border-slate-800">
                {apiKeyStatus?.status_detail}
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                Enter Gemini API Key (starts with AIzaSy...)
              </label>
              <input
                type="password"
                value={apiKeyInput}
                onChange={(e) => setApiKeyInput(e.target.value)}
                placeholder="AIzaSy..."
                className="w-full bg-slate-950 border border-slate-800 focus:border-sky-500 rounded-xl px-4 py-3 text-white font-mono text-sm focus:outline-none"
              />
              <p className="text-[11px] text-slate-500 mt-2">
                Get a free API key at{" "}
                <a
                  href="https://aistudio.google.com/app/apikey"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sky-400 underline hover:text-sky-300"
                >
                  aistudio.google.com/app/apikey
                </a>
              </p>
            </div>

            {keyMessage && (
              <div
                className={`p-3 rounded-xl mb-4 text-xs font-medium flex items-center gap-2 ${
                  keyMessage.isError
                    ? "bg-rose-950/70 border border-rose-800 text-rose-300"
                    : "bg-emerald-950/70 border border-emerald-800 text-emerald-300"
                }`}
              >
                {keyMessage.isError ? <AlertCircle className="w-4 h-4 flex-shrink-0" /> : <CheckCircle2 className="w-4 h-4 flex-shrink-0" />}
                <span>{keyMessage.text}</span>
              </div>
            )}

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setApiKeyModalOpen(false)}
                className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-bold transition"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleSaveApiKey}
                disabled={!apiKeyInput.trim() || isSavingKey}
                className="px-5 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 disabled:opacity-50 text-white text-sm font-bold transition flex items-center gap-2 shadow-lg shadow-sky-900/40"
              >
                {isSavingKey ? "Verifying..." : "Verify & Save Key"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
