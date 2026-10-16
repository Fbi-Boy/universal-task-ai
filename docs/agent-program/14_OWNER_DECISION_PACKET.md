# Sprint 0 — Owner Decision Packet

**Status: DECISIONS PENDING — this document proposes defaults, not approvals.**  
Prepared: 2026-10-16  
Repository: `Fbi-Boy/universal-task-ai`

This packet collects the decisions that block a trustworthy Sprint 0 exit. The owner can accept, reject, or amend each proposal. No provider is selected, no spend is authorized, and no production integration is approved by this document.

## 1. Decisions that unblock the next sprint

### D1 — First integrated vertical slice

**Decision owner:** Product owner  
**Current state:** PENDING  
**Recommended default:** Deliver one complete, authenticated student flow: create/open a task → request an AI draft → inspect/edit the draft → explicitly save the artifact to that task → reopen it. Use controlled test data. Do not include campus scraping, attendance actions, WhatsApp production delivery, or billing in this first slice.

**Why:** It proves identity, task ownership, AI-run state, artifact persistence, review/approval and failure recovery together without depending on unconfirmed third-party access.

**Alternatives:**  
- A. Task/project management only, then add AI artifacts in a later slice.  
- B. Campus assignment sync first, once an authorized provider and access method are supplied.  
- C. Another narrowly scoped slice described by the owner.

**Owner decision:** `PENDING` — choose A, B, C, or amend the recommendation.

### D2 — Identity and workspace model

**Decision owner:** Product owner + A0 architecture; A12 independently reviews security  
**Current state:** PENDING  
**Recommended default:** Require per-user sessions and enforce workspace/resource ownership server-side. Treat the current global bearer API key and fixed `DEFAULT_USER` / in-memory settings as development primitives only—not production multi-user authentication or tenant isolation.

**Options to evaluate:** a managed identity provider with standards-based sessions; an application-owned identity/session implementation; or an existing campus identity provider if its authorization and long-term access model fit the product. Provider selection is deliberately not made here.

**Minimum acceptance regardless of provider:** unauthenticated requests are rejected; user A cannot read or mutate user B's tasks, settings, runs or artifacts; secrets are kept server-side; session/token rotation and revocation are defined; authorization tests cover cross-tenant access.

**Owner decision:** `PENDING` — identify any mandatory identity provider, or authorize a provider comparison before choosing.

### D3 — Durable data and artifact storage

**Decision owner:** Product owner + A0/A5; A12 reviews privacy/security  
**Current state:** PENDING  
**Recommended default:** Use a durable relational database with migrations for users/workspaces, tasks/projects, AI runs, artifacts, approvals and audit metadata. Store artifact ownership and lifecycle explicitly; do not treat an in-memory store as durable SaaS storage. Keep binary/file storage behind an owned adapter if needed.

**Owner choices needed:** acceptable hosting/data region, expected budget, backup/restore expectations, retention/deletion policy, and whether generated files may contain sensitive coursework or personal information.

**Owner decision:** `PENDING` — supply constraints or authorize a brief option comparison.

### D4 — First campus source and access method

**Decision owner:** Product owner  
**Current state:** BLOCKED — no campus/platform and authorized API/access method confirmed  
**Recommended default:** Do not start a campus connector until the owner names the institution/platform and provides official API documentation or confirms another explicitly authorized integration method. Prefer documented APIs, OAuth/SSO or permitted exports. Do not bypass authentication, scrape protected pages, or store campus credentials without an approved security model.

**Evidence required:** provider name, official documentation, permission/terms, test account or sandbox availability, supported assignment fields, rate limits and expected data-refresh behavior.

**Owner decision:** `PENDING` — identify the first campus/provider, or defer this integration beyond the first slice.

### D5 — WhatsApp and notification route

**Decision owner:** Product owner; A8/A9 propose implementation, A12 reviews consent and abuse controls  
**Current state:** PENDING  
**Recommended default:** Begin with an in-app notification/task reminder path that can be tested without third-party credentials. When WhatsApp is approved, use the official WhatsApp Business Platform or an explicitly authorized provider, verified webhook signatures, opt-in/opt-out, idempotency, delivery status, rate limits and secret rotation. No unofficial WhatsApp Web automation.

**Owner choices needed:** whether WhatsApp is in the first release, approved provider/account, message-cost budget, opt-in language, allowed message types and retention.

**Owner decision:** `PENDING` — choose `IN-APP FIRST`, name an authorized WhatsApp provider, or defer messaging.

### D6 — Model provider and spend limits

**Decision owner:** Product owner; A7/A11 propose enforcement, A12 reviews data handling  
**Current state:** PENDING  
**Recommended default:** Keep providers configurable behind the existing model gateway; enforce server-side per-user/workspace usage limits and timeouts, and never expose provider secrets to the browser. Do not enable paid production usage until the owner sets a budget and data-handling rule.

**Owner choices needed:** preferred provider(s), monthly budget or hard cap, models/features permitted, whether coursework/personal data can be sent to external model services, and fallback behavior when limits are reached.

**Owner decision:** `PENDING` — give provider and budget constraints, or authorize a low-cost comparison only.

