# 11 — Program Risk Register

This initial register captures risks seen in the product proposal and earlier static repository audit. A0/A12 must refresh each item against current source, PRs, and test evidence every sprint. A risk owner is a canonical role from docs/agent-system; assignment is not proof that the risk is mitigated.

| ID | Risk | Likelihood / impact | Mitigation | Owner | Initial status |
|---|---|---|---|---|---|
| R-01 | Single global API key mistaken for SaaS user identity | High / Critical | Add user/session/workspace auth while preserving local developer mode; authorization and cross-tenant regression tests | A5 | OPEN |
| R-02 | Default user and in-memory settings are not durable per-user SaaS state | High / High | Persist settings for authenticated user/workspace; migration and restart tests | A5 | OPEN |
| R-03 | Dashboard prototype uses illustrative activity/metrics | High / High | Replace with real API data or visibly mark demo; browser tests for truthful states | A4 | OPEN |
| R-04 | Frontend build/lockfile/current PR screenshot behavior not yet verified | Medium / High | Re-run dependency install, lint/typecheck/build and browser smoke on latest PR head | A4 + A12 | VERIFY |
| R-05 | WhatsApp inbound payload mapping was unfinished in earlier main audit | High / High | Re-verify current branch; complete provider mapping, account link, opt-in, signature, dedupe and sandbox end-to-end test | A8 | OPEN |
| R-06 | Campus LMS APIs/permissions vary by provider | High / High | Choose one authorized pilot, follow official API/consent rules and maintain separate adapters/capability claims | A8 | OPEN |
| R-07 | Attendance automation risks academic integrity/privacy | Medium / Critical | Limit to reminders and official-link navigation; no spoofing, hidden check-in or identity deception | A0 + A8 | CONTROL REQUIRED |
| R-08 | Duplicate webhook/retry can create duplicate AI task or external side effect | Medium / High | Unique event keys, idempotency ledger, queue/outbox, documented retry semantics and regression tests | A8 + A6/A7 | OPEN |
| R-09 | Prompt injection/model output can request unauthorized tools or expose content | Medium / Critical | Preserve deterministic runtime boundary, least privilege, approval, sandbox and untrusted-input tests | A7 + A12 | CONTROL REQUIRED |
| R-10 | Workflow canvas may be mistaken for an executor or bypass permissions | High / High | Typed versioned workflow, server graph validation, trusted worker, allowed-tool contract and approval gate | A9 | OPEN |
| R-11 | Pages drift into inconsistent visual systems | High / Medium | Page-specific source-backed boards, shared token/component owner, owner design approval and screenshot comparison | A2 + A3 | OPEN |
| R-12 | Too many parallel agents create contract/style/migration/file conflicts | High / High | Concurrency cap, one owner per shared path, frozen contracts, small PRs and independent review | A0 | CONTROL REQUIRED |
| R-13 | Free model endpoint/quota may change or fail | High / Medium | Configurable ModelGateway, budgets, timeouts and honest provider failure/fallback; never promise unlimited free usage | A7 | OPEN |
| R-14 | Usage/payment webhooks could be replayed or double-counted | Medium / High | Verified signatures, idempotent usage ledger, state transitions, reconciliation and cross-tenant tests | A0 + A5 + A12; activate A11 for billing | FUTURE |
| R-15 | Simple ERD/flowchart validator is confused with complete parser/editor | Medium / Medium | Claim only supported formats; require actual parse/render/version/export acceptance tests per format | A10 | OPEN |
| R-16 | Container build/rehearsal is mistaken for a live production rollout | Medium / High | Distinguish build, rehearsal and deployment; require immutable artifact, health/rollback evidence and owner approval | A13 | CONTROL REQUIRED |
| R-17 | Design screenshots/assets are copied without usage rights | Medium / High | Link references for research, record licensing/usage and use authorized product assets only | A2 + A3 | CONTROL REQUIRED |

## Risk handling

- BLOCKER / CRITICAL: no merge or release until the owner and A0 agree on an effective mitigation and A12 validates evidence.
- HIGH: must be mitigated or explicitly re-scoped by the product owner before release; do not silently downgrade it.
- OPEN: investigation or mitigation is still required.
- CONTROL REQUIRED: the control is mandatory for every ticket that touches the relevant boundary.
- VERIFY: re-run against the latest code; earlier observations are not assumed current.
- FUTURE: not in active scope yet; revisit when that phase starts.
- VERIFIED: may be used only after a current source/test/review link proves the mitigation works.
