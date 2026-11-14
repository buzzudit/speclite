---
name: speclite
description: Scaffold or adapt a lightweight project operating system for a new repo or a mature planning-first workspace. Use when Codex needs to bootstrap a repo, merge into an already-operating workflow, create or adapt planning docs, enforce story-driven execution, add testing and design policy, tighten an existing operating model without inventing parallel structure, produce a narrated walkthrough video of a product (Demo Maker), or build a new Claude Code skill from domain expertise (Skill Builder).
---

# Speclite

Create or adapt a planning-first project operating model using the starter templates in `assets/starter-pack/`. This skill has two equally important jobs:

- bootstrap a new or lightly structured repo
- operate inside an already-structured planning-first repo without breaking its live conventions

Default to adapting the repo that exists, not replacing it with a generic scaffold.

## Operating Modes

Choose one of these repo modes first:

- Bootstrap mode: use when the repo is empty, nearly empty, or clearly missing the operating system needed for planning-first execution.
- Existing-repo mode: use when the repo already has planning docs, story folders, testing policy, bootstrap steps, or other active operating conventions.

Within either repo mode, use one of these interaction modes:

- Guided mode: if the request is underspecified, ask only for project name, project type, audience/user, planning-first vs app-first posture, whether the repo is being bootstrapped or adapted, and whether stories, testing, bootstrap, compliance, or design modules are needed.
- Fast-path mode: if the brief and repo shape are explicit enough, restate your assumptions and scaffold or adapt immediately.

Default to existing-repo mode when there is meaningful structure on disk. Default to guided mode only when the brief is too thin to avoid avoidable rework.

## Single-Person Planning Budget

Use a single-person planning budget by default.

Rules:

- planning budget varies by repo maturity
- in new or lightly structured repos, establish only the minimum operating artifacts needed to begin execution
- in mature repos, prefer updating existing canonical docs and stories over creating new planning artifacts
- keep planning outputs short and few by default
- allow more planning only when compliance, pricing, workflow, integration, launch, or comparable execution risk materially justifies it
- when lite and risk conflict, bias to risk

## Default Pack

Default scaffold:

- root operating docs
- `planning/vision.md`
- `planning/bookkeeping.md`
- `planning/story-management.md`
- `planning/testing-strategy.md`
- `planning/design-direction.md`
- `stories/index.md`

Do not add bootstrap steps by default in Bootstrap mode. Add the bootstrap module when the user explicitly asks for a sequenced plan or when the existing repo already uses bootstrap-step execution.

Do not add the compliance module unless the project touches legal, privacy, safety, claims, regulated, or trust-sensitive work, or the existing repo already treats compliance as a canonical operating constraint.

Do not add the design module only as decoration. Add it when the repo is design-sensitive, UI-facing, messaging-sensitive, or already manages design artifacts in-repo.

## Canonical Documents

When these files exist, treat them as authoritative unless the user explicitly asks to change them:

- `planning/regulations.md`
- `planning/bootstrap-plan.md`
- `planning/story-management.md`
- `planning/testing-strategy.md`
- `planning/design-direction.md`

Implications:

- read them before proposing structural changes
- adapt new work to them rather than layering generic defaults on top
- do not create parallel docs that duplicate their authority
- if two canonical docs conflict, surface the conflict and propose a narrow fix instead of silently choosing one

If a repo already has a clear equivalent under a different name, adapt to the repo's convention rather than forcing these exact filenames.

## Decision Tree

1. Inspect the repo before writing anything.
2. Decide whether this is Bootstrap mode or Existing-repo mode.
3. If the repo is empty or nearly empty, scaffold the default pack unless the user asked for a lighter setup.
4. If the repo already has operating docs, story folders, testing policy, bootstrap steps, or design artifacts, read those first and add only what is missing.
5. If the repo has coherent but different conventions, adapt to them rather than overwriting them.
6. If canonical docs already exist, preserve their authority and merge intentionally.
7. If the user asks for a lighter or app-first setup, scaffold only the requested modules and keep planning overhead low.

