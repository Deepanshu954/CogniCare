import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import React from "react";
import { UiScaleProvider, useUiScale } from "@/lib/uiScaleContext";

const mockStorage: Record<string, string> = {};

beforeEach(() => {
  for (const key in mockStorage) {
    delete mockStorage[key];
  }

  const localStorageMock = {
    getItem: vi.fn((key: string) => mockStorage[key] || null),
    setItem: vi.fn((key: string, val: string) => {
      mockStorage[key] = val;
    }),
    removeItem: vi.fn((key: string) => {
      delete mockStorage[key];
    }),
    clear: vi.fn(() => {
      for (const key in mockStorage) {
        delete mockStorage[key];
      }
    }),
  };

  Object.defineProperty(window, "localStorage", {
    value: localStorageMock,
    writable: true,
  });

  document.documentElement.removeAttribute("data-scale");
});

const TestComponent = () => {
  const { scale, setScale, scaleLabel } = useUiScale();
  return (
    <div>
      <span data-testid="scale-value">{scale}</span>
      <span data-testid="scale-label">{scaleLabel}</span>
      <button onClick={() => setScale("normal")}>Set Normal</button>
      <button onClick={() => setScale("extra-large")}>Set Extra Large</button>
    </div>
  );
};

describe("UiScaleContext", () => {
  it("provides default scale as large", () => {
    render(
      <UiScaleProvider>
        <TestComponent />
      </UiScaleProvider>
    );

    expect(screen.getByTestId("scale-value").textContent).toBe("large");
    expect(screen.getByTestId("scale-label").textContent).toBe("Large (Standard)");
    expect(document.documentElement.getAttribute("data-scale")).toBe("large");
  });

  it("allows changing scale to normal and extra-large", () => {
    render(
      <UiScaleProvider>
        <TestComponent />
      </UiScaleProvider>
    );

    fireEvent.click(screen.getByText("Set Normal"));
    expect(screen.getByTestId("scale-value").textContent).toBe("normal");
    expect(document.documentElement.getAttribute("data-scale")).toBe("normal");
    expect(window.localStorage.setItem).toHaveBeenCalledWith(
      "cognicare_ui_scale",
      "normal"
    );

    fireEvent.click(screen.getByText("Set Extra Large"));
    expect(screen.getByTestId("scale-value").textContent).toBe("extra-large");
    expect(document.documentElement.getAttribute("data-scale")).toBe("extra-large");
    expect(window.localStorage.setItem).toHaveBeenCalledWith(
      "cognicare_ui_scale",
      "extra-large"
    );
  });
});
