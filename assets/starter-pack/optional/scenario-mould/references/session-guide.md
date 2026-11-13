# Session Guide — Steps 1–4

Loaded at Step 1. Covers orientation, component selection, output resolution,
contract reading, and the adaptive interview.

---

## Orientation

Run once before Step 1; skip on a return visit or when the user already knows
the skill.

Explain briefly what the user gets:

- An **offline interactive HTML model** (the mould) of one UI component, with
  controls for scenarios, viewport widths, data states, and content variations.
- A **scenario × width result matrix** with severity-rated verdicts for every
  cell.
- A **Markdown report** with findings, recommendations, breakpoints, and a
  scorecard — ready for design review or engineering handoff.

Clarify the boundary: the mould is a model, not the product. A calibration step
compares the model to the real component; until calibration passes, results are
provisional. Severity 3–4 findings should always be confirmed in the real build.

Start from the user's concern: a component, a screenshot, a file path, or a
description is enough. No preparation checklist. Ask only for missing
information.

---

## Step 1 — Choose the component

A component qualifies for scenario moulding when it meets at least two of these
criteria:

1. **Variable content** — it renders data it does not control (server-driven
   lists, user-generated labels, dynamic counts, translated strings).
2. **Finite space** — it occupies a single row, a fixed height, a constrained
   width, or a bounded container that cannot grow freely.
3. **A degradation mechanism** — it has a designed fallback when content exceeds
   space (overflow menu, truncation, wrapping, collapsing, "+N more").
4. **Multiple data states** — it must handle empty, loading, error, partial, and
   overflow conditions, not just the happy path.
5. **Conditional visibility** — items are shown or hidden by role, feature flag,
   data presence, or viewport width.

### Detection patterns

Scan the codebase for these signals (adapt to the framework):

| Signal | What to look for |
|--------|------------------|
| Overflow menus | `More`, `overflow`, `+N`, `showMore`, a `Dropdown` next to a list or bar |
| Truncation | `text-overflow`, `ellipsis`, `truncate`, `line-clamp`, CSS `overflow: hidden` on text containers |
| Width-reactive code | `ResizeObserver`, `offsetWidth`, `clientWidth`, `getBoundingClientRect`, `useMeasure`, `useBreakpoint`, container queries |
| Horizontal strips | `Tabs`, `Toolbar`, `Breadcrumb`, `SegmentedControl`, `ActionBar`, `Header`, `FilterBar`, `Legend`, `ChipRow`, `TagList` |
| Pinned vs free items | `pinned`, `sticky`, `priority`, `alwaysVisible`, a sort or partition before render |
| Variable data | `.map()` over a prop or query result that feeds visible items |
| State-dependent rendering | `isLoading`, `isEmpty`, `isError`, `Skeleton`, `EmptyState`, `ErrorBoundary`, `Fallback`, `Placeholder` |
| Conditional visibility | `v-if`, `v-show`, conditional JSX (`{condition && <Item />}`), `display: none` toggled by data, role-gated rendering |

### Presenting candidates

When scanning the repo produces candidates, present a short ranked table:

```
| Component       | File                        | Why it qualifies                              | What would break                    |
|-----------------|-----------------------------|-----------------------------------------------|-------------------------------------|
| PatientStatusBar| src/components/StatusBar.tsx | Variable fields, single row, overflow at 960px | Empty fields, long names, 7+ items  |
| FilterChipRow   | src/components/Filters.tsx   | Dynamic count, "+N more", wrapping disabled    | 10+ filters, German labels          |
| NavSidebar      | src/layout/Sidebar.tsx       | Collapsible, role-gated sections, deep nesting | Empty sections, long group names    |
```

Then ask with the host's question tool: at most **3 candidates** (the first
marked "(Recommended)"), plus a final option: **"I'll provide it myself —
screenshot or description"**.

If there are no qualifying candidates in the repo, say so and ask the user for a
screenshot or description.

### When the user provides a screenshot or description

From a screenshot:

1. Infer tiers from grouping, visual weight (fill vs outline, dividers,
   selected-item styling), and spatial hierarchy.
2. Estimate heights, padding, border radius, font size, bar width, and state
   them as estimates to confirm.
3. Transcribe visible labels, then replace them with **synthetic labels of the
   same length** — never carry real data forward.
4. Note any visible states (selected, disabled, active, hover, empty) and
   degradation mechanisms (ellipsis, overflow indicator, collapsed groups).

If a source file is also named, code wins over the screenshot where they
disagree, and the screenshot fills in visual details the code doesn't specify.

An unbuilt design (Figma frame, wireframe, sketch) is valid input. Say what you
assumed and carry it to Step 3.

### When the user names a component directly

Acknowledge it, skip the repo scan, and continue to Step 2.

---

## Step 2 — Resolve output

Agree the output folder before writing any file.

**Default locations** (in priority order):

1. The calling workflow's evidence folder, if this was invoked from a story or
   review.
2. A folder the user names.
3. A mutually agreed folder (ask once; the current directory is acceptable if
   the user confirms).