Do not replace substantial existing docs without an explicit user request.
Do not create a second operating system inside a repo that already has one.

## Module Selection

Use these module rules:

- Core module: always offer `agents.md`, `progress.md`, `planning/vision.md`, and `planning/bookkeeping.md`.
- Stories module: add `planning/story-management.md` and `stories/index.md` when the project benefits from tracked execution work. If stories already exist, treat story-driven execution as mandatory.
- Testing module: add `planning/testing-strategy.md` when the repo will contain implementation work, integration work, or any meaningful review/verification surface.
- Bootstrap module: add `planning/bootstrap-plan.md` and `steps/step-01.md` when the user wants ordered milestone execution or when the repo already uses numbered step outputs.
- Compliance module: add `planning/regulations.md` only for trust-heavy or sensitive projects.
- Design module: add `planning/design-direction.md` and `design/` guidance when the project has a marketing site, product UX, operational surfaces, or meaningful visual/messaging design work.
- Demo Maker module: add `planning/demo-maker-workflows.md`, `demos/demo-plan.md`, `prompts/implement-demo-maker.md` and the `tour/` tooling when the user wants a narrated walkthrough video of a web app or prototype, with an AI voiceover in sync with scripted on-screen actions.
- Owner-run demo module: add `planning/owner-run-demo-workflows.md`, `demos/owner-run-demo-plan.md`, and `prompts/implement-owner-run-demo.md` when the user wants an AI-launched owner demo where AI scripts visible mouse movement, keyboard-style input, clicks, waits, triggers, and live AI narration.
- Scenario Mould module: add `.claude/skills/scenario-mould/` (SKILL.md, references, scripts) when the project has UI components that depend on variable content, server-driven lists, or multiple data states and must survive a range of viewports. The mould generates and stress-tests scenarios across layout, data state, content, interaction, and accessibility dimensions with an offline HTML model and a severity-rated report.
- Heuristic Evaluation module: add `.claude/skills/heuristic-evaluation/` (SKILL.md) when the project needs structured UX review. A 12-heuristic framework: the NNG 10, a Human-Centered AI heuristic, and a Product-Market Alignment heuristic for startups and early-stage products. Pairs well with the Scenario Mould — both use the same 0–4 severity scale.
- Skill Builder module: add `.claude/skills/skill-builder/` (SKILL.md, references, scripts, schemas, templates) when the user wants to encode a methodology, playbook, or domain expertise as a reusable Claude Code skill. The builder interviews the author, auto-gathers provenance (academic and industry), generates typed ports for composition, scaffolds verification scripts, and produces a complete skill package. Invoke with `/skill-builder`.

If the user asks for a minimal setup, the safe fallback is core only.

## Repo Adaptation Rules

In Existing-repo mode:

- prefer merging into the established operating model over copying templates
- treat the current foldering, naming, and story flow as the default unless the user asked for a reset
- add missing modules only when they solve a real gap
- update existing docs in place when possible instead of creating alternates
- keep repo-specific terminology if it already maps cleanly to the same concepts
- keep artifact count and artifact length minimal by default, especially in mature repos

Use starter templates as reference material, not as a reason to overwrite mature docs.

## Scaffolding Rules

When you scaffold:

- Copy the closest starter templates from `assets/starter-pack/`, then adapt placeholders and wording for the actual project.
- Prefer sparse roots and consistent foldering.
- Keep planning docs separate from execution stories.
- If the stories module is present, require story-driven implementation with the full lifecycle below.
- Require a `Test Level` before implementation when the testing module is present.
- Require verification and done evidence on completed stories.
- Update `progress.md` when project direction, active work, or status materially changes.
- State the selected modules and assumptions in your response.
- Keep the initial planning surface as small as the repo can support safely.

For existing repos, merge intentionally. Do not duplicate policies or create parallel systems unless the user explicitly wants a reset.

