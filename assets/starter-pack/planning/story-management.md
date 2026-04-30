# {{PROJECT_NAME}} Story Management

Status: active

## Purpose

Use markdown files for lightweight story tracking.

## Folder Layout

Stories live under:

```text
stories/<area>/<status>/qm-0001-short-title.md
```

The index lives at:

```text
stories/index.md
```

## Default Areas

Use these areas unless the project explicitly updates this policy:

- `planning`
- `product`
- `research`
- `ops`
- `site`

## Statuses

Use these statuses only:

- `backlog`
- `ready`
- `doing`
- `review`
- `done`
- `blocked`
- `parked`

## Story File Template

Use `stories/story-template.md` or the starter template bundled with the skill as the baseline structure.

## Pull Rules

- No implementation without a story.
- Pull from `ready`, not directly from `backlog`, unless the story is clarified first.
- Prefer one `doing` story at a time unless parallel work is intentionally planned.
- Before implementing a story, move it to `doing`, update the story `Status`, update `stories/index.md`, and commit that checkpoint.
- Choose the story's `Test Level` from `planning/testing-strategy.md` before implementation.
- Verify the work at the chosen test level and record the results in `Done Evidence`.
- When a story is completed, update the story file, move it to the final status folder, update `stories/index.md`, update `progress.md` if project status or direction changed, and make the after-story commit.
- If a story becomes blocked or unclear, move it to `blocked` and record the blocker instead of continuing informally.

## Definition of Ready

A story is ready when it has:

- a clear outcome
- acceptance criteria
- an expected `Test Level`
- known target files or work area
- no unresolved blocker for the first implementation step

## Definition of Done

A story is done when:

- acceptance criteria are met
- relevant files are updated
- verification is recorded
- untested risk is recorded when applicable
- `stories/index.md` is updated
- the story file path matches its `Area` and `Status`
- `progress.md` is updated if project direction or active work changed
- the work is committed
