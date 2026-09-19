import { act, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { useDelayedFlag } from "./useDelayedFlag";

describe("useDelayedFlag", () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  it("is false until the delay has elapsed", () => {
    const { result } = renderHook(() => useDelayedFlag(true, 4000));
    expect(result.current).toBe(false);
    act(() => vi.advanceTimersByTime(3999));
    expect(result.current).toBe(false);
    act(() => vi.advanceTimersByTime(1));
    expect(result.current).toBe(true);
  });

  it("never fires if the work finishes first, and resets afterwards", () => {
    const { result, rerender } = renderHook(({ on }) => useDelayedFlag(on, 4000), {
      initialProps: { on: true },
    });
    act(() => vi.advanceTimersByTime(2000));
    rerender({ on: false });
    act(() => vi.advanceTimersByTime(10_000));
    expect(result.current).toBe(false);
  });

  it("goes back to false when active turns off after firing", () => {
    const { result, rerender } = renderHook(({ on }) => useDelayedFlag(on, 100), {
      initialProps: { on: true },
    });
    act(() => vi.advanceTimersByTime(100));
    expect(result.current).toBe(true);
    rerender({ on: false });
    expect(result.current).toBe(false);
  });
});