## Version Control Guidance

When Speclite spawns or bootstraps a project:

- **Create a local repo if not present.** If the target directory is not already a git repository, run `git init` and make an initial commit with the scaffolded files before proceeding. A project without version control from the start loses history that matters later.
- **Commit often.** The agent should commit automatically after completing each meaningful unit of work — a story, a planning doc, a scaffold pass, a fix. Small, frequent commits are cheaper than reconstructing intent from a large diff. Do not batch unrelated changes or wait for the user to ask.
- **Suggest a push after major work.** After completing a significant milestone — a module scaffold, a batch of stories, a bootstrap step, a skill installation — remind the user to push to the remote if one is configured. The agent should not push without the user's confirmation, but should surface the prompt so work is not stranded locally.

## Story-Driven Execution Protocol

No implementation without a story when the repo uses story management.

For non-trivial work and small planning work, stories should include lightweight traceability to the upstream plan, step, or canonical document they advance.

Keep traceability story-first and minimal: cite the related path or story ID and one short reason. Do not require trace links for trivial bookkeeping or low-substance admin changes.

For behavior-changing stories, include a compact `Spec Delta` section.

Use `Added`, `Changed`, and `Removed` headings and keep each item to a one-line impact statement. Do not require spec delta for pure refactors, file moves, or bookkeeping-only stories.

Minimum visible protocol:

1. Start from a story, not an untracked task.
2. Create or move the story to `doing` before implementation or planning edits.
3. Update the story metadata and `stories/index.md`.
4. Make the checkpoint commit when the repo's workflow expects it.
5. Implement the change.
6. Verify at the appropriate test level.
7. Record done evidence, including verification and residual risk.
8. Move the story to `done` when complete.
9. Update `stories/index.md` again.
10. Make the completion commit when the repo's workflow expects it.

If the story becomes blocked or unclear mid-stream, move it to `blocked` and record the blocker rather than continuing informally.

## Story Path Enforcement

When a repo uses markdown story management, enforce folder-path correctness:

- story path must be `stories/<area>/<status>/story-file.md`
- `Area` metadata must match `<area>`
- `Status` metadata must match `<status>`
- if `Area` or `Status` changes, move the file in the same change

Do not leave a story's metadata and file path out of sync.

## Testing Policy

When the repo uses a testing strategy, prefer a concrete test-level system over vague guidance.

Use the presence of a `Spec Delta` to clarify when behavior changed and therefore needs behavior-appropriate verification. Do not require a spec delta section for non-behavioral work.

Recommended levels:

- Level 0: captured/admin work with no substantive artifact
- Level 1: documentation, planning, queue, and bookkeeping work
- Level 2: low-risk product or site changes with smoke coverage
- Level 3: medium-risk logic, integrations, or workflow changes with targeted automated tests
- Level 4: launch-critical, pricing, access, compliance-sensitive, or broad-regression-risk changes with comprehensive verification

Rules:

- choose the highest level justified by risk, not the easiest level to satisfy
- require verification depth proportional to the story's risk
- prefer layered automated verification over manual-only checks when practical
- require completed stories to record what was run and what risk remains

## Fallback Verification

If a relevant test cannot run, record all of the following in the story:

- what was not run
- why it was blocked or unavailable
- what fallback check was used instead
- the residual risk

Do not treat missing test execution as silently acceptable.

## Bootstrap-Step Repos

If `planning/bootstrap-plan.md` exists, treat it as the canonical sequence for milestone execution.

Rules:

- each numbered step should produce `steps/step-nn.md` with two-digit numbering
- major supporting artifacts for a step should keep the same step prefix
- do not treat bootstrap sequencing as optional if the repo already runs on it
- when a new step is added, keep the numbering and step outputs consistent with the existing sequence
- for non-trivial stories tied to a bootstrap step, include a simple story-level trace link back to the relevant step or canonical planning document

## Template Map

