# {{PROJECT_NAME}} Owner-Run AI Demo Workflows

Status: optional module
Last Updated: {{DATE}}

## Purpose

Use this module when a repo needs a repeatable owner-run demo where AI launches the demo, drives the visible workflow, and narrates the flow live.

Core framing:

> Two-in-One Demo: the demo is launched by AI. The AI scripts the mouse movement, keyboard-style input, clicks, triggers, and waits, while the voiceover is generated live by AI.

This is an owner or team-run capability for demos, sales recordings, founder walkthroughs, or review sessions. It is not a polished public end-user feature.

## When To Use

Use this pattern when:

- the app is owned by the team and can expose hidden demo state safely
- the demo needs the real OS cursor to move, click, scroll, and wait visibly
- narration should be generated live by AI and synchronized with the visual workflow
- the workflow benefits from stable app state, explicit targets, and repeatable timing
- a local AI agent or owner environment can run a harness script

Avoid this pattern when:

- the target is mostly arbitrary third-party webpages
- the app cannot expose stable state or DOM targets
- an ordinary scripted video, static walkthrough, or product tour is enough
- owner machines cannot grant OS input or browser inspection permissions

This works best for apps we own. It is more brittle on arbitrary webpages because the app cannot provide fake typing, stable targets, narration checkpoints, or reliable workflow state.

## Architecture

### App Responsibilities

The app owns demo state and narration.

- expose hidden owner-demo mode, usually behind a query flag such as `?workflowDemo=owner-demo`
- publish workflow state on `window`, for example `window.__ownerRunDemo`
- render stable DOM targets using explicit `data-demo-*` attributes
- own narration playback and run state
- own app-side fake typing when fake typing is acceptable
- keep normal user behavior unchanged outside owner-demo mode
- fail visibly when narration or required workflow state is unavailable

### Harness Responsibilities

The local harness owns orchestration and visible OS input.

- run locally from the AI or owner environment
- open or focus the browser
- use CDP, Playwright, browser APIs, or equivalent only to read DOM bounds, route, readiness, and workflow state
- use real OS-level input for visible mouse movement, clicks, and scrolling
- re-measure targets before every visible action
- sequence workflow steps, waits, typing, narration checkpoints, and abort behavior
- stop cleanly on Escape, Ctrl-C, or failure

Do not use browser JavaScript clicks for visible actions. Do not add a fake pointer overlay.

## Browser State Contract

Expose a small state object on `window.__ownerRunDemo`. Keep the shape stable so the harness can inspect readiness and failure without coupling to framework internals.

```ts
type OwnerRunDemoPhase =
  | 'idle'
  | 'loading'
  | 'prepare'
  | 'preAction'
  | 'narrating'
  | 'settle'
  | 'advance'
  | 'complete'
  | 'unsupported'
  | 'error'

interface OwnerRunDemoState {
  ownerDemo: boolean
  state: 'idle' | 'running' | 'complete' | 'unsupported' | 'error'
  phase: OwnerRunDemoPhase
  stepId: string | null
  runId: number
  route?: string
  activeJob?: unknown
  pendingAction?: string | null
  error?: string | null
}
```

Rules:

- `ownerDemo` is `true` only in the hidden owner-demo mode.
- `runId` changes when a new run starts, so stale audio, timers, or harness loops can abort.
- `phase` should make waits explicit enough for the harness to avoid racing the UI.
- `error` must be visible in the app and readable by the harness.

## Step Metadata Contract

Keep workflow steps declarative. The app may own the list, the harness may own the list, or both may share a checked-in JSON/TS module. The key rule is that every visible action maps to stable targets and wait conditions.

```ts
interface OwnerRunDemoStep {
  id: string
  label: string
  narration: string
  route?: string
  primaryTarget: string
  moveTargets: string[]
  clickTarget?: string
  scrollTarget?: string
  typing?: Array<{
    target: string
    value: string
    delayMs?: number
    clearFirst?: boolean
  }>
  waitFor?: Array<{
    kind: 'target-visible' | 'route' | 'network-idle' | 'job-complete' | 'custom'
    target?: string
    timeoutMs?: number
  }>
  beforeNarrationMs?: number
  minStepMs?: number
  afterActionMs?: number
}
```

## Stable Target Conventions

Use explicit attributes. Do not rely on visible text selectors.

Recommended examples:

- `data-demo-tour="start-button"`
- `data-demo-route="settings"`
- `data-demo-tab="reconciled"`
- `data-demo-field="jira-key"`
- `data-demo-result-panel="deep-agent"`

Guidelines:

- targets should be stable across copy changes
- targets should be present only where they are meaningful
- interactive targets should have real browser focus, disabled, visibility, and pointer behavior
- harness measurement should reject hidden, disabled, zero-size, or pointer-blocked targets

