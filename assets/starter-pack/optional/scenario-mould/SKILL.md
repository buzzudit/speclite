---
name: scenario-mould
user-invocable: true
description: >
  Generate and stress-test UI component scenarios across viewports, data states,
  content edge cases, and interaction patterns with an offline HTML model and a
  severity-rated report. Use when long labels, crowded navigation, hidden actions,
  empty states, error conditions, or narrow viewports raise concerns during design
  or non-production review.
---

# Scenario Mould

One UI component modelled exactly, tested across widths, data states, and content
variations, with a verdict for every scenario × width cell. The mould generates
scenarios from the component's contract — not random fuzzing — and rates every
finding on the Nielsen Norman Group 0–4 severity scale.

The output is two files: a one-file HTML mould (the interactive tester) and a
written Markdown report.

## Using this as a designer

Start with `/scenario-mould` followed by a component reference and your concern.

Example invocations:
- `/scenario-mould Check whether this navigation works with long German labels and 7+ items`
- `/scenario-mould Does this patient status bar degrade gracefully when half the fields are empty?`
- `/scenario-mould Test the filter chip row — I think it breaks on mobile with 10+ filters`
- `/scenario-mould Test the entire experience — all major components and nav`

The agent agrees the scope, generates scenarios and variations, builds and
verifies the mould, and explains which cases need attention. Findings give
engineering actionable references like "S7 at 720px — overflow menu hides the
active tab".

Offer this method when a concrete layout or state concern arises, not as a
required activity. The designer may stop after findings, explore alone, or
request guided testing now or later. Do not require a method selection, extra
test records, retests, or another confirmation loop beyond the already-verified
mould. When guided testing is requested, load `references/designer-testing.md`.

## Context

If called from a larger workflow (a usability review, a design sprint, a story):
inherit the work item and research question and place output accordingly.
Standalone use is supported — agree an output folder with the user; no calling
workflow is required.

Pairs well with a usability heuristic evaluation and a UX-copy audit; all three
share the severity scale below and can feed the same design review.

## Scenario dimensions

The mould generates scenarios across these dimensions, choosing which apply to
the component under test:

1. **Layout** — viewport widths from 320px (reflow) through 200%-zoom equivalents
   to the widest supported width. How the component degrades: overflow menus,
   truncation, wrapping, collapsing.
2. **Data state** — empty, loading/skeleton, partial (some fields present, others
   missing), full, overflow (more items than the UI was designed for), error,
   nothing-received (API returned but with no data).
3. **Content** — extreme label lengths, near-duplicate labels, special characters,
   localization inflation (+30% for German/Finnish), missing display names,
   numeric edge values (0, negative, very large).
4. **Interaction** — disabled items, multi-selection edge cases, focus management
   after overflow, active item hidden in a collapsed menu, keyboard-only
   navigation through degraded states.
5. **Accessibility** — 200% zoom (WCAG 2.2 SC 1.4.4), forced high-contrast mode,
   reduced motion, screen-reader label accuracy after truncation.

Not every dimension applies to every component. The interview (Step 4) determines
which dimensions matter and generates scenarios from confirmed bounds.

## Non-negotiables

- **Synthetic data only.** Invent every label and name; model real shape
  (lengths, counts, worst cases). If the user offers real data, steer them to
  their organization's data-handling guidance and don't use it.
- **One file, zero dependencies.** The mould is a single HTML file with no build
  step, no CDN, and no fetched fonts. It works offline.
- **Workspace layout.** Preview central; Playground a collapsible, resizable left
  panel; Result a collapsible, resizable bottom panel. Follow
  `references/mould-contract.md` for sizing invariants.
- **Real measurement.** `canvas.measureText` with the same font strings as the
  CSS. Never estimate from character counts.
- **The mould is a model, not the product.** It is only as good as its
  calibration check; a PASS depends on established fidelity. Confirm severity 3–4
  findings in the real build.
- **Resolve the output folder before writing.** Show paths before writing and
  confirm once written. Never use a suffixed filename unless replacement was
  explicitly authorized.

## Enforcement

Load `references/enforcement.md` before interviewing or building. Record actual
user decisions, agree controls and scenarios, run the pre-build session check.
After building, run browser checks and strict result/report validation. Never
claim complete verification from the result-data checker alone. User-delegated
decisions are allowed with disclosed assumptions; silence is not delegation.

## Session flow

Reuse supplied answers and existing artifacts. Give brief progress lines.
Don't make every step a stopping point. For a returning designer who wants to
test an existing artifact, use the testing guide without restarting generation.