Starter templates live here:

- `assets/starter-pack/root/agents.md`
- `assets/starter-pack/root/progress.md`
- `assets/starter-pack/planning/vision.md`
- `assets/starter-pack/planning/bookkeeping.md`
- `assets/starter-pack/planning/story-management.md`
- `assets/starter-pack/planning/testing-strategy.md`
- `assets/starter-pack/planning/design-direction.md`
- `assets/starter-pack/stories/index.md`
- `assets/starter-pack/stories/story-template.md`
- `assets/starter-pack/optional/compliance/planning/regulations.md`
- `assets/starter-pack/optional/bootstrap/planning/bootstrap-plan.md`
- `assets/starter-pack/optional/bootstrap/steps/step-01.md`
- `assets/starter-pack/optional/owner-run-demo/planning/owner-run-demo-workflows.md`
- `assets/starter-pack/optional/owner-run-demo/demos/owner-run-demo-plan.md`
- `assets/starter-pack/optional/owner-run-demo/prompts/implement-owner-run-demo.md`

- `assets/starter-pack/optional/demo-maker/planning/demo-maker-workflows.md`
- `assets/starter-pack/optional/demo-maker/demos/demo-plan.md`
- `assets/starter-pack/optional/demo-maker/prompts/implement-demo-maker.md`
- `assets/starter-pack/optional/demo-maker/tooling/` (`lib.mjs`, `voice.mjs`, `mux.mjs`, `script.template.mjs`, `walkthrough.template.mjs`)

- `assets/starter-pack/optional/scenario-mould/` (complete Claude Code skill: `SKILL.md`, `references/` with session-guide, mould-contract, enforcement, report-format, designer-testing, mould-reference.html; `scripts/` with verify_session.py, verify_mould.py, verify_browser.cjs, verify_delivery.py)

- `assets/starter-pack/optional/heuristic-evaluation/SKILL.md` (single-file Claude Code skill: 12-heuristic UX evaluation framework)

- `assets/starter-pack/optional/skill-builder/` (complete Claude Code skill: `SKILL.md`, `references/` with interview-guide, generation-contract, provenance-guide, port-catalog; `scripts/` with validate_manifest.py, validate_skill_package.py, discover_compositions.py)
- `assets/skill-builder/schemas/` (skill-manifest.schema.json, port-types.json, deliverable-types.json)
- `assets/skill-builder/templates/` (shape templates for session-flow, reference, one-shot, recurring-check; deliverable templates; verification script templates)

Use these as starting points, not immutable output. Replace placeholders such as `{{PROJECT_NAME}}`, `{{PROJECT_TYPE}}`, and `{{PRIMARY_USER}}`.

## Compliance Heuristics

Offer the compliance module when the project mentions any of these themes:

- regulated industries
- user data, privacy, or security
- legal review
- claims handling
- medical, insurance, finance, payroll, or safety-sensitive workflows
- public trust, outbound claims, or approval-heavy operations

If the user says the project is low-risk and internal, skip this module unless asked.

## Design Module

Treat design as a first-class operating artifact when the repo is design-sensitive.

At minimum, distinguish between:

- marketing-site design
- product UX
- internal ops surfaces

Do not treat design as one undifferentiated bucket when the surfaces have different audiences, constraints, or compliance posture.

### Design Outputs

When the design module is active, expect some combination of:

- `planning/design-direction.md` as the canonical design brief
- `design/` for prompt packs, wireframes, comparative explorations, and review notes
- low-fidelity wireframes
- prompt packs for external design generation tools when relevant
- review artifacts that compare options and lock a direction

If UI implementation is planned, require a canonical design brief before implementation starts.

### Design Acceptance Criteria

Design work should be reviewable against explicit criteria such as:

- audience fit
- boundary compliance
- CTA clarity
- mobile behavior
- implementation readiness

For trust-heavy or regulated work, also verify that design and copy stay within the repo's compliance and marketing boundaries.

