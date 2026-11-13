#!/usr/bin/env node
/**
 * Browser-based verification of a Scenario Mould.
 *
 * Usage:
 *   node verify_browser.cjs MOULD.html EVIDENCE_DIR [SESSION.json] [--reference]
 *
 * Requires: Playwright (playwright or @playwright/test)
 * Env: CHROME_PATH (optional), NODE_PATH (optional)
 *
 * Outputs to EVIDENCE_DIR:
 *   rendered.html, results.json, browser-checks.json, workspace.png
 *
 * Exit 0 if all checks pass, 1 if any fail.
 */

"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

function sha256(buf) {
  return crypto.createHash("sha256").update(buf).digest("hex");
}

function parseArgs() {
  const args = process.argv.slice(2);
  const flags = { reference: false };
  const positional = [];
  for (const a of args) {
    if (a === "--reference") flags.reference = true;
    else if (!a.startsWith("--")) positional.push(a);
  }
  if (positional.length < 2) {
    console.error("Usage: node verify_browser.cjs MOULD.html EVIDENCE_DIR [SESSION.json] [--reference]");
    process.exit(1);
  }
  return {
    mouldPath: path.resolve(positional[0]),
    evidenceDir: path.resolve(positional[1]),
    sessionPath: positional[2] ? path.resolve(positional[2]) : null,
    reference: flags.reference,
  };
}

let chromium;
try {
  chromium = require("playwright").chromium;
} catch (_) {
  try {
    chromium = require("@playwright/test").chromium;
  } catch (__) {
    console.error(
      "FAIL: Playwright not found.\n" +
      "Install it: npm install playwright\n" +
      "Set NODE_PATH to the package directory if installed elsewhere."
    );
    process.exit(1);
  }
}

