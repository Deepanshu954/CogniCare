"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { User } from "@/types";
import { apiClient } from "@/lib/api";

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<User>;
  register: (data: any) => Promise<User>;
  logout: () => Promise<void>;
  quickLogin: (account: "margaret" | "sarah" | "arthur" | "emily") => Promise<User>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const savedToken = localStorage.getItem("cognicare_token");
    if (savedToken) {
      setToken(savedToken);
      fetchMe(savedToken);
    } else {
      setIsLoading(false);
    }
  }, []);

  const fetchMe = async (jwtToken: string) => {
    try {
      const res = await apiClient.get<User>("/auth/me", {
        headers: { Authorization: `Bearer ${jwtToken}` },
      });
      setUser(res.data);
    } catch (e) {
      console.warn("Session restore failed, clearing token.");
      localStorage.removeItem("cognicare_token");
      setToken(null);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string): Promise<User> => {
    const res = await apiClient.post("/auth/login", { email, password });
    const { access_token, user: loggedInUser } = res.data;
    localStorage.setItem("cognicare_token", access_token);
    setToken(access_token);
    setUser(loggedInUser);
    return loggedInUser;
  };

  const register = async (data: any): Promise<User> => {
    const res = await apiClient.post("/auth/register", data);
    const { access_token, user: registeredUser } = res.data;
    localStorage.setItem("cognicare_token", access_token);
    setToken(access_token);
    setUser(registeredUser);
    return registeredUser;
  };

  const logout = async () => {
    try {
      await apiClient.post("/auth/logout");
    } catch (_) {}
    localStorage.removeItem("cognicare_token");
    setToken(null);
    setUser(null);
  };

  const quickLogin = async (account: "margaret" | "sarah" | "arthur" | "emily"): Promise<User> => {
    const email = `${account}@example.com`;
    return login(email, "Password123!");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        login,
        register,
        logout,
        quickLogin,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
