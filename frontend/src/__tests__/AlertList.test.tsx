import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { AlertList } from "../components/caregiver/AlertList";
import { Alert } from "../types";

vi.mock("@/lib/api", () => ({
  apiClient: {
    post: vi.fn().mockResolvedValue({ data: {} }),
  },
}));

describe("AlertList Component", () => {
  it("renders all clear message when alerts array is empty", () => {
    const handleRefresh = vi.fn();
    render(<AlertList alerts={[]} patientId="p1" onRefresh={handleRefresh} />);

    expect(screen.getByText("All Clear")).toBeDefined();
    expect(screen.getByText(/No safety alerts or emergency events/i)).toBeDefined();
  });

  it("renders alerts with correct severity badges and titles", () => {
    const alerts: Alert[] = [
      {
        id: "alert-1",
        patient_id: "p1",
        alert_type: "SOS_BUTTON",
        severity: "CRITICAL",
        status: "OPEN",
        summary: "Urgent: Margaret pressed the SOS button in living room.",
        created_at: new Date().toISOString(),
      },
    ];

    const handleRefresh = vi.fn();
    render(<AlertList alerts={alerts} patientId="p1" onRefresh={handleRefresh} />);

    expect(screen.getByText(/Urgent: Margaret pressed the SOS button/i)).toBeDefined();
    expect(screen.getByText("OPEN")).toBeDefined();
    expect(screen.getByRole("button", { name: /Acknowledge/i })).toBeDefined();
  });
});