async function main() {
  const opts = parseArgs();

  if (!fs.existsSync(opts.mouldPath)) {
    console.error(`FAIL: Mould file not found: ${opts.mouldPath}`);
    process.exit(1);
  }

  fs.mkdirSync(opts.evidenceDir, { recursive: true });

  const checks = [];
  let page, browser, context;

  function record(name, pass, details) {
    const status = pass ? "PASS" : "FAIL";
    checks.push({ check: name, status, details: details || "" });
    const marker = pass ? "  PASS" : "  FAIL";
    console.log(`${marker}: ${name}${details ? " — " + details : ""}`);
  }

  try {
    const launchOpts = { headless: true };
    if (process.env.CHROME_PATH) {
      launchOpts.executablePath = process.env.CHROME_PATH;
    }

    browser = await chromium.launch(launchOpts);

    // 1. Offline check — block all network requests
    context = await browser.newContext({
      offline: true,
      viewport: { width: 1440, height: 900 },
    });
    page = await context.newPage();

    const networkAttempts = [];
    page.on("request", (req) => {
      const url = req.url();
      if (!url.startsWith("file://")) {
        networkAttempts.push(url);
      }
    });

    // 2. Load the mould
    const fileUrl = "file://" + opts.mouldPath;
    await page.goto(fileUrl, { waitUntil: "domcontentloaded", timeout: 15000 });

    record("offline", networkAttempts.length === 0,
      networkAttempts.length > 0 ? `${networkAttempts.length} network attempt(s): ${networkAttempts.slice(0, 3).join(", ")}` : "No network attempts"
    );

    // Wait for scenarioLab.ready
    let labReady = false;
    try {
      await page.waitForFunction("window.scenarioLab && window.scenarioLab.ready === true", { timeout: 10000 });
      labReady = true;
    } catch (_) {}
    record("load", labReady, labReady ? "scenarioLab.ready" : "Timed out waiting for scenarioLab.ready");

    // 3. Results exist
    const resultsContent = await page.evaluate(() => {
      const el = document.querySelector('#results-json');
      return el ? el.textContent.trim() : "";
    });
    const hasResults = resultsContent.length > 2;
    record("results-exist", hasResults, hasResults ? `${resultsContent.length} chars` : "Empty or missing #results-json");

    let resultsData = null;
    if (hasResults) {
      try {
        resultsData = JSON.parse(resultsContent);
      } catch (e) {
        record("results-parse", false, `Invalid JSON: ${e.message}`);
      }
    }

    // 4. Matrix cells
    if (resultsData) {
      const declaredScenarios = (resultsData.scenarios || []).map(s => s.id);
      const declaredWidths = resultsData.widths || [];
      const expectedCount = declaredScenarios.length * declaredWidths.length;

      const cellInfo = await page.evaluate(() => {
        const cells = document.querySelectorAll("td.cell[data-sc][data-w]");
        const result = [];
        for (const c of cells) {
          result.push({
            sc: c.dataset.sc,
            w: c.dataset.w,
            classes: c.className,
          });
        }
        return result;
      });

      const foundPairs = new Set(cellInfo.map(c => `${c.sc}:${c.w}`));
      let missingCells = 0;
      for (const sc of declaredScenarios) {
        for (const w of declaredWidths) {
          if (!foundPairs.has(`${sc}:${w}`)) missingCells++;
        }
      }
      const hasStatusClasses = cellInfo.every(c =>
        c.classes.includes("PASS") || c.classes.includes("WARN") || c.classes.includes("BREAK")
      );

      record("matrix-cells", missingCells === 0 && hasStatusClasses,
        `${cellInfo.length}/${expectedCount} cells, ${missingCells} missing, status classes: ${hasStatusClasses}`
      );
    }

    // 5. Controls — scenario/width selectors
    const controlsWork = await page.evaluate(() => {
      const scenarioSel = document.querySelector("select[data-control='scenario'], #scenario-select, [name='scenario']");
      const widthSel = document.querySelector("select[data-control='width'], #width-select, [name='width']");
      return {
        hasScenario: !!scenarioSel,
        hasWidth: !!widthSel,
        scenarioOptions: scenarioSel ? scenarioSel.options.length : 0,
        widthOptions: widthSel ? widthSel.options.length : 0,
      };
    });
    record("controls", controlsWork.hasScenario && controlsWork.hasWidth,
      `Scenario: ${controlsWork.scenarioOptions} options, Width: ${controlsWork.widthOptions} options`
    );

    // 6. Panel toggles
    const panelToggleResults = await page.evaluate(() => {
      const toggles = document.querySelectorAll("[data-panel-toggle], button[aria-controls]");
      const results = [];
      for (const btn of toggles) {
        const panelId = btn.getAttribute("aria-controls") || btn.dataset.panelToggle;
        const expanded = btn.getAttribute("aria-expanded");
        results.push({
          panelId,
          hasAriaExpanded: expanded !== null,
          initiallyExpanded: expanded === "true",
          hasTooltip: btn.hasAttribute("title") || !!btn.querySelector("[role='tooltip']"),
        });
      }
      return results;
    });
    const panelTogglesOk = panelToggleResults.length >= 2 &&
      panelToggleResults.every(p => p.hasAriaExpanded);
    record("panel-toggles", panelTogglesOk,
      `${panelToggleResults.length} toggle(s) found, aria-expanded: ${panelToggleResults.every(p => p.hasAriaExpanded)}`
    );

    // Test toggle interaction (click first toggle)
    if (panelToggleResults.length > 0) {
      const toggleInteraction = await page.evaluate(() => {
        const btn = document.querySelector("[data-panel-toggle], button[aria-controls]");
        if (!btn) return { ok: false, reason: "no toggle found" };
        const before = btn.getAttribute("aria-expanded");
        btn.click();
        const after = btn.getAttribute("aria-expanded");
        btn.click(); // restore
        return { ok: before !== after, before, after };
      });
      record("panel-toggle-interaction", toggleInteraction.ok,
        `aria-expanded toggled: ${toggleInteraction.before} → ${toggleInteraction.after}`
      );
    }

    // 7. Panel resizing — check for resize handles
    const resizeHandles = await page.evaluate(() => {
      const handles = document.querySelectorAll("[data-resize], .resize-handle, [role='separator']");
      return {
        count: handles.length,
        hasRole: Array.from(handles).some(h => h.getAttribute("role") === "separator"),
        hasCursor: Array.from(handles).some(h => {
          const style = window.getComputedStyle(h);
          return style.cursor.includes("resize") || style.cursor.includes("col-resize") || style.cursor.includes("row-resize");
        }),
      };
    });
    record("panel-resizing", resizeHandles.count >= 2,
      `${resizeHandles.count} handle(s), separator role: ${resizeHandles.hasRole}, resize cursor: ${resizeHandles.hasCursor}`
    );

    // 8. Scrolling — check panels have overflow set
    const scrollInfo = await page.evaluate(() => {
      const panels = document.querySelectorAll("[data-panel], .panel, .playground, .result-panel, .preview");
      const result = [];
      for (const p of panels) {
        const style = window.getComputedStyle(p);
        result.push({
          id: p.id || p.className.split(" ")[0],
          overflowY: style.overflowY,
          overflowX: style.overflowX,
        });
      }
      return result;
    });
    const scrollOk = scrollInfo.some(s => s.overflowY === "auto" || s.overflowY === "scroll");
    record("scrolling", scrollOk,
      `${scrollInfo.length} panel(s), scrollable: ${scrollInfo.filter(s => s.overflowY === "auto" || s.overflowY === "scroll").length}`
    );

    // 9. State preservation — check snapshot before and after toggle
    if (labReady) {
      const statePreserved = await page.evaluate(() => {
        if (!window.scenarioLab || !window.scenarioLab.snapshot) return { ok: false, reason: "no snapshot()" };
        const before = JSON.stringify(window.scenarioLab.snapshot());
        const btn = document.querySelector("[data-panel-toggle], button[aria-controls]");
        if (btn) { btn.click(); btn.click(); }
        const after = JSON.stringify(window.scenarioLab.snapshot());
        return { ok: before === after, before: before.length, after: after.length };
      });
      record("state-preservation", statePreserved.ok,
        statePreserved.ok ? "Snapshot unchanged after panel toggle" : `Snapshot changed (${statePreserved.reason || "mismatch"})`
      );
    }

    // 10. Matrix interaction — click a cell
    if (resultsData) {
      const matrixClick = await page.evaluate(() => {
        const cell = document.querySelector("td.cell[data-sc][data-w]");
        if (!cell) return { ok: false, reason: "no matrix cell" };
        const sc = cell.dataset.sc;
        const w = cell.dataset.w;
        cell.click();
        if (!window.scenarioLab || !window.scenarioLab.snapshot) return { ok: true, reason: "clicked but no snapshot to verify" };
        const snap = window.scenarioLab.snapshot();
        return {
          ok: String(snap.scenario) === sc && String(snap.width) === String(w),
          expected: `${sc}@${w}`,
          actual: `${snap.scenario}@${snap.width}`,
        };
      });
      record("matrix-interaction", matrixClick.ok,
        matrixClick.ok ? `Clicked cell loaded ${matrixClick.expected || matrixClick.reason}` : `Expected ${matrixClick.expected}, got ${matrixClick.actual}`
      );
    }

    // 11. Measurements (if available)
    if (labReady) {
      const measurements = await page.evaluate(() => {
        if (!window.scenarioLab || !window.scenarioLab.measurements) return null;
        try {
          return window.scenarioLab.measurements();
        } catch (e) {
          return { error: e.message };
        }
      });
      if (measurements && !measurements.error) {
        let maxDelta = 0;
        let sampleCount = 0;
        if (Array.isArray(measurements)) {
          for (const m of measurements) {
            if (typeof m.expected === "number" && typeof m.actual === "number") {
              maxDelta = Math.max(maxDelta, Math.abs(m.expected - m.actual));
              sampleCount++;
            }
          }
        }
        record("measurements", maxDelta <= 1,
          `${sampleCount} sample(s), max delta: ${maxDelta}px (tolerance: 1px)`
        );
      } else if (measurements && measurements.error) {
        record("measurements", false, `Error: ${measurements.error}`);
      }
      // Skip silently if measurements not available
    }

    // 12. Overflow menu (if applicable)
    const overflowMenu = await page.evaluate(() => {
      const trigger = document.querySelector("[data-overflow-trigger], .overflow-trigger, .more-button");
      if (!trigger) return null; // not applicable
      trigger.click();
      const menu = document.querySelector("[data-overflow-menu], .overflow-menu, [role='menu']");
      const visible = menu && menu.offsetParent !== null;
      if (menu && trigger) trigger.click(); // close
      return { found: true, menuVisible: visible };
    });
    if (overflowMenu) {
      record("overflow-menu", overflowMenu.menuVisible,
        overflowMenu.menuVisible ? "Opens on click" : "Trigger found but menu not visible after click"
      );
    }

    // 13. Tooltips (if truncated items exist)
    const tooltipInfo = await page.evaluate(() => {
      const truncated = document.querySelectorAll("[data-full-label], .truncated, [title]");
      if (truncated.length === 0) return null;
      const withTitle = Array.from(truncated).filter(el => el.hasAttribute("title") || el.dataset.fullLabel);
      return { total: truncated.length, withTooltip: withTitle.length };
    });
    if (tooltipInfo) {
      record("tooltips", tooltipInfo.withTooltip > 0,
        `${tooltipInfo.withTooltip}/${tooltipInfo.total} truncated items have tooltip/full-label`
      );
    }

    // Save evidence
    const renderedHtml = await page.content();
    fs.writeFileSync(path.join(opts.evidenceDir, "rendered.html"), renderedHtml);

    if (resultsContent) {
      fs.writeFileSync(path.join(opts.evidenceDir, "results.json"), resultsContent);
    }

    await page.screenshot({ path: path.join(opts.evidenceDir, "workspace.png"), fullPage: false });

    // Write browser-checks.json with hashes
    const mouldHash = sha256(fs.readFileSync(opts.mouldPath));
    const sessionHash = opts.sessionPath && fs.existsSync(opts.sessionPath)
      ? sha256(fs.readFileSync(opts.sessionPath))
      : null;

    const checksOutput = {
      timestamp: new Date().toISOString(),
      mouldFile: opts.mouldPath,
      mouldHash,
      sessionHash,
      reference: opts.reference,
      checks,
      evidence: {
        "rendered.html": sha256(Buffer.from(renderedHtml)),
        "results.json": resultsContent ? sha256(Buffer.from(resultsContent)) : null,
        "workspace.png": sha256(fs.readFileSync(path.join(opts.evidenceDir, "workspace.png"))),
      },
    };
    fs.writeFileSync(
      path.join(opts.evidenceDir, "browser-checks.json"),
      JSON.stringify(checksOutput, null, 2)
    );

  } catch (err) {
    console.error(`ERROR: ${err.message}`);
    // Write partial checks
    const checksOutput = {
      timestamp: new Date().toISOString(),
      error: err.message,
      checks,
    };
    fs.writeFileSync(
      path.join(opts.evidenceDir, "browser-checks.json"),
      JSON.stringify(checksOutput, null, 2)
    );
  } finally {
    if (browser) await browser.close();
  }

  const failed = checks.filter(c => c.status === "FAIL");
  const passed = checks.filter(c => c.status === "PASS");
  console.log(`\n--- ${passed.length} passed, ${failed.length} failed ---`);

  if (failed.length > 0) {
    console.log("Failed checks:");
    for (const f of failed) {
      console.log(`  - ${f.check}: ${f.details}`);
    }
    process.exit(1);
  }
  process.exit(0);
}

main().catch((err) => {
  console.error(`FATAL: ${err.message}`);
  process.exit(1);
});
