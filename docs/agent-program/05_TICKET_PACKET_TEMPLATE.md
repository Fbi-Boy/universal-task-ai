# 05 — Ticket Packet Template

Every AI assignment must have a ticket packet. If the packet cannot be filled, the task is not READY. Use GitHub Issue as the canonical assignment record and copy this template into the issue.

## Required fields

### Identity
- Ticket ID and title:
- Epic/workstream:
- Primary agent:
- Independent reviewer:
- Owner decision needed (yes/no and why):
- Target base branch + base SHA:
- Feature/fix/docs branch:
- Dependencies and linked issues:

### Problem and user value
- User role/persona:
- Job to be done:
- Current behavior verified in source:
- Expected outcome:
- Evidence the problem exists:

### Scope
- Included:
- Explicitly excluded:
- Acceptance criteria (Given / When / Then):
- Files/directories the agent may edit:
- Files/directories the agent must not edit:
- Shared API/data/design contracts affected:

### Architecture, data and permission
- Existing module to reuse:
- API request/response contract:
- Data entities/migration:
- Identity and workspace scope:
- Allowed actions/permissions:
- Secret or personal data:
- Retry/idempotency/timeout/cancellation behavior:
- Compatibility/rollback:

### Design (required for visual changes)
- Page/route and role:
- Approved reference board:
- Approval status/record:
- Shared tokens/components to use:
- States: initial/loading/empty/validation/success/partial/failure/unauthorized/disabled/mobile:
- Screenshot checkpoints/viewports:

### Risks and test plan
- Happy path:
- At least five relevant edge/failure cases:
- Unit tests:
- API/contract/integration tests:
- Security/tenant-isolation tests:
- Browser/accessibility tests:
- Exact commands to run:
- Required documentation:

### Exit conditions
- [ ] Acceptance criteria have evidence.
- [ ] Scope and file ownership respected.
- [ ] Shared contracts and permissions are correct.
- [ ] Tests actually ran; unrun tests are labelled NOT RUN.
- [ ] Independent review and findings are recorded.
- [ ] CI passed on latest PR HEAD.
- [ ] Screenshot/reference comparison included for visual work.
- [ ] Limitations and follow-ups are documented.
- [ ] A0 accepted integration; owner approval received where required.

## Issue status definitions

- **READY** — fully specified, dependency clear, design approved if applicable.
- **IN_PROGRESS** — assigned agent is actively working in its branch.
- **BLOCKED** — needs decision, upstream contract, credential, provider access, or failing environment.
- **REVIEW** — PR open, implementer self-review complete, evidence attached.
- **ACCEPTED** — independent review and required CI pass.
- **DONE** — merged and status/docs updated.

Never label incomplete work DONE to improve a progress chart.
