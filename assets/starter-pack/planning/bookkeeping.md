# {{PROJECT_NAME}} Bookkeeping Rules

## Purpose

Keep the workspace easy to navigate as it grows.

## Naming Rules

- Use lowercase kebab-case for project files and folders unless a tool or framework requires another convention inside its own folder.
- Use `.md` for planning and operating documents.
- Use two-digit step numbers for bootstrap step artifacts.
- Prefer descriptive names over abbreviations.
- Keep the root intentionally sparse.

## Root Rules

Allowed root files:

- `agents.md`
- `progress.md`
- repo metadata such as `README.md`, `.gitignore`, or license files

Do not put planning drafts, step files, screenshots, exports, build output, or dependencies at the root.

## Planning Rules

- Use `planning/` for canonical strategy and operating documents.
- If a document is strategic, long-lived, and not a numbered step, it probably belongs in `planning/`.

## Step Rules

- If the bootstrap module is active, each numbered step in `planning/bootstrap-plan.md` gets a `steps/step-nn.md` file.
- Keep the main step file as the source of truth for that step's status, objective, deliverables, and next action.

## Story Rules

- Use `stories/` for markdown-first work tracking.
- Treat `planning/story-management.md` as authoritative for story areas, statuses, and movement rules.

## Progress Rules

- Maintain overall project status in `progress.md`.
- Keep `progress.md` concise.
- Update `progress.md` whenever direction, current focus, or major operating decisions change.

## Suggested Top-Level Folders

- `planning/`
- `steps/`
- `stories/`
- `research/`
- `design/`
- `site/`
- `app/`
- `assets/`
- `docs/`

Create folders only when they support actual project structure.

## Before Adding a File

Ask:

1. Is this a root operating doc?
2. Is this a planning document?
3. Is this a numbered step artifact?
4. Is this a tracked story?
5. Is this implementation code?
6. Is this supporting research, design, or assets?
