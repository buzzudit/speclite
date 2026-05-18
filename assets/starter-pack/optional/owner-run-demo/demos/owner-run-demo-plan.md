# {{DEMO_NAME}} Owner-Run AI Demo Plan

Status: draft
Owner: {{OWNER}}
Last Updated: {{DATE}}

## Demo Summary

Demo name:

Audience:

What the demo proves:

Starting state:

Ending state:

## Required Local Services

- App:
- Backend/API:
- Database or seed data:
- Browser:
- Harness:

## Required Owner Permissions

- OS input permission:
- Browser inspection permission:
- Automation permission:
- Other:

## Required Browser And Debug Setup

- Browser/profile:
- Remote debugging port:
- Demo URL or route:
- Query flag, for example `?workflowDemo=owner-demo`:

## Required API Keys Or Narration Services

- Narration provider:
- Backend endpoint:
- Required env vars:
- Fallback when unavailable:

## Orchestration Model

Primary orchestrator:

- [ ] `app-orchestrated`
- [ ] `harness-orchestrated`
- [ ] `hybrid`

Why this model:

Start button semantics:

- [ ] Runs the whole demo
- [ ] Arms the harness
- [ ] Begins a hybrid handoff
- [ ] No visible Start button

Progression owner:

Handoff contract, if hybrid:

Completion signal required before advancing:

## App State Contract

Window state object:

```ts
window.__ownerRunDemo
```

Required fields:

- `ownerDemo`:
- `orchestrationModel`:
- `state`:
- `phase`:
- `stepId`:
- `currentStep`:
- `runId`:
- `narrationStatus`:
- `actionStatus`:
- `canAdvance`:
- `lastCompletedAction`:
- `lastCompletedStep`:
- `route`:
- `pendingAction`:
- `timingFallback`:
- `error`:

## Stable DOM Target List

| Target id | Attribute | Purpose | Route/screen | Notes |
| --- | --- | --- | --- | --- |
| start-button | `data-demo-tour="start-button"` | Start demo | | |
| jira-key | `data-demo-field="jira-key"` | Fake typing field | | |
| deep-agent | `data-demo-result-panel="deep-agent"` | Result panel | | |

## Narration Steps

| Step id | Label | Narration goal | Min step ms | Notes |
| --- | --- | --- | --- | --- |
| 01-intro | Intro | | | |

## Step Synchronization Contract

Required invariant:

```ts
nextStep.narrationStart >= currentStep.narrationComplete
nextStep.narrationStart >= currentStep.actionComplete
nextStep.narrationStart >= currentStep.settleComplete
```

| Step id | Narration owner | Action owner | Advance trigger | Completion signal |
| --- | --- | --- | --- | --- |
| 01-intro | app | harness | narration-and-action-complete | |

| Step id | narrationStart | narrationComplete | actionStart | actionComplete | settleComplete | advanceAllowed |
| --- | --- | --- | --- | --- | --- | --- |
| 01-intro | | | | | | |

## Visible Cursor Actions

| Step id | Move targets | Click target | Scroll target | Waits |
| --- | --- | --- | --- | --- |
| 01-intro | | | | |

## Fake Typing Segments

| Step id | Target | Value | Clear first | Delay ms | Notes |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## Wait Conditions

| Step id | Kind | Target | Timeout ms | Failure message |
| --- | --- | --- | --- | --- |
| | target-visible | | | |
| | route | | | |
| | job-complete | | | |

## Failure And Abort Behavior

- Escape:
- Ctrl-C:
- Missing target:
- Narration unavailable:
- Unsupported platform:
- Backend/API failure:

## Acceptance Criteria

- [ ] Hidden owner-demo mode is available behind an owner-only flag.
- [ ] Normal user behavior is unchanged outside owner-demo mode.
- [ ] Primary orchestration model is declared before implementation.
- [ ] Start button semantics are explicit and verified.
- [ ] One runner owns step progression.
- [ ] Narration and visible actions do not advance as separate uncoordinated systems.
- [ ] Next step narration starts only after current narration, action, and settle phases complete.
- [ ] Manual advance is disabled while narration or action is running.
- [ ] Stable `data-demo-*` targets exist for every visible action.
- [ ] App exposes readable `window.__ownerRunDemo` state.
- [ ] App owns live AI narration and prevents overlapping playback.
- [ ] Narration completion is awaitable or has a recorded timeout fallback.
- [ ] Action completion is awaitable or has an observed completion signal.
- [ ] Harness uses OS-level input for visible cursor movement, clicks, and scrolling.
- [ ] Harness uses browser automation only for state, route, readiness, and bounds.
- [ ] Harness re-measures targets before every visible action.
- [ ] Verification proves visible actions happened and rejects speech-only advancement.
- [ ] Fake typing, if used, looks browser-real.
- [ ] Failure states are visible and include the current step.
- [ ] Owner setup and rerun instructions are documented.

## Test Plan

Test level:

Static checks:

Harness dry run:

Visual verification:

Narration verification:

Synchronization verification:

Visible action evidence:

Abort verification:

Residual risk:
