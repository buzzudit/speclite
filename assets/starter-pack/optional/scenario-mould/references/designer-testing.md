# Designer Testing Guide

Load this reference when a designer asks to test, document, or investigate
findings from a delivered mould. This supports layout and scenario
investigation — it is not an automatic usability study and does not replace
production testing or participant research.

---

## Start from the question

Reuse the component, scenarios, calibration, and earlier decisions from the
mould's session record. Establish only what is missing: what the designer wants
to learn, and which cases answer that question.

The designer may:

- **Explore alone** — open the mould, switch scenarios and widths, form their
  own observations. The agent is available for questions.
- **Walk cases with the agent** — the agent explains what to look for in each
  scenario × width cell and helps interpret results.
- **Compare with a real design or build** — open the mould beside the live
  component or design file and check fidelity case by case.
- **Use another method** — the mould's scenario IDs and severity ratings feed
  into any review process the designer prefers.

Do not present a method menu or require a selection. Follow the designer's lead.

For an existing mould:

- Check its version and the calibration result in the session record.
- Review recorded limitations (model notes, provisional calibration, delegated
  assumptions).
- Do not rebuild or restart the interview unless the component's source has
  changed, the designer asks for new scenarios, or the mould's limitations
  block the question.
- If the mould was changed since delivery, rerun the technical checks
  (verify_mould.py, verify_browser.cjs) before claiming verified results.

---

## Run selected cases

Begin with cases that answer the designer's question: a known issue, the
everyday calibration case, a flagged combination, or a specific scenario they
named.

For each case:

1. **Set up.** Explain how to select the scenario and width in the Playground
   panel. Name the scenario ID (e.g., S5) and the target width. If the case
   involves a state variation (empty, error, partial data), explain which
   control to change and what it simulates.

2. **What to try.** Describe what the designer should do in the Preview panel:
   - Look at visible items, truncation, and overflow indicators.
   - Open the overflow menu if one appears — check what moved there.
   - Hover truncated labels to see the full text in the tooltip.
   - For state scenarios: check whether the state is communicated clearly.
   - For interaction scenarios: try the action (click, select, focus) and
     observe what changes.
   - Resize the browser window or drag the panel border to see transitions.

3. **What to observe.** Name the specific things to check:
   - Which items are visible, truncated, or hidden?
   - Does the overflow menu contain the right items?
   - Is the active/selected item still reachable?
   - For state scenarios: is the state obvious without reading tooltips?
   - At what point does the component degrade (the breakpoint)?

4. **Interpret.** Help the designer read the Result panel's verdict, flags, and
   severity ratings for this cell. Explain what each flag means in plain
   language. Connect the mould's result to what the designer sees in Preview.

**Separation of model and observation:**

- The mould's PASS / WARN / BREAK is a model prediction based on measurement
  and rules. It is not an observation of the real component.
- What the designer sees in the Preview panel is an observation of the model,
  not of the real component.
- What the designer sees in the real component (if comparing side by side) is
  the ground truth.
- Keep these three layers distinct. Never infer a real-component observation
  from a model result. Never upgrade a model PASS to "confirmed working"
  without a real-component check.
- Cases not run stay untested — do not mark them as passed or failed.

---

## State scenario testing

When the designer's question involves data-state scenarios (empty, loading,
error, partial, nothing-received, overflow), apply these additional checks:

**Clarity at each width:**

- Does the empty state communicate "no data" clearly, or does it look broken?
- At narrow widths, is the empty-state message still readable, or does it get
  truncated or hidden behind an overflow?
- Does a loading/skeleton state accurately preview the shape of the loaded
  content, or does it mislead about what will appear?

**Graceful degradation:**

- Does an error state at a narrow width still show the error message?
- If the component collapses items into an overflow menu, does the error
  indicator survive the collapse?
- When partial data arrives (some fields present, others missing), do the
  missing fields show a clear absent state or leave an ambiguous gap?

**Recovery and interaction:**

- Can the user act on an error state (retry, dismiss, navigate away)?
- At narrow widths, is the recovery action still reachable?
- If the error is inside an overflow menu, can the user find and act on it?

**Loading states:**

- Does the skeleton or spinner match the eventual layout closely enough that
  the transition feels stable (no layout shift)?
- If loading takes long enough for the user to scroll or resize, does the
  loading state hold up?

Note findings with the scenario ID, width, and the specific state being tested.

---

## Record only what is useful

Recording is optional. The designer chooses whether and how to record.

**In conversation:** Keep observations in the chat. Suitable for a quick
investigation with a few cases.

**In a Markdown file:** One file beside the mould (or the designer's chosen
location) with:

- Question being investigated
- Method (walked with agent, solo exploration, side-by-side comparison)
- Mould artifact path and version (file hash or date)
- For each tested case:
  - Scenario ID and width
  - What was tested (the action or observation)
  - Observed behavior (what actually happened)
  - Evidence reference (screenshot path, or "visual inspection")
  - Whether the finding matches, differs from, or extends the mould's result
- Agreed changes or design decisions
- Open questions
- Cases not run that matter (and why they were skipped)

**Rules:**

- No mandatory screenshots. A written observation is valid evidence.
- Never invent evidence. If a case was not observed, say so.
- Mark unconfirmed conclusions as provisional.
- No participant-identifying details or real user data.
- Synthetic content only — the mould's labels are already synthetic.

**CSV format for repeated runs or many cases:**

Use when running the same cases across mould versions, or when testing more
than a dozen cases in one session.

| Column | Description |
|--------|-------------|
| `artifact_version` | File hash or date of the mould |
| `scenario_id` | e.g., S5 |
| `width_px` | e.g., 720 |
| `method` | walked, solo, comparison, other |
| `expected` | What the mould predicted (PASS/WARN/BREAK + flags) |
| `observed` | What the designer saw |
| `status` | confirmed, blocked, skipped, not_run |
| `evidence` | Screenshot path or "visual inspection" |
| `decision` | Agreed action, or blank |
| `retest_of` | Links to a previous run's row, if retesting |

Status values:

- **confirmed** — the observation matches or contradicts the model, and the
  designer has a conclusion.
- **blocked** — could not test (environment issue, missing access, component
  not built yet). Record the blocker.
- **skipped** — deliberately not tested this session. Record why.
- **not_run** — not yet attempted. No conclusion.

Explain blocked and skipped cases. Keep previous observations when retesting
and link retests to the original run.

---

## Close or return later

**Closing a session:**

- Summarize what was learned: which cases confirmed the mould's findings,
  which revealed something new, which are still open.
- State the limits: what was not tested, what depends on real-component
  comparison, what needs a different method (accessibility audit, participant
  study, copy review).
- List agreed actions: design changes, engineering tickets, follow-up tests.

**Returning later:**

- Reuse the existing record. Pick up from where the designer left off.
- Run affected cases after a component change — don't rerun everything unless
  the change was structural.
- Don't claim an issue is resolved until an observation in the updated
  component supports it. A mould change alone is not resolution.

**Offer retesting only when:**

- The component source changed and the designer wants to verify the fix.
- An open question from the previous session can now be answered.
- The designer asks.

Do not prompt for retesting as a closing ritual.
