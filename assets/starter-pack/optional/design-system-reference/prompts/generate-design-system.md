# Generate Design System Reference

## When to Offer

Offer this generation when ALL of the following are true:

- The design module is active (the repo has or is getting `planning/design-direction.md`).
- The repo contains at least one CSS file with CSS custom properties (`:root { --color-*, --radius-*, --font-* }` or equivalent).
- The app has shipped enough UI that tokens and components are in use (not an empty scaffold).

Ask the user: "Your app has a CSS design system. Want me to generate a standalone reference page and preview it in the browser?"

If the user declines, skip silently. Do not ask again in the same session.

## What to Extract

Read every CSS file that defines the project's design system (typically `globals.css`, `theme.css`, `variables.css`, or Tailwind `@theme` blocks). Extract:

### 1. Tokens

- **Colors**: every `--color-*` custom property. Group into core (bg, surface, border, text hierarchy) and semantic (red/yellow/green/blue triads). Show rendered swatches with the variable name and resolved value.
- **Radii**: every `--radius-*` property. Show rendered boxes at each radius with usage notes (which components use which radius).
- **Shadows**: every `box-shadow` value used in component classes. Show rendered examples at each elevation.
- **Spacing**: the set of padding/margin/gap values actually used. Show as a visual scale. Note whether the project uses a strict scale or ad-hoc values.
- **Fonts**: every `--font-*` family and the weights loaded. Show specimen text in each family.

### 2. Typography

- **Font families**: rendered specimens with variable names.
- **Type scale**: every distinct `font-size` + `font-weight` + `font-family` combination used in component classes, ordered largest to smallest. For each, show: rendered text, the size/weight/family, and which CSS classes use it.
- **Weight usage**: a table mapping each weight (400, 500, 600, 700) to its role in the system.
- **Conventions**: note patterns like "condensed is always 700", "uppercase always has letter-spacing", etc.

### 3. Components

Render live examples of every component class found in the stylesheet. For each:

- Show all variants (e.g., `.btn`, `.btn-primary`, `.btn-destructive`).
- Show states where relevant (hover description, disabled, error, active).
- Label with the CSS class name(s).
- Note the tokens used (which radius, which colors).

Typical components to look for:

- Buttons (default, primary, destructive, disabled)
- Badges and tags (status badges with dots, stage badges, nav badges, filter chips, tags)
- Form inputs (normal, error, disabled, with labels and hints)
- Stat cards (default and active, with colored values)
- Toasts / notifications (success, info, warning)
- Banners (error, warning/stale-data, inline messages)
- Progress indicators (bars, scores, urgency)
- Empty states

### 4. Patterns

Show assembled compositions that demonstrate how components work together:

- A data table with status badges, progress bars, and sortable headers.
- A confirm/destructive dialog.
- A detail card layout with key-value rows.
- A conventions summary: surface hierarchy, border usage, text hierarchy, interactive states, focus style, transition values, uppercase label rules, and any notable constraints (no dark mode, desktop-only, etc.).

## Output Contract

Generate a single standalone HTML file:

- **Location**: repo root as `design-system.html`, or `docs/design-system.html` if a `docs/` directory exists.
- **No build step**: the file must open directly in a browser with no server, no npm, no build.
- **No external dependencies** except Google Fonts if the project already uses them.
- **Inline all styles**: copy the project's CSS custom properties into a `<style>` block. Copy component class definitions needed for the rendered examples. Do not `@import` the project's CSS — the page must be self-contained.
- **Tabbed navigation**: use vanilla JS tabs (no framework) to switch between Tokens, Typography, Components, and Patterns sections.
- **Accurate**: every swatch, specimen, and component must use the actual token values from the project's CSS. Do not substitute generic colors or approximate values.
- **Labeled**: every rendered example must show the CSS class name or variable name it demonstrates.
- **Concise**: this is a developer reference, not a marketing page. No hero sections, no decorative illustrations, no prose beyond brief usage notes.

## After Generation

1. Open the generated page in the browser for the user to review.
2. Tell the user the file location.
3. Do not add it to `.gitignore` unless the user asks.
4. Do not modify the project's actual CSS — this is read-only extraction.

## Maintenance

The generated page is a snapshot. If the project's styles change significantly, the user can ask for it to be regenerated. The page does not auto-update.
