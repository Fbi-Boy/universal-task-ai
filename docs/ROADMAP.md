# Universal Task AI — Living Roadmap

The roadmap tracks implemented, verified milestones. A checkbox is marked complete only when the repository contains the implementation and regression coverage appropriate to that milestone.

## Phase 0 — Foundation

- [x] Public repository created
- [x] Engineering Constitution
- [x] README and development baseline
- [x] Strict Task Contract
- [x] Task Contract validation
- [x] Initial unit tests
- [x] CI workflow configured
- [x] Baseline security regression suite

## Phase 1 — Understanding and Planning

- [x] Task Analyzer
- [x] Requirement extraction
- [x] Ambiguity classification
- [x] Planner schema
- [x] Plan validation
- [x] Router policy
- [x] Execution budget / max turns

## Phase 2 — Safe Tool Runtime

- [x] Tool interface and registry
- [x] Tool permission model
- [x] Tool input/output guardrails
- [x] Audit event model
- [x] Calculator
- [x] File reader policy
- [ ] Web search provider implementation
- [x] Web reader / resolved-address policy
- [x] Python execution only inside a real container sandbox

## Phase 3 — Review and Reliability

- [x] Deterministic validators
- [x] Failure classification
- [x] Bounded retry policy
- [x] Idempotency primitive
- [x] Human approval state machine
- [x] Run state persistence
- [x] Reviewer agent integration

## Phase 4 — Memory and Long-Running Work

- [x] Short-term memory primitive
- [x] Durable task/run state
- [x] Retention policy primitive
- [x] Bounded background job runner
- [x] Long-term semantic memory
- [x] Resume orchestration after interruption

## Phase 5 — Local Agent

- [x] Local permission broker
- [x] Filesystem root containment policy
- [x] Network policy enforcement
- [x] Process/resource limits enforced by sandbox
- [x] Secret redaction primitive
- [x] Local persistent audit sink
- [x] Approval UI

## Phase 6 — Product

- [x] Minimal FastAPI API
- [x] Web UI
- [x] Task/run history UI
- [x] Live execution events
- [x] Artifact management
- [x] User settings
- [x] Authentication
- [x] Rate limits
- [ ] Production deployment

## Phase 7 — Production Hardening

- [ ] Real external search adapter
- [x] Safe HTTP reader with resolved-address revalidation
- [x] Docker/OCI execution sandbox
- [x] Network egress allowlist
- [x] Resource quotas
- [x] Database migrations
- [ ] Distributed queue
- [ ] Secret management integration
- [ ] Full integration/security CI

## Engineering rule

A feature that increases model authority must update the threat model, permissions, tests, and documentation in the same change. A checkbox is not complete merely because a stub exists.
