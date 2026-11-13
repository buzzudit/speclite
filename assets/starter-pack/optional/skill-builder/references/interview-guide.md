# Interview Guide

Load this file at the start of every `/skill-builder` session. It governs the
deep methodology extraction that is the core of the skill-building process.

---

## Interview principles

1. **Extract, don't prescribe.** The author is the domain expert. The builder's
   job is to draw out their methodology, not impose one.
2. **Challenge, don't accept.** Every methodological choice should survive a
   "why?" and a "what if not?" The builder pushes back constructively.
3. **Ground, don't assume.** Every step gets provenance. The builder researches
   before presenting.
4. **Structure, don't constrain.** The builder maps the methodology to a skill
   shape, but the methodology drives the shape, not the reverse.

---

## Phase 1: Opening

One question: "What does this skill do? Describe it the way you would explain
it to a colleague who will use it."

Listen for:
- The domain (what field or discipline)
- The subject (what is being evaluated, generated, or analyzed)
- The audience (who uses this skill and what they need)
- The trigger (when should someone reach for this skill)

---

## Phase 2: Shape determination

From the opening answer, infer the shape. Use these heuristics:

| Signal | Likely shape |
|--------|-------------|
| "I walk through a series of steps..." | session-flow |
| "I evaluate against criteria..." | session-flow or recurring-check |
| "I look up the relevant..." | reference |
| "I generate a..." | one-shot |
| "I check whether..." | recurring-check |
| "I need context before I can..." | session-flow |
| "It's the same check every time..." | recurring-check |

Present the recommendation: "Based on your description, this sounds like a
[shape] skill. Here's why: [reasoning]. Does that match, or should we consider
a different approach?"

---

## Phase 3: Deep extraction

The longest phase. Adapt depth to the shape.

### Session-flow extraction (4-8 exchanges)

For each step the author describes:

1. **Record:** Step name, what it does, in one sentence.
2. **Input probe:** "What information do you need before this step?"
3. **Failure probe:** "What could go wrong? What mistakes do you see?"
4. **Quality probe:** "How do you know when this step is done well?"
5. **Challenge probe** (selective, not every step):
   - "Why this approach rather than [alternative]?" — when the builder knows
     of a different method in the literature
   - "What evidence supports this?" — when the step seems idiosyncratic
   - "What would you skip under time pressure?" — to identify core vs. nice-to-have

Map each step to the session contract phases:
- Intake steps → session-guide.md (Steps 1-2)
- Interview steps → session-guide.md (Steps 3-4)
- Execution steps → execution-contract.md
- Output steps → report-format.md

### Reference extraction (2-4 exchanges)

For each knowledge area:
1. "What are the main topics this reference covers?"
2. "For each topic, what's the key information someone needs?"
3. "When would the agent consult this? What triggers it?"
4. "What are the sources for this knowledge?"

### One-shot extraction (2-3 exchanges)

1. "What goes in?"
2. "What comes out?"
3. "What rules govern the transformation?"
4. "What are the edge cases?"

### Recurring-check extraction (3-5 exchanges)

1. "What criteria are you assessing?"
2. "How is each criterion scored?"
3. "What are the thresholds for pass/fail?"
4. "Does trending matter — do you track improvement over time?"
5. "What triggers a re-check?"

---

## Phase 4: Provenance research

After methodology extraction, the builder researches grounding.

Search strategy:
1. Identify the domain keywords from the methodology.
2. Search for foundational academic works (seminal papers, textbooks,
   established frameworks).
3. Search for industry standards and practices (ISO, WCAG, OWASP, vendor
   guides, regulatory requirements).
4. Map citations to methodology steps.

Present findings grouped by methodology step:
- "For step [X], I found: [academic source] and [industry source]."
- "I could not find grounding for step [Y]. Is there a source I'm missing, or
  is this your original contribution? I'll mark it [unverified]."

Then ask for organizational evidence.

---

## Phase 5: Quality criteria

Ask: "For each deliverable, what would a bad output look like?"

Categorize each criterion:
- **Schema check**: Can be validated by checking JSON/markdown structure.
- **Completeness check**: Can be validated by counting required items.
- **Consistency check**: Can be validated by cross-referencing fields.
- **Judgment check**: Requires human review — cannot be automated.

For automated criteria, ask: "Is this a hard gate (blocks delivery) or a soft
check (produces a warning)?"

---

## Phase 6: Ports and composition

Present the port type vocabulary. For each input/output the author described,
propose a type.

Then scan installed skills for composition:
- Output type matches another skill's input type → note the pairing.
- This skill's input type matches another skill's output type → note the reverse.

---

## Phase 7: Deliverables

Present the deliverable catalog. Ask which formats the skill produces.

For markdown reports, ask about required sections.
For HTML artifacts, ask about interactivity needs.
For JSON data, ask about the schema.
For scorecards, ask about the grading scale.

---

## Adaptive depth

Not every phase needs the same depth. Adjust based on:

- **Complex domain, novel methodology**: Full depth on phases 3 and 4.
- **Well-known methodology (e.g., Nielsen heuristics)**: Light on phase 3
  (the methodology is established), full on phase 4 (provenance is easy).
- **Simple transformation**: Light on all phases — get to generation fast.
- **Author is experienced and precise**: Less probing, more confirming.
- **Author is exploring**: More challenging, more alternatives presented.

The builder should never ask more questions than the skill's complexity warrants.
