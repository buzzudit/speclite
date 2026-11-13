# Mould Contract — Build and Check

Load at Step 5. Read `mould-reference.html` only when building.

---

## Step 5 — Build

Copy `references/mould-reference.html` as the starting point and adapt its
component model to the agreed contract from Step 4.

### Time estimate

Open the build step with an honest estimate:

- ~10 minutes for a component close to the reference (one row, three tiers,
  normal-state only).
- 15–25 minutes for a component with additional tiers, multiple state variants,
  or complex degradation rules.
- Longer if the component has non-standard overflow behaviour, animated
  transitions that affect layout, or unusual measurement requirements. Say so
  and why.

### Adaptation map

Locate sections by their banner comments (`/* === SECTION NAME === */`), not by
line numbers. Adapt in this order:

#### 1. Page, panes, controls, result matrix

Keep unchanged:

- The three-pane workspace (Playground, Preview, Result).
- Independent collapsible/resizable panels with toggle icons.
- Drag-resize handles with keyboard support.
- The result matrix layout, cell interactions, and export mechanism.
- Panel sizing bounds and scroll behaviour.

Adapt only:

- Page `<title>` and the hidden header's title, model note, and calibration
  content.
- Control labels, select options, and input bounds to match the agreed variables.

#### 2. Component CSS and MEASUREMENT

Copy from the real component's source:

- Font families, sizes, weights, and line heights.
- Padding, margins, borders, border-radius, and gaps.
- Background colours and text colours per tier and state.
- The `--ff` and `--component-*` custom properties.

Derive canvas font strings from these values. Every `measureText` call must use
the exact CSS font shorthand (`"600 14px / 1.25 'Inter', system-ui"`, not
`"14px Inter"`). Record the mapping in a comment beside the font-string
constants.

#### 3. DATA and SCENARIOS

Replace the reference's vocabulary, widths, and scenarios with the confirmed
contract and synthetic labels.

**Vocabulary rules:**

- Invent every label. Model real shape: match the length distribution, character
  composition, and worst-case values of the actual label set.
- A tier of three-letter codes proves nothing about a tier of full department
  names. Use renamed real-length equivalents.
- Include near-duplicate pairs when the interview flagged ambiguity risk.
- Include localization-inflated variants when the interview confirmed l10n
  applies (+30% for German/Finnish is the default multiplier).

**State modelling:**

Each scenario declares a `state` property from this enum:

| State | Meaning | Data layer behaviour |
|-------|---------|---------------------|
| `normal` | All data present and valid | Full item set rendered |
| `empty` | No items at all | Empty-state message or placeholder rendered |
| `loading` | Data in flight | Skeleton placeholders rendered at expected item positions |
| `error` | Fetch or validation failed | Error indicator rendered; partial data may be present |
| `partial` | Some fields present, others missing | Present fields rendered; missing fields show fallback |
| `overflow` | More items than the UI was designed for | Over-cap items handled by the degradation rule |

Not every state applies to every component. Include only the states that the
interview confirmed or that the component's source handles. A state the source
does not handle is a finding, not a scenario to skip.

**Scenario structure:**

```javascript
const SCENARIOS = [
  {
    id: "S1",
    title: "Everyday — calibration case",
    state: "normal",
    items: [ /* synthetic labels at everyday counts */ ],
    calibration: true
  },
  {
    id: "S2",
    title: "Empty — no items returned",
    state: "empty",
    items: []
  },
  {
    id: "S3",
    title: "Loading — data in flight",
    state: "loading",
    items: null
  },
  // ... S4 through Sn
];
```

**Minimum scenario count:** 12–20 scenarios covering:

