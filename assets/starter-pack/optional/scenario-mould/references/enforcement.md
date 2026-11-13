# Enforcement

Load this file before interviewing or building. It governs how the agent agrees
scope with the user, records decisions, validates the build, and gates delivery.

---

## Before building — agree and record

Ask what the user wants to vary. Confirm the exact widget — do not silently
narrow scope (e.g., from a full shopping cart to its action bar alone). When the
user names a component, confirm you are both looking at the same element before
proceeding.

Agree on all of the following before writing any HTML:

- **Controls**: which variables the mould exposes (item count, label set,
  data state, active selection, disabled items, etc.)
- **Bounds and defaults**: min/max for each control, the default value, and
  what the source of truth is (code, design spec, user statement)
- **Scenarios**: the ordered list S1–Sn, including which dimensions each
  scenario exercises (layout, state, content, interaction, accessibility)
- **Calibration case and width**: which scenario and viewport the user considers
  "everyday" — this becomes S1
- **What counts as broken**: severity thresholds — what the user considers
  must-fix-before-release (3), friction (2), cosmetic (1), intended (0)
- **Output folder and filenames**: resolved before any file is written

Prefer fewer questions with richer answers over an exhaustive questionnaire.
Group missing decisions into a concise proposal rather than asking one at a time.

An explicit request to "choose the details" or "you decide" is valid delegation.
Silence or choosing a subject to test is not delegation. The agent keeps the
session record; the designer never edits JSON or runs commands.

---

## Decision records

Every agreed point is recorded in the session JSON with this shape:

```json
{
  "status": "confirmed",
  "value": "The spec allows a maximum of 12 items with overflow after 6",
  "evidence": "User message: 'it caps at 12, anything past 6 goes into More'"
}
```

For delegated decisions:

```json
{
  "status": "delegated",
  "value": "Readability floor set to 8 characters",
  "evidence": "User said: 'you pick the details, I trust your judgment'",
  "assumptions": "8-character floor based on shortest meaningful English medical term; disclosed in report"
}
```

Rules:

- `status` is one of: `confirmed`, `delegated`, `deferred`
- `evidence` must reference an actual user message or source artifact — never
  fabricated or paraphrased beyond recognition
- `delegated` requires a nonempty `assumptions` string, disclosed verbatim in
  the report
- The agent must read and verify cited evidence; a script checks presence and
  non-emptiness, not truth
- Deferred decisions are captured but not acted on; they surface in the report
  as open questions

---

## Session JSON fields

Save the session record beside the mould in the agreed output folder. Required
top-level fields:

### decisions

Records for each of these keys: `scope`, `layout`, `variables`, `states`,
`calibration`, `broken`, `output`. Each is a decision record as above.

### scenarios

Ordered, independent scenario declarations:

```json
[
  {
    "id": "S1",
    "title": "Everyday — calibration case",
    "dimensions": ["layout", "content"],
    "state": "full"
  },
  {
    "id": "S5",
    "title": "Empty inbox — nothing received",
    "dimensions": ["state", "layout"],
    "state": "nothing-received"
  }
]
```

- `dimensions` is a non-empty array from: `layout`, `state`, `content`,
  `interaction`, `accessibility`
- `state` is optional; when present it is one of: `full`, `empty`, `loading`,
  `error`, `partial`, `nothing-received`, `overflow`
- Each scenario is independent — no scenario depends on another's output

### widths

Finite positive integers. Must include:

- A 200%-zoom equivalent (e.g., 720px for a 1440px design)
- The widest supported width
- 320px when the component must reflow (WCAG 2.2 SC 1.4.10)
- At least one intermediate width between the narrowest and widest

### calibration

```json
{ "scenario": "S1", "width": 1440 }
```

Both must appear in the scenarios and widths lists respectively.

### coverage

Maps coverage categories to scenario IDs. Required keys:

| Key | Description | Can be waived? |
|-----|-------------|----------------|
| `everyday` | The calibration case | No |
| `empty` | No items / empty state | Yes, with reason |
| `missing` | Partial data — some fields absent | Yes, with reason |
| `long-labels` | Labels at or beyond typical max length | Yes, with reason |
| `near-duplicates` | Labels that look alike after truncation | Yes, with reason |
| `stress` | Deliberate out-of-range stress tests | No — two distinct IDs required |
| `error-state` | Error condition rendering | Yes, with reason |
| `loading-state` | Loading/skeleton rendering | Yes, with reason |
| `partial-data` | Some fields present, others null/missing | Yes, with reason |

A waived category uses: `{"not_applicable": true, "reason": "...", "source": "..."}`.
Tags require review of the real scenario — do not tag mechanically.

### variables

Per agreed control:

```json
{
  "id": "itemCount",
  "label": "Number of items",
  "bounds": "1–12",
  "default": "6",
  "evidence": "User confirmed max 12",
  "probe": { "action": "fill", "value": "8", "selector": "#ctrl-itemCount" }
}
```

- `probe.action` is one of: `fill`, `select`, `check`, `uncheck`
- Each selector must match exactly one control in the mould
- Bounds and default are descriptive strings (they may be ranges, enums, or
  prose like "any valid ISO date")