### Design Handoff

Do not jump from idea to build without a locked design direction when the repo is design-sensitive.

Before UI implementation:

- tie design work to a story
- capture the selected direction in the canonical design brief or equivalent
- record why rejected directions were not chosen when that context matters
- confirm implementation is following the chosen surface, not a blended compromise

### Design Verification

When verifying design work, use checks that fit the surface:

- rendered review
- responsive review
- consistency review against planning docs
- consistency review against regulatory or trust-boundary docs when applicable

## Owner-Run Demo Module

Use this optional module when the repo needs a repeatable owner-run AI demo workflow, not a public product tour.

Core framing:

> Two-in-One Demo: the demo is launched by AI. The AI scripts the mouse movement, keyboard-style input, clicks, triggers, and waits, while the voiceover is generated live by AI.

Add this module when:

- the app is owned by the team and can expose hidden demo state
- visible actions must use the real OS cursor
- live AI narration needs to be synchronized with app workflow state
- a local owner or AI environment can run a harness script

Do not add this module for arbitrary webpages, a fake pointer overlay, or a public end-user demo feature.

Scaffold from:

- `assets/starter-pack/optional/owner-run-demo/planning/owner-run-demo-workflows.md`
- `assets/starter-pack/optional/owner-run-demo/demos/owner-run-demo-plan.md`
- `assets/starter-pack/optional/owner-run-demo/prompts/implement-owner-run-demo.md`

Preserve the boundary:

- App responsibilities: hidden owner-demo mode, `window.__ownerRunDemo`, stable `data-demo-*` targets, narration playback, run state, app-side fake typing when appropriate, and visible app failures.
- Harness responsibilities: local orchestration, browser state and bounds reads, target re-measurement, OS-level cursor/click/scroll input, waits, aborts, and failure reporting.

Hard rules:

- every owner demo must declare one primary orchestrator before implementation: `app-orchestrated`, `harness-orchestrated`, or `hybrid`
- do not implement narration and visual actions as separate advancing systems unless the plan defines the handoff contract and completion signals
- browser automation may read state, route, readiness, and DOM bounds
- browser automation must not perform visible clicks
- visible mouse movement, clicks, and scrolling must come from OS-level input
- text selectors are too brittle; use explicit `data-demo-*` attributes
- fake typing is acceptable only when it has real focus, visible caret, character-by-character entry, and natural app state updates
- live narration must not overlap or be cut off
- a step is not complete when narration text changes; it is complete only after narration ended, the visible action finished, and the UI settled
- if the app shows a Start button, define whether it runs the whole demo, arms the harness, or begins a hybrid handoff
- verification must prove visible actions happened, not just narration or state changes

For macOS, the module recommends Node orchestration plus Python `ctypes`/CoreGraphics events such as `CGEventCreateMouseEvent`, `CGEventCreateScrollWheelEvent`, and `CGEventPost`. Avoid compiled native helpers unless already approved because unsigned binaries may be blocked.

## Demo Maker Module

Use this optional module to make a narrated walkthrough video (mp4) of a web app or prototype.

Core framing:

> Demo Maker: write the story as beats, generate the voice first, then record the real product at the pace of the voice, and place every line exactly where its action starts.

How it differs from the owner-run demo: Demo Maker produces a finished video from a headless browser with an injected cursor and click ripples, with pre-generated voice clips placed by timing. The owner-run demo is a live run with the real OS cursor and live narration. Do not mix them; pick one per demo.

Add this module when:

- the product runs in a browser and can be reset to a clean, repeatable start state
- the goal is a shareable or re-recordable walkthrough, concept review or pre-interview asset
- the owner wants an AI voiceover in sync with the visible workflow

Scaffold from:

- `assets/starter-pack/optional/demo-maker/planning/demo-maker-workflows.md`
- `assets/starter-pack/optional/demo-maker/demos/demo-plan.md`
- `assets/starter-pack/optional/demo-maker/prompts/implement-demo-maker.md`
- `assets/starter-pack/optional/demo-maker/tooling/`