- Everyday (calibration case) — `S1`, always first.
- Empty — no data at all.
- Error — fetch failure or invalid data.
- Loading — skeleton/placeholder state.
- Every tier at cap — one scenario per tier with maximum confirmed items.
- Nothing-received — API responded but payload is empty or null.
- Long labels — longest confirmed or localization-inflated labels.
- Near-duplicate labels — when ambiguity was flagged.
- Partial data — subset of fields present.
- Overflow — items beyond the designed cap.
- Two explicit out-of-range stress tests — scenarios deliberately beyond the
  confirmed bounds, marked as stress.

Explain distinct coverage when the mould exceeds 20 scenarios.

**Width set:** always include:

- 320 px (reflow, if applicable — WCAG 2.2 SC 1.4.10).
- The 200%-zoom equivalent of the primary target width (e.g., 720 px for a
  1440 px screen — WCAG 2.2 SC 1.4.4).
- The user's everyday width from the calibration case.
- The widest supported width.
- At least one intermediate width.

#### 4. MODEL and LAYOUT ENGINE

Rewrite the layout model to match the component's actual rules:

- Tier ordering and grouping logic.
- Degradation sequence: what gives way first as width shrinks (overflow menu,
  truncation, wrapping, collapsing, hiding).
- Readability floor: the minimum character count that still carries meaning.
  Below this, truncation is rated severity 2+.
- Minimum item width.
- Pinned vs. free item behaviour.
- Selection state: what "active" or "selected" looks like and what happens when
  the active item enters an overflow menu.

Remove example-only rules from the reference. Do not carry over layout logic
that doesn't apply to this component.

For state variants, the layout engine must:

- Render skeleton placeholders at the same positions and sizes as normal items
  during `loading` state.
- Render an empty-state message centered in the component area during `empty`
  state.
- Render an error indicator (banner or inline) during `error` state, with any
  partial data still visible when the source component shows it.
- Render present fields normally and missing fields with a fallback (em-dash,
  "—", grey placeholder) during `partial` state.

#### 5. EVALUATION

Keep the severity roll-up logic and the `highestSeverityOf()` function.

Choose flag predicates from the interview's "what counts as broken" answers,
with actionable messages. Each flag definition needs:

- `code`: short uppercase identifier (e.g., `TRUNCATED`, `OVERFLOW_HIDDEN`).
- `name`: human-readable label.
- `test`: a function of `(scenario, width, layoutResult)` → boolean.
- `severity`: integer 0–4 from the agreed scale.
- `message`: a function returning a specific, actionable string describing what
  happened and where.

**Standard layout flags** (adapt from reference):

| Code | Fires when | Default severity |
|------|-----------|-----------------|
| `TRUNCATED` | Any label shorter than its full text | 2 |
| `BELOW_FLOOR` | Truncated label below the readability floor | 3 |
| `OVERFLOW_HIDDEN` | Items moved to an overflow menu | 1 |
| `ACTIVE_HIDDEN` | The active/selected item is in the overflow menu | 3 |
| `AMBIGUOUS` | Near-duplicate labels become identical after truncation | 3 |
| `OVERFLOWS_CONTAINER` | Component wider than its container | 3 |
| `WRAPS_UNEXPECTEDLY` | Component grows to multiple rows when designed as single-row | 2 |

**State-aware flags** (add for state scenarios):

| Code | Fires when | Default severity |
|------|-----------|-----------------|
| `EMPTY_HIDDEN` | Empty state shows nothing — no message, no placeholder, just blank space | 3 |
| `ERROR_OBSCURED` | Error indicator not visible or pushed off-screen at this width | 4 |
| `LOADING_MISLEADING` | Skeleton count/size doesn't match expected normal-state layout | 2 |
| `PARTIAL_AMBIGUOUS` | Missing-field fallback is indistinguishable from a real value | 3 |
| `STATE_UNLABELLED` | The component's current state (loading, error, empty) has no text or ARIA announcement | 2 |
| `NO_RECOVERY` | Error state has no retry action or guidance visible at this width | 3 |

Override default severities with the interview's agreed ratings. A flag the user
said is intended behaviour gets severity 0.

#### 6. RENDER

