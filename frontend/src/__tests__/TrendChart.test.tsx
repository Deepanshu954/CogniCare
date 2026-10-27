import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import React from "react";
import { TrendChart } from "@/components/caregiver/TrendChart";

// Mock recharts ResponsiveContainer to avoid jsdom 0-width issues
vi.mock("recharts", async () => {
  const original = await vi.importActual<any>("recharts");
  return {
    ...original,
    ResponsiveContainer: ({ children }: any) => (
      <div data-testid="responsive-container" style={{ width: 500, height: 300 }}>
        {children}
      </div>
    ),
  };
});

describe("TrendChart Component", () => {
  it("renders empty state message when data is empty", () => {
    render(<TrendChart data={[]} />);
    expect(
      screen.getByText("No longitudinal data points available yet.")
    ).toBeDefined();
  });

  it("renders chart container when longitudinal data is provided", () => {
    const mockData = [
      { date: "2026-10-01", score: 85, baseline_score: 80 },
      { date: "2026-10-02", score: 90, baseline_score: 82 },
    ];
    render(<TrendChart data={mockData} />);
    expect(screen.getByTestId("responsive-container")).toBeDefined();
  });
});
