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
- Declare one primary orchestrator before implementation: `app-orchestrated`, `harness-orchestrated`, or `hybrid`.
- Do not let narration and visible actions advance as separate uncoordinated systems.
- A step is complete only after narration ended, visible action completed, and the UI settled.
- If the app shows a Start button, define whether it runs the whole demo, arms the harness, or begins a hybrid handoff.
- Verification must prove visible actions happened, not just narration or state changes.

Implementation steps:

1. Inspect the target app, routes, existing scripts, and local run commands.
2. Identify the demo workflow, audience, starting state, ending state, and required services.
3. Choose and document the primary orchestration model: `app-orchestrated`, `harness-orchestrated`, or `hybrid`.
4. Define Start button semantics and the single runner that owns step progression.
5. Define the step synchronization contract before writing code.
6. Add hidden owner-demo mode, usually behind `?workflowDemo=owner-demo`.
7. Add stable DOM targets using explicit `data-demo-*` attributes.
8. Add app-side owner demo state on `window.__ownerRunDemo`.
9. Add app-side narration state and live AI narration playback.
10. Make narration awaitable through completion, error, or timeout-backed signals.
11. Add app-side fake typing only where it can look browser-real and report completion.
12. Add a local harness under `scripts/demo/`, for example `scripts/demo/run-owner-demo.mjs`, only when the selected model needs harness-owned orchestration or OS input.
13. Use OS-level input for visible mouse movement, clicks, and scrolling.
14. Use CDP, Playwright, browser APIs, or equivalent only for state and bounds.
15. Re-measure targets before every visible action.
16. Disable manual advance while narration or action is running.
17. Add owner permission and setup instructions for the supported platform.
18. Verify the workflow visually and with the repo's build, lint, typecheck, or static checks.
19. Document how to rerun it.

App state schema:

```ts
type OwnerRunDemoPhase =
  | 'idle'
  | 'loading'
  | 'prepare'
  | 'preAction'
  | 'acting'
  | 'narrating'
  | 'settle'
  | 'advance'
  | 'complete'
  | 'unsupported'
  | 'error'

interface OwnerRunDemoState {
  ownerDemo: boolean
  orchestrationModel: 'app-orchestrated' | 'harness-orchestrated' | 'hybrid'
  state: 'idle' | 'running' | 'complete' | 'unsupported' | 'error'
  phase: OwnerRunDemoPhase
  stepId: string | null
  currentStep: string | null
  runId: number
  narrationStatus: 'idle' | 'queued' | 'playing' | 'complete' | 'timeout' | 'error'
  actionStatus: 'idle' | 'queued' | 'running' | 'complete' | 'timeout' | 'error'
  canAdvance: boolean
  lastCompletedAction?: string | null
  lastCompletedStep?: string | null
  route?: string
  activeJob?: unknown
  pendingAction?: string | null
  timingFallback?: string | null
  error?: string | null
}
```

Step metadata schema:

```ts
interface OwnerRunDemoStep {
  id: string
  label: string
  narration: string
  narrationOwner: 'app' | 'harness'
  actionOwner: 'app' | 'harness' | 'none'
  advanceTrigger: 'narration-and-action-complete' | 'manual-after-complete' | 'custom'
  completionSignal: string
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
  settleMs?: number
}
```

Step synchronization contract:

For every step, define `narrationStart`, `narrationComplete`, `actionStart`, `actionComplete`, `settleComplete`, and `advanceAllowed`.

Required invariant:

```ts
nextStep.narrationStart >= currentStep.narrationComplete
nextStep.narrationStart >= currentStep.actionComplete
nextStep.narrationStart >= currentStep.settleComplete
```

Synchronization rules:

- Only one narration may be active at a time.
- Narration must return completion, error, or timeout-backed state.
- Clicks, drags, typing, drawing, scrolls, and app-side animations must return completion signals.
- Next, Start, and manual advance controls must be disabled while a step is narrating or acting.
- If speech synthesis or AI audio never fires `ended`, use a calculated timeout and expose it in `timingFallback`.
- The next step cannot start narration until the current narration, action, and settle milestones are complete.

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
- The primary orchestration model is documented and implemented.
- Start button semantics match the selected orchestration model.
- One runner owns step progression.
- Step synchronization proves narration, action, and settle phases finish before the next narration starts.
- `window.__ownerRunDemo` exposes readable state and visible errors.
- Stable `data-demo-*` targets exist for every action.
- Live AI narration is app-owned, synchronized, and does not overlap.
- Narration and actions expose completion signals or recorded timeout fallbacks.
- The harness uses OS-level input for visible actions.
- The harness uses browser automation only for measurement and state.
- Verification proves visible actions happened and rejects speech-only advancement.
- Missing targets, unsupported platforms, narration failures, and aborts fail cleanly.
- Setup and rerun instructions are documented.
- The repo's relevant validation checks pass, or blocked checks are recorded with fallback verification and residual risk.