## Harness Guidance

Recommended local harness:

- put the runner at `scripts/demo/run-owner-demo.mjs`
- launch or attach to Chrome with remote debugging enabled
- use CDP WebSocket or Playwright only for measurement and state
- read `window.__ownerRunDemo`
- query `[data-demo-*]` targets
- measure `getBoundingClientRect()`
- detect disabled, visible, and receives-pointer state
- use OS-level input for real visible actions

The harness should re-measure before every mouse move, click, scroll, and typing segment. Layout can shift during narration, loading, route changes, and animations.

Abort behavior:

- Escape or Ctrl-C stops orchestration
- the harness releases any held input state
- the app marks the run as `error` or returns to `idle`
- failures include the current step id, target, wait condition, and visible message

## macOS Implementation Guidance

Use Node for orchestration and Python `ctypes` with CoreGraphics for real cursor events.

Recommended approach:

- Node harness manages browser attachment, state reads, timing, and step sequencing
- Python helper emits OS-level events through CoreGraphics
- mouse movement uses eased paths with multiple small moves
- clicks use real mouse down/up events
- scrolling uses real wheel events
- avoid compiled native helpers unless already approved

CoreGraphics APIs commonly used:

- `CGEventCreateMouseEvent`
- `CGEventCreateScrollWheelEvent`
- `CGEventPost`

Unsigned compiled helpers may be blocked by enterprise tools such as Airlock or Santa. Prefer Python/CoreGraphics or already-approved system tools.

## Windows And Linux Portability

Each platform must preserve the rule that visible actions come from OS-level input, not invisible browser JavaScript.

Windows options may include PowerShell, .NET, or Python libraries capable of moving the real cursor and sending real clicks, scrolls, and key events.

Linux options may include `xdotool`, `ydotool`, or desktop-environment-specific APIs, depending on display server and permissions.

Before running the full demo, confirm the chosen tool can move the actual cursor on the owner machine.

## Narration Rules

Voiceover is live AI narration, preferably generated through the app backend or app-controlled endpoint.

- only one audio element and run id may be active at a time
- prefetch next clips where possible
- playback may be slightly faster than normal
- a step must not advance until both audio has ended and the minimum visual timing has elapsed
- narration must not overlap or get cut off
- fail visibly if narration is unavailable
- the harness should wait for app-owned narration checkpoints instead of guessing audio duration

## Input Rules

Real mouse means the actual OS cursor.

Fake keyboard is acceptable only when it looks browser-real:

- real field focus
- visible caret
- character-by-character typing
- app state updated naturally

For external or unowned websites, prefer real keyboard events because app-side fake typing is unavailable.

## Owner Permissions And Setup

### macOS

Before running a demo:

- grant Accessibility permission to the app that runs the harness, such as Terminal, iTerm, Codex, or the relevant agent app
- if using Apple Events or `osascript`, enable browser automation permissions as needed
- for Chrome Apple Events, allow JavaScript from Apple Events if that path is used
- accept macOS Automation prompts when one app controls another
- launch Chrome with remote debugging when needed, for example:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9223 \
  --user-data-dir=/tmp/owner-demo-chrome-profile
```

Troubleshooting:

- if the cursor does not move, check Accessibility permission first
- if the browser cannot be inspected, check the remote debugging port and profile
- if narration fails, check API keys and backend availability
- if an unsigned helper is blocked, prefer Python/CoreGraphics or approved system tools

### Windows And Linux

Equivalent OS input permissions or tools may be required. The owner should confirm the automation tool can move the real cursor before running the full demo.

For browser inspection, launch or attach to a browser profile that allows the harness to read state and DOM bounds. Keep this profile separate from everyday browsing when practical.

## Verification Checklist

Before accepting a demo workflow:

- [ ] Hidden owner-demo mode does not affect normal user behavior.
- [ ] `window.__ownerRunDemo` is present only in owner-demo mode.
- [ ] Required `data-demo-*` targets are stable and do not rely on text selectors.
- [ ] Harness uses browser automation only for state, readiness, and bounds.
- [ ] Visible mouse movement, clicks, and scrolling use OS-level input.
- [ ] Targets are re-measured before every visible action.
- [ ] Narration is generated live, app-owned, and synchronized with step advancement.
- [ ] Audio never overlaps or gets cut off during normal runs.
- [ ] Fake typing, when used, shows real focus, caret, and character-by-character entry.
- [ ] Escape or Ctrl-C aborts cleanly.
- [ ] Missing narration, missing targets, or unsupported platform fail visibly.
- [ ] Build, lint, typecheck, or static checks pass for the changed app.
- [ ] The owner setup instructions include required permissions, browser launch, and API keys.
- [ ] The README or runbook documents how to rerun the demo.