**File naming:**

| File | Pattern |
|------|---------|
| Mould | `YYYY-MM-DD_[component-name]_scenario-mould.html` |
| Report | `YYYY-MM-DD_[component-name]_scenario-mould-report.md` |

Rules:

- Use a short, lowercase, hyphenated component name.
- Show resolved paths before writing and confirm once written.
- Use repo-relative links between the report and the mould.
- If an output file already exists at the resolved path, ask before overwriting.
  Never silently use a suffixed filename unless replacement was explicitly
  authorized.
- Create only these two files (plus the session record, in the same folder).

After saving, return paths, findings summary, and calibration limits to the
caller.

---

## Step 3 — Read the component

Before writing any HTML, read the component's source, CSS, and surrounding
context. Describe the following in plain language:

### Layout contract

| Aspect | What to capture |
|--------|-----------------|
| **Tiers** | Ordered groups within the component and their styling differences (e.g., "pinned items are filled pills; free items are outline pills; overflow items live in a dropdown") |
| **Caps** | Minimum and maximum items per tier, and where these limits come from (a prop, a backend constraint, a design spec) |
| **Degradation order** | What gives way first as space decreases — e.g., "free items enter the overflow menu right-to-left, then pinned items truncate, then the bar itself scrolls" |
| **Readability floor** | The minimum character count or width at which a truncated label still carries meaning |
| **Minimum item width** | The narrowest an item can be before it loses function |

### State contract

| Aspect | What to capture |
|--------|-----------------|
| **Empty state** | What renders when there are zero items (a placeholder message, a CTA, nothing, the component hides entirely) |
| **Loading state** | Skeleton, spinner, shimmer, or nothing; how many skeleton items appear; does the layout shift when data arrives |
| **Error state** | Inline error, toast, fallback content, retry affordance, or silent failure |
| **Partial data** | What happens when some fields are present and others are null/undefined (e.g., a status bar with 3 of 7 fields populated) |
| **Nothing-received** | The API returned successfully but with an empty array or null payload — distinct from "loading" and from "error" |

### Interaction contract

| Aspect | What to capture |
|--------|-----------------|
| **Selection** | What "active" or "selected" looks like; what happens to a selected item when it enters an overflow menu |
| **Disabled items** | How disabled items render; can they appear in overflow; do they take space |
| **Focus management** | Tab order through the component; what gets focus when the overflow menu opens or closes |
| **Hover/tooltip** | Whether truncated items show full labels on hover |

### Data and vocabulary

| Aspect | What to capture |
|--------|-----------------|
| **Label vocabulary** | The real set of labels with their length distribution, renamed synthetically — a mould built on "Aaa Bbb" names proves nothing; use labels whose lengths match the real distribution |
| **Reference widths** | Always include a 200%-zoom case (e.g., 720px for a 1440px design, per WCAG 2.2 SC 1.4.4), the widest supported width, and 320px if the page must reflow (WCAG 1.4.10). Add the user's known breakpoints |
| **State transitions** | The expected sequence: loading → data (or error); empty → first item added; full → item removed |

### Confirmation

Summarize the contract in **2–4 plain sentences**. End with:

> "You can update any of this at any time — if something looks wrong or has
> changed, we'll adjust before we go further."

---

## Step 4 — Interview

No fixed questionnaire. Every question must be one you could not answer from
Step 3. Load `references/enforcement.md` and record the user's decisions.

### Round 1 — Open with the concern

