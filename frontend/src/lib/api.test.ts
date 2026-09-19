import { describe, expect, it } from "vitest";
import { buildQuery, extractErrorMessage } from "./api";

describe("buildQuery", () => {
  it("skips empty values and serialises the rest", () => {
    expect(buildQuery({ q: "", country: "IN", page: 2, x: undefined, y: null })).toBe(
      "?country=IN&page=2",
    );
  });

  it("returns an empty string when nothing is set", () => {
    expect(buildQuery({})).toBe("");
  });

  it("keeps zero as a real value", () => {
    expect(buildQuery({ min_salary: 0 })).toBe("?min_salary=0");
  });

  it("encodes special characters", () => {
    expect(buildQuery({ q: "a&b" })).toBe("?q=a%26b");
  });
});

describe("extractErrorMessage", () => {
  it("uses string detail from domain errors", () => {
    expect(extractErrorMessage({ detail: "Email already in use" }, "x")).toBe(
      "Email already in use",
    );
  });

  it("formats the first FastAPI validation error with its field", () => {
    const body = { detail: [{ loc: ["body", "salary"], msg: "must be > 0" }] };
    expect(extractErrorMessage(body, "x")).toBe("salary: must be > 0");
  });

  it("falls back for unknown bodies", () => {
    expect(extractErrorMessage(null, "fallback")).toBe("fallback");
  });
});
