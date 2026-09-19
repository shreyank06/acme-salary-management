import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { DistributionChart } from "./DistributionChart";

describe("DistributionChart", () => {
  it("renders one row per bucket with its count", () => {
    render(
      <DistributionChart
        data={{
          currency: "USD",
          buckets: [
            { start: 0, end: 50_000, count: 3 },
            { start: 50_000, end: 100_000, count: 7 },
          ],
        }}
      />,
    );
    expect(screen.getAllByRole("listitem")).toHaveLength(2);
    expect(screen.getByText("7")).toBeInTheDocument();
  });

  it("shows an empty state when there are no buckets", () => {
    render(<DistributionChart data={{ currency: "USD", buckets: [] }} />);
    expect(screen.getByText("No data.")).toBeInTheDocument();
  });
});