Lead with a **two-line inference summary** of what you read in Step 3 (e.g.,
"This is a single-row status bar with 7 possible fields, 3 pinned. It truncates
labels and hides low-priority fields behind a More menu at narrow widths.").

Then ask:

> "What goes wrong with this component today, or what are you worried will go
> wrong?"

For a new design (not yet built), treat the design intent as the expected
behavior and test whether the design holds under stress.

### Round 2 — Component-type questions

Ask only the **2–4 questions** that match the component type. Pull options from
what you read in Step 3. Cover **both layout and state/content dimensions**.

#### One-row bar overflowing into a menu

- Realistic vs maximum item count; may pinned items ever enter the menu?
- Ellipsis acceptable, or must certain labels stay whole?
- What does the bar look like with zero items? With one item?
- Can all items be in an error or disabled state simultaneously?

#### Tabs / segmented control

- Does the active tab stay visible, or can it scroll or enter an overflow menu?
  Scroll arrows or overflow menu?
- Can tabs be disabled? Can all tabs be disabled at once?
- What does an empty tab panel look like? A loading tab panel?
- How many tabs at maximum; is the set dynamic or fixed?

#### Breadcrumb

- Which crumbs are sacred (first, last)? May middle crumbs collapse to "…"?
- Real hierarchy depth — can it grow unbounded?
- What happens when a breadcrumb segment is missing or untitled?

#### Chip / filter / token row

- Wrap to multiple rows, or stay in one row? If one row, what's the overflow?
- "+N more" — is that sufficient, or must chips stay individually removable?
- Maximum number of applied filters; empty filter state (no filters applied)?
- Can a chip be in a loading or error state?

#### Data-table header / columns

- Pinned columns — which, and how narrow before the value is useless?
- Horizontal scroll allowed? User-configurable column set?
- What renders in a cell when the value is null, loading, or errored?
- Does the table have an empty state? A loading skeleton?

#### Card / tile grid

- Reflow by count or minimum width? Is a single-column layout acceptable?
- Fixed or content-driven height? What happens when content overflows a card?
- Empty card state, error card state, skeleton card during loading?

#### Nav / sidebar

- Collapsible to icons? What happens to long group names when collapsed?
- Must the active item's full path stay visible?
- Empty sections (no items in a group) — hidden, or shown with a message?
- Loading state for async nav sections?

#### Status / metric strip

- Must every metric be visible, or can low-priority ones hide?
- Abbreviation rules (12.4k, $1.2M) — what's the threshold?
- Empty-value state (null metric) — dash, "N/A", hidden, or error indicator?
- Stale data indicator? Loading skeleton for individual metrics?

#### Other component types

Derive **three questions** from the component's contract:

1. What must never disappear?
2. What may degrade, and how far?
3. What does the empty, error, or loading case look like?

### Round 3 — Branch questions

Ask only follow-ups that the Round 2 answers opened. These are the common
branches:

| Branch trigger | Follow-up |
|----------------|-----------|
| Count named | Backend hard max and 95th percentile; propose cap and over-cap scenarios |
| Label length named | Longest real label; does localization inflate it (German/Finnish typically +30%); add length-stress scenarios |
| "Breaks on small screens" | Narrow viewport, 200% zoom, a side panel stealing width, or tablet portrait (disambiguate) |
| Ellipsis acceptable | What's the readability floor? Becomes the default |
| Labels must stay whole | Drop the ellipsis truncation path; overflow or wrap is the only degradation; premature truncation becomes a severity-3 flag |
| Similar-looking labels | Real near-duplicates? Add an AMBIGUOUS flag and a dedicated scenario |
| User-configurable set | Min/max configured items; what happens when a user-configured item is missing from the data |
| A specific bug or ticket | Reconstruct as a named scenario and report its S number |
| What counts as broken | Map to severity levels — hidden safety item = 4, must-fix = 3, friction = 2, cosmetic = 1, intended = 0 |
| Empty state described | Does it match the design? Is there a CTA? What's the transition to first-item? |
| Error state described | Inline or modal? Retry affordance? Does it preserve layout space or collapse? |
| Loading state described | Skeleton count matches final count? Layout shift on data arrival? |
| Partial data described | Which combinations of present/missing fields are realistic? Add specific partial scenarios |

Stop as soon as you can write the scenario list (usually 4–8 questions total,
never more than ten).

### Calibration case

Always ask these two questions (unless the user already answered them):

1. **Which situation do users see most often?** (The everyday case, not the
   worst case.)
2. **At what screen width do most users see this?** (Offer common widths
   including 200% zoom, plus "Not sure"; if unsure, use the most common
   supported width and say so.)

This pair becomes **S1** (marked **"everyday — calibration case"**), the state
the mould opens on. The calibration check in Step 6 compares the mould's S1 at
that width against the real component.

If a screenshot was offered, check whether it shows this case; if not, ask
whether they can provide one for calibration.

### Closing Step 4

List **S1 through Sn**, one line each, with S1 as the calibration case. Mark
each scenario's origin:

| Origin | Meaning |
|--------|---------|
| **User** | The user named this scenario or concern directly |
| **Standard** | Standard coverage: every tier at cap, nothing-received, long labels, near-duplicate labels, empty state, error state, partial data |
| **Stress** | A deliberate out-of-range stress test beyond normal operating bounds |

At least **two** scenarios must be marked **Stress**.

Example:

```
S1  Everyday — calibration case: 5 items, 2 pinned, at 1440px          [User]
S2  All 7 items present, 3 pinned                                       [Standard: tier cap]
S3  Empty state — zero items                                             [Standard: empty]
S4  Error state — API failure                                            [Standard: error]
S5  Partial data — 3 of 7 fields present, rest null                     [Standard: partial]
S6  Nothing received — API returned empty array                          [Standard: nothing-received]
S7  Long German-inflated labels (+30%), all fields present               [Standard: long labels]
S8  Near-duplicate labels: "Physical Therapy" / "Physical Therapy Eval"  [Standard: near-duplicates]
S9  12 items, all tiers full, longest real label (stress)                [Stress: count + length]
S10 All items disabled, error banner, 200% zoom at 720px                 [Stress: compound degradation]
```

Ask to confirm:

> "Does this cover what you're worried about, or should I add another scenario,
> a width, or a known issue?"

If the user explicitly delegates remaining choices, record the delegation, state
assumptions, and proceed. **Silence is not delegation.**

The agent maintains the session record and runs checks; the designer never edits
JSON or runs commands.