Render the actual component shape. The render function receives the current
scenario, width, overrides, and layout-engine output.

- Match the component's visual structure: tiers, dividers, selected state,
  overflow indicator, tooltips.
- Render state variants using the state property: skeletons for loading,
  empty-state messages, error banners, partial-field fallbacks.
- Tooltips show the full label on hover for any truncated item.
- Overflow menus open on click and list hidden items.

Do not render decorative elements that don't affect layout measurement. Do
render anything that consumes space (icons, badges, status indicators, action
buttons).

#### 7. STATE / MODES

- `CALIBRATION` object holds the agreed scenario ID, width, result, and evidence.
- `pg.scId` defaults to `CALIBRATION.scenario` (S1).
- `pg.W` defaults to `CALIBRATION.width`.
- The mould opens showing the calibration case at the calibration width.

Set `pg.scId` from `CALIBRATION.scenario`, not from a hardcoded string.

#### 8. exportResults()

Preserve the JSON contract. The exported block must contain:

- `title`: component name and variant.
- `scenarios`: array of `{id, title, state}` declarations.
- `widths`: the tested width set.
- `options`: current override values including `floor`.
- `severityScale`: all five labels keyed 0–4.
- `calibration`: `{scenario, width, result, note}` — `result` is one of
  `"matched"`, `"differs"`, `"not checked"`.
- `results`: array of `{scenario, title, state, width, status, highestSeverity, flags}`.
  Each flag: `{code, name, severity, message}`. `severity` is an integer 0–4.
  `highestSeverity` is the row's peak and must equal `Math.max(...flags.map(f => f.severity))`,
  rolling up to the row's `status`.
- `breakpoints`: per-scenario array of `{scenario, metric, width}`.
  A threshold never reached is `null`, never a guessed number.
- `tally`: `{PASS, WARN, BREAK}` counts matching the matrix.

Declare all scenarios independently. Every scenario × width cell appears exactly
once in results; each result's `title` must match its scenario declaration.

Write the JSON into `<script type="application/json" id="results-json">` after
every layout-affecting change. The matrix uses base scenarios, not playground
slider values. Tie every layout-affecting option to its cache key.

Keep initialization behind `document.fonts.ready`. If an offline font substitute
is used, note it as a calibration limitation.

### Results block shape (illustrative)

```json
{
  "title": "Patient status bar — expanded & collapsed",
  "scenarios": [
    {"id": "S1", "title": "Everyday — calibration case", "state": "normal"},
    {"id": "S2", "title": "Empty — no items", "state": "empty"},
    {"id": "S3", "title": "Loading — data in flight", "state": "loading"},
    {"id": "S4", "title": "Error — fetch failed", "state": "error"},
    {"id": "S5", "title": "Partial — vitals missing", "state": "partial"},
    {"id": "S6", "title": "All tiers at cap", "state": "normal"},
    {"id": "S7", "title": "Long German labels", "state": "normal"},
    {"id": "S8", "title": "Overflow — 12 items", "state": "overflow"}
  ],
  "widths": [320, 720, 960, 1280, 1440, 1920],
  "options": {"floor": 8},
  "severityScale": {
    "0": "Not a problem",
    "1": "Cosmetic",
    "2": "Minor",
    "3": "Major",
    "4": "Catastrophe"
  },
  "calibration": {
    "scenario": "S1",
    "width": 1440,
    "result": "not checked",
    "note": "Pending real-product comparison"
  },
  "results": [
    {
      "scenario": "S1",
      "title": "Everyday — calibration case",
      "state": "normal",
      "width": 720,
      "status": "WARN",
      "highestSeverity": 2,
      "flags": [
        {
          "code": "TRUNCATED",
          "name": "Labels ellipsized",
          "severity": 2,
          "message": "3 of 5 items truncated: Medications → Medic…, Appointments → Appoi…, Documents → Docum…"
        }
      ]
    },
    {
      "scenario": "S2",
      "title": "Empty — no items",
      "state": "empty",
      "width": 720,
      "status": "BREAK",
      "highestSeverity": 3,
      "flags": [
        {
          "code": "EMPTY_HIDDEN",
          "name": "No empty-state message",
          "severity": 3,
          "message": "Component renders blank space — no indication that data is absent"
        }
      ]
    },
    {
      "scenario": "S4",
      "title": "Error — fetch failed",
      "state": "error",
      "width": 320,
      "status": "BREAK",
      "highestSeverity": 4,
      "flags": [
        {
          "code": "ERROR_OBSCURED",
          "name": "Error not visible",
          "severity": 4,
          "message": "Error banner pushed off-screen at 320px — user sees stale data with no failure indication"
        }
      ]
    }
  ],
  "breakpoints": [
    {
      "scenario": "S1",
      "overflowAppearsAt": 890,
      "noTruncationFrom": 1340,
      "allItemsVisibleFrom": 1340
    },
    {
      "scenario": "S4",
      "errorVisibleFrom": 480,
      "errorFullyReadableFrom": 720
    }
  ],
  "tally": {"PASS": 28, "WARN": 14, "BREAK": 6}
}
```

