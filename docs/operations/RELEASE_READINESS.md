# Release readiness

This checklist defines the boundary between a tested release candidate and a real production rollout.

## Batch controls

1. **Version identity** — the API exposes the immutable application version and optional build SHA through the public health response.
2. **Local smoke test** — `scripts/smoke_local.py` verifies liveness, authentication denial, and authenticated tool discovery without invoking side-effecting tools.
3. **Production preflight** — `scripts/production_preflight.py` fails closed unless deployment SSH settings are present and `UTA_IMAGE` is an immutable GHCR sha256 digest.
4. **Rollback discipline** — production deployment accepts an explicit immutable image tag; operators can redeploy the previous known-good digest.
5. **Verification gate** — CI, integration/security, and production rehearsal must pass before a release is treated as deployable.

## Local use

Start the local application with the existing launcher, configure `UNIVERSAL_TASK_AI_API_KEY`, then run:

```bash
python scripts/smoke_local.py
```

The smoke test intentionally does not create tasks, execute tools, modify files, or contact external services.

## Production use

Run the preflight with deployment environment variables and an immutable image:

```bash
UTA_IMAGE=ghcr.io/OWNER/REPO@sha256:<64-hex> \
python scripts/production_preflight.py
```

A passing preflight is necessary but not sufficient for deployment. The protected GitHub production environment and manual deployment workflow remain the final authorization boundary.

## Security rule

Never replace a digest with a mutable tag in production. Never treat a successful rehearsal as proof that a real production target was deployed.


## Browser approval flow
The web UI requires an explicit approval actor ID and sends it as the bounded `actor_id` request field for both approve and reject decisions. The actor identifier is stored only in browser session storage and is not a capability grant.
