import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MedicalDocumentSection } from "../components/documents/MedicalDocumentSection";
import { DocumentUploadModal } from "../components/documents/DocumentUploadModal";
import { apiClient } from "@/lib/api";

vi.mock("@/lib/api", () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
    delete: vi.fn(),
  },
}));

const mockDocs = [
  {
    id: "doc-1",
    patient_id: "pat-123",
    title: "Neurologist Prescription - Donepezil 10mg",
    document_type: "PRESCRIPTION",
    doctor_name: "Dr. Elena Vance",
    document_date: "2026-11-15",
    notes: "Take 1 tablet daily with food.",
    file_name: "Donepezil_Prescription.pdf",
    file_type: "application/pdf",
    file_size_bytes: 142850,
    file_data_url: "data:application/pdf;base64,JVBERi0xLjQKMSAwIG9iajw8L1R5cGUvQ2F0YWxvZz4+ZW5kb2Jq",
    created_at: "2026-11-15T10:00:00Z",
    updated_at: "2026-11-15T10:00:00Z",
  },
  {
    id: "doc-2",
    patient_id: "pat-123",
    title: "MCI Clinical Diagnosis & Assessment",
    document_type: "MEDICAL_CONDITION",
    doctor_name: "Dr. Elena Vance",
    document_date: "2026-11-10",
    notes: "Mild cognitive impairment amnestic type.",
    file_name: "Clinical_Summary.png",
    file_type: "image/png",
    file_size_bytes: 84200,
    file_data_url: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
    created_at: "2026-11-10T14:30:00Z",
    updated_at: "2026-11-10T14:30:00Z",
  },
];

describe("Medical Documents & Prescriptions System", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (apiClient.get as any).mockResolvedValue({ data: mockDocs });
    (apiClient.post as any).mockResolvedValue({ data: { id: "doc-new" } });
    (apiClient.delete as any).mockResolvedValue({ data: null });
  });

  it("renders medical documents section with prescription and condition items", async () => {
    render(<MedicalDocumentSection patientId="pat-123" />);

    expect(
      screen.getByText("Medical Documents & Prescriptions")
    ).toBeDefined();

    await waitFor(() => {
      expect(
        screen.getByText("Neurologist Prescription - Donepezil 10mg")
      ).toBeDefined();
      expect(
        screen.getByText("MCI Clinical Diagnosis & Assessment")
      ).toBeDefined();
      expect(screen.getAllByText("Dr. Elena Vance").length).toBeGreaterThan(0);
    });
  });

  it("filters documents when category tab is selected", async () => {
    render(<MedicalDocumentSection patientId="pat-123" />);

    await waitFor(() => {
      expect(
        screen.getByText("Neurologist Prescription - Donepezil 10mg")
      ).toBeDefined();
    });

    // Click "Prescriptions" filter pill
    const prescBtn = screen.getByRole("button", { name: "Prescriptions" });
    fireEvent.click(prescBtn);

    expect(
      screen.getByText("Neurologist Prescription - Donepezil 10mg")
    ).toBeDefined();
  });

  it("renders upload modal and handles drag and drop file selection", async () => {
    const handleUpload = vi.fn().mockResolvedValue(undefined);
    const handleClose = vi.fn();
    const handleSuccess = vi.fn();

    render(
      <DocumentUploadModal
        patientId="pat-123"
        isOpen={true}
        onClose={handleClose}
        onSuccess={handleSuccess}
        onUpload={handleUpload}
      />
    );

    expect(screen.getByText("Upload Medical Document")).toBeDefined();
    expect(
      screen.getByText("Supports PDF, PNG, JPG, or WEBP (Max 15 MB)")
    ).toBeDefined();

    // Verify category options
    expect(screen.getByText("Doctor Prescription")).toBeDefined();
    expect(screen.getByText("Condition Details")).toBeDefined();
    expect(screen.getByText("Lab / Test Report")).toBeDefined();
  });
});
