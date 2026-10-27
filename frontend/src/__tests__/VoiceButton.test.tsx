import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import React from "react";
import { VoiceButton } from "@/components/elderly/VoiceButton";

describe("VoiceButton Component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders with tap to talk label in idle state", () => {
    const handleTranscript = vi.fn();
    render(<VoiceButton onTranscript={handleTranscript} />);

    expect(screen.getByText("Tap to Talk")).toBeDefined();
    expect(
      screen.getByText("Tap the microphone anytime to speak with your assistant")
    ).toBeDefined();
  });

  it("displays thinking state when isProcessing is true", () => {
    const handleTranscript = vi.fn();
    render(<VoiceButton onTranscript={handleTranscript} isProcessing={true} />);

    expect(screen.getByText("Thinking")).toBeDefined();
    const button = screen.getByRole("button");
    expect(button.hasAttribute("disabled")).toBe(true);
  });

  it("handles unsupported speech recognition gracefully", () => {
    const handleTranscript = vi.fn();
    const alertMock = vi.spyOn(window, "alert").mockImplementation(() => {});

    // Ensure no SpeechRecognition on window
    delete (window as any).SpeechRecognition;
    delete (window as any).webkitSpeechRecognition;

    render(<VoiceButton onTranscript={handleTranscript} />);
    const button = screen.getByRole("button");
    fireEvent.click(button);

    expect(alertMock).toHaveBeenCalledWith(
      "Voice speech recognition is not supported in this browser. Please type your message."
    );
    alertMock.mockRestore();
  });
});
