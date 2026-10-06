"use client";

import React, { useState, useEffect } from "react";
import { CognitiveActivity, ActivitySession } from "@/types";
import { apiClient } from "@/lib/api";
import {
  CheckCircle2,
  RotateCcw,
  Trophy,
  ArrowRight,
  Eye,
  Compass,
  Sparkles,
  Clock,
  Palette,
  Layers,
} from "lucide-react";

interface ActivityPlayerProps {
  activity: CognitiveActivity;
  patientId: string;
  onFinish: () => void;
}

interface VisualItem {
  name: string;
  category: string;
  color: string;
  bgColor: string;
  icon: string; // SVG path or emoji symbol
  description: string;
}

interface QuestionItem {
  prompt: string;
  type: "visual_memory" | "clock_time" | "compass_direction" | "stroop_color" | "shape_sequence";
  options: string[];
  correct: string;
  // Game specific visuals
  displayWord?: string;
  displayColor?: string;
  clockHours?: number;
  clockMinutes?: number;
  compassBearing?: "North" | "South" | "East" | "West";
  sequenceItems?: { label: string; color: string; shape: string }[];
  studyCards?: VisualItem[];
}

export const ActivityPlayer: React.FC<ActivityPlayerProps> = ({
  activity,
  patientId,
  onFinish,
}) => {
  const [session, setSession] = useState<ActivitySession | null>(null);
  const [stepIndex, setStepIndex] = useState(0);
  const [selectedChoice, setSelectedChoice] = useState<string | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [finalScore, setFinalScore] = useState<any>(null);
  const [questionStartTime, setQuestionStartTime] = useState<number>(Date.now());
  const [isLoading, setIsLoading] = useState(false);

  // Memorization Study Phase for Memory Recall game
  const [isStudyingPhase, setIsStudyingPhase] = useState<boolean>(true);
  const [studyCountdown, setStudyCountdown] = useState<number>(5);

  // Initialize Session
  useEffect(() => {
    const initSession = async () => {
      try {
        const res = await apiClient.post<ActivitySession>(
          `/patients/${patientId}/activity-sessions`,
          { activity_id: activity.id, difficulty: 1 }
        );
        setSession(res.data);
        setQuestionStartTime(Date.now());
      } catch (e) {
        console.error("Failed to start cognitive activity session:", e);
      }
    };
    initSession();
  }, [activity.id, patientId]);

  // Visual Items Pool for Memory Game
  const memoryGallery: VisualItem[] = [
    {
      name: "Vintage Teapot",
      category: "Home & Hearth",
      color: "text-sky-400",
      bgColor: "bg-sky-950/60 border-sky-500/50",
      icon: "🫖",
      description: "Porcelain blue floral kettle",
    },
    {
      name: "Golden Sunflower",
      category: "Garden Bloom",
      color: "text-amber-400",
      bgColor: "bg-amber-950/60 border-amber-500/50",
      icon: "🌻",
      description: "Tall blooming garden flower",
    },
    {
      name: "Crimson Apple",
      category: "Fresh Orchard",
      color: "text-rose-400",
      bgColor: "bg-rose-950/60 border-rose-500/50",
      icon: "🍎",
      description: "Sweet crisp red orchard apple",
    },
  ];

  // Questions generator with rich visual artifacts
  const getQuestions = (): QuestionItem[] => {
    switch (activity.activity_type) {
      case "ATTENTION_STROOP":
        return [
          {
            prompt: "Look at the INK COLOR of this paint card. What color is the ink?",
            type: "stroop_color",
            displayWord: "BLUE",
            displayColor: "#EF4444", // Red ink
            options: ["Red", "Blue", "Green"],
            correct: "Red",
          },
          {
            prompt: "What is the actual INK COLOR of the word below?",
            type: "stroop_color",
            displayWord: "GREEN",
            displayColor: "#F59E0B", // Amber ink
            options: ["Amber", "Green", "Purple"],
            correct: "Amber",
          },
          {
            prompt: "What is the actual INK COLOR shown on this card?",
            type: "stroop_color",
            displayWord: "YELLOW",
            displayColor: "#0284C7", // Sky blue ink
            options: ["Yellow", "Sky Blue", "Pink"],
            correct: "Sky Blue",
          },
        ];

      case "WORD_SEQUENCE":
        return [
          {
            prompt: "Which shape and number appeared SECOND in the sequence card above?",
            type: "shape_sequence",
            sequenceItems: [
              { label: "4", color: "bg-red-500", shape: "● Circle" },
              { label: "8", color: "bg-indigo-500", shape: "◆ Diamond" },
              { label: "1", color: "bg-amber-500", shape: "★ Star" },
            ],
            options: ["4 (Circle)", "8 (Diamond)", "1 (Star)"],
            correct: "8 (Diamond)",
          },
          {
            prompt: "Which shape card was at the VERY END of this sequence?",
            type: "shape_sequence",
            sequenceItems: [
              { label: "3", color: "bg-emerald-500", shape: "▲ Triangle" },
              { label: "7", color: "bg-cyan-500", shape: "■ Square" },
              { label: "9", color: "bg-purple-500", shape: "● Circle" },
              { label: "2", color: "bg-rose-500", shape: "★ Star" },
            ],
            options: ["3 (Triangle)", "7 (Square)", "2 (Star)"],
            correct: "2 (Star)",
          },
        ];

      case "ORIENTATION_MATCH":
        return [
          {
            prompt: "Look at the analog clock face below. What time is it showing?",
            type: "clock_time",
            clockHours: 3,
            clockMinutes: 0,
            options: ["3:00", "6:00", "12:15"],
            correct: "3:00",
          },
          {
            prompt: "The compass needle is pointing toward the direction where the sun rises in the morning. Which direction is this?",
            type: "compass_direction",
            compassBearing: "East",
            options: ["East", "West", "North"],
            correct: "East",
          },
          {
            prompt: "Look at this second clock face. What time is the clock showing?",
            type: "clock_time",
            clockHours: 9,
            clockMinutes: 0,
            options: ["9:00", "1:00", "12:45"],
            correct: "9:00",
          },
        ];

      case "MEMORY_RECALL":
      default:
        return [
          {
            prompt: "Which picture card was shown alongside the Vintage Teapot?",
            type: "visual_memory",
            studyCards: memoryGallery,
            options: ["Golden Sunflower", "Brass Key", "Grand Piano"],
            correct: "Golden Sunflower",
          },
          {
            prompt: "Which of these delicious fruits was shown in the memory gallery?",
            type: "visual_memory",
            studyCards: memoryGallery,
            options: ["Crimson Apple", "Purple Grape", "Juicy Orange"],
            correct: "Crimson Apple",
          },
        ];
    }
  };

  const questions = getQuestions();
  const currentQ = questions[stepIndex] || questions[0];

  const handleSelectChoice = async (option: string) => {
    if (isAnswered || !session) return;
    const latency = Math.max(200, Date.now() - questionStartTime);
    const isCorrect = option === currentQ.correct;

    setSelectedChoice(option);
    setIsAnswered(true);

    try {
      await apiClient.post(
        `/patients/${patientId}/activity-sessions/${session.id}/answers`,
        {
          question_id: `q_${stepIndex}`,
          user_answer: option,
          is_correct: isCorrect,
          response_time_ms: latency,
        }
      );
    } catch (e) {
      console.error("Failed to record answer:", e);
    }
  };

  const handleNext = async () => {
    if (stepIndex + 1 < questions.length) {
      setStepIndex(stepIndex + 1);
      setSelectedChoice(null);
      setIsAnswered(false);
      setQuestionStartTime(Date.now());
    } else {
      setIsLoading(true);
      try {
        const res = await apiClient.post<ActivitySession>(
          `/patients/${patientId}/activity-sessions/${session!.id}/complete`
        );
        setFinalScore(res.data);
        setIsCompleted(true);
      } catch (e) {
        console.error("Failed to complete session:", e);
      } finally {
        setIsLoading(false);
      }
    }
  };

  // Helper component to render an interactive SVG Analog Clock Face
  const renderClock = (hours: number, minutes: number) => {
    const hourAngle = (hours % 12) * 30 + minutes * 0.5;
    const minuteAngle = minutes * 6;

    return (
      <div className="flex flex-col items-center justify-center my-6">
        <svg
          width="200"
          height="200"
          viewBox="0 0 200 200"
          className="drop-shadow-2xl filter"
        >
          {/* Outer Gold Rim & Dial */}
          <circle cx="100" cy="100" r="94" fill="#0F172A" stroke="#38BDF8" strokeWidth="8" />
          <circle cx="100" cy="100" r="88" fill="#1E293B" stroke="#0284C7" strokeWidth="2" />
          
          {/* Hour Markers (12, 3, 6, 9) */}
          <text x="100" y="32" textAnchor="middle" fill="#F8FAFC" fontSize="20" fontWeight="900">12</text>
          <text x="175" y="107" textAnchor="middle" fill="#F8FAFC" fontSize="20" fontWeight="900">3</text>
          <text x="100" y="180" textAnchor="middle" fill="#F8FAFC" fontSize="20" fontWeight="900">6</text>
          <text x="25" y="107" textAnchor="middle" fill="#F8FAFC" fontSize="20" fontWeight="900">9</text>

          {/* Hour Hand */}
          <line
            x1="100"
            y1="100"
            x2="100"
            y2="52"
            stroke="#F59E0B"
            strokeWidth="8"
            strokeLinecap="round"
            transform={`rotate(${hourAngle} 100 100)`}
          />

          {/* Minute Hand */}
          <line
            x1="100"
            y1="100"
            x2="100"
            y2="34"
            stroke="#38BDF8"
            strokeWidth="5"
            strokeLinecap="round"
            transform={`rotate(${minuteAngle} 100 100)`}
          />

          {/* Center Pin */}
          <circle cx="100" cy="100" r="7" fill="#E2E8F0" />
          <circle cx="100" cy="100" r="3" fill="#0F172A" />
        </svg>
        <span className="text-sm font-semibold text-slate-400 mt-2 flex items-center gap-1.5">
          <Clock className="w-4 h-4 text-amber-400" />
          <span>Look closely at the gold and blue clock hands</span>
        </span>
      </div>
    );
  };

  // Helper component to render an interactive Compass Rose SVG
  const renderCompass = (bearing: string) => {
    return (
      <div className="flex flex-col items-center justify-center my-6">
        <svg width="200" height="200" viewBox="0 0 200 200" className="drop-shadow-2xl">
          <circle cx="100" cy="100" r="92" fill="#0F172A" stroke="#F59E0B" strokeWidth="6" />
          <circle cx="100" cy="100" r="84" fill="#1E293B" stroke="#B45309" strokeWidth="2" strokeDasharray="4 4" />

          {/* Cardinal Directions */}
          <text x="100" y="32" textAnchor="middle" fill="#38BDF8" fontSize="22" fontWeight="900">N</text>
          <text x="175" y="108" textAnchor="middle" fill="#10B981" fontSize="22" fontWeight="900">E</text>
          <text x="100" y="180" textAnchor="middle" fill="#94A3B8" fontSize="22" fontWeight="900">S</text>
          <text x="25" y="108" textAnchor="middle" fill="#94A3B8" fontSize="22" fontWeight="900">W</text>

          {/* Glowing Compass Needle pointing East */}
          <polygon
            points="100,85 165,100 100,115"
            fill="#10B981"
            filter="drop-shadow(0 0 8px rgba(16,185,129,0.7))"
          />
          <polygon points="100,85 35,100 100,115" fill="#64748B" />

          <circle cx="100" cy="100" r="8" fill="#F8FAFC" />
        </svg>
        <span className="text-sm font-semibold text-emerald-400 mt-2 flex items-center gap-1.5">
          <Compass className="w-4 h-4" />
          <span>Needle pointing toward the green arrow ({bearing})</span>
        </span>
      </div>
    );
  };

  return (
    <div className="max-w-3xl mx-auto bg-slate-900 border-2 border-sky-500/40 rounded-3xl p-5 sm:p-8 md:p-10 shadow-2xl transition-all">
      {!isCompleted ? (
        <>
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-800 mb-6 gap-3">
            <div>
              <span className="text-xs uppercase tracking-wider text-sky-400 font-extrabold flex items-center gap-1.5 mb-1">
                <Sparkles className="w-3.5 h-3.5" />
                {activity.category}
              </span>
              <h2 className="text-2xl sm:text-3xl font-black text-white">
                {activity.title}
              </h2>
            </div>
            <div className="self-start sm:self-center px-4 py-1.5 rounded-full bg-slate-800 border border-slate-700 text-sm font-bold text-slate-300">
              Question {stepIndex + 1} of {questions.length}
            </div>
          </div>

          {/* Special Study Phase for Memory Game on first question */}
          {activity.activity_type === "MEMORY_RECALL" && stepIndex === 0 && isStudyingPhase ? (
            <div className="text-center py-4">
              <div className="inline-flex items-center gap-2 bg-indigo-500/20 border border-indigo-400 text-indigo-300 px-4 py-1.5 rounded-full text-sm font-bold mb-4">
                <Eye className="w-4 h-4" />
                <span>Memory Gallery — Look at these 3 picture cards carefully</span>
              </div>

              {/* Visual Picture Cards Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 my-6">
                {memoryGallery.map((card, idx) => (
                  <div
                    key={idx}
                    className={`p-6 rounded-2xl border-2 flex flex-col items-center justify-center text-center shadow-lg transition-transform hover:scale-105 ${card.bgColor}`}
                  >
                    <div className="text-6xl sm:text-7xl mb-3">{card.icon}</div>
                    <h4 className={`text-xl font-black ${card.color} mb-1`}>
                      {card.name}
                    </h4>
                    <span className="text-xs font-semibold text-slate-300">
                      {card.description}
                    </span>
                  </div>
                ))}
              </div>

              <p className="text-slate-400 text-base mb-6">
                Take your time to memorize these 3 picture cards. Whenever you are ready, press the button below to answer questions!
              </p>

              <button
                type="button"
                onClick={() => setIsStudyingPhase(false)}
                className="w-full sm:w-auto min-h-[64px] bg-sky-600 hover:bg-sky-500 text-white text-xl font-black px-10 py-4 rounded-2xl border-2 border-sky-400 shadow-xl flex items-center justify-center gap-2 mx-auto cursor-pointer"
              >
                <span>I&apos;m Ready to Answer!</span>
                <ArrowRight className="w-6 h-6" />
              </button>
            </div>
          ) : (
            /* Question Phase with Visual Display */
            <div className="my-6">
              <h3 className="text-xl sm:text-2xl font-extrabold text-white text-center mb-6 leading-relaxed">
                {currentQ.prompt}
              </h3>

              {/* 1. Stroop Visual Paint Splash Card */}
              {currentQ.type === "stroop_color" && currentQ.displayWord && (
                <div className="my-6 flex flex-col items-center justify-center">
                  <div
                    className="w-full max-w-sm py-8 px-6 rounded-3xl border-4 flex flex-col items-center justify-center shadow-2xl transition"
                    style={{
                      borderColor: currentQ.displayColor,
                      backgroundColor: "rgba(15, 23, 42, 0.9)",
                    }}
                  >
                    <Palette className="w-8 h-8 mb-2" style={{ color: currentQ.displayColor }} />
                    <span
                      className="text-6xl sm:text-7xl font-black tracking-widest uppercase drop-shadow-md"
                      style={{ color: currentQ.displayColor }}
                    >
                      {currentQ.displayWord}
                    </span>
                    <span className="text-xs uppercase font-bold text-slate-400 mt-3">
                      Ink Color Card
                    </span>
                  </div>
                </div>
              )}

              {/* 2. Visual Clock Face */}
              {currentQ.type === "clock_time" &&
                currentQ.clockHours !== undefined &&
                currentQ.clockMinutes !== undefined &&
                renderClock(currentQ.clockHours, currentQ.clockMinutes)}

              {/* 3. Visual Compass */}
              {currentQ.type === "compass_direction" &&
                currentQ.compassBearing &&
                renderCompass(currentQ.compassBearing)}

              {/* 4. Sequence Shape Cards */}
              {currentQ.type === "shape_sequence" && currentQ.sequenceItems && (
                <div className="flex flex-wrap items-center justify-center gap-3 sm:gap-4 my-6">
                  {currentQ.sequenceItems.map((seq, idx) => (
                    <div
                      key={idx}
                      className={`p-4 sm:p-5 rounded-2xl flex flex-col items-center justify-center text-white border-2 border-white/20 shadow-lg min-w-[90px] sm:min-w-[110px] ${seq.color}`}
                    >
                      <span className="text-3xl sm:text-4xl font-black mb-1">{seq.label}</span>
                      <span className="text-xs font-bold text-white/90">{seq.shape}</span>
                    </div>
                  ))}
                </div>
              )}

              {/* Options Grid */}
              <div className="grid grid-cols-1 gap-3.5 max-w-md mx-auto mt-6">
                {currentQ.options.map((opt, i) => {
                  const isSelected = selectedChoice === opt;
                  return (
                    <button
                      key={i}
                      onClick={() => handleSelectChoice(opt)}
                      disabled={isAnswered}
                      className={`w-full min-h-[64px] text-lg sm:text-xl font-black py-4 px-6 rounded-2xl border-2 transition-all transform active:scale-98 cursor-pointer flex items-center justify-between ${
                        isSelected
                          ? isSelected && opt === currentQ.correct
                            ? "bg-emerald-600 border-emerald-400 text-white shadow-lg shadow-emerald-900/40"
                            : "bg-amber-600 border-amber-400 text-white"
                          : "bg-slate-800 hover:bg-slate-700 border-slate-600 text-slate-100 hover:border-sky-400"
                      }`}
                    >
                      <span>{opt}</span>
                      {isSelected && opt === currentQ.correct && (
                        <CheckCircle2 className="w-6 h-6 text-emerald-200" />
                      )}
                    </button>
                  );
                })}
              </div>

              {/* Next Question / Finish Button */}
              {isAnswered && (
                <div className="pt-6 border-t border-slate-800 flex justify-center mt-6">
                  <button
                    onClick={handleNext}
                    disabled={isLoading}
                    className="w-full sm:w-auto min-w-[220px] min-h-[64px] bg-sky-600 hover:bg-sky-500 text-white text-xl sm:text-2xl font-black px-8 py-4 rounded-2xl border-2 border-sky-400 shadow-xl flex items-center justify-center gap-3 transition-transform active:scale-95 cursor-pointer"
                  >
                    <span>{stepIndex + 1 < questions.length ? "Next Question" : "Finish Game"}</span>
                    <ArrowRight className="w-6 h-6" />
                  </button>
                </div>
              )}
            </div>
          )}
        </>
      ) : (
        /* Completion View */
        <div className="text-center py-6">
          <div className="w-24 h-24 bg-gradient-to-tr from-emerald-500 to-sky-500 rounded-3xl flex items-center justify-center text-white mx-auto mb-6 shadow-xl shadow-emerald-500/20">
            <Trophy className="w-14 h-14" />
          </div>

          <h2 className="text-3xl sm:text-4xl font-black text-white mb-3">
            Exercise Complete!
          </h2>
          <p className="text-xl text-slate-300 max-w-md mx-auto mb-6">
            {finalScore?.feedback_message || "You completed this daily mind exercise wonderfully!"}
          </p>

          <div className="grid grid-cols-2 gap-4 max-w-sm mx-auto mb-8 bg-slate-800/80 p-5 rounded-2xl border border-slate-700">
            <div>
              <div className="text-sm font-semibold text-slate-400">Score</div>
              <div className="text-3xl font-black text-sky-400">
                {finalScore?.total_score || 85}
              </div>
            </div>
            <div>
              <div className="text-sm font-semibold text-slate-400">Accuracy</div>
              <div className="text-3xl font-black text-emerald-400">
                {finalScore?.accuracy_rate || 100}%
              </div>
            </div>
          </div>

          <button
            onClick={onFinish}
            className="min-h-[64px] bg-sky-600 hover:bg-sky-500 text-white text-xl sm:text-2xl font-black px-10 py-4 rounded-2xl border-2 border-sky-300 shadow-xl cursor-pointer"
          >
            Back to Activities
          </button>
        </div>
      )}
    </div>
  );
};
