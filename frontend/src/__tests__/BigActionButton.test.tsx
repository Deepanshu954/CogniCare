import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import React from "react";
import { BigActionButton } from "@/components/elderly/BigActionButton";

describe("BigActionButton Component", () => {
  it("renders title, subtitle, and fires click handler", () => {
    const handleClick = vi.fn();
    render(
      <BigActionButton
        icon={<span>🧠</span>}
        title="Play Brain Game"
        subtitle="Fun memory exercises"
        onClick={handleClick}
      />
    );

    expect(screen.getByText("Play Brain Game")).toBeDefined();
    expect(screen.getByText("Fun memory exercises")).toBeDefined();

    const button = screen.getByRole("button");
    fireEvent.click(button);
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
