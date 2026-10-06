import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import React from "react";
import { AdherenceGauge } from "@/components/caregiver/AdherenceGauge";

describe("AdherenceGauge Component", () => {
  it("renders adherence percentage and counts", () => {
    render(<AdherenceGauge percentage={85} completed={3} total={4} />);

    expect(screen.getByText("85%")).toBeDefined();
    expect(screen.getByText("3 Taken")).toBeDefined();
    expect(screen.getByText("1 Pending")).toBeDefined();
  });
});
