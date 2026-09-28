# Production Go-Live Checklist

This checklist is an operator gate for the first real deployment. A successful local or CI rehearsal is **not** evidence that production is deployed.

## 1. Infrastructure and access

- [ ] A production host and supported Docker Engine / Compose version are provisioned.
- [ ] The host is patched, time-synchronized, monitored, and restricted to required inbound ports.
- [ ] SSH access uses a dedicated deployment identity with least privilege.
- [ ] The GitHub `production` Environment has required reviewers configured where supported.
- [ ] Environment secrets are set: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PATH`, `DEPLOY_SSH_KEY`, and `DEPLOY_KNOWN_HOSTS`.
- [ ] The SSH known-hosts entry was obtained and verified through a trusted channel; host checking remains enabled.
- [ ] The deployment directory contains the reviewed `docker-compose.prod.yml` and required non-secret configuration.

## 2. Immutable release and configuration

- [ ] A release image exists in GHCR for a reviewed commit.
- [ ] The exact image digest (`sha256:...`) is recorded; do not deploy mutable tags such as `latest`.
- [ ] The deployment input is confirmed to resolve to the intended immutable image. If the workflow accepts only a tag, verify that the tag is the full commit SHA and record the resulting digest before rollout.
- [ ] Required runtime secrets are provisioned through the approved secret mechanism and are not stored in the repository, image, command line, or logs.
- [ ] Public API authentication is enabled and the initial API key is distributed through a secure channel.
- [ ] External search/network access is configured only if required; egress restrictions remain enabled.
- [ ] Persistent storage location, permissions, capacity, and backup policy are verified.

## 3. Pre-deployment gate

- [ ] CI unit tests and integration/security checks pass for the exact release commit.
- [ ] Production rehearsal passes for the exact release commit.
- [ ] The image is built from the reviewed commit and its digest/provenance are retained.
- [ ] Database/schema migration and backward-compatibility expectations are reviewed.
- [ ] A backup or recovery point exists for persistent run, approval, and audit state.
- [ ] A previous known-good immutable image digest and rollback operator are identified.
- [ ] Maintenance window and an operator with production access are available.

## 4. Deploy and verify

- [ ] Trigger the protected **Production Deployment** workflow with the reviewed release identifier.
- [ ] Confirm the deployment job succeeds; do not paste secrets or raw logs containing sensitive values into tickets or chat.
- [ ] Confirm Compose services are running and restart counts are stable.
- [ ] Verify `/health` returns healthy and `/ready` reports durable dependencies ready.
- [ ] Verify unauthenticated requests to protected API endpoints are rejected.
- [ ] Verify an authenticated, low-risk smoke task succeeds without enabling filesystem, browser, process, or network capabilities unnecessarily.
- [ ] Verify the expected release identity matches the deployed commit/image.
- [ ] Verify container hardening (non-root user, read-only root filesystem, not privileged, dropped capabilities, resource limits, and immutable sandbox image digest where applicable).
- [ ] Verify logs and audit events are produced without API keys, tokens, passwords, raw secret values, or raw approval invocation arguments.
- [ ] Verify monitoring, alerts, disk capacity, and backup jobs are active.

## 5. Rollback and incident readiness

- [ ] Rollback steps are documented and tested against the known-good immutable image.
- [ ] The operator knows how to stop new task intake while preserving audit evidence.
- [ ] Rollback does not delete persistent volumes or approval/audit databases.
- [ ] A failed readiness check, authentication regression, unexpected capability grant, secret exposure, or audit persistence failure triggers a stop-and-investigate decision.
- [ ] Incident contact and secret-rotation procedures are available.

## 6. Sign-off record

Record this outside source control; never put credentials or private host details in this file.

- Release commit:
- Image digest:
- Deployment date/time (UTC):
- Operator:
- CI run:
- Rehearsal run:
- Health and readiness result:
- Smoke test result:
- Backup/recovery point:
- Rollback image digest:
- Known issues / follow-up:
- Final decision: **NOT DEPLOYED / DEPLOYED / ROLLED BACK**

The roadmap may mark production deployment complete only after a real rollout is verified and the sign-off record is completed. Checking boxes in this document or passing rehearsal alone does not constitute deployment.
