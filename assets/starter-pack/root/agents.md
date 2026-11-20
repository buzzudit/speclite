# {{PROJECT_NAME}} Agent Instructions

- Keep the root sparse and follow the naming and folder rules in `planning/bookkeeping.md`.
- If `planning/regulations.md` exists, treat it as the canonical compliance guardrail for legal, privacy, claims, trust, and approval-sensitive work.
- If `planning/bootstrap-plan.md` exists, treat it as the canonical ordered sequence and write step outputs to `steps/step-nn.md`.
- If `planning/story-management.md` exists, tie tracked implementation or documentation changes to a story before editing repo files.
- If `planning/testing-strategy.md` exists, choose the correct `Test Level` before implementation and record verification in the story's `Done Evidence`.
- Keep planning docs separate from execution stories.
- When adding, removing, or upgrading a dependency, provider, or infrastructure service, update `planning/tech-stack.md` in the same change.
- If `planning/stubs.md` exists, treat it as the canonical list of prototype stubs. When adding a new stub or replacing one with a real implementation, update that file in the same change.
- Commit automatically after completing work — do not ask for confirmation.
- Update `progress.md` when project direction, active work, or status materially changes.
- Prefer adapting coherent existing conventions over replacing them.
- Every completed task response should end with **Up Next** and 1-3 concrete recommended next actions.
- **Story writing in plan mode:** When asked to write a story, ask 9–12 discovery questions one by one (unless the user specifies otherwise). Only write the story file and update `stories/index.md` — do not begin implementation unless explicitly asked.
