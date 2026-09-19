import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { Pagination } from "./Pagination";

describe("Pagination", () => {
  it("shows the visible range and total", () => {
    render(<Pagination page={2} pages={4} total={100} pageSize={25} onPage={() => {}} />);
    expect(screen.getByText("26–50 of 100")).toBeInTheDocument();
    expect(screen.getByText("Page 2 of 4")).toBeInTheDocument();
  });

  it("disables Previous on the first page and Next on the last", () => {
    const { rerender } = render(
      <Pagination page={1} pages={3} total={60} pageSize={25} onPage={() => {}} />,
    );
    expect(screen.getByRole("button", { name: "Previous" })).toBeDisabled();
    rerender(<Pagination page={3} pages={3} total={60} pageSize={25} onPage={() => {}} />);
    expect(screen.getByRole("button", { name: "Next" })).toBeDisabled();
  });

  it("calls onPage with the neighbouring page", async () => {
    const onPage = vi.fn();
    render(<Pagination page={2} pages={4} total={100} pageSize={25} onPage={onPage} />);
    await userEvent.click(screen.getByRole("button", { name: "Next" }));
    await userEvent.click(screen.getByRole("button", { name: "Previous" }));
    expect(onPage).toHaveBeenNthCalledWith(1, 3);
    expect(onPage).toHaveBeenNthCalledWith(2, 1);
  });

  it("handles an empty result", () => {
    render(<Pagination page={1} pages={0} total={0} pageSize={25} onPage={() => {}} />);
    expect(screen.getByText("0–0 of 0")).toBeInTheDocument();
  });
});
