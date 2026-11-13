---
name: skill-builder
user-invocable: true
description: >
  Build a new Claude Code skill for any domain through deep conversational
  interview. Extracts methodology, auto-gathers provenance (academic and
  industry), generates typed ports for composition, scaffolds verification
  scripts, and produces a complete skill package ready for .claude/skills/.
---

# Skill Builder

Create a new speclite-compatible Claude Code skill from a domain expert's
methodology through guided conversation. The builder deeply interviews the
author, challenges assumptions, researches provenance, and generates a complete
skill package with schemas, reference docs, and verification scripts.

The output is a ready-to-install `.claude/skills/<name>/` directory.

## Using this skill

Start with `/skill-builder` followed by a brief description of what the skill
should do.

Example invocations:
- `/skill-builder A security review checklist for API endpoints`
- `/skill-builder A content strategy audit that evaluates messaging against brand guidelines`
- `/skill-builder A code review skill that checks for accessibility anti-patterns`
- `/skill-builder An onboarding flow evaluation for SaaS products`

The builder will interview you to extract your methodology, then generate the
full skill package.

## Skill shapes

The builder supports four skill archetypes. It recommends one based on the
interview, but the author can override.

### Session-flow

The most complete shape. A multi-step guided session with intake, adaptive
interview, execution, verification, and deliverable generation.

Use when: the methodology requires understanding context before acting,
judgment calls during execution, and structured output.

Examples: usability evaluation, scenario mould, security audit, content review.

File structure:
```
.claude/skills/<name>/
  SKILL.md
  skill-manifest.json
  references/
    session-guide.md
    execution-contract.md
    enforcement.md
    report-format.md
    provenance.md
  scripts/
    verify_session.py
    verify_artifact.py
    verify_delivery.py
```

### Reference

A knowledge base the agent consults, not user-invoked. Loaded automatically
when the agent recognizes the need or when another skill declares it as input.

Use when: the skill is a body of knowledge (a heuristic set, a style guide, a
regulatory reference) rather than a process.

File structure:
```
.claude/skills/<name>/
  SKILL.md
  skill-manifest.json
  references/
    <topic>.md
    index.md
```

### One-shot

Input goes in, one artifact comes out. No interview, no session state. Lighter
than session-flow.

Use when: the transformation is deterministic or near-deterministic, context is
minimal, and the output format is fixed.

File structure:
```
.claude/skills/<name>/
  SKILL.md
  skill-manifest.json
  references/
    generation-contract.md
  scripts/
    verify_output.py
```

### Recurring check

Periodic assessment against fixed criteria. Produces a checklist or scorecard
each run, with optional trend tracking across runs.

Use when: the same criteria need to be re-evaluated regularly, tracking
improvement or regression over time.

File structure:
```
.claude/skills/<name>/
  SKILL.md
  skill-manifest.json
  references/
    check-criteria.md
    scoring-rubric.md
  scripts/
    verify_check.py
```

## Session flow

The `/skill-builder` session follows nine steps.

### Step 1 — Orientation

Explain what the builder does in a blockquote:

> Welcome to the Skill Builder. I'll interview you to understand your
> methodology, research its academic and industry grounding, and generate a
> complete Claude Code skill package.
>
> Steps:
> 1. Orientation (now)
> 2. Domain and shape — what does this skill do?
> 3. Methodology extraction — walk me through your process
> 4. Provenance gathering — ground the methodology in research
> 5. Deliverable design — what does the skill produce?
> 6. Verification criteria — what does a bad output look like?
> 7. Port definition — what goes in and comes out?
> 8. Generation — build the skill package
> 9. Refinement — review and iterate
>
> Most sessions take 20–40 minutes for a session-flow skill, less for simpler
> shapes.

Ask: "What does this skill do? Describe it the way you would explain it to a
colleague who will use it."

### Step 2 — Domain and shape

From the Step 1 answer, identify the domain and recommend a shape. Present the
recommendation with reasoning and ask to confirm.

Resolve:
- Is this a multi-step guided session (session-flow), a knowledge base
  (reference), a single transform (one-shot), or a periodic check
  (recurring-check)?
- Who invokes it? User via slash command, or agent when it recognizes the need?
- What triggers it? When should someone reach for this skill?
- Is there an optional lifecycle stage (discover, model, build, measure)?

### Step 3 — Deep methodology extraction

The core of the interview. Work through the author's methodology step by step.

Open with: "Walk me through how you would do this manually. Start from the
beginning — what is the first thing you look at or ask?"

For each step the author describes:
1. Record the step name, input, judgment, and output.
2. Ask: "What information do you need before you can do this step?"
3. Ask: "What could go wrong here? What mistakes do you see people make?"
4. Ask: "How do you know when this step is done well?"

Challenge where appropriate:
- "Why this approach rather than [known alternative]?"
- "What evidence supports this step?"
- "What would you skip if you had 10 minutes instead of an hour?"

Continue until the methodology is complete — the author describes the final
deliverable and what "done" looks like.

For **reference** skills, Step 3 extracts the knowledge structure: what topics,
how they're organized, when each is relevant, and what sources they draw from.

