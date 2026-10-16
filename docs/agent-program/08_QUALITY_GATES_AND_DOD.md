# 08 — Quality Gates & Definition of Done

## Gate overview

| Gate | Required outcome | Approver | Stop condition |
|---|---|---|---|
| G0 — Problem | persona, goal, scope, edge cases, acceptance criteria | A0 + owner if scope decision | unclear outcome or unauthorized goal |
| G1 — Design | 3–5 image/screenshot references, coherent synthesis, design-system mapping, owner approval | Owner + A0/A2/A3 | no page-specific approval |
| G2 — Contract | API/data/state/permission/error contracts and dependencies frozen | A0 + domain owners + A12 | schema or ownership ambiguity |
| G3 — Implementation | scoped branch, allowed files, working vertical slice, tests/docs | workstream owner | scope creep or security shortcut |
| G4 — Independent review | diff, failure modes, accessibility, permissions, dependencies reviewed | A12 + appropriate domain reviewer | unresolved blocker/high-severity issue |
| G5 — Evidence | exact test outputs, API/E2E evidence, screenshots; checks correctly marked | A12 | missing/failed required test or false claim |
| G6 — Integration/release | latest-head CI passes, migrations/rollback checked, docs updated | A0; owner for high risk | unverified release, unsafe migration or missing owner approval |

Backend-only work may mark G1 not applicable only with a reason. Any change visible to a user must follow G1, even if called a quick fix; small accessibility/content changes may reuse an existing approved board if the visual direction does not change.

## Definition of Done

- [ ] Acceptance criteria are mapped to reproducible evidence.
- [ ] Code reuses current architecture and does not introduce unapproved parallel systems.
- [ ] Server-side identity, role permissions and tenant scope are enforced where data/actions are involved.
- [ ] Data schema, migration, constraints, indexes, upgrade and rollback/recovery are addressed.
- [ ] Input/output sizes, validation, timeouts and rate limits are bounded where applicable.
- [ ] Idempotency/deduplication covers webhook, worker retry and repeated requests where relevant.
- [ ] Sensitive side effects use explicit authorization/approval and audit.
- [ ] Secret and personal-data leakage checks are considered.
- [ ] Loading, empty, success, validation, offline/timeout, permission denied, retry and failure states are truthful.
- [ ] UI follows approved references and shared tokens; screenshot comparison is attached.
- [ ] Keyboard, focus, labels, contrast and responsive behavior reviewed for UI.
- [ ] Tests actually run: unit, API/contract, integration/security and browser/E2E as applicable.
- [ ] Lint, type check, build and CI pass on latest PR HEAD.
- [ ] Documentation/contracts/runbooks and Program State updated.
- [ ] Independent reviewer findings resolved and attached.
- [ ] Remaining limitations and unrun checks are explicit.
- [ ] Merge/release approvals obtained.

## Severity and blocking

**BLOCKER:** secret exposure, cross-tenant access, permission bypass, spoofed official action, destructive data loss, unbounded execution, or false production claim. Never merge.

**HIGH:** broken main user flow, incorrect task/run status, duplicate side effect, unsafe migration, unauthorized write, or a major accessibility/contract failure. Do not merge until fixed or owner formally re-scopes the release.

**MEDIUM:** important error/retry/empty states, incomplete test coverage, unusable layout on a target viewport, or undocumented compatibility issue. Must be fixed before marking feature DONE; may be scheduled only if product owner explicitly accepts the known risk and release policy permits it.

**LOW:** minor polish with no meaningful security/correctness/usability impact; log as issue.

## Evidence table format

| Check | Command or action | Environment/commit | Result | Evidence link |
|---|---|---|---|---|
| Unit | actual command | exact SHA | PASS/FAIL/NOT RUN | CI/log |
| API/integration | actual command | exact SHA | PASS/FAIL/NOT RUN | CI/log |
| Browser | route/viewports/actions | exact SHA | PASS/FAIL/NOT RUN | screenshot/video |
| Security | negative scenario | exact SHA | PASS/FAIL/NOT RUN | test/issue |
| Build | actual build command | exact SHA | PASS/FAIL/NOT RUN | CI/log |

A clean screenshot does not prove an API works. A passing unit test does not prove multi-tenant isolation. A CI run on an older SHA does not validate the latest PR head.
