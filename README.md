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

Optional modules include bootstrap steps, compliance constraints, design direction, and owner-run AI demo workflows.

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