### reviews

Added only after review — see the delivery gate below. Not present in the
initial session record.

---

## Browser contract

### Reference classes — do not remove

Keep these Result-pane identifiers from the reference mould:

`res-summary`, `res-verdict`, `pg-flags`, `res-widths`, `res-thresh`,
`res-metrics`, `res-matrix`, `.res-legend`

Keep scenario/width/description classes and panel IDs. Adapt widget controls and
data, not the Result shell. Keep matrix `td.cell[data-sc][data-w]` cells with
PASS/WARN/BREAK classes, text, and hover flag names/ratings. Colors must be
applied to rendered cells (not unused CSS). Use reference verdict badges and
severity colors consistently.

### window.scenarioLab adapter

Every mould exposes `window.scenarioLab` with:

- **ready**: `true` only after fonts loaded, initial render complete, and
  results computed
- **snapshot()**: serializable `{scenario, width, overrides, results}` — panel
  operations must not change it
- **setCase(scenario, width)**: reset overrides, select a base case, render,
  recompute results
- **measurements()**: nonempty samples `{label, expected, actual, delta}`;
  expected from model calculations, actual from rendered DOM; compare canvas
  `measureText` against rendered widget fonts; tolerance 1px
- **interactions**: `{scenario, width, selector, accessible, visible, text?}`
  probes for overflow access and full-label tooltips; if inapplicable,
  `{notApplicable: true, reason: "..."}` — review before accepting
- **referenceVariables**: only for checking the shipped reference starter;
  generated moulds use the session record for variable validation

Review adapters against source; fabricated hooks can fool automation. Compare
real product geometry during calibration — a passing model/DOM check does not
establish fidelity to a real product.

### Host requirements

Node.js, Playwright, and a Chromium-based browser for browser checks. The mould
itself stays dependency-free. Set `NODE_PATH` to the Playwright package dir if
needed and optionally `CHROME_PATH`. Never silently install dependencies.

### Browser check command

```bash
node scripts/verify_browser.cjs MOULD.html EVIDENCE_DIR SESSION.json
```

Opens the file offline, records network attempts (must be zero), checks matrix
cells, controls, panel toggles/resizing, scrolling containers, model geometry,
menus and tooltips. Writes `rendered.html`, `results.json`,
`browser-checks.json`, `workspace.png` with input/output hashes. Rerun after
changing the mould or session.

A `--reference` mode checks the shipped reference mould. Missing
Playwright/browser or a failed check = incomplete, not passed.

---

## Data and report validation

The export block (`<script type="application/json" id="results-json">`) requires:

- Intact `title` matching the mould's heading
- All declared `scenarios` with matching IDs and titles
- All declared `widths`
- All five severity labels (0–4) in `severityScale`
- Complete `calibration` with scenario, width, result, and note
- Exact scenario × width cells — every combination present, none extra
- Each flag with `code`, `name`, `message`, and integer `severity` (0–4)
- `highestSeverity` per row = the row's peak; must roll up to status
- `tally` with PASS, WARN, BREAK counts matching the actual cells
- Per-scenario `breakpoints` — null for a threshold never reached, never a
  guessed number

### Validation command

```bash
python3 scripts/verify_mould.py EVIDENCE_DIR/rendered.html
python3 scripts/verify_mould.py EVIDENCE_DIR/rendered.html --report REPORT.md
```

The `--report` flag additionally checks the Markdown report's headers, scenario
coverage, findings, breakpoints, literal Calibration line, assumptions, and the
fenced `scenario-mould-results` appendix against the export.

---

## Delivery gate

After review, add `reviews` records to the session JSON for each of these keys:

| Key | What it covers |
|-----|---------------|
| `source-fidelity` | Mould matches the real component's layout contract |
| `synthetic-data` | All data is synthetic; no real names, PHI, PII |
| `coverage` | Scenarios cover the agreed dimensions and edge cases |
| `visual` | Rendered mould visually represents the component |
| `recommendations` | Report recommendations are grounded and actionable |

Each review record:

```json
{
  "status": "reviewed",
  "evidence": "Compared mould S1@1440 against live dashboard — items and spacing match"
}
```

Or, when incomplete:

```json
{
  "status": "provisional",
  "evidence": "Visual comparison done at 1440px only",
  "limitation": "Narrow widths not compared — no staging access"
}
```

### Delivery validation command

```bash
python3 scripts/verify_delivery.py MOULD.html SESSION.json EVIDENCE_DIR REPORT.md
```

Confirms hashes, reviews are present and reviewed/provisional with evidence and
limitation where required, and that data, browser, and calibration outcomes are
consistent.

### Delivery rules

- Record designer review only if it happened; optional designer testing is not
  a prerequisite
- Delivery requires disclosure of model limits and follow-up; it doesn't
  authorize sending without the user's knowledge
- Any failed data/browser check blocks a complete delivery
- Unchecked calibration may be shared with an explicit limitation; never relabel
  it "matched" to pass
- Present separate outcomes for: contract checks, browser checks, and
  calibration — a single green "contract passed" is not acceptable
- The session record is hashed: finalize reviews and rerun browser checks first
