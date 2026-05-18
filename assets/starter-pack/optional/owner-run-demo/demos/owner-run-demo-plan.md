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

## App State Contract

Window state object:

```ts
window.__ownerRunDemo
```

Required fields:

- `ownerDemo`:
- `state`:
- `phase`:
- `stepId`:
- `runId`:
- `route`:
- `pendingAction`:
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
- [ ] Stable `data-demo-*` targets exist for every visible action.
- [ ] App exposes readable `window.__ownerRunDemo` state.
- [ ] App owns live AI narration and prevents overlapping playback.
- [ ] Harness uses OS-level input for visible cursor movement, clicks, and scrolling.
- [ ] Harness uses browser automation only for state, route, readiness, and bounds.
- [ ] Harness re-measures targets before every visible action.
- [ ] Fake typing, if used, looks browser-real.
- [ ] Failure states are visible and include the current step.
- [ ] Owner setup and rerun instructions are documented.

## Test Plan

Test level:

Static checks:

Harness dry run:

Visual verification:

Narration verification:

Abort verification:

Residual risk:
