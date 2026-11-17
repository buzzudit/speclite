# Lens Checklists

Seven lenses. Each lists what to check, where to look, and the **finding shape** —
what actually counts as a defect, as opposed to a design choice you happen to
dislike.

Keep these current. When a new subsystem lands, add it here in the same change,
or the audit silently stops covering it.

Adapt each lens to the project's actual stack and conventions discovered in
phase 0. The checks below are common patterns; skip checks that do not apply
and add project-specific checks where needed.

---

## Lens 1 — Authorization & access control

Highest-consequence lens. Look for anywhere the access boundary can be crossed.

**Check**

- Database tables: does the database enforce row-level or object-level access
  control? Check for tables without policies, rules, or application-layer
  scoping.
- Server actions, API routes, and mutation endpoints: do they derive the
  authorized scope from the session/token, or trust client-supplied input?
- Service-role or admin-level database access: where is it used, and is it
  constrained to an audited wrapper or whitelist?
- Admin routes: are they gated on a role or permission check?
- Least-authenticated surfaces: upload endpoints, webhook receivers, public API
  routes, OAuth callbacks. Check token scope, single-use enforcement, expiry.
- Cron and background job endpoints: how are they authenticated?
- Multi-tenancy boundaries: if the app serves multiple organizations or users,
  can one cross into another's data?

**Finding shape:** a reachable path where a caller reads or writes data outside
their authorized scope, or reaches a route their role should not. Not: "the
database layer does the work" — that is architecture.

---

## Lens 2 — Input & data integrity

**Check**

- Server actions and API handlers: are inputs validated before use, or cast
  and trusted?
- AI/LLM-generated output written to storage: is it schema-validated before
  the write, or trusted structurally?
- File upload: type and size enforced **server-side**, not only in the client.
- CSV/data import: row count limits, malformed rows, injection into downstream
  fields.
- Database migrations: irreversible operations, missing foreign keys, columns
  made nullable that the code reads as non-null, defaults that mask a bug.
- Form submissions: can a user submit data that puts a record into an
  impossible state?

**Finding shape:** specific input that reaches storage or output in a state the
code later assumes impossible.

---

## Lens 3 — Secrets & sensitive data

**Check**

- Environment variables exposed to the client bundle (e.g., `NEXT_PUBLIC_*`,
  `VITE_*`, `REACT_APP_*` carrying keys, secrets, or tokens).
- Logger and error-reporter call sites: can sensitive data (names, emails, IDs,
  financial data, health data) reach a log line or error payload?
- Error messages surfaced to the client containing record contents.
- Sensitive data in URLs or query strings.
- Email or notification templates containing sensitive identifiers in subject
  or body.
- Committed secrets: `.env` files, key directories, API keys in source. Check
  `git ls-files` and `.gitignore`.
- Third-party API calls: what data is sent in the request body or headers?

**Finding shape:** a named data type reaching a named sink. "Logging could
leak data" is not a finding; "`logger.info` is called with the full user row
at `queries.ts:88`" is.

---

## Lens 4 — Error handling & failure modes

**Check**

- Empty or swallowing `catch` blocks.
- Missing `await` on async calls, especially before a redirect or response.
- External calls without timeout or retry strategy.
- Cron/background jobs on failure, double-fire, or overlapping run. Is work
  idempotent?
- Mutate-then-fail: a sequence that writes, then throws, leaving state partial
  with no rollback and no compensating action.
- Error boundaries and error pages: does a thrown error render something
  actionable, or a blank screen?

**Finding shape:** a failure the user is not told about, or state left
inconsistent after a partial failure.

---

## Lens 5 — Architecture & coupling

**Check**

- Client components importing server-only modules (service-role clients, node
  built-ins, secrets).
- Duplicated business logic able to diverge: the same calculation or rule in
  two places that can get out of sync.
- Cache and revalidation after mutations: a write that does not invalidate the
  view it affects.
- N+1 queries on list views.
- API contract drift: the client calls an endpoint with assumptions that do not
  match the actual handler (field names, status codes, auth requirements).
- Type declarations vs database schema: a type asserting non-null where the
  column is nullable.

**Finding shape:** two code paths that must agree and do not, or a boundary
crossing that leaks server concerns into the client.

---

## Lens 6 — Plan / doc coherence

Cheap to check, and the lens that keeps planning docs trustworthy.
`check_doc_coherence.py` does the mechanical part.

**Check**

- `planning/tech-stack.md` versions vs installed `package.json` files (or
  equivalent dependency manifests).
- `planning/stubs.md` in both directions: stub markers in code with no entry,
  and entries that are now fully implemented.
- Story index: every link resolves, and the linked file's status matches the
  section it is listed under and the folder it sits in.
- `progress.md` vs actual state — including deploy claims.
- Features described in planning docs with no implementation.
- Root-file rules (from `planning/bookkeeping.md` if it exists) vs what is
  actually at the repo root.

**Finding shape:** a specific doc line contradicted by a specific code line. Cite
both. Drift on a *safety* or *security* claim is P1, not P3 — see `severity.md`.

---

## Lens 7 — Compliance & trust claims

Skip this lens if the project has no compliance docs, marketing claims, or trust
assertions in its planning corpus.

**Check**

- Every claim under resolved headings in compliance or regulatory docs, treated
  as falsifiable. Produce a verdict for each: verified, contradicted,
  unverifiable. This table is a required report section.
- Marketing copy vs what the product does. Claims about security, privacy,
  performance, outcomes, or certifications that the code does not support.
- Audit or access logging coverage on every sensitive-data access path.

**Finding shape:** a documented or advertised guarantee the code does not
deliver.

---

## Pre-seeded candidates

This section is project-specific. After phase 0, populate it with candidates
already visible in the tree — things you noticed during orientation that are
worth confirming or dismissing. This saves the lens sweep from rediscovering
what is already obvious.

Format:

| # | Candidate | Lens |
|---|---|---|
| 1 | (describe what you noticed and where) | (lens number) |

Confirm or dismiss each — do not spend a sweep rediscovering them. If one is
dismissed, say so in the report; a reader who knows about it needs to know it
was checked.
