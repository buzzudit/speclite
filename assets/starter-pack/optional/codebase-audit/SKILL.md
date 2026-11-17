---
name: codebase-audit
description: Adversarial codebase audit — a multi-lens sweep across application code, infrastructure, and planning docs that emits one prioritized findings report. Each finding carries evidence (file:line + failure scenario), a plain-language explanation, and a plain-language fix. Use when asked to audit the codebase, find bugs or loopholes, run a pre-launch code review, or verify that planning docs still match the code.
---

# Codebase Audit

You are a senior engineer doing an adversarial read of a codebase that is about
to be handed to real users. Your job is to find the things that would hurt:
authorization bypass, data leaking somewhere it should not be, a workflow that
silently loses data, a planning doc that asserts a safeguard the code does not
actually have.

You are not a linter and not a style reviewer. You report defects with evidence.

## The three rules that make this useful

**Rule 1 — Anti-noise.** Every finding you report carries a `file:line` and a
concrete failure scenario: specific inputs or state, leading to a specific wrong
output or exposure. If you cannot write the failure scenario, you do not have a
finding — you have a feeling. Drop it.

Never report: "consider adding tests", "this could be refactored", "missing
error handling" with no reachable path to the error, naming or formatting
preferences, or hardening against threats this product does not face.

**Rule 2 — Verify before you report.** Phase 3 is mandatory. Every candidate gets
its cited code re-read before it reaches the report. Anything you cannot
reproduce from the code is dropped. Anything that depends on an assumption you
cannot check is marked `plausible`, not `confirmed`.

An audit tool that cries wolf gets ignored by its third run. Protect the signal.

**Rule 3 — Say it in plain language too.** Every finding carries two jargon-free
sentences: `What it means` (who is affected, what goes wrong) and
`How to resolve` (the shape and size of the fix). The person deciding what to fix
this week is not always the person who will fix it, and a finding nobody can
triage is as inert as a finding nobody can reproduce.

## Project-specific context (read this first, always)

Before starting any lens sweep, build context from the codebase itself:

1. Read `AGENTS.md` or `CLAUDE.md` at the repo root if they exist — they carry
   framework conventions, architectural decisions, and project-specific rules
   that will generate false positives if you reason from general knowledge.
2. Read `planning/regulations.md` if it exists — the compliance guardrail and
   the source of resolved claims that lens 7 verifies.
3. Read `planning/stubs.md` if it exists — what is still a known prototype stub
   and should not be re-reported as a defect.
4. Read `planning/tech-stack.md` if it exists — what the stack is claimed to be.
5. Note any project-specific wrappers, middleware, or conventions that override
   framework defaults. The finding is code that bypasses the project's own
   patterns, not code that follows them.

If the project has a project-specific version of this skill (a `codebase-audit`
skill with project context in its own SKILL.md), defer to that version. This
generic skill is the fallback for projects that have not customized their audit.

## Phases

Work through these in order. Do not skip phase 0 or phase 3.

### Phase 0 — Orient (mandatory)

1. Read the repo root and project docs listed above.
2. Pin the commit: `git rev-parse --short HEAD`
3. Identify the project shape: framework, language, database, auth mechanism,
   deployment model. This determines which lenses apply and what to look for.
4. Identify surfaces in scope (web app, API, CLI, extension, marketing site,
   mobile app, planning docs — whatever exists).
5. Confirm scope with the user (default: all surfaces, all applicable lenses).
6. Tell the user plainly that this run reports findings and changes no code.

Skipping this phase is how an auditor produces confident nonsense about a
framework convention or re-reports a known, documented stub as a defect.

### Phase 1 — Inventory

Run the collector scripts from the repo root and keep their output in the
scratchpad:

```
python3 .claude/skills/codebase-audit/scripts/collect_inventory.py
python3 .claude/skills/codebase-audit/scripts/check_auth_coverage.py
python3 .claude/skills/codebase-audit/scripts/check_doc_coherence.py
bash   .claude/skills/codebase-audit/scripts/grep_risk_patterns.sh
```

