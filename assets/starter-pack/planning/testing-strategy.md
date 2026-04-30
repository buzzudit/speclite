# {{PROJECT_NAME}} Testing Strategy

Status: active baseline
Last Updated: {{DATE}}

## Purpose

Choose verification depth consistently and record what was actually checked.

## Core Rules

- every story must declare a `Test Level`
- every completed story must record verification in `Done Evidence`
- when a relevant test cannot be run, record the blocker, fallback check, and remaining risk
- code and workflow changes should prefer layered automated verification over manual-only checks when practical
- documentation-only work may use lighter verification when the risk is low

## Test Levels

### Level 0

Use for captured work that is not ready for meaningful verification.

Expected verification:

- basic file or status correctness only

### Level 1

Use for documentation, planning artifacts, story bookkeeping, and low-risk copy changes.

Expected verification:

- `git diff --check`
- targeted searches for required terms or decisions
- manual review against upstream planning documents

### Level 2

Use for low-risk implementation work with limited surface area.

Expected verification:

- Level 1 checks
- at least one runnable smoke test, preview check, or equivalent execution path
- manual confirmation of the changed behavior

### Level 3

Use for medium-risk logic, integrations, or multi-step workflows.

Expected verification:

- Level 2 checks
- targeted automated tests
- edge-case or negative-path verification where failure would be user-visible

### Level 4

Use for launch-critical, compliance-sensitive, submission, pricing, or infrastructure work.

Expected verification:

- Level 3 checks
- broad automated coverage for the changed path
- explicit remaining-risk review

## Default Policy

- planning and story-management work defaults to Level 1
- implementation work should usually start at Level 2 or above
- compliance-sensitive behavior should assume Level 3 or Level 4 by default
