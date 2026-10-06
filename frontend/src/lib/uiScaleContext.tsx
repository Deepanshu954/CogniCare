"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

export type UiScale = "normal" | "large" | "extra-large";

interface UiScaleContextType {
  scale: UiScale;
  setScale: (scale: UiScale) => void;
  scaleLabel: string;
}

const UiScaleContext = createContext<UiScaleContextType | undefined>(undefined);

export const UiScaleProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [scale, setScaleState] = useState<UiScale>("large");

  useEffect(() => {
    const saved = localStorage.getItem("cognicare_ui_scale") as UiScale;
    if (saved && ["normal", "large", "extra-large"].includes(saved)) {
      setScaleState(saved);
      document.documentElement.setAttribute("data-scale", saved);
    } else {
      document.documentElement.setAttribute("data-scale", "large");
    }
  }, []);

  const setScale = (newScale: UiScale) => {
    setScaleState(newScale);
    localStorage.setItem("cognicare_ui_scale", newScale);
    document.documentElement.setAttribute("data-scale", newScale);
  };

  const scaleLabels: Record<UiScale, string> = {
    normal: "Normal (Laptop)",
    large: "Large (Standard)",
    "extra-large": "Extra Large (Senior Focus)",
  };

  return (
    <UiScaleContext.Provider
      value={{
        scale,
        setScale,
        scaleLabel: scaleLabels[scale],
      }}
    >
      {children}
    </UiScaleContext.Provider>
  );
};

export const useUiScale = () => {
  const context = useContext(UiScaleContext);
  if (!context) {
    throw new Error("useUiScale must be used within a UiScaleProvider");
  }
  return context;
};