Hard rules:

- the product must carry the journey before recording: a first screen that sets up the person and moment, a guided path with one next action per screen, and the strongest moment built as a screen; fix the product first if it does not
- write the beats table first and get the owner's approval of the narration before generating any voice, because the text is sent to the voice service
- the voice key lives in a git-ignored `.env` or the environment; never print it or commit it; if the key lacks a permission, do not work around it and record what could not be verified
- generate all voice clips first and measure them; pace the recording by the clips, never the reverse
- always calibrate picture time against the clock using high-contrast anchors (title card, closing card, chapter labels); the offset varies between runs
- use a full ffmpeg and ffprobe for H.264 and AAC; the bundled Playwright ffmpeg cannot
- use real clicks through the helper and stable selectors, and start from a clean state
- verification must prove sync: length, calibration residuals, frames at beat starts, and audio onsets against placed times; record what a person still has to check by ear

Expressive voice: use `eleven_v3` with performance tags such as [calm], [curious], [thoughtful], [whispers], [short pause], and direct with punctuation. v3 has no request stitching.

## Scenario Mould Module

Use this optional module to generate and stress-test UI component scenarios across viewports, data states, content edge cases, and interaction patterns.

Core framing:

> Scenario Mould: model one component exactly, generate scenarios from its contract, test every scenario × width cell, and rate findings on a shared severity scale.

How it differs from the demo modules: Scenario Mould produces a diagnostic artifact (an offline interactive HTML model and a severity-rated report) for design review and engineering handoff. The demo modules produce presentation artifacts (a live demo or a video). They complement each other — a mould can validate the component before a demo is built.

Add this module when:

- the project has UI components that depend on variable content (server-driven lists, variable label lengths, dynamic counts)
- components must survive a range of viewports, data states (empty, loading, error, partial), or accessibility conditions (200% zoom, forced colors)
- layout or state-handling concerns arise during design review or prototyping
- the team wants engineering-actionable findings with severity ratings and scenario IDs

Do not add this module for projects without meaningful UI components, or for purely backend or CLI work.

Scaffold from:

- `assets/starter-pack/optional/scenario-mould/` — a complete Claude Code skill directory

The module installs as `.claude/skills/scenario-mould/` in the target repo. It contains:

- `SKILL.md` — skill definition with session flow, severity scale, and non-negotiables
- `references/session-guide.md` — Steps 1–4: component selection, output resolution, contract reading, adaptive interview
- `references/mould-contract.md` — Steps 5–6: build contract, invariants, state scenario modelling, verification
- `references/enforcement.md` — decision recording, session JSON schema, browser contract, delivery gate
- `references/report-format.md` — Steps 7–8: report structure, table headers, calibration, handoff
- `references/designer-testing.md` — optional guided testing for designers
- `references/mould-reference.html` — neutral starter (three-tier bar with 16 scenarios and 12 flags including state-aware flags)
- `scripts/verify_session.py` — validates session JSON (Python 3 stdlib only)
- `scripts/verify_mould.py` — validates results-json and report (Python 3 stdlib only)
- `scripts/verify_browser.cjs` — browser interaction checks (Node + Playwright)
- `scripts/verify_delivery.py` — delivery gate with three separate verdicts (Python 3 stdlib only)

Hard rules:

- synthetic data only — never use real user data, PHI, or PII
- one file, zero dependencies — the mould works offline with no CDN or build step
- real measurement with `canvas.measureText`, never character-count estimates
- the mould is a model, not the product — calibration establishes fidelity; severity 3–4 findings must be confirmed in the real build
- scenarios are generated from the component's contract, not random fuzzing — every scenario has an ID, a rationale, and a severity threshold
- state scenarios (empty, loading, error, partial) are first-class — not an afterthought to layout testing
- the delivery gate requires three separate verdicts (contract, browser, calibration) — a single green "passed" is not acceptable