For **one-shot** skills, Step 3 extracts the transformation: input format,
output format, the rules that govern the transform, and edge cases.

For **recurring-check** skills, Step 3 extracts the criteria: what is being
assessed, how it's scored, what the thresholds are, and whether trending matters.

### Step 4 — Provenance gathering

Research academic and industry grounding for each methodology step. This is
where the builder does its own work, not just transcribes the author.

**Academic layer (required, agent-gathered):**
- Search for published research, established frameworks, standards bodies.
- For each methodology step, find at least one academic citation.
- Mark anything that could not be verified as `[unverified]`.

**Industry layer (required, agent-gathered):**
- Search for industry best practices, peer guidance, regulatory standards.
- For each methodology step, find at least one industry citation.

**Present findings:** "I found these sources that ground your methodology. Any
I should add or correct?"

**Organizational layer (optional, user-supplied):**
- Ask: "Does your organization have internal standards, past studies, or prior
  art that should be incorporated? This is optional."
- If yes, record verbatim with attribution.

**Conflict rules:**
- When layers conflict, state the conflict.
- Prefer organizational context for local relevance, academic for method rigor.
- Flag conflicts for human review.
- Never present organizational data as academic or vice versa.

### Step 5 — Deliverable design

Present the deliverable catalog (load from
`assets/skill-builder/schemas/deliverable-types.json`):

| Format | Description |
|--------|-------------|
| markdown | Structured report with headings, tables, scores |
| html | Single-file interactive artifact, works offline |
| json | Machine-readable structured data |
| diagram | SVG or Mermaid diagram |
| scorecard | Tabular ratings with grades |
| pdf | Print-ready document |
| csv | Flat tabular export |

Ask: "Which outputs does your skill produce? For each, what sections or
structure does it need?"

### Step 6 — Verification criteria

Ask: "For each deliverable, what would a bad output look like? What should
never happen?"

For each quality criterion:
- Can it be automated? (schema check, completeness check, consistency check)
- Is it a hard gate (blocks delivery) or a soft check (warning)?
- What is the minimum acceptable standard?

The builder translates these into verification script specifications.

### Step 7 — Port definition

Based on inputs/outputs identified, propose typed ports using the vocabulary
from `assets/skill-builder/schemas/port-types.json`.

Check against installed skills' manifests for composition opportunities.
Report: "This skill's output type X matches skill Y's input type X — they can
compose."

Add a `## Composition` section to the generated SKILL.md.

### Step 8 — Generation

Generate the complete skill package:

1. Select the template set for the chosen shape.
2. Populate each template from the interview context.
3. Generate the `skill-manifest.json`.
4. Generate verification scripts from the quality criteria.
5. Write all files to a staging area.
6. Run `scripts/validate_manifest.py` against the manifest.
7. Present the file list and a summary for review.

### Step 9 — Refinement

The author reviews the generated package. Accept change requests and
regenerate affected files. Iterate until the author confirms.

On confirmation, write the final package to `.claude/skills/<name>/`.

## Provenance system

Every generated skill carries provenance. The provenance section in SKILL.md
and the `provenance` field in skill-manifest.json must both be populated.

Rules:
- At least one academic and one industry citation per core methodology step.
- Unverified claims are marked `[unverified]`.
- Organizational evidence is optional and always attributed.
- The builder gathers academic and industry evidence; the user supplies
  organizational evidence.

## Typed ports

Skills declare inputs and outputs using types from the shared port vocabulary.
The builder validates that port types exist in the registry and suggests
compositions with installed skills.

Port type widening: some types can substitute for broader types (e.g.,
`severity-findings` widens to `artifact-json`). Widening rules are defined in
`port-types.json`.

## Verification generation

The builder auto-generates Python verification scripts (stdlib only, no pip
dependencies) from the quality criteria collected in Step 6.

Script patterns:
- **Schema validation**: Check JSON structure against expected fields.
- **Completeness check**: Verify required sections/items exist and are non-empty.
- **Consistency check**: Cross-reference related fields (e.g., scorecard totals
  match item scores).
- **Format check**: Validate markdown structure, heading hierarchy, table format.

Every script exits 0 on pass, 1 on fail, with human-readable output.

The delivery gate script (`verify_delivery.py`) always checks:
1. All other verification scripts pass.
2. Session decisions are recorded (session-flow only).
3. All deliverables exist and are non-empty.
4. Provenance is present and cites at least one academic and one industry source.

## Non-negotiables

- **Synthetic data only.** All examples in generated skills use invented data.
- **Provenance required.** No skill ships without academic and industry citations.
- **Verification required.** Every skill has at least one automated check.
- **Schema compliance.** Every skill-manifest.json validates against the schema.
- **One shape per skill.** Mixed shapes are separate skills that compose via ports.

## Templates

The builder reads templates from `assets/skill-builder/templates/`. Templates
use Mustache-style placeholders that the agent fills during generation. The
agent is the renderer — it reads the template, understands the structure, and
generates content for each section.

Template locations:
- `templates/shapes/<shape>/` — per-shape file templates
- `templates/deliverables/` — per-format deliverable templates
- `templates/verification/` — verification script templates
