import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import React from "react";
import { TodayCard } from "@/components/elderly/TodayCard";
import { Reminder } from "@/types";

describe("TodayCard Component", () => {
  it("renders empty state when no reminder is provided", () => {
    render(<TodayCard onAcknowledge={vi.fn()} onSnooze={vi.fn()} />);
    expect(screen.getByText("You are all caught up!")).toBeDefined();
  });

  it("renders scheduled reminder and triggers acknowledge callback", () => {
    const handleAck = vi.fn();
    const handleSnooze = vi.fn();

    const sampleReminder: Reminder = {
      id: "rem-1",
      patient_id: "pat-1",
      source_type: "MEDICATION",
      title: "Take Donepezil 10mg",
      description: "Take with water",
      scheduled_for: new Date().toISOString(),
      status: "SCHEDULED",
      priority: "HIGH",
      created_at: new Date().toISOString(),
    };

    render(
      <TodayCard
        reminder={sampleReminder}
        onAcknowledge={handleAck}
        onSnooze={handleSnooze}
      />
    );

    expect(screen.getByText("Take Donepezil 10mg")).toBeDefined();

    const ackButton = screen.getByText("I Did This!");
    fireEvent.click(ackButton);
    expect(handleAck).toHaveBeenCalledWith("rem-1");
  });
});
