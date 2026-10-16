# 06 — Design Research, Image References & Approval

## The design process is evidence-led

The design agent must not start with “make it modern”. It begins with the route, role, user goal, key data, risk, viewport and known design tokens. Then it studies real visual references and recommends a coherent direction.

### Required research packet per page or closely related page cluster

1. **Page brief:** persona, job-to-be-done, primary action, secondary actions, key information, status states, constraints and viewport.
2. **Reference set:** 3–5 relevant screenshot/image references from at least two independent domains. Include one real product/official UI or documentation reference to verify interaction behavior where available.
3. **Evidence card per image:** screenshot, direct source URL, title/product/designer, date inspected, why it matches this task, pattern to borrow, pattern to reject, asset/license caveat.
4. **Comparison matrix:** hierarchy, information density, navigation, interaction, accessibility, responsiveness, empty/error states, and fit to Universal Task AI.
5. **Synthesis:** one recommended visual direction and wireframe/page structure. Do not present a collage with no conclusion.
6. **System mapping:** existing semantic color tokens, typography, spacing, grid, component and icon system to reuse. Proposed global changes go through A0/A2 review.
7. **Approval record:** owner accepts, accepts with changes or rejects; include comments and a stable link to the board/issue.
8. **Implementation comparison:** screenshot of the real running page at desktop and mobile sizes, with intentional deviations documented.

## Where to research

- Pinterest, Dribbble and Behance: explore visual composition, layout alternatives and visual patterns.
- Real products and official docs: establish interaction behavior and real data/state expectations.
- GitHub repositories: study implementation patterns, component structure, tests, maintenance, dependencies and license.
- Accessibility references: check keyboard behavior, focus, labels, contrast and responsive use.

Research search examples should be page-specific: “task detail panel dense SaaS project management desktop”, “workflow node editor inspector run history”, “ERD schema text canvas”, “workspace members permission settings”, not just “best dashboard UI”.

## Approval gate

Reference board statuses:
- NEEDS RESEARCH
- READY FOR OWNER REVIEW
- APPROVED
- APPROVED WITH CHANGES
- REJECTED
- SUPERSEDED

No production UI implementation begins unless the route is APPROVED or APPROVED WITH CHANGES and changes have been incorporated. A prototype may be allowed solely for comparison when it is clearly labelled and isolated from production integration.

An approval is tied to a particular route/role, board revision, and design-system version. A material layout/navigation change requires renewed approval. Small content/accessibility fixes that do not alter the approved visual direction do not need a full resubmission.

## Consistency rules

- Shared app shell, typography, spacing, semantic colors, radii, shadows, icon family and states are owned centrally.
- Dark/diagram/code surfaces can be denser but still use the same semantic tokens.
- Role-specific layouts are created only when the task and permissions genuinely differ; otherwise reuse the shell with permission-aware actions.
- No arbitrary gradients, fake charts, invented metrics, decorative widgets, mixed icon sources, orphaned components or inert actions.
- Product references are not licenses to copy logos/artwork/source assets. Cite sources and use assets only when usage rights permit.
- Reference screenshots show inspiration, not proof that a feature exists or that an integration is supported.
