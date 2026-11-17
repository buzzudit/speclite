# Severity Rubric

Four levels. Assign by **consequence if it fires**, not by how hard it is to fix
and not by how clever the finding is.

## P0 — Breach or corruption

Stop and fix before any other work.

- Cross-tenant or cross-user data exposure: one user can read or write another's
  data through an authorization gap
- Authentication or authorization bypass on any route or action
- Secret, key, or credential exposed to the client bundle, a log, or the repo
- Irreversible data loss or corruption on a reachable path
- Sensitive data sent to a third party outside the trust boundary

A P0 needs a reachable path. "The database layer is the only thing enforcing
access control" is the design, not a P0. "This route takes a user id from the
client and does not re-check it" is a P0.

## P1 — Ship blocker

Blocks handing the product to real users.

- A critical path breaks or silently produces wrong output
- Data is accepted and then lost, or attached to the wrong record
- A compliance or privacy gap that would fail a reasonable review: unlogged
  access to sensitive data, sensitive data in a log, unprotected admin actions
- An integration failure mode that strands a user action with no recovery or
  notification

## P2 — Real defect

Wrong behavior that a user will hit but can work around or recover from.

- Wrong behavior on a secondary path
- A silent failure where the user believes the action succeeded
- A missing error state, so a failure renders as an empty or frozen UI
- A race or ordering bug with a visible but non-destructive outcome

## P3 — Drift or hygiene

Real, but no current user impact. Worth fixing before it becomes P2.

- Planning doc asserts something the code no longer does, or vice versa
- Duplicated logic that can diverge but has not yet
- Dead code, committed build output, stale committed data files
- Story index or status drift, root-sparseness violations

## Confidence, separately

Severity is about consequence. Confidence is about evidence, and the two are
independent — a `plausible` P0 still leads the report.

- **confirmed** — the failure scenario is reproducible by reading the code
- **plausible** — reasoning is sound but depends on something unverifiable from
  the repo (provider runtime behavior, a production config value, a deploy
  setting). Say what would settle it.

Anything below `plausible` is not a finding. Drop it.

## Tie-breaks

- Authorization or data-exposure consequence beats everything else at the same
  apparent severity
- A silent failure outranks a loud one: the user does not know to recover
- Doc-vs-code drift on a *safety* or *security* claim is P1, not P3 — someone
  is relying on it
