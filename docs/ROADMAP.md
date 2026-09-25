# Universal Task AI — Living Roadmap

This roadmap is intentionally changeable. New requirements can add, remove, reorder, or split work.

## Phase 0 — Foundation

- [x] Public repository created
- [x] Engineering Constitution
- [x] README and development baseline
- [x] Strict Task Contract
- [x] Task Contract validation
- [x] Initial unit tests
- [ ] CI verification on GitHub
- [ ] Baseline security test suite

## Phase 1 — Understanding and Planning

- [x] Task Analyzer
- [x] Requirement extraction
- [x] Ambiguity classification
- [x] Planner schema
- [x] Plan validation
- [ ] Router policy
- [ ] Execution budget / max turns

## Phase 2 — Safe Tool Runtime

- [ ] Tool interface and registry
- [ ] Tool permission model
- [ ] Tool input/output guardrails
- [ ] Audit events
- [ ] Calculator
- [ ] File reader
- [ ] Web search
- [ ] Web reader
- [ ] Python execution only inside sandbox

## Phase 3 — Review and Reliability

- [ ] Reviewer agent
- [ ] Deterministic validators
- [ ] Retry policy
- [ ] Failure classification
- [ ] Idempotency rules
- [ ] Human approval state machine
- [ ] Run state persistence

## Phase 4 — Memory and Long-Running Work

- [ ] Short-term run state
- [ ] Durable task state
- [ ] Long-term memory
- [ ] Retention policy
- [ ] Background jobs
- [ ] Resume after interruption

## Phase 5 — Local Agent

- [ ] Local permission broker
- [ ] Sandboxed workspace
- [ ] Filesystem scopes
- [ ] Network policy
- [ ] Process/resource limits
- [ ] Secret redaction
- [ ] Local audit log
- [ ] Approval UI

## Phase 6 — Product

- [ ] Web UI
- [ ] Task/run history
- [ ] Live execution events
- [ ] Artifact management
- [ ] User settings
- [ ] Authentication
- [ ] Rate limits
- [ ] Deployment

## Engineering rule

A feature that increases model authority must update the threat model, permissions, tests, and documentation in the same change.

Reference patterns include OpenAI agent guardrails/tracing, stateful workflow persistence, and simple composable agent patterns. These are references, not code to copy blindly.
