import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Navbar } from "../components/ui/Navbar";
import { UiScaleProvider } from "../lib/uiScaleContext";

// Mock next/navigation
const mockPush = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockPush }),
  usePathname: () => "/app/my-day",
}));

// Mock authContext
const mockLogout = vi.fn().mockResolvedValue(undefined);
let mockUser: any = {
  id: "u-123",
  display_name: "Margaret Smith",
  email: "margaret@example.com",
  role: "ELDERLY",
};

vi.mock("@/lib/authContext", () => ({
  useAuth: () => ({
    user: mockUser,
    logout: mockLogout,
    isLoading: false,
  }),
}));

describe("Navbar Component", () => {
  it("renders CogniCare branding and elderly navigation links", () => {
    render(
      <UiScaleProvider>
        <Navbar />
      </UiScaleProvider>
    );

    expect(screen.getByText("CogniCare")).toBeDefined();
    expect(screen.getByText("Senior Companion")).toBeDefined();
    expect(screen.getByText("My Day")).toBeDefined();
    expect(screen.getByText("Brain Games")).toBeDefined();
    expect(screen.getByText("Assistant")).toBeDefined();
  });

  it("handles scale adjustments and logout action", () => {
    render(
      <UiScaleProvider>
        <Navbar />
      </UiScaleProvider>
    );

    // Check scale buttons
    const normalBtn = screen.getByRole("button", { name: "Normal" });
    const xlBtn = screen.getByRole("button", { name: "XL Senior" });
    expect(normalBtn).toBeDefined();
    expect(xlBtn).toBeDefined();

    fireEvent.click(xlBtn);
    fireEvent.click(normalBtn);

    // Logout
    const logoutBtn = screen.getByTitle("Sign out");
    expect(logoutBtn).toBeDefined();
    fireEvent.click(logoutBtn);
    expect(mockLogout).toHaveBeenCalled();
  });
});
