# Provenance Guide

Load this file during Step 4 (provenance gathering) and when generating
provenance sections in skill output.

---

## Three evidence layers

### Academic (required, agent-gathered)

Published research, established frameworks, and standards bodies that ground
the methodology. The agent researches these during the interview.

Examples:
- Nielsen, J. (1994). "Severity Ratings for Usability Problems." NNG.
- Parasuraman, R. & Riley, V. (1997). "Humans and Automation." Human Factors.
- ISO 9241-11:2018. Ergonomics of human-system interaction.
- Strauss, A. & Corbin, J. (1990). Basics of Qualitative Research.

Format in skill-manifest.json:
```json
{
  "claim": "Severity scales improve inter-rater reliability",
  "source": "Nielsen, J. (1994). Severity Ratings for Usability Problems.",
  "year": 1994,
  "doi": null,
  "verified": true
}
```

Format in SKILL.md:
```markdown
- **Severity scales improve inter-rater reliability** — Nielsen, J. (1994).
  Severity Ratings for Usability Problems. NNG. ✓
```

### Industry (required, agent-gathered)

Practices from peer organizations, vendor guidance, and regulatory or
accessibility standards that validate the approach.

Examples:
- WCAG 2.2 Success Criteria (W3C)
- OWASP Top 10 (OWASP Foundation)
- Apple Human Interface Guidelines
- Google HEART framework for UX metrics

Format in skill-manifest.json:
```json
{
  "claim": "Color contrast must meet a minimum 4.5:1 ratio",
  "source": "WCAG 2.2 SC 1.4.3",
  "type": "standard",
  "url": null
}
```

### Organizational (optional, user-supplied)

Internal strategy, product landscape, past studies, survey data, and customer
context. Always attributed to the person who supplied it.

Format in skill-manifest.json:
```json
{
  "claim": "Our users complete forms on mobile 68% of the time",
  "source": "Q3 2025 analytics review",
  "supplied_by": "Product team"
}
```

---

## Gathering strategy

### Step 1: Identify domain keywords

From the methodology extraction, identify the discipline, method names, and
key concepts. Example: "usability evaluation" → keywords: usability, heuristic
evaluation, severity rating, user testing.

### Step 2: Search for academic grounding

For each methodology step, search for:
- The foundational paper or framework it draws from
- Validation studies or meta-analyses
- Standards bodies that codify the approach

Prioritize:
1. Foundational/seminal works (Nielsen, Norman, Shneiderman, etc.)
2. Standards (ISO, W3C, IEEE)
3. Recent validation studies
4. Textbooks and review articles

### Step 3: Search for industry practices

For each methodology step, search for:
- Industry standards (WCAG, OWASP, SOC 2, HIPAA)
- Vendor best practices (Google, Apple, Microsoft design guidelines)
- Regulatory requirements (ADA, GDPR, FTC)
- Widely-adopted frameworks (HEART, AARRR, RICE)

### Step 4: Present and confirm

Group citations by methodology step. Present to the author:
- What was found and for which step
- What could not be grounded (marked [unverified])
- Ask for corrections or additions

### Step 5: Prompt for organizational evidence

"Does your organization have internal standards, past studies, or prior art
that should be incorporated? This is optional."

---

## Conflict resolution

When evidence layers conflict:
1. **State the conflict explicitly** in the provenance section.
2. **Academic for method**: use the academic source for how to do the work.
3. **Organizational for context**: use the organizational source for what the
   specific environment requires.
4. **Flag for human review**: add a note that a domain expert should reconcile.

Never present organizational data as academic (generalized truth).
Never present academic data as organizational (local context).

---

## Minimum requirements

Every generated skill must have:
- At least one academic citation per core methodology step
- At least one industry citation per core methodology step
- Organizational citations where supplied
- [unverified] tags on any claim without a confirmed source
- A provenance.md file aggregating all citations (session-flow skills)
- A provenance section in SKILL.md (all shapes)
- Provenance data in skill-manifest.json (all shapes)