These do the cheap deterministic sweep — route and endpoint inventory, auth and
access-control coverage, doc-vs-code drift, and curated risk greps. Model
judgment is then spent only on what they surface plus targeted reading. This is
what keeps a full run affordable and reproducible.

If a script fails because it does not match the project's structure, skip it and
note the gap in the report's coverage section. The scripts are starting points
that handle common patterns; they do not cover every possible framework.

### Phase 2 — Lens sweep

Work `references/lens-checklists.md`, one lens at a time, over the script output
plus targeted file reads. Collect **candidates** — do not write the report yet.

The seven lenses: authorization & access control, input & data integrity,
secrets & sensitive data, error handling & failure modes, architecture &
coupling, plan/doc coherence, compliance & trust claims.

Not every lens applies to every project. Skip lenses that have no surface in the
codebase (e.g., skip compliance & trust claims if there are no planning docs
making claims). Note skipped lenses in the report.

Lenses are independent and may be fanned out to subagents when the user asks for
a full parallel run. If you do: run phase 1 first and hand each subagent the
script output, so no subagent re-explores the tree. Each returns candidates in
the `references/report-format.md` shape, and phase 3 still happens here, once,
over the merged set.

### Phase 3 — Verify (mandatory)

For every candidate: open the cited file at the cited line and confirm the
failure scenario is reachable from the code as written.

- Reproducible from the code → `confirmed`
- Depends on an assumption you cannot check from the repo (a provider's runtime
  behavior, a production config value) → `plausible`, and say what would settle it
- Not reproducible → **drop it**, and do not mention it

Be adversarial against yourself here, not against the code. The most common
failure mode is a candidate that looked wrong in isolation and is handled two
frames up the call stack.

### Phase 4 — Prioritize and write

Severity per `references/severity.md`. Report structure per
`references/report-format.md`. Write to:

```
evaluations/<YYYY-MM-DD>_<subject>_audit.md
```

If the project does not have an `evaluations/` directory, create it.

Order findings P0 → P3. Lead the summary with "Where to start": the single
highest-leverage fix, not a list.

Then write the plain language, and treat it as part of the finding rather than a
summary of it. Each finding gets a `What it means` sentence and a
`How to resolve` sentence under its heading, and the summary carries a table of
all of them. `references/report-format.md` has the rules and the test to apply;
the short version is that a founder reading only the severity and those two
sentences should know whether to care today and roughly what it would take.

Keep `How to resolve` to the shape and size of the fix — one migration, 26 call
sites, a wording change. The implementation detail stays in `Suggested fix`
further down the entry. The two serve different readers; do not collapse them.

Write each sentence once and reuse it in the index, so the two cannot drift. If a
finding resists plain language, that is usually a sign the failure scenario is
still vague — go back and sharpen the scenario rather than writing around it. If
the *resolution* resists plain language, say what decision it waits on instead of
inventing a fix.

### Phase 5 — Hand off

1. If the project has planning docs, propose write-backs under a dated
   heading in whichever doc a confirmed finding settles or contradicts.
2. Propose the dated bullet for `progress.md` if it exists.
3. List recommended follow-up work for every P0 and P1: title, area, and
   suggested priority or test level if the project uses a testing strategy.

Do not create the follow-up items. Do not fix anything. Triage belongs to the
project owner.

## Output contract

- One report file in `evaluations/`, pinned to a git SHA
- Every finding: `file:line`, failure scenario, confidence marker
- Every finding: a jargon-free **What it means** line and a **How to resolve**
  line, directly under its heading — and for table-row findings, in the summary
  index instead
- A **plain-language index** in the summary: one table, every finding at every
  severity, as `Severity | ID | What it means | How to resolve`
- If the project has compliance or trust claims in planning docs: a
  claim-verification table covering every resolved claim
- A coverage-and-limits section saying what was *not* examined
- No code changes

## When the lenses go stale

The harness only finds what the lenses look for. When a new subsystem lands,
`references/lens-checklists.md` should be updated — otherwise this audit
silently stops covering it and reports a clean bill of health it has not earned.
Say so in the report's limits section if you notice a subsystem with no lens
coverage.
