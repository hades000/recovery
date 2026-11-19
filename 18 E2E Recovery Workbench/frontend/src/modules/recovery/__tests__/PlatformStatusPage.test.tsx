import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import i18n from "i18next";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { PlatformStatusPage } from "@/modules/recovery/pages/PlatformStatusPage";
import { json, renderWithApi } from "./render";

const info = (overrides: Partial<{ temporal: boolean; visiblePublicTables: number }> = {}) => ({
  service: "ace-recovery",
  environment: "DEV",
  flags: { temporal: overrides.temporal ?? true, drools: true },
  database: { schema: "recovery", recoveryTables: 93, aceViews: 30, visiblePublicTables: overrides.visiblePublicTables ?? 0 },
});

const health = {
  target: "localhost:7233",
  namespace: "rwb-recovery",
  state: "NAMESPACE_STATE_REGISTERED",
  retentionDays: 30,
  taskQueues: [
    { name: "rwb-case", workflowPollers: 0 },
    { name: "rwb-integration", workflowPollers: 0 },
    { name: "rwb-platform", workflowPollers: 2 },
  ],
};

const problem = (status: number, messageCode: string, detail: string, messageTh: string) =>
  json({ type: `urn:rwb:problem:${messageCode}`, title: "x", status, detail, messageCode, messageTh, traceId: "t1" }, status, "application/problem+json");

describe("PlatformStatusPage", () => {
  beforeEach(async () => {
    await i18n.changeLanguage("en");
  });
  afterEach(async () => {
    await i18n.changeLanguage("th");
  });

  it("shows the database boundary and Temporal health", async () => {
    const seen: Request[] = [];
    renderWithApi(<PlatformStatusPage />, (req) => {
      seen.push(req);
      if (req.url.endsWith("/platform/info")) return json(info());
      if (req.url.endsWith("/admin/temporal/health")) return json(health);
      return json({}, 404);
    });

    expect(await screen.findByText("ace-recovery")).toBeInTheDocument();
    expect(screen.getByText("30")).toBeInTheDocument();
    expect(screen.getByText("Boundary in place")).toBeInTheDocument();
    expect(await screen.findByText("rwb-recovery")).toBeInTheDocument();
    expect(screen.getByText("30 days")).toBeInTheDocument();
    expect(screen.getByText("rwb-platform")).toBeInTheDocument();
    expect(seen[0]?.headers.get("Authorization")).toBe("Bearer test-token");
    expect(seen[0]?.headers.get("X-Correlation-Id")).toBeTruthy();
  });

  it("flags a broken boundary in words, not only colour", async () => {
    renderWithApi(<PlatformStatusPage />, (req) =>
      req.url.endsWith("/platform/info") ? json(info({ temporal: false, visiblePublicTables: 3 })) : json({}, 404),
    );
    expect(await screen.findByText("Boundary broken")).toBeInTheDocument();
  });

  it("does not call Temporal when the flag is off", async () => {
    const urls: string[] = [];
    renderWithApi(<PlatformStatusPage />, (req) => {
      urls.push(req.url);
      return json(info({ temporal: false }));
    });
    expect(await screen.findByText("The workflow service is switched off in this environment.")).toBeInTheDocument();
    expect(urls.some((u) => u.includes("/admin/temporal"))).toBe(false);
    expect(screen.queryByRole("button", { name: "Run smoke workflow" })).not.toBeInTheDocument();
  });

  it("starts the smoke workflow and shows its ID", async () => {
    const user = userEvent.setup();
    renderWithApi(<PlatformStatusPage />, (req) => {
      if (req.url.endsWith("/platform/info")) return json(info());
      if (req.url.endsWith("/admin/temporal/health")) return json(health);
      if (req.url.endsWith("/admin/workflows/smoke") && req.method === "POST")
        return json({ workflowId: "platform-smoke-20261117", workflowType: "PlatformSmokeWorkflow" }, 202);
      return json({}, 404);
    });

    await user.click(await screen.findByRole("button", { name: "Run smoke workflow" }));

    expect(await screen.findByText("Smoke workflow platform-smoke-20261117 started.")).toBeInTheDocument();
  });

  it("shows MSG-P3-036 when the workflow service is down", async () => {
    renderWithApi(<PlatformStatusPage />, (req) => {
      if (req.url.endsWith("/platform/info")) return json(info());
      return problem(503, "MSG-P3-036", "The workflow service is not available. Try again in a few minutes.", "ระบบเวิร์กโฟลว์ไม่พร้อมใช้งาน กรุณาลองใหม่ในอีกไม่กี่นาที");
    });

    expect(await screen.findByText("The workflow service is not available. Try again in a few minutes.")).toBeInTheDocument();
    expect(screen.getByText("Reference MSG-P3-036")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
  });

  it("shows the Thai message when the UI is Thai", async () => {
    await i18n.changeLanguage("th");
    renderWithApi(<PlatformStatusPage />, () =>
      problem(401, "MSG-P4-001", "You have no Recovery Workbench role. Ask your team manager to request one.", "คุณยังไม่มีสิทธิ์ใช้งาน Recovery Workbench กรุณาติดต่อผู้จัดการทีมเพื่อขอสิทธิ์"),
    );
    expect(await screen.findByText("คุณยังไม่มีสิทธิ์ใช้งาน Recovery Workbench กรุณาติดต่อผู้จัดการทีมเพื่อขอสิทธิ์")).toBeInTheDocument();
  });

  it("shows a forbidden state without a retry", async () => {
    renderWithApi(<PlatformStatusPage />, (req) => {
      if (req.url.endsWith("/platform/info")) return json(info());
      return problem(403, "MSG-P4-002", "You cannot do this here. Your role does not include it.", "x");
    });
    expect(await screen.findByText("You cannot open this page")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Try again" })).not.toBeInTheDocument();
  });

  it("retries after an error", async () => {
    const user = userEvent.setup();
    let calls = 0;
    renderWithApi(<PlatformStatusPage />, (req) => {
      if (req.url.endsWith("/platform/info")) {
        calls += 1;
        return calls === 1 ? json({}, 500) : json(info({ temporal: false }));
      }
      return json({}, 404);
    });
    await user.click(await screen.findByRole("button", { name: "Try again" }));
    await waitFor(() => expect(screen.getByText("ace-recovery")).toBeInTheDocument());
  });
});
