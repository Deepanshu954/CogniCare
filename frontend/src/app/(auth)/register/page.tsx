"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/authContext";
import { Navbar } from "@/components/ui/Navbar";
import { Brain, Lock, Mail, User, Phone, ArrowRight } from "lucide-react";

export default function RegisterPage() {
  const { register } = useAuth();
  const router = useRouter();

  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("ELDERLY");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      const user = await register({
        display_name: displayName,
        email,
        password,
        role,
        phone_number: phoneNumber,
      });
      if (user.role === "ELDERLY") {
        router.push("/app/my-day");
      } else {
        router.push("/caregiver/dashboard");
      }
    } catch (err: any) {
      setError(err.message || "Registration failed.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar />

      <div className="flex-1 flex items-center justify-center p-4">
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-10 max-w-lg w-full shadow-2xl">
          <div className="text-center mb-8">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white mx-auto mb-3 shadow-lg shadow-sky-500/20">
              <Brain className="w-7 h-7" />
            </div>
            <h1 className="text-3xl font-extrabold text-white">Create Account</h1>
            <p className="text-sm text-slate-400 mt-1">Get started with CogniCare support</p>
          </div>

          {error && (
            <div className="mb-6 p-4 rounded-xl bg-rose-950/60 border border-rose-800 text-rose-300 text-sm font-semibold">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Role Selector */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
                I am using this as:
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setRole("ELDERLY")}
                  className={`py-3 px-4 rounded-xl font-bold text-sm border-2 transition ${
                    role === "ELDERLY"
                      ? "bg-sky-600/30 border-sky-400 text-sky-300"
                      : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-600"
                  }`}
                >
                  Senior / Elderly User
                </button>
                <button
                  type="button"
                  onClick={() => setRole("CAREGIVER")}
                  className={`py-3 px-4 rounded-xl font-bold text-sm border-2 transition ${
                    role === "CAREGIVER"
                      ? "bg-indigo-600/30 border-indigo-400 text-indigo-300"
                      : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-600"
                  }`}
                >
                  Family Caregiver
                </button>
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1.5">
                Full Name
              </label>
              <div className="relative">
                <User className="w-5 h-5 text-slate-500 absolute left-3.5 top-3.5" />
                <input
                  type="text"
                  required
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="e.g. Margaret Connor"
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl py-3 pl-11 pr-4 text-white text-base focus:outline-none focus:border-sky-400"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1.5">
                Email Address
              </label>
              <div className="relative">
                <Mail className="w-5 h-5 text-slate-500 absolute left-3.5 top-3.5" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl py-3 pl-11 pr-4 text-white text-base focus:outline-none focus:border-sky-400"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock className="w-5 h-5 text-slate-500 absolute left-3.5 top-3.5" />
                <input
                  type="password"
                  required
                  minLength={8}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="At least 8 characters"
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl py-3 pl-11 pr-4 text-white text-base focus:outline-none focus:border-sky-400"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1.5">
                Phone Number (Optional)
              </label>
              <div className="relative">
                <Phone className="w-5 h-5 text-slate-500 absolute left-3.5 top-3.5" />
                <input
                  type="tel"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  placeholder="+1 (555) 000-0000"
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl py-3 pl-11 pr-4 text-white text-base focus:outline-none focus:border-sky-400"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full min-h-[52px] bg-sky-600 hover:bg-sky-500 text-white font-bold rounded-xl text-lg shadow-lg shadow-sky-600/30 transition-transform active:scale-98 flex items-center justify-center gap-2 cursor-pointer mt-6"
            >
              <span>{isLoading ? "Creating Account..." : "Complete Registration"}</span>
              <ArrowRight className="w-5 h-5" />
            </button>
          </form>

          <p className="text-center text-sm text-slate-400 mt-6">
            Already have an account?{" "}
            <Link href="/login" className="text-sky-400 hover:underline font-bold">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
