import { describe, expect, it } from "vitest";
import type { EmployeeInput } from "./types";
import { validateEmployee } from "./validation";

const valid: EmployeeInput = {
  full_name: "Asha Rao",
  email: "asha@acme.com",
  job_title: "Engineer",
  department: "Engineering",
  country: "IN",
  salary: 2_000_000,
  hire_date: "2022-01-01",
};

describe("validateEmployee", () => {
  it("accepts a valid employee", () => {
    expect(validateEmployee(valid)).toEqual({});
  });

  it("flags every invalid field", () => {
    const errors = validateEmployee({
      ...valid, full_name: " ", email: "nope", job_title: "", department: "",
      country: "", salary: 0, hire_date: "",
    });
    expect(Object.keys(errors).sort()).toEqual(
      ["country", "department", "email", "full_name", "hire_date", "job_title", "salary"],
    );
  });

  it("rejects fractional salaries", () => {
    expect(validateEmployee({ ...valid, salary: 10.5 }).salary).toBeDefined();
  });
});
