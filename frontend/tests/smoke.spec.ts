import { expect, test } from "@playwright/test";

test("overview loads and workflow draft supports adding a step", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Good evening, builder/i })).toBeVisible();
  await expect(page.getByText("Preview data only — metrics and activity are illustrative, not live workspace data.")).toBeVisible();
  await page.screenshot({ path: "test-results/overview-desktop.png", fullPage: true });

  await page.getByRole("button", { name: /Explore workflows/i }).first().click();
  await expect(page.getByText("Workflow canvas")).toBeVisible();
  const initialCount = await page.locator(".flow-node").count();
  await page.getByRole("button", { name: /Webhook Incoming HTTP event/i }).click();
  await expect(page.locator(".flow-node")).toHaveCount(initialCount + 1);
  const addedNode = page.locator(".flow-node").nth(initialCount);
  await expect(addedNode).toBeVisible();
  await expect(addedNode).toContainText("Webhook");
  await expect(page.getByText(/Webhook added to the visual draft/i)).toBeVisible();

  const library = page.locator(".node-library");
  const librarySearch = page.getByRole("searchbox", { name: "Find a node" });
  await librarySearch.fill("schedule");
  await expect(library.getByRole("button", { name: /Schedule Run at a set time/i })).toBeVisible();
  await expect(library.getByRole("button", { name: /Webhook Incoming HTTP event/i })).toHaveCount(0);
  await librarySearch.fill("no-such-node");
  await expect(library.getByRole("status")).toContainText(/No nodes match/i);
  await librarySearch.fill("");
  await expect(library.getByRole("button", { name: /Webhook Incoming HTTP event/i })).toBeVisible();

  await page.getByRole("button", { name: /Add step/i }).click();
  await expect(page.locator(".flow-node")).toHaveCount(initialCount + 2);
  await expect(page.getByText(/Step added to the visual draft/i)).toBeVisible();

  const approvalSwitch = page.getByRole("switch", { name: "Require approval" });
  await expect(approvalSwitch).toHaveAttribute("aria-checked", "true");
  await approvalSwitch.click();
  await expect(approvalSwitch).toHaveAttribute("aria-checked", "false");

  const auditSwitch = page.getByRole("switch", { name: "Audit every step" });
  await expect(auditSwitch).toHaveAttribute("aria-checked", "true");
  await auditSwitch.click();
  await expect(auditSwitch).toHaveAttribute("aria-checked", "false");

  await page.setViewportSize({ width: 390, height: 844 });
  await page.reload();
  await expect(page.locator(".sidebar-open")).toHaveCount(0);
  await expect(page.getByRole("button", { name: "Open navigation" })).toBeVisible();
  await page.getByRole("button", { name: /Explore workflows/i }).first().click();
  await expect(page.getByText("Workflow canvas")).toBeVisible();
  await page.screenshot({ path: "test-results/workflow-mobile.png", fullPage: true });
  await page.getByRole("button", { name: "Open navigation" }).click();
  await expect(page.locator(".sidebar-open .mobile-close")).toBeVisible();
  await page.screenshot({ path: "test-results/navigation-mobile-open.png", fullPage: true });
});
