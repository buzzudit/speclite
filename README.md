# SpecLite Skill

A lightweight system to run projects with **just enough planning + clear execution**.

---

## What it does

* Sets up a minimal planning structure
* Adapts to existing repos instead of overwriting them
* Keeps work tracked through simple stories
* Avoids process bloat

---

## Modes

**Repo mode**

* Bootstrap → new or empty repo
* Existing → adapt what’s already there

**Interaction mode**

* Guided → asks a few key questions
* Fast-path → assumes and proceeds

---

## Core idea

* Don’t replace working systems
* Plan only what’s needed
* No work without a tracked story
* Risk decides how much rigor is needed

---

## Default setup

```
planning/
  vision.md
  bookkeeping.md
  story-management.md
  testing-strategy.md
  design-direction.md

stories/
  index.md
```

Optional modules include bootstrap steps, compliance constraints, design direction, owner-run AI demo workflows, Demo Maker (narrated walkthrough videos), Scenario Mould (UI component scenario generation and stress testing), and Heuristic Evaluation (12-heuristic UX review with a startup/product lens).

---

## Owner-run AI demos

Speclite can scaffold a repeatable owner-run demo pattern for apps you own:

* Hidden owner-demo mode in the app
* Stable `data-demo-*` targets
* App-owned `window.__ownerRunDemo` state
* Live AI narration controlled by the app
* A local harness that reads browser state and bounds
* Real OS-level mouse movement, clicks, and scrolling

The rule is strict: browser automation may inspect state and measure targets, but visible actions must come from OS-level input. This is for owner-run demos, not public end-user tours.

Starter files live under:

```
assets/starter-pack/optional/owner-run-demo/
```

---

## Demo Maker (narrated walkthrough videos)

Speclite can scaffold a repeatable way to make a narrated walkthrough video of a web app or prototype:

* A scripted browser drives the real UI, with a visible cursor, click ripples, chapter labels and title cards
* An AI voice (ElevenLabs, expressive `eleven_v3` with performance tags) narrates one line per beat
* Voice clips are generated first, so the recording is paced by the voice
* Picture time is calibrated against the clock, then every line is placed at its beat in an mp4
* Re-recording is one command, and unchanged lines are cached

It makes a finished video. For a live demo with the real OS cursor, use the owner-run demo module instead.

Starter files live under:

```
assets/starter-pack/optional/demo-maker/
```

---

## Scenario Mould (UI scenario stress testing)

Speclite can scaffold a Claude Code skill that generates and stress-tests UI component scenarios:

* One component modelled exactly in an offline, zero-dependency HTML file
* Scenarios generated across layout, data state, content, interaction, and accessibility dimensions
* Every scenario × width cell evaluated and rated on a 0–4 severity scale
* Findings give engineering-actionable references like "S7 at 720px — overflow menu hides the active tab"
* State scenarios (empty, loading, error, partial) are first-class, not an afterthought
* A written Markdown report with matrix, recommendations, scorecard, and calibration status
* Four verification scripts ensure the mould's contract, browser behavior, and delivery gate

It's a diagnostic tool for design review. For presentation artifacts, use the demo modules instead.

Starter files live under:

```
assets/starter-pack/optional/scenario-mould/
```

---

## Heuristic Evaluation (12-heuristic UX review)

Speclite can scaffold a structured UX evaluation skill with 12 heuristics:

* The Nielsen Norman Group 10 usability heuristics (complete, with full checklist items)
* Heuristic 11: Human-Centered AI and Automation — grounded in Billings (1991) and Amershi et al. (2019)
* Heuristic 12: Product-Market Alignment and Value Clarity — for startups and early-stage products: does the product communicate its value, earn trust from a cold start, and fit into real workflows?

Uses the same 0–4 severity scale as the Scenario Mould. Pairs well with it for combined design reviews.

Starter files live under:

```
assets/starter-pack/optional/heuristic-evaluation/
```

---

## Stories (how work happens)

* Start with a story
* Move it → doing
* Implement
* Verify
* Record result
* Move to done

---

## Testing (pick based on risk)

* L1: docs / planning
* L2: simple UI
* L3: logic / integrations
* L4: critical work

---

## Rules

* Don’t duplicate systems
* Don’t overwrite existing structure
* Respect canonical docs if they exist
* Keep everything minimal

---

## When to use

* Real projects where you want structure
* AI-assisted builds where things can drift

## When not to

* Quick throwaway work

---

## TL;DR

Plan a little. Track everything. Don’t overcomplicate.
