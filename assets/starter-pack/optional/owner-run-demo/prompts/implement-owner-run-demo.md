# Implement Owner-Run AI Demo Workflow

Use this prompt when asking an agent to add a real owner-run demo to a target repo.

## Prompt

You are working in `{{TARGET_REPO}}`.

Goal:
Implement an owner-run AI demo workflow using the Speclite Owner-Run AI Demo pattern.

Core framing:
Two-in-One Demo: the demo is launched by AI. The AI scripts the mouse movement, keyboard-style input, clicks, triggers, and waits, while the voiceover is generated live by AI.

Rules:

- Inspect the target app before editing.
- Preserve the app's existing architecture and conventions.
- Keep this owner-run, hidden, and local-first.
- Do not add a polished public end-user demo feature.
- Do not add a fake pointer overlay.
- Do not require a compiled native helper.
- Do not depend on brittle text selectors.
- Do not use browser JavaScript clicks for visible actions.
- Visible cursor movement, clicks, and scrolling must use real OS-level input.
- Browser automation may be used only to read state, route, readiness, DOM targets, and bounds.

Implementation steps:

1. Inspect the target app, routes, existing scripts, and local run commands.
2. Identify the demo workflow, audience, starting state, ending state, and required services.
3. Add hidden owner-demo mode, usually behind `?workflowDemo=owner-demo`.
4. Add stable DOM targets using explicit `data-demo-*` attributes.
5. Add app-side owner demo state on `window.__ownerRunDemo`.
6. Add app-side narration state and live AI narration playback.
7. Add app-side fake typing only where it can look browser-real.
8. Add a local harness under `scripts/demo/`, for example `scripts/demo/run-owner-demo.mjs`.
9. Use OS-level input for visible mouse movement, clicks, and scrolling.
10. Use CDP, Playwright, browser APIs, or equivalent only for state and bounds.
11. Re-measure targets before every visible action.
12. Add owner permission and setup instructions for the supported platform.
13. Verify the workflow visually and with the repo's build, lint, typecheck, or static checks.
14. Document how to rerun it.

App state schema:

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

Step metadata schema:

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

Stable target examples:

- `data-demo-tour="start-button"`
- `data-demo-route="settings"`
- `data-demo-tab="reconciled"`
- `data-demo-field="jira-key"`
- `data-demo-result-panel="deep-agent"`

macOS harness guidance:

- Use Node for orchestration.
- Use Python `ctypes` with CoreGraphics for real cursor events.
- Use `CGEventCreateMouseEvent`, `CGEventCreateScrollWheelEvent`, and `CGEventPost`.
- Smooth mouse movement with eased paths.
- Click with real mouse down/up events.
- Scroll with real wheel events.
- Avoid compiled native helpers unless already approved.

Owner setup guidance:

- Document Accessibility permission for Terminal, iTerm, Codex, or the relevant agent app.
- Document browser automation permissions when Apple Events or `osascript` are used.
- Document Chrome remote debugging launch, for example `--remote-debugging-port=9223` and `--user-data-dir=/tmp/owner-demo-chrome-profile`.
- Document API keys and backend availability required for live narration.
- For Windows/Linux, document equivalent OS input permissions and tools.

Acceptance criteria:

- The owner-demo mode is hidden and normal user behavior is unchanged.
- `window.__ownerRunDemo` exposes readable state and visible errors.
- Stable `data-demo-*` targets exist for every action.
- Live AI narration is app-owned, synchronized, and does not overlap.
- The harness uses OS-level input for visible actions.
- The harness uses browser automation only for measurement and state.
- Missing targets, unsupported platforms, narration failures, and aborts fail cleanly.
- Setup and rerun instructions are documented.
- The repo's relevant validation checks pass, or blocked checks are recorded with fallback verification and residual risk.
