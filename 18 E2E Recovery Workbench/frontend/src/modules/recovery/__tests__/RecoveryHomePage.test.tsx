import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { RecoveryRoutes, recoveryMenu } from "@/modules/recovery/routes";
import { json, renderWithApi } from "./render";

describe("recovery routes", () => {
  it("opens the overview at /recovery in Thai by default", async () => {
    renderWithApi(<RecoveryRoutes />, () => json({}), "/");
    expect(await screen.findByRole("link", { name: "ตรวจสอบสถานะระบบ" })).toHaveAttribute("href", "/recovery/platform");
  });

  it("lists every screen in the Recovery menu group", () => {
    expect(recoveryMenu.map((m) => m.to)).toEqual(["/recovery", "/recovery/platform"]);
  });
});
