import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import React from "react";
import { PatientHeader } from "@/components/caregiver/PatientHeader";
import { PatientDetail, PatientSummary } from "@/types";

describe("PatientHeader Component", () => {
  it("renders default fallback when patient and summary are empty", () => {
    render(<PatientHeader />);
    expect(screen.getByText("Patient")).toBeDefined();
    expect(screen.getByText("All Systems Normal")).toBeDefined();
    expect(screen.getByText("100%")).toBeDefined();
  });

  it("renders patient details and summary stats properly", () => {
    const mockPatient: PatientDetail = {
      id: "p1",
      display_name: "Margaret Smith",
      date_of_birth: "1948-03-12",
      medical_notes: "Hypertension",
      emergency_contacts: [
        { id: "e1", name: "Sarah Smith", phone: "555-0192", relationship: "Daughter" },
      ],
    };

    const mockSummary: PatientSummary = {
      patient_id: "p1",
      display_name: "Margaret Smith",
      status: "ATTENTION_NEEDED",
      adherence_percentage: 85,
      total_medications: 4,
      open_alerts_count: 2,
    };

    render(<PatientHeader patient={mockPatient} summary={mockSummary} />);

    expect(screen.getByText("Margaret Smith")).toBeDefined();
    expect(screen.getByText("Attention Needed")).toBeDefined();
    expect(screen.getByText("85%")).toBeDefined();
    expect(screen.getByText("4")).toBeDefined();
    expect(screen.getByText("2")).toBeDefined();
  });
});
