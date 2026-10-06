import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { WeeklySummaryCard } from "../components/caregiver/WeeklySummaryCard";
import { Report } from "../types";

describe("WeeklySummaryCard Component", () => {
  it("renders empty state call to action when no report is present", () => {
    const handleGenerate = vi.fn();
    render(<WeeklySummaryCard onGenerateNew={handleGenerate} />);

    expect(screen.getByText("No Reports Generated Yet")).toBeDefined();
    const btn = screen.getByRole("button", { name: /Generate Weekly Report/i });
    expect(btn).toBeDefined();
    fireEvent.click(btn);
    expect(handleGenerate).toHaveBeenCalledTimes(1);
  });

  it("renders report content and metrics snapshot when report is passed", () => {
    const report: Report = {
      id: "rep-1",
      patient_id: "p1",
      report_type: "WEEKLY",
      period_start: "2026-09-29",
      period_end: "2026-10-06",
      ai_narrative_summary: "Margaret maintained 92% medication adherence and consistent cognitive scores.",
      metrics_snapshot: {
        adherence_percentage: 92,
        cognitive_composite_score: 84.5,
        cognitive_sessions_completed: 14,
        alerts_triggered_count: 0,
      },
      created_at: "2026-10-06T10:00:00Z",
    };

    render(<WeeklySummaryCard report={report} onGenerateNew={vi.fn()} />);

    expect(screen.getByText(/Report: 2026-09-29 to 2026-10-06/i)).toBeDefined();
    expect(screen.getByText(/Margaret maintained 92% medication adherence/i)).toBeDefined();
    expect(screen.getByText("92%")).toBeDefined();
    expect(screen.getByText("84.5/100")).toBeDefined();
  });
});