| Step | Action |
|------|--------|
| 1 | Find the UI component (scan the repo, or take the user's screenshot or description) |
| 2 | Resolve the output folder and both filenames |
| 3 | Read the component's source and CSS; describe the layout contract in plain language |
| 4 | Interview adaptively; agree scenario dimensions, bounds, and the calibration case |
| 5 | Build the mould, one progress line per milestone |
| 6 | Verify it loads, then check it against the real component (calibration) |
| 7 | Report: summary, recommendations, full results, scorecard |
| 8 | Save within the agreed scope, explain findings, offer guided testing when useful |

Feedback and revisiting findings are optional; no closing questionnaire.

Load `references/session-guide.md` at Step 1, `references/mould-contract.md` at
Step 5 (and read `references/mould-reference.html` only when building), and
`references/report-format.md` at Step 7.

## Verify before reporting

Never report results you haven't verified. The results block is filled at
runtime, so verify the rendered DOM:

```bash
"<Chrome>" --headless=new --disable-gpu --virtual-time-budget=6000 \
  --dump-dom "file://$PWD/MOULD.html" > /tmp/dom.html
python3 .claude/skills/scenario-mould/scripts/verify_mould.py /tmp/dom.html
python3 .claude/skills/scenario-mould/scripts/verify_mould.py /tmp/dom.html --report REPORT.md
```

The Python checker validates result data and report structure. Browser checks
separately verify rendering, colors, controls, offline behavior, and opening
state. Calibration against the real product is a separate visual comparison. Fix
deterministic failures before claiming completion.

## Severity scale

Shared 0–4 scale (Nielsen Norman Group), used across all scenario dimensions:

| Rating | Label | Example |
|--------|-------|---------|
| 0 | Not a problem | Intended behavior — full label visible on hover |
| 1 | Cosmetic | Noticeable but task unaffected — tooltip-only item names |
| 2 | Minor | Friction — items below the readability floor, unclear empty states |
| 3 | Major | Needed content cut off, hidden, or hard to reach — fix before release |
| 4 | Catastrophe | Blocks the task, data loss risk, or safety-critical item hidden with no indication |

Rate by **frequency** (how many scenario × width cells), **impact** (can the user
still reach the item?), and **persistence** (a width range, or one pixel?).
Roll up the highest rating in a cell: a 3 anywhere means the row is at least 3.

Escalate a hidden or truncated safety-critical item (e.g., allergy alert,
critical medication, financial warning) to the relevant safety or compliance
review — flag it; a layout fix alone does not resolve it.

## Batch mode — full experience

When the user wants to test an entire experience (all major components and
navigation), use batch mode instead of running separate single-component
sessions. Batch mode runs one interview for the whole product, then iterates
per component with shared context.

### What batch mode shares across components

- **Seed data vocabulary** — patient names, payer names, auth numbers, etc. are
  invented once and reused. Every component sees the same synthetic universe.
- **Width set** — agreed once for the product, not per component.
- **Calibration width** — the user's everyday viewport applies to all components.
- **Scenario dimensions** — empty, loading, error, partial, stress bounds are
  agreed at the product level and inherited per component (each component picks
  the subset that applies).
- **Severity thresholds** — what counts as broken is agreed once.

### What stays per component

- **Layout engine** — each component's measurement model, column definitions,
  compression logic, and flags are specific to its contract.
- **Scenarios** — generated from the shared dimensions but adapted to what each
  component renders (a table has different scenarios than a timeline).
- **Flags** — each component defines its own flag set based on its degradation
  mechanisms.
- **Mould HTML** — one file per component, each self-contained and offline.
- **Component report** — one report per component with findings and scorecard.

### Batch output

| File | Purpose |
|------|---------|
| `[component].html` | Per-component mould (same as single mode) |
| `[component]-report.md` | Per-component report (same as single mode) |
| `rollup-report.md` | Cross-component summary with aggregated scorecard |
| `shared-data.md` | Documents the shared seed data and agreed dimensions |

### Batch session flow

| Step | Action |
|------|--------|
| B1 | Scan the product — identify all major components that qualify for moulding |
| B2 | Single interview — agree shared dimensions, seed data, widths, calibration, severity thresholds |
| B3 | Write `shared-data.md` — the shared contract that all component moulds inherit |
| B4 | Per component: read source → adapt scenarios → build mould → verify → write report (Steps 3–8 from single mode, no re-interview) |
| B5 | Write rollup report — aggregate findings across all components |

Load `references/session-guide.md` at B1 (batch section),
`references/mould-contract.md` at B4 per component, and
`references/report-format.md` at B4 (component) and B5 (rollup).

### Efficiency rules

- **No re-interview.** The shared dimensions from B2 carry forward. Per-component
  questions are limited to layout-specific details the source doesn't answer
  (e.g., "does this sidebar collapse to icons?").
- **Reuse seed data.** The `shared-data.md` contract provides the synthetic
  vocabulary. Each mould imports names, payers, counts from it — don't reinvent
  per component.
- **Brief progress.** One line per component milestone, not a full orientation
  each time.
- **Fail fast.** If a component doesn't qualify for moulding (no variable content,
  no finite space, no degradation mechanism), skip it and note why in the rollup.

## Working notes

- Stay inside the component's real contract. A harness that permits impossible
  states produces false positives.
- One component modelled exactly beats a configurable framework for three.
- If the component wraps instead of overflowing, degradation labels become "grew
  to N rows" / "pushed content below the fold."
- Scenario IDs get quoted in review comments, so append, never renumber.
- Explain abbreviations in plain language on first use (audience ranges from
  front-end engineers to PMs).
- State scenarios (empty, error, loading) are modelled as data variations in the
  mould, not as separate HTML files.
