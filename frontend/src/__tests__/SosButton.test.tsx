import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import React from "react";
import { SosButton } from "@/components/elderly/SosButton";
import { apiClient } from "@/lib/api";

vi.mock("@/lib/api", () => ({
  apiClient: {
    post: vi.fn(),
  },
}));

describe("SosButton Component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the SOS trigger button", () => {
    render(<SosButton patientId="patient-123" />);
    expect(screen.getByText("PRESS FOR HELP (SOS)")).toBeDefined();
  });

  it("opens modal and displays countdown on click", () => {
    render(<SosButton patientId="patient-123" />);
    fireEvent.click(screen.getByText("PRESS FOR HELP (SOS)"));

    expect(screen.getByText("Sending Emergency Alert!")).toBeDefined();
    expect(screen.getByText("Cancel (I am OK)")).toBeDefined();
    expect(screen.getByText("Send Now")).toBeDefined();
  });

  it("cancels modal when Cancel button is pressed", () => {
    render(<SosButton patientId="patient-123" />);
    fireEvent.click(screen.getByText("PRESS FOR HELP (SOS)"));

    fireEvent.click(screen.getByText("Cancel (I am OK)"));
    expect(screen.queryByText("Sending Emergency Alert!")).toBeNull();
  });

  it("dispatches SOS alert when Send Now is clicked", async () => {
    (apiClient.post as any).mockResolvedValueOnce({ data: { status: "dispatched" } });

    render(<SosButton patientId="patient-123" />);
    fireEvent.click(screen.getByText("PRESS FOR HELP (SOS)"));

    fireEvent.click(screen.getByText("Send Now"));

    await waitFor(() => {
      expect(screen.getByText("Help is on the Way!")).toBeDefined();
    });

    expect(apiClient.post).toHaveBeenCalledWith("/patients/patient-123/sos", {
      message: "Emergency SOS triggered by elderly user from safety button.",
      location_note: "User app screen",
    });
  });
});
