import { describe, expect, it } from "vitest";
import { formatCompactMoney, formatMoney, formatNumber } from "./format";

describe("format", () => {
  it("formats currency without decimals", () => {
    expect(formatMoney(106696, "USD")).toBe("$106,696");
    expect(formatMoney(2500000, "INR")).toContain("2,500,000");
  });

  it("formats compact currency", () => {
    expect(formatCompactMoney(1_070_000_000, "USD")).toBe("$1.07B");
  });

  it("formats plain numbers with separators", () => {
    expect(formatNumber(10000)).toBe("10,000");
  });
});