### Build progress lines

Post one short progress line per milestone during build. Never dump raw code.

1. Data model and label vocabulary written (synthetic labels, real lengths,
   state variants defined).
2. Scenarios S1–Sn encoded, opening on S1 at [width] px.
3. Layout engine and state renderer adapted — severities set from agreed
   ratings.
4. Mould built — moving on to checks.

Say so in one clause if a milestone was trivial (e.g., "steps 1–2 were
straightforward for a three-tier bar").

---

## Invariants

Every mould must satisfy all of the following. The browser checker and contract
verifier test these; a failure blocks delivery.

### File and dependency

- One file. No build step, no CDN, no fetched fonts, no imported modules.
- Works offline. No network requests of any kind.

### Workspace layout

- **Three panes**: Playground (controls at left), Preview (component rendering
  in the main area), Result (verdict and matrix at bottom).
- Preview is the main area. Playground is a collapsible, resizable left panel.
  Result is a collapsible, resizable bottom panel.
- Both panels start **expanded**. No stacked or side-by-side layout switch.

### Independent panels

- Each panel has its own collapse/expand toggle.
- Toggle icons: panel-outline SVGs with tooltips and accessible labels
  (`aria-label`, `aria-expanded`).
- Collapsing one panel does not affect the other.
- Preserve focus when toggling. Collapsing a panel moves focus to its toggle
  icon.
- Reopening panels alongside Preview restores their last size.

### Drag resizing

- Drag Playground's right border or Result's top border.
- Handles appear on hover and keyboard focus. Show resize cursors
  (`col-resize`, `row-resize`).
- Arrow keys resize 10 px; Shift+Arrow 40 px.
- Expose separator role, orientation, value bounds, and current size via ARIA
  attributes.

### Sizing bounds

- Preview minimum height: 20 px.
- Playground width: 120 px to 65% of available width.
- Result minimum height: 100 px. Can grow to available height minus Preview's
  minimum and the panel gap (no 65% cap).

### State preservation

- Collapse/reopen restores the panel's previous size and scroll position.
- Resizing or toggling panels never changes: scenario selection, override
  values, simulated width, or exported results.
- Panels scroll independently. Preview scrolls horizontally for wide widgets
  and expands into freed space when a panel is collapsed.
- Keep resize handles reachable at all panel sizes.

### Presentation

- Playground and Result have a slightly darker background than Preview.
- Hide the page header (keep its title, model note, and calibration content
  in the file's source for the report).
- Reopen controls use an icon-only toggle, not a visible header.
- No reload persistence (no localStorage, no URL hash state).

### Reference chrome

- Page, pane, and matrix styling stays as in the reference: minimal, neutral,
  system-ui font stack. Only the component's own CSS and its `--ff` /
  `--component-*` custom properties are adapted.

### Real measurement

- All text measurement uses `canvas.measureText` with the exact CSS font
  shorthand strings.
- Never estimate widths from character counts.
- Never hard-code pixel widths for labels.

### Scenarios

- At least 12–20 named scenarios with distinct, confirmed coverage.
- Coverage requirements: everyday (calibration), empty, error, loading, every
  tier at cap, nothing-received, long labels, near-duplicates, partial data,
  two out-of-range stress tests.
- Each scenario has a unique `id` (S1, S2, …) and a descriptive `title`.
- S1 is always the calibration case, marked `calibration: true`.
- State scenarios declare their `state` property from the enum.

### Flags and severity

- Every `FLAG_DEFS` entry has `code`, `name`, `test`, `severity`, `message`.
- `highestSeverityOf()` rolls up the highest flag severity per cell.
- Status mapping: severity 0–1 → PASS, severity 2 → WARN, severity 3–4 → BREAK.
- Intended behaviour is severity 0, never BREAK.

### Breakpoints

- Computed via binary search, not typed.
- At minimum: where overflow appears, where truncation starts, where overflow
  clears.
- For state scenarios: where error indicators become visible, where empty-state
  messages fit, where loading skeletons align.
- A threshold never reached is `null`, never a guessed number.

### Results matrix

- Every scenario is a row; every width is a column.
- Each cell shows PASS / WARN / BREAK with flag codes in the hover title.
- Clicking a cell loads that scenario × width combination in Preview.
- Computed from `exportResults()` data. Rebuilt only when a layout-affecting
  option changes.

### Machine-readable results

- `exportResults()` writes the full JSON into
  `<script type="application/json" id="results-json">`.
- The report is written from this block, not from a reading of the page.
- Every scenario × width cell appears exactly once.
- `severity` is an integer 0–4. `highestSeverity` is the row's peak and must
  match the flags.

### Tooltips

- Every truncated label shows a tooltip on hover with its full text.
- Overflow-menu items show their full label.

### Calibration

- The mould opens on the calibration case: `pg.scId = CALIBRATION.scenario`,
  `pg.W = CALIBRATION.width`.
- `CALIBRATION` holds `{scenario, width, result, note}`.
- `result` starts as `"not checked"` and is updated after Step 6 calibration.
- Populate the model note in the hidden header and include calibration in the
  results JSON.

---

## Step 6 — Check

Run every check in order. A failure at any step must be fixed before proceeding.

### 6.1 Syntax check

Extract the main `<script>` body to a temp file and run:

```bash
node --check /tmp/mould-script.js
```

A silent exit is a pass. Any error means the mould won't load — fix it.

### 6.2 Load check

Dump the rendered DOM with headless Chrome:

```bash
"<Chrome>" --headless=new --disable-gpu --virtual-time-budget=6000 \
  --dump-dom "file://$PWD/MOULD.html" > /tmp/dom.html
```

An empty or missing `results-json` block in the dump means the mould did not
initialize. Fix and re-dump.

No Chrome/Edge available: ask the user to open the mould and confirm it renders.

### 6.3 Contract check

```bash
python3 .claude/skills/scenario-mould/scripts/verify_mould.py /tmp/dom.html
```

This validates:

- Schema of the results JSON.
- Exact scenario × width cells present.
- Severity integers and roll-ups.
- Tally matches matrix.
- Null thresholds (not guessed numbers).
- Calibration rules.
- State properties on scenarios.

A NOTE line is guidance, not a failure.

### 6.4 Browser interaction checks

Run the browser checker or perform manually:

- Every scenario loads when selected — the Preview updates.
- Changing the simulated width moves the widget.
- The Result verdict responds to scenario/width changes.
- Overflow menus open on click and list correct items.
- Both panels start open with darker backgrounds than Preview.
- Each panel's icon collapses/reopens independently:
  - Tooltip text and `aria-expanded` update correctly.
  - Keyboard toggle works (Enter/Space).
  - Collapsing a panel moves focus to its toggle.
- Drag both borders — indicators on hover/focus/drag, sizes stay bounded.
- Arrow keys resize (10 px), Shift+Arrow (40 px).
- Drag handles remain reachable after resizing.
- Result can expand until Preview is at its 20 px minimum.
- Collapse/reopen after resizing returns the chosen sizes.
- Preview expands into freed space when a panel collapses.
- Scenario, overrides, width, and exported results are unchanged across
  toggle/resize actions.
- Long content scrolls independently in each panel.
- Preview scrolls horizontally for wide widgets.
- State scenarios render their state variant (skeletons, empty message,
  error banner, partial fallbacks).
- Repeat at a narrow browser width.

The Python verifier does not cover these — don't claim they passed from
script output alone.

### 6.5 Calibration

**With a screenshot of the real component at the calibration case:**

1. Screenshot the mould Preview at the same scenario and width (use
   `--window-size` to match).
2. Compare item by item: visible items, truncation positions, overflow
   contents, overall widths.
3. State differences plainly: "The real component fits 'Medications' in full;
   the mould truncates it — the mould's pill padding is 2 px wider."
4. If the match is close enough, mark calibration as `"matched"`.
5. If it differs, fix the model (fonts, padding, gaps, layout rule) and
   re-check.
6. After two fix rounds without a match, mark calibration as `"differs"` with
   a specific note and mark results as provisional.

**Without a screenshot:**

1. Ask the user to open the mould beside the real product.
2. Ask: "Does the mould match the real product for this case?"
3. If not, fix and re-check as above.
4. If no comparison is possible, mark as `"not checked"` and results as
   provisional.

Write the outcome into `CALIBRATION.result` and `CALIBRATION.note`.

---

## Browser adapter

`window.scenarioLab` exposes programmatic access for the browser checker.
Adapt per component but keep this shape:

```javascript
window.scenarioLab = {
  ready: false, // true only after fonts, initial render, and results are complete

  snapshot() {
    // Returns serializable {scenario, width, overrides, results}
    // Panel operations must not change it
  },

  setCase(scenario, width) {
    // Reset overrides, select a base case, render
  },

  measurements() {
    // Returns nonempty samples [{label, expected, actual, delta, matches}]
    // expected from model calculations, actual from rendered DOM
    // Never copy one into the other
    // Compare canvas-measured and rendered widget fonts
    // Tolerance: 1 px
  },

  interactions: {
    // Per-scenario probes:
    // {scenario, width, selector, accessible, visible, text?}
    // For overflow access and full-label tooltips
    // If inapplicable: {notApplicable: true, reason}
  }
};
```

Review adapters against the source component. Fabricated hooks can fool
automation. Compare real product geometry during calibration — a passing
model/DOM check does not establish fidelity to the real product.

### Host requirements

- Node.js, Playwright, and a Chromium-based browser (for the browser checker).
- The mould itself stays dependency-free.
- Set `NODE_PATH` to the Playwright package directory if needed.
- Optionally set `CHROME_PATH`.
- Never silently install dependencies.

### Browser checker invocation

```bash
node scripts/verify_browser.cjs MOULD.html EVIDENCE_DIR SESSION.json
```

Opens the mould offline, records network attempts, checks matrix cells,
controls, panel toggles/resizing, scrolling, model geometry, menus and tooltips.

Writes:

- `rendered.html` — the rendered DOM.
- `results.json` — the exported results block.
- `browser-checks.json` — pass/fail per check with detail.
- `workspace.png` — screenshot with input/output hashes.

Rerun after changing the mould or session. A `--reference` mode checks the
shipped `mould-reference.html` to satisfy the delivery gate.

Missing Playwright, missing browser, or a failed check = **incomplete**, not
passed.