### D7 — Design direction for the representative screens

**Decision owner:** Product owner after A3 consistency review  
**Current state:** READY FOR OWNER REVIEW; NOT APPROVED  
**Recommendation from reference research:** light neutral shell; persistent and predictable navigation; restrained accent color; compact but readable task information; responsive desktop/mobile behavior; clear loading/empty/error/disabled/success states; explicit AI run, tool, approval and artifact context.

**Explicitly avoid:** fake metrics or charts, decorative gradients used as a substitute for hierarchy, copied assets without license review, inert controls and divergent per-page styling.

**Review evidence:** [Design-reference PR #185](https://github.com/Fbi-Boy/universal-task-ai/pull/185) and [issue #180](https://github.com/Fbi-Boy/universal-task-ai/issues/180). A3 consistency review, actual-running-app screenshot comparison, accessibility review and asset-license review remain separate gates.

**Owner decision:** `PENDING` — approve the recommendation, reject it with a direction, or request a focused revision after A3 review.

### D8 — Independent QA/security reviewer (A12) identity

**Decision owner:** Repository owner/maintainer  
**Current state:** BLOCKED — no distinct, authorized GitHub account is mapped to A12  
**Required action:** Add or identify an actual GitHub account that is allowed to review these changes and is independent of the A0 author/reviewer. Then request that account on the audit and applicable implementation PRs. Role IDs such as `A12` are governance labels, not GitHub usernames.

**Non-negotiable:** An A0 comment, an automated workflow pass, or the absence of objections is not A12 approval. Do not mark the independent review gate accepted until a distinct authorized reviewer records findings and disposition.

**Owner decision:** `PENDING` — supply the GitHub username or arrange another authorized independent reviewer.

### D9 — GitHub Project board access

**Decision owner:** Repository owner/maintainer  
**Current state:** BLOCKED — existing-board visibility and project write access were not available through the connected GitHub actions used for setup  
**Recommended action:** Use a Projects-capable authorized path to inspect existing boards first; reuse a suitable board or create one only after confirming none is suitable. Record its real URL and verify the canonical issues/fields in the UI or API. Do not create a duplicate based on missing visibility.

**Tracking:** [issue #182](https://github.com/Fbi-Boy/universal-task-ai/issues/182).

**Owner decision:** `PENDING` — provide access or the verified board URL and the authorized person who can validate configuration.

## 2. What is already drafted vs. what is approved

- [PR #183 — Sprint 0 audit/state](https://github.com/Fbi-Boy/universal-task-ai/pull/183): audit and program-state documentation. CI and Integration/Security checks passed on the last verified head; independent A12 review is still pending.
- [PR #184 — student workflow requirements](https://github.com/Fbi-Boy/universal-task-ai/pull/184): requirements draft reviewed by A0. The document is explicitly a draft; provider, identity, budget and first-slice decisions are not approved.
- [PR #185 — design reference review](https://github.com/Fbi-Boy/universal-task-ai/pull/185): reference board and synthesis. A0 alignment was recorded; A3 consistency review and product-owner design approval remain pending.
- [issue #177](https://github.com/Fbi-Boy/universal-task-ai/issues/177): repository baseline and in-flight PR audit; must not be closed as accepted before the independent review requirement is satisfied.
- [issue #179](https://github.com/Fbi-Boy/universal-task-ai/issues/179): requirements evidence exists, but unresolved owner decisions and required review gates remain.
- [issue #180](https://github.com/Fbi-Boy/universal-task-ai/issues/180): reference research exists, but A3 and owner approval remain.
- [issue #181](https://github.com/Fbi-Boy/universal-task-ai/issues/181): shared contract/security review depends on the audit gate.
- [issue #182](https://github.com/Fbi-Boy/universal-task-ai/issues/182): Project board verification is access-blocked.

These are point-in-time references. Refresh each PR's current head and checks before making a merge/acceptance decision.

## 3. Sprint 0 exit checklist

- [ ] D1 first vertical slice selected.
- [ ] D2 identity/session direction and tenant isolation criteria recorded.
- [ ] D3 persistence, hosting, retention and deletion constraints recorded.
- [ ] D4 campus provider/access route selected or explicitly deferred.
- [ ] D5 notification/WhatsApp scope and consent constraints recorded.
- [ ] D6 model provider/data policy and spend limits recorded.
- [ ] D7 design direction decided after A3 review.
- [ ] D8 distinct authorized A12 reviewer mapped and independent review completed.
- [ ] D9 GitHub Project board verified/reused/created through an authorized path.
- [ ] Shared contracts and security review have named owners, test evidence and dispositions.
- [ ] Sprint 1 tickets each have a scoped vertical slice, dependencies, file ownership, acceptance criteria and test commands.
- [ ] Program State is refreshed against actual main SHA, current PR heads and workflow results.

## 4. Lightweight decision reply format

Reply in the issue or PR thread with the key and answer, for example:

- `D1 = A`
- `D4 = defer until later`
- `D7 = approve recommendation`
- `D8 = @actual-github-reviewer`

Any unmentioned choice stays **PENDING**. No silence is treated as approval.
