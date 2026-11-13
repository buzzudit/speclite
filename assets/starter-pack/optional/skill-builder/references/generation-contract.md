# Generation Contract

Load this file when generating the skill package (Step 8). It governs how
templates are populated, files are written, and the package is validated.

---

## Generation process

1. **Collect context.** Assemble all interview outputs into a generation context:
   - name, description, shape, invocable, command
   - methodology steps with inputs, judgments, outputs
   - provenance (academic, industry, organizational)
   - deliverables with formats and structures
   - verification criteria (automated/manual, gate/warning)
   - port definitions with types
   - composition opportunities
   - lifecycle stage (if declared)
   - severity scale (if applicable)

2. **Select templates.** Load the template set for the chosen shape from
   `assets/skill-builder/templates/shapes/<shape>/`.

3. **Generate SKILL.md.** Populate the SKILL.md template with:
   - Frontmatter: name, user-invocable, description
   - Purpose paragraph
   - Usage examples (from the interview)
   - Methodology section (from Step 3)
   - Provenance section (from Step 4)
   - Non-negotiables (from domain-specific constraints)
   - Severity scale (if applicable)
   - Port declarations (from Step 7)
   - Composition section (from port matching)

4. **Generate skill-manifest.json.** Populate the manifest schema with all
   structured data. Validate against `skill-manifest.schema.json`.

5. **Generate reference docs.** For session-flow:
   - `session-guide.md` — from intake and interview steps
   - `execution-contract.md` — from execution steps
   - `enforcement.md` — from decision recording and session schema
   - `report-format.md` — from deliverable specifications
   - `provenance.md` — aggregated citations

   For other shapes, generate the shape-specific reference docs.

6. **Generate verification scripts.** From the quality criteria:
   - One script per verification category (session, artifact, delivery)
   - Each check function maps to one criterion
   - Exit 0 on pass, 1 on fail

7. **Validate.** Run `validate_manifest.py` against the manifest. Fix any
   schema violations before presenting.

8. **Present.** Show the file list, a summary of what was generated, and the
   manifest. Ask for review.

---

## File naming rules

- Skill directory: `.claude/skills/<name>/` where name is kebab-case
- SKILL.md and skill-manifest.json at root
- Reference docs in `references/` with kebab-case names
- Scripts in `scripts/` with snake_case names and `.py` extension
- HTML artifacts with kebab-case names and `.html` extension

---

## Verification script generation

For each automated criterion, generate a check function:

```python
def check_<criterion_id>(data, errors):
    """<criterion description>"""
    # Validation logic here
    if not <condition>:
        errors.append("<human-readable failure message>")
```

Wrap all checks in a main function that:
1. Parses the input file (JSON or markdown)
2. Runs each check function
3. Reports results
4. Exits with appropriate code

Script constraints:
- Python 3 stdlib only — no pip dependencies
- Each script is self-contained
- Human-readable output on both pass and fail
- verify_delivery.py orchestrates all other scripts

---

## Template rendering

Templates use `{{placeholder}}` markers. The agent reads the template,
understands the intended structure, and writes the content for each section.
This is not a mechanical find-and-replace — the agent generates prose,
adapts structure, and makes judgment calls about what to include.

When a template section doesn't apply to the skill being built, omit it
rather than leaving a placeholder or writing "N/A".

When the skill needs a section the template doesn't have, add it. Templates
are starting points, not constraints.

---

## Manifest validation rules

The generated skill-manifest.json must:
- Validate against skill-manifest.schema.json
- Have at least one academic provenance entry
- Have at least one industry provenance entry
- Have at least one deliverable
- Have at least one verification criterion
- Have at least one output port
- Have name matching the skill directory name
- Have shape matching the actual file structure
