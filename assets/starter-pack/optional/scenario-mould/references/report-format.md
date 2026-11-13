# Report Format

Steps 7–8 of the Scenario Mould session flow: writing the report and handing off.

## Report structure

Write every section from the results block and exported JSON, not from reading
the page visually. Check scorecard totals against matrix rows (the verifier does
too). Use enforcement.md's exact table headers.

### Header

Open with:

```markdown
# Scenario Mould Report: [component name]
```

Then two lines:

1. A relative link to the mould file (opens in any browser)
2. The calibration result: "Checked against the real component: S1 at [width]px —
   matched", or what differed, or "Not checked against the real component — treat
   results as provisional."

---

## Section 1 — Test Summary

A one-minute read. Include:

**What works well**: 2–3 sentences about behaviors that held across scenarios
and widths. Be specific — e.g., "Pinned notes never leave the bar at any tested
width, even with all 7 present" or "Empty state messaging is clear and
consistently visible down to 480px."

**Most critical issues**: 2–4 entries in this format:

| Scenario | Width | Issue | Severity |
|----------|-------|-------|----------|
| S5: Interim consult note | 720px | Status, scheduling, and documents cannot all fit — the bar overflows off-screen | 3 |
| S11: Long linked appointment | 960–1920px | Clinic name wraps to 3 lines and pushes the column taller than its neighbors | 2 |
| S3: Loading state | 480px | Skeleton count (3) doesn't match everyday item count (7) — misleading | 2 |

State-related issues (empty, error, loading, partial) are first-class findings,
not a separate category.

---

## Section 2 — Recommendations

1–5 recommendations, highest severity first. Each recommendation:

- Names the flag code and where it fires (scenario IDs, widths)
- Describes the user impact in one sentence
- Suggests a concrete direction (a rule change, cap, or breakpoint to move —
  not "make it more robust")
- Cross-references the matching usability heuristic where one applies:
  - Items hidden behind an overflow menu → recognition rather than recall
  - Active item hidden in a menu → visibility of system status
  - Ellipsis that reads like a different label → error prevention via ambiguous
    labels
  - Duplicate labels after truncation → match between system and real world
  - Empty state with no guidance → help and documentation
  - Error state hidden at narrow width → error prevention
  - Loading state misrepresenting content → visibility of system status

Order by severity then affected-cell count. If over 5 recommendations, note how
many lower-severity findings live only in the full results.

Each recommendation is an opportunity, not a requirement. Frame accordingly.

---

## Section 3 — Full Results

### Severity scale

Reprint the shared scale:

| Rating | Label | Description |
|--------|-------|-------------|
| 0 | Not a problem | Intended behavior |
| 1 | Cosmetic | Noticeable, task unaffected |
| 2 | Minor | Friction or confusion |
| 3 | Major | Needed content cut off, hidden, or hard to reach |
| 4 | Catastrophe | Blocks the task, data loss, or safety risk |

### Results matrix

Table headers (exact, for parsing):

```
| Scenario | 720px | 960px | 1280px | ... |
```

Each cell holds the scenario ID only. Color/status comes from the export data.

### Findings by scenario

For each scenario with severity 1+ findings:

An italic narrative note per scenario explaining what happens to the user.

Then the findings table:

```
| Scenario | Width | Code | Severity | Message |
```

Every severity-1+ flag in export order. Escape pipes in messages as `&#124;`,
replace newlines with spaces.

### Breakpoints

```
| Scenario | Metric | Width |
```

Every exported metric in order. "never" for null (threshold never reached).
Metrics include: overflowAt, noTruncationFrom, allVisibleFrom, errorVisibleFrom,
emptyMessageVisibleFrom, and any component-specific thresholds.

### Safety-critical items

Flag any hidden or truncated safety-critical items (allergy alerts, medication
warnings, critical status indicators, financial warnings) for safety review
instead of only scoring them. A layout fix alone does not resolve a safety
concern.

---

## Section 4 — Scorecard

Table per enforcement.md headers:

```
| Scenario | Widths tested | PASS | WARN | BREAK | Highest Severity |
```

Every scenario plus a Total row. Total's "Widths tested" is the count of unique
widths followed by a title.

After the table:

1. Flag any severity-4 finding prominently
2. List every assumption the user did not confirm (if a third or more of the
   contract came from delegation, note that results are provisional)
3. Note that results come from a model, not the live product (true for PASS as
   much as BREAK), and that severity 3–4 findings should be confirmed in the
   real build
4. Close with a specific, motivating line and the clearest next step

---

## Assumptions section

List all delegated decisions and their stated assumptions. Distinguish between:
- User-confirmed decisions (cite the evidence)
- Agent-delegated decisions (cite the delegation instruction and assumption)

If more than a third of the decisions were delegated, add a prominent note that
results carry those assumptions.

---

## Calibration section

Must contain one of these literal lines (for script parsing):

- `Calibration: matched`
- `Calibration: differs`
- `Calibration: not checked`

If "differs": describe what differed and the impact on result interpretation.
If "not checked": state results are provisional.

---

## Scenario mould results appendix

A fenced code block with the language tag `scenario-mould-results` containing
the complete exported JSON from the results block:

````markdown
```scenario-mould-results
{ ... the full export JSON ... }
```
````

This appendix is the machine-readable record. The verifier checks it against the
DOM export.

---

## Step 8 — Save and hand off

Save within the agreed scope. Rules:

- Show the path before writing and confirm once written
- Honor an explicit request not to save
- Return paths, findings, and calibration limits to the caller
- Explain findings and limitations in plain language
- Offer guided testing only when useful (load designer-testing.md)
- Explain that observations, feedback, and revisiting findings are optional
- No closing questionnaire or repeated confirmation loop
- If the user requests changes, apply them and rerun applicable checks before
  updating the report

When handing off to a calling workflow: return the output paths, a one-line
summary of the highest finding, the calibration status, and any model
limitations.

---

## Table header reference

For reliable script parsing, these exact headers are required:

| Table | Headers |
|-------|---------|
| Matrix | `Scenario \| 720px \| ...` (widths from export) |
| Findings | `Scenario \| Width \| Code \| Severity \| Message` |
| Breakpoints | `Scenario \| Metric \| Width` |
| Scorecard | `Scenario \| Widths tested \| PASS \| WARN \| BREAK \| Highest Severity` |
