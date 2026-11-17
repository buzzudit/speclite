# Report Format

Write to `evaluations/<YYYY-MM-DD>_<subject>_audit.md`.

## Finding record

Every finding carries all of these. A candidate missing a `file:line` or a
failure scenario is dropped in phase 3, not softened into prose.

```markdown
### F-07 · Authorization & access control · P1 · App

**What it means:** A user at one organization can edit another organization's
records, and the log will blame their own organization for it.

**How to resolve:** Take the organization from the signed-in session instead of
trusting whatever the form sends.

**Location:** `app/src/actions/records.ts:142`
**Confidence:** confirmed

**What's wrong:** `updateRecord` reads `orgId` from the submitted form data
and passes it to the update without re-deriving it from the session.

**Failure scenario:** A signed-in user at org A edits the hidden `orgId` field
to org B's uuid and submits. The action writes against org B's row; the
database access policy is the only remaining barrier, and the audit entry
records org A as the actor.

**Suggested fix:** Derive `orgId` from the session and ignore any
client-supplied value.

**Suggested follow-up:** Harden record mutations against client-supplied org ids
— area `product`, priority high.
```

IDs run `F-01`, `F-02`, … in report order (P0 first), so they are citable in
follow-up work.

## The two plain-language lines

Every finding gets both, directly under its heading and before `Location`:

```
**What it means:**    one sentence — who is affected, what goes wrong
**How to resolve:**   one sentence — the fix, in the same plain register
```

One sentence each; two at the absolute most.

It is written for someone who will not read the rest of the entry: a founder
triaging on a phone, a compliance reviewer, a non-technical stakeholder.
So it says **who is affected and what goes wrong**, not what the code does.

- No jargon. Not RLS, policy, predicate, proxy, RPC, service role, presigned,
  race condition, N+1, revalidation, middleware. If a term would need a
  footnote, the sentence is not finished.
- No file paths, no function names, no restating the severity.
- Name the consequence in the world: a user's record is overwritten, the email
  shows a name on a lock screen, the ex-employee keeps access, the live site is
  not running your latest work.
- Keep it exact. "Anyone who visits your website can read the log of which
  organizations you looked at" is plain *and* precise. "Security issue in the
  audit table" is plain and useless.
- Say what is true today. If a finding is latent, the line says so ("nothing
  uses it yet"), because the reader is deciding what to fix this week.

The test: if someone read only the severity and these two lines, would they know
whether to care today, and roughly what it would take? If not, rewrite them.

### What "How to resolve" is, and is not

It is the shape of the fix and its size, in the same plain register as
`What it means`. "Turn on row security for that one table and block public
access — a single migration." "Point both deploy services at `main`." "Remove
the placeholder text until you have real copy."

It is **not** the implementation. The exact predicate, the function to call, the
constant to change — all of that belongs in `Suggested fix` further down the
entry, which is written for whoever does the work. These two serve different
readers and should not be collapsed into one.

- Lead with the verb. "Default the AI setting to off", not "the AI setting
  should be defaulted to off".
- Say the size when you honestly know it, because that is what triage turns on:
  one migration, 26 call sites, a wording change, no code at all.
- Never invent certainty. If the right fix depends on something unresolved —
  a signed agreement, a product decision, which of two conventions wins — say
  so, and name the decision rather than guessing at it.
- A finding you would fix by deleting the feature should say that. "Make
  the feature actually work correctly — or remove it until it can" is a more
  useful sentence than a repair plan for something that may not be worth
  repairing.

Findings reported as table rows (P2 and P3) have no heading, so both sentences
live in the summary index instead.

## Report structure

```markdown
# Codebase Audit — <subject>

**Auditor:** Claude (codebase-audit skill)
**Date:** <date>
**Commit:** <short sha>
**Surfaces:** <list surfaces examined>
**Lenses run:** <list lenses run, note any skipped>

---

## Section 1: Summary

### Counts

| Severity | Count |
|---|---|
| P0 | n |
| P1 | n |
| P2 | n |
| P3 | n |

### Where to start

One paragraph. The single highest-leverage fix and why it is first — usually the
worst consequence, not the quickest win. Name one thing, not a list.

### What's solid

Two or three sentences on what the audit *tried* to break and could not. This is
not padding: it tells the reader which guarantees they can rely on, and it keeps
the report honest about scope.

### All findings in plain language

A table covering **every** finding at every severity, in report order, with no
jargon. This is the part of the report a non-engineer can act on, and for P2/P3
findings it is the only plain-language text they get.

```markdown
| Severity | ID | What it means | How to resolve |
|---|---|---|---|
| **P0** | F-01 | Anyone who visits your website can read the private log of which organizations you looked at and why. | Turn on row security for that one table and block public access — a single migration. |
| **P1** | F-03 | As soon as a team has more than one member, the app breaks for them. | Add "and this user" to all 26 of those lookups. |
```

For findings with a full entry in §2, these are the same two sentences as the
entry's own — write each once and reuse it, so they cannot drift. Keep the rows
in ID order, not grouped by severity; the severity column already sorts, and ID
order lets a reader follow a row straight to its entry.

This table is the report's most-forwarded artifact. Someone will paste it into a
message, a ticket or a board without the rest of the document, so every row has
to stand alone: no "see above", no bare `file:line`, no pronoun whose referent
is in §2.

---

## Section 2: Findings

P0, then P1, P2, P3, each `### F-nn · Lens · Severity · Surface` per the record
above.

---

## Section 3: Compliance claim verification

(Include only if the project has planning docs with resolved claims or trust
assertions.)

Every claim under resolved headings in compliance/regulatory docs, plus any
safety or security claim in project planning docs.

| Claim | Source | Verdict | Evidence |
|---|---|---|---|
| 30-minute idle timeout implemented | regulations.md:82 | verified | `app/src/lib/session-timeout.ts:14` |
| ... | ... | contradicted / unverifiable | `file:line` or what would settle it |

Three verdicts only: **verified**, **contradicted**, **unverifiable**. A
contradicted safety claim is at least P1 and must also appear in section 2.

---

## Section 4: Coverage and limits

What was **not** examined, so this cannot be mistaken for exhaustive:

- Runtime behavior: concurrency, load, production data states
- Third-party sandbox behavior
- Anything with no lens coverage (name the subsystem)
- Files or directories skipped, and why
- Lenses skipped, and why

---

## Section 5: Recommended follow-up

One row per P0/P1. Title, area, suggested priority. Not created as tasks.
```

## Tone

Plain and specific. No hedging on confirmed findings, no dramatics on P3s. The
reader is the person who wrote this code — tell them what breaks and where, not
how they should feel about it.

`What it means`, `How to resolve` and the plain-language index are the exception
to "the reader wrote this code": assume those will be read by someone who did
not, and possibly forwarded to someone who cannot read code at all. Write them so
that staying accurate and staying readable are the same job.
