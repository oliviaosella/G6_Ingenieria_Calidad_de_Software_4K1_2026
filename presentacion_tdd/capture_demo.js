const { chromium } = require("C:/Users/PEDRO_T/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core");

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  page.setDefaultTimeout(5000);
  await page.goto("http://localhost:5173/", { waitUntil: "domcontentloaded" });

  await page.screenshot({ path: "presentacion_tdd/demo-home.png", animations: "disabled" });
  await page.getByRole("button", { name: /Safari/ }).evaluate((element) => element.click());
  await page.waitForTimeout(250);
  await page.screenshot({ path: "presentacion_tdd/demo-actividad.png", animations: "disabled" });

  const dateButton = page.locator("button.date-pill").first();
  if (await dateButton.count()) {
    await dateButton.evaluate((element) => element.click());
    await page.waitForTimeout(250);
    await page.locator(".booking-section").screenshot({ path: "presentacion_tdd/demo-turnos.png", animations: "disabled" });
    const timeButton = page.locator("button.time-pill:not([disabled])").nth(1);
    await timeButton.evaluate((element) => element.click());
    await page.getByRole("button", { name: /Continuar/ }).evaluate((element) => element.click());
    await page.waitForTimeout(250);
    await page.locator(".booking-section").screenshot({ path: "presentacion_tdd/demo-participantes.png", animations: "disabled" });

    const fields = page.locator("input");
    await fields.nth(0).fill("Ana García");
    await fields.nth(1).fill("30111222");
    await fields.nth(2).fill("28");
    await page.getByRole("button", { name: /Continuar/ }).evaluate((element) => element.click());
    await page.waitForTimeout(250);
    await page.locator(".booking-section").screenshot({ path: "presentacion_tdd/demo-confirmar.png", animations: "disabled" });

    await page.locator('input[type="email"]').fill("ana@example.com");
    await page.locator('input[type="checkbox"]').check();
    await page.getByRole("button", { name: /Confirmar reserva/ }).evaluate((element) => element.click());
    await page.waitForTimeout(350);
    await page.locator(".booking-section").screenshot({ path: "presentacion_tdd/demo-comprobante.png", animations: "disabled" });
  }

  console.log(JSON.stringify({
    buttons: await page.locator("button").allTextContents(),
    inputs: await page.locator("input").evaluateAll((elements) => elements.map((element) => ({
      name: element.name,
      type: element.type,
      placeholder: element.placeholder,
    }))),
  }, null, 2));
  await browser.close();
})();
