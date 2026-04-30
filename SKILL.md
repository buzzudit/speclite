---
name: speclite
description: Scaffold or adapt a lightweight project operating system for a new repo or a mature planning-first workspace. Use when Codex needs to bootstrap a repo, merge into an already-operating workflow, create or adapt planning docs, enforce story-driven execution, add testing and design policy, or tighten an existing operating model without inventing parallel structure.
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

## Story-Driven Execution Protocol

No implementation without a story when the repo uses story management.

For non-trivial work, stories should include lightweight traceability to the upstream plan, step, or canonical document they advance.

Keep traceability story-first and minimal: cite the related path or story ID and one short reason. Do not require trace links for trivial bookkeeping or low-substance admin changes.

For behavior-changing stories, include a compact `Spec Delta` section.

Use `Added`, `Changed`, and `Removed` headings and keep each item to a one-line impact statement. Do not require spec delta for pure refactors, file moves, or bookkeeping-only stories.

Minimum protocol:

1. Start from a story, not an untracked task.
2. Pull the story from `ready` to `doing` before implementation.
3. Update the story metadata and `stories/index.md`.
4. Make the checkpoint commit when the repo's workflow expects it.
5. Implement the change.
6. Verify at the appropriate test level.
7. Record done evidence, including verification and residual risk.
8. Move the story to its final status folder.
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
