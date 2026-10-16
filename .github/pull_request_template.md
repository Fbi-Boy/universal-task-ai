## Purpose and user outcome
<!-- Why is this change needed? Which user/role and acceptance criteria does it serve? -->

## Scope
- Included:
- Explicitly excluded:

## Coordination
- [ ] Linked GitHub Issue and dependencies
- [ ] Only assigned paths/contracts changed
- [ ] Shared contract/ADR updated or confirmed unchanged
- [ ] Design board linked and owner-approved for UI work
- [ ] No overlapping agent ownership or undocumented contract change

## Implementation and data
- [ ] Reused existing repository architecture
- [ ] API/schema and tenant/permission behavior reviewed
- [ ] Migration and rollback plan included, if applicable
- [ ] Secrets and personal data are not present in source, logs, URLs, screenshots or fixtures
- [ ] No fabricated metric, status, integration or success state

## Evidence and tests
- [ ] Acceptance criteria mapped to evidence in issue/PR
- [ ] Unit tests run: result / link
- [ ] API/integration/security tests run: result / link
- [ ] Lint/typecheck/build run: result / link
- [ ] Browser/accessibility checks run when relevant: result / link
- [ ] UI screenshots from the running app attached at desktop and mobile sizes
- [ ] Compared implementation to the approved design reference board
- [ ] Not-run tests are explicitly labelled NOT RUN (not treated as PASS)

## Risk review
- [ ] Authentication, workspace scope and permissions checked
- [ ] Retry/idempotency/timeout/partial-failure checked where applicable
- [ ] Error/empty/loading/disabled/recovery states are truthful
- [ ] No unsupported campus/attendance/official submission behavior
- [ ] Known limitations and follow-up issues listed

## Review and release
- [ ] A12 independent review completed for implementation work
- [ ] Required CI checks pass on the latest PR HEAD
- [ ] Documentation and program state updated
- [ ] No production deployment or secret/permission mutation performed without approval
