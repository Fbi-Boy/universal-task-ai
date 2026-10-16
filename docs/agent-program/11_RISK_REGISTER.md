# 11 — Program Risk Register

This initial register captures risks observed in the repository and product proposal; A0/A12 must refresh status against the live main branch every sprint. Statuses are not test results.

| ID | Risk | Likelihood / impact | Mitigation | Owner | Initial status |
|---|---|---|---|---|---|
| R-01 | One global API key is used as SaaS identity | High / Critical | Introduce user/session/workspace auth, preserve local mode separately, add authorization and cross-tenant tests | A8 | OPEN |
| R-02 | Default user + in-memory settings do not represent durable per-user settings | High / High | Persist settings per authenticated user/workspace; migration and restart tests | A3 | OPEN |
| R-03 | Dashboard prototype shows example activity/metrics | High / High | Visibly label demo; replace with real APIs or remove; browser tests for truthfulness | A7 | OPEN |
| R-04 | Frontend build/lockfile or screenshot behavior not yet verified at current PR HEAD | Medium / High | Re-run install/lint/typecheck/build/smoke and resolve current issues | A4 + A12 | VERIFY |
| R-05 | WhatsApp inbound payload mapping is unfinished in audited main | High / High | Complete provider mapping, account linking, opt-in, signature, idempotency and end-to-end sandbox test | A5 | OPEN |
| R-06 | Campus LMS/integrations differ by platform and permissions | High / High | Select one authorized pilot; official API/consent; separate adapters and provider capability list | A5 | OPEN |
| R-07 | Attendance automation could create academic-integrity/privacy risk | Medium / Critical | Only reminders/open official links; no spoofing, hidden check-in or identity deception | A0 + A8 | CONTROL REQUIRED |
| R-08 | Duplicate webhook/worker retries may run task twice | Medium / High | Unique external event key, idempotency ledger, queue/outbox, retry semantics and regression tests | A8 + A6/A7 | OPEN |
| R-09 | Model output/prompt injection could request unauthorized tool or leak content | Medium / Critical | Existing deterministic permission boundary, untrusted-source handling, approval and sandbox | A7 + A12 | CONTROL REQUIRED |
| R-10 | Workflow canvas could be mistaken for an executor or bypass policy | High / High | Typed versioned graph + server validation + trusted worker + allowlisted tool/approval contract | A9 | OPEN |
| R-11 | Design fragments diverge between pages/roles | High / Medium | Reference boards, single design system owner, owner approval, screenshot comparison | A2 + A3 | OPEN |
| R-12 | Many parallel AIs create conflicting API, CSS, migration or file changes | High / High | Concurrency cap, single file owner, frozen contracts, small branches, independent review | A0 | CONTROL REQUIRED |
| R-13 | Free-model endpoints/quotas may change or fail | High / Medium | Model gateway, configurable provider, usage budget, timeout/fallback policy; never promise unlimited free use | A4 | OPEN |
| R-14 | Billing usage/provider webhooks can be double counted or spoofed | Medium / High | Verified signatures, dedupe IDs, server-side ledger and reconciliation tests | A0 + A5 + A12 | FUTURE |
| R-15 | Diagram validators are mistaken for full parsers/renderers | Medium / Medium | Advertise only formats with real parser/render/export acceptance tests | A10 | OPEN |
| R-16 | Release workflow may create image, mistaken for production deployment | Medium / High | Explicitly distinguish container build, rehearsal and live rollout; owner approval and evidence | A13 | CONTROL REQUIRED |
| R-17 | Reference screenshot assets could be copied without usage rights | Medium / High | Link source only, record license/usage, use licensed/internal assets in product | A2 + A3 | CONTROL REQUIRED |

## Risk handling

- CRITICAL / HIGH: owner and A0 must be notified; no release if unmitigated.
- OPEN means investigation/mitigation is still required.
- CONTROL REQUIRED means a mandatory control must be demonstrated for any relevant ticket.
- FUTURE means not in active scope, but risk must be reviewed before that phase begins.
- VERIFIED means independent evidence supports that the control is implemented; update only after review/tests.
