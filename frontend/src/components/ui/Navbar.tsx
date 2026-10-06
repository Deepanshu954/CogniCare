"use client";

import React from "react";
import Link from "next/link";
import { useRouter, usePathname } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import { useUiScale } from "@/lib/uiScaleContext";
import { Brain, Heart, AlertCircle, LogOut, User as UserIcon } from "lucide-react";

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const { scale, setScale } = useUiScale();
  const router = useRouter();
  const pathname = usePathname();

  const handleLogout = async () => {
    await logout();
    router.push("/");
  };

  const isElderly = user?.role === "ELDERLY";

  return (
    <header className="bg-slate-900/90 backdrop-blur border-b border-slate-800 sticky top-0 z-40 px-4 sm:px-8 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Logo */}
        <Link
          href={isElderly ? "/app/my-day" : "/caregiver/dashboard"}
          className="flex items-center gap-3 group focus:ring-2 focus:ring-sky-400 rounded-lg p-1"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-sky-500/20">
            <Brain className="w-6 h-6" />
          </div>
          <div>
            <span className="text-2xl font-bold tracking-tight bg-gradient-to-r from-sky-400 to-indigo-300 bg-clip-text text-transparent">
              CogniCare
            </span>
            <span className="hidden sm:inline-block ml-2 text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
              {isElderly ? "Senior Companion" : "Caregiver Tower"}
            </span>
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="flex items-center gap-2 sm:gap-6">
          {user ? (
            <>
              {isElderly ? (
                <>
                  <Link
                    href="/app/my-day"
                    className={`text-lg font-medium px-3 py-1.5 rounded-lg transition-colors ${
                      pathname === "/app/my-day"
                        ? "bg-sky-500/20 text-sky-300 font-bold border border-sky-500/40"
                        : "text-slate-300 hover:text-white"
                    }`}
                  >
                    My Day
                  </Link>
                  <Link
                    href="/app/activities"
                    className={`text-lg font-medium px-3 py-1.5 rounded-lg transition-colors ${
                      pathname.startsWith("/app/activities")
                        ? "bg-sky-500/20 text-sky-300 font-bold border border-sky-500/40"
                        : "text-slate-300 hover:text-white"
                    }`}
                  >
                    Brain Games
                  </Link>
                  <Link
                    href="/app/assistant"
                    className={`text-lg font-medium px-3 py-1.5 rounded-lg transition-colors ${
                      pathname === "/app/assistant"
                        ? "bg-sky-500/20 text-sky-300 font-bold border border-sky-500/40"
                        : "text-slate-300 hover:text-white"
                    }`}
                  >
                    Assistant
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    href="/caregiver/dashboard"
                    className={`text-sm font-medium px-3 py-1.5 rounded-lg transition-colors ${
                      pathname === "/caregiver/dashboard"
                        ? "bg-indigo-500/20 text-indigo-300 font-bold border border-indigo-500/40"
                        : "text-slate-300 hover:text-white"
                    }`}
                  >
                    Dashboard
                  </Link>
                  <Link
                    href="/caregiver/reports"
                    className={`text-sm font-medium px-3 py-1.5 rounded-lg transition-colors ${
                      pathname.startsWith("/caregiver/reports")
                        ? "bg-indigo-500/20 text-indigo-300 font-bold border border-indigo-500/40"
                        : "text-slate-300 hover:text-white"
                    }`}
                  >
                    Reports
                  </Link>
                </>
              )}

                {/* User badge & Logout */}
                <div className="flex items-center gap-2 sm:gap-3 pl-2 sm:pl-4 border-l border-slate-800">
                  {/* UI Scale Switcher */}
                  <div className="flex items-center bg-slate-800/80 rounded-lg p-0.5 border border-slate-700/80 text-xs font-semibold" title="Display & Touch Sizing">
                    <button
                      type="button"
                      onClick={() => setScale("normal")}
                      className={`px-2 py-1 rounded-md transition ${
                        scale === "normal"
                          ? "bg-sky-600 text-white shadow-sm font-bold"
                          : "text-slate-400 hover:text-white"
                      }`}
                    >
                      Normal
                    </button>
                    <button
                      type="button"
                      onClick={() => setScale("large")}
                      className={`px-2 py-1 rounded-md transition ${
                        scale === "large"
                          ? "bg-sky-600 text-white shadow-sm font-bold"
                          : "text-slate-400 hover:text-white"
                      }`}
                    >
                      Large
                    </button>
                    <button
                      type="button"
                      onClick={() => setScale("extra-large")}
                      className={`px-2 py-1 rounded-md transition ${
                        scale === "extra-large"
                          ? "bg-sky-600 text-white shadow-sm font-bold"
                          : "text-slate-400 hover:text-white"
                      }`}
                    >
                      XL Senior
                    </button>
                  </div>

                  <span className="hidden lg:inline text-sm font-medium text-slate-300">
                    {user.profile?.display_name || user.email}
                  </span>
                  <button
                    onClick={handleLogout}
                    title="Sign out"
                    className="flex items-center gap-1.5 text-sm text-slate-400 hover:text-red-400 bg-slate-800/80 hover:bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700 transition-colors cursor-pointer"
                  >
                    <LogOut className="w-4 h-4" />
                    <span className="hidden sm:inline">Logout</span>
                  </button>
                </div>
            </>
          ) : (
            <div className="flex items-center gap-3">
              <Link
                href="/login"
                className="text-sm font-semibold text-slate-200 hover:text-white px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 transition"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="text-sm font-semibold text-white px-4 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 transition shadow-md shadow-sky-600/20"
              >
                Get Started
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
};
