import AxeBuilder from "@axe-core/playwright";
import { expect, test, type Page } from "@playwright/test";

// Journey: sign in through the mock Entra ID as RW-PLATADM, open Platform status, check the ADR-010
// boundary and Temporal health, run the smoke workflow, and scan the page for accessibility.

async function signInAs(page: Page, username: string, roles: string[]) {
  await page.goto("/recovery/platform");
  await page.getByRole("button", { name: "เข้าสู่ระบบ" }).first().click();
  // mock-oauth2-server interactive login form
  await page.locator("input[name=username]").fill(username);
  await page
    .locator("textarea[name=claims]")
    .fill(JSON.stringify({ aud: ["api://rwb-recovery"], roles, preferred_username: username }));
  await page.locator("input[type=submit]").click();
  await page.waitForURL("**/recovery/platform");
}

test("platform admin sees the boundary, Temporal health and runs the smoke workflow", async ({ page }) => {
  await signInAs(page, "platform.admin@local.test", ["RW-PLATADM"]);

  await expect(page.getByRole("heading", { name: "สถานะระบบ" })).toBeVisible();
  await expect(page.getByText("ขอบเขตการเข้าถึงถูกต้อง")).toBeVisible();
  await expect(page.getByText("rwb-recovery")).toBeVisible();
  await expect(page.getByRole("cell", { name: "rwb-platform" })).toBeVisible();

  await page.getByRole("button", { name: "เรียกใช้เวิร์กโฟลว์ทดสอบ" }).click();
  await expect(page.getByText(/เริ่มเวิร์กโฟลว์ทดสอบ platform-smoke-\d{8} แล้ว/)).toBeVisible();

  const scan = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]).analyze();
  const blocking = scan.violations.filter((v) => v.impact === "serious" || v.impact === "critical");
  expect(blocking, JSON.stringify(blocking, null, 2)).toEqual([]);
});

test("auditor can read health but gets MSG-P4-002 when starting the smoke workflow", async ({ page }) => {
  await signInAs(page, "auditor@local.test", ["RW-AUDIT"]);

  await expect(page.getByRole("cell", { name: "rwb-platform" })).toBeVisible();
  await page.getByRole("button", { name: "เรียกใช้เวิร์กโฟลว์ทดสอบ" }).click();
  await expect(page.getByText("อ้างอิง MSG-P4-002")).toBeVisible();
});

test("a person with no Workbench role sees MSG-P4-001", async ({ page }) => {
  await signInAs(page, "no.role@local.test", []);
  await expect(page.getByText("คุณยังไม่มีสิทธิ์ใช้งาน Recovery Workbench กรุณาติดต่อผู้จัดการทีมเพื่อขอสิทธิ์")).toBeVisible();
});
