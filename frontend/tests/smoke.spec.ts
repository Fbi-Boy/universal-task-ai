import { expect, test } from "@playwright/test";

test("overview loads and workflow draft supports adding a step", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Good evening, builder/i })).toBeVisible();
  await expect(page.getByText("Execution volume · illustrative preview")).toBeVisible();
  await page.screenshot({ path: "test-results/overview-desktop.png", fullPage: true });

  await page.getByRole("button", { name: /Explore workflows/i }).first().click();
  await expect(page.getByText("Workflow canvas")).toBeVisible();
  const initialCount = await page.locator(".flow-node").count();
  await page.getByRole("button", { name: /Add step/i }).click();
  await expect(page.locator(".flow-node")).toHaveCount(initialCount + 1);
  await expect(page.getByText(/Step added to the visual draft/i)).toBeVisible();

  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({ path: "test-results/workflow-mobile.png", fullPage: true });
  await page.getByRole("button", { name: "Open navigation" }).click();
  await expect(page.getByRole("button", { name: "Close navigation" })).toBeVisible();
});
