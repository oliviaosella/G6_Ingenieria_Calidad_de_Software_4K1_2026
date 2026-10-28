const { chromium } = require("C:/Users/PEDRO_T/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core");
const path = require("path");

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe" });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto("file:///" + path.resolve("presentacion_tdd/ecoharmony_tdd_rebuild.html").replace(/\\/g, "/"), { waitUntil: "load" });
  const slides = page.locator("section.slide");
  for (let i = 0; i < await slides.count(); i++) {
    await slides.nth(i).screenshot({ path: `presentacion_tdd/qa-${String(i + 1).padStart(2, "0")}.png`, animations: "disabled" });
  }
  await browser.close();
})();