Severity scale (shared with usability heuristic evaluations and UX-copy audits):

| Rating | Label |
|--------|-------|
| 0 | Not a problem |
| 1 | Cosmetic |
| 2 | Minor |
| 3 | Major |
| 4 | Catastrophe |

## Skill Builder Module

Use this optional module to create new Claude Code skills for any domain through
guided conversational interview.

Core framing:

> Skill Builder: interview a domain expert, extract their methodology, ground it
> in academic and industry evidence, and generate a complete Claude Code skill
> package with schemas, reference docs, and verification scripts.

Add this module when:

- the user wants to encode a methodology, playbook, or domain expertise as a
  reusable Claude Code skill
- the user is formalizing an existing process into a repeatable skill
- the user wants to compose existing skills in new ways

Do not add this module for projects that only consume existing skills without
creating new ones.

Scaffold from:

- `assets/starter-pack/optional/skill-builder/` — the Claude Code skill
- `assets/skill-builder/schemas/` — JSON schemas for skill manifests and port types
- `assets/skill-builder/templates/` — shape, deliverable, and verification templates

The module installs as `.claude/skills/skill-builder/` in the target repo, plus
the `assets/skill-builder/` framework files at the repo root. It contains:

- `SKILL.md` — skill definition with nine-step interview flow and four shape
  archetypes (session-flow, reference, one-shot, recurring-check)
- `references/interview-guide.md` — deep methodology extraction playbook
- `references/generation-contract.md` — file generation rules and validation
- `references/provenance-guide.md` — three evidence layers and gathering strategy
- `references/port-catalog.md` — typed port vocabulary for skill composition
- `scripts/validate_manifest.py` — validates skill-manifest.json (Python 3 stdlib)
- `scripts/validate_skill_package.py` — validates a complete skill directory
- `scripts/discover_compositions.py` — finds composable skill pairs by port type

Hard rules:

- every generated skill must have a valid skill-manifest.json
- provenance is required: at least one academic and one industry citation per
  core methodology step; organizational evidence is optional and user-supplied
- verification scripts are auto-generated from quality criteria collected during
  the interview; every skill has at least one automated check
- typed ports are declared for every skill; the builder discovers composition
  opportunities with installed skills
- synthetic data only in all examples
- the builder deeply interviews the author and challenges assumptions; it does
  not accept methodology claims without probing
- templates are starting points, not constraints; the agent adapts structure to
  the domain

Skill shapes:

| Shape | Description | File count |
|-------|-------------|------------|
| session-flow | Multi-step guided session with intake, interview, execution, verification | Full (SKILL.md + references + scripts) |
| reference | Knowledge base the agent consults, not user-invoked | Minimal (SKILL.md + reference entries) |
| one-shot | Input in, single artifact out | Light (SKILL.md + contract + verify script) |
| recurring-check | Periodic assessment against criteria | Medium (SKILL.md + criteria + rubric + verify) |

Provenance layers:

| Layer | Required | Gathered by |
|-------|----------|-------------|
| Academic | Yes | Agent (auto-research during interview) |
| Industry | Yes | Agent (auto-research during interview) |
| Organizational | No | User (prompted during interview) |

## Mature Repo Maintenance

For mature planning-first repos, perform periodic drift checks across the operating system.

At minimum, check for consistency between:

- `planning/`
- active bootstrap steps
- story-management rules
- current story queue and statuses
- current implementation direction
- whether non-trivial stories still trace back to the active plans or steps they are supposed to advance

Use a drift check after a meaningful batch of story completions, such as every five stories, or whenever planning direction may have shifted.

## Expected Output

When you finish, report:

- which repo mode and interaction mode you used
- which modules you scaffolded
- which files were created vs adapted
- the main assumptions you locked
- any canonical docs you treated as authoritative
- whether you merged into an existing operating model or scaffolded a new one
- the next 1-3 setup actions the user should take
