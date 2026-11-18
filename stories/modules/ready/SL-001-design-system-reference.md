# SL-001: Design System Reference Module

Status: ready
Priority: medium
Owner: Codex
Area: modules
Test Level: 2
Created: 2026-11-18

## User Story

As a developer starting a UI-facing project, I want Speclite to offer to generate a design-system reference page from my app's existing styles, so that I can see my tokens, typography, and components in one place and make informed design decisions without digging through CSS.

## Context

When a project already has a stylesheet with custom properties, font stacks, component classes, and color tokens, the developer's mental model of the system is scattered across hundreds of CSS lines. A standalone HTML page that extracts and renders the actual tokens and components makes the system visible and reviewable.

This module fits into the existing Design module flow. When the design module is active and the repo contains a CSS file with custom properties, Speclite should ask the user whether they'd like a design-system reference page generated and previewed in the browser.

The generation is a one-shot task (not a recurring skill), so this is a prompt template with a generation contract, not a Claude Code slash-command skill.

## Trace

Upstream:
- `SKILL.md` Module Selection — adds a new optional module.
- `assets/starter-pack/planning/design-direction.md` — the design system reference supplements the design brief.

Downstream:
- Projects that install the design module get this as an additional offer.

## Acceptance Criteria

- [ ] An optional module exists at `assets/starter-pack/optional/design-system-reference/`.
- [ ] The module contains a generation prompt (`prompts/generate-design-system.md`) with a contract for what to extract and how to structure the output.
- [ ] SKILL.md's Module Selection section lists the new module with its trigger conditions.
- [ ] SKILL.md's Template Map lists the new module's assets.
- [ ] When the design module is active and the repo has a CSS file with custom properties, Speclite offers to generate and preview the reference page.
- [ ] The generated page is a standalone HTML file (no build step, no dependencies beyond Google Fonts if the project uses them).
- [ ] The page has tabbed sections covering at minimum: tokens (colors, radii, shadows, spacing), typography (families, scale, weights), components (rendered examples with class names), and patterns (assembled compositions).
- [ ] The page is opened in the browser for review after generation.

## Spec Delta

Added:
- `assets/starter-pack/optional/design-system-reference/prompts/generate-design-system.md` — generation prompt and contract.
- Module entry in SKILL.md Module Selection.
- Module entry in SKILL.md Template Map.

Changed:
- Not applicable.

Removed:
- Not applicable.

## Notes

- The page is a development reference, not a production artifact — it should live at the repo root or in `docs/`, not in the app's source tree.
- The generation reads the project's actual CSS (globals.css, theme files, component styles) and mirrors the real tokens and classes, not a generic template.
- Inspired by the design-system.html generated for the SBM Ideas project (RA-064 branch).

## Decisions

- One-shot prompt template, not a Claude Code skill: the generation is a single pass with no recurring invocation pattern, so a prompt contract is the right shape. If users later want to re-run it after style changes, the prompt can be invoked again manually.
- Standalone HTML with inlined styles: avoids any build dependency. The page imports Google Fonts only if the project already uses them.

## Done Evidence

- Before commit:
- After commit:
- Files:
- Verification:
- Untested Risk:
