# Production deployment

The repository provides a protected manual GitHub Actions deployment workflow for a production environment.

Required GitHub Environment secrets:
- `DEPLOY_HOST`
- `DEPLOY_USER`
- `DEPLOY_PATH`
- `DEPLOY_SSH_KEY`
- `DEPLOY_KNOWN_HOSTS`

The workflow:
1. accepts only an immutable GHCR image digest in the form `sha256:<64 lowercase hexadecimal characters>`
2. deploys `ghcr.io/fbi-boy/universal-task-ai@sha256:...`, never a mutable tag
3. runs only against the protected `production` environment
4. uses read-only repository/package permissions
5. requires an SSH known-hosts value rather than disabling host verification
6. fails closed when deployment configuration, digest, or path validation is invalid
7. shell-quotes remote commands and rejects unsafe host, user, and deployment-path characters
8. pulls the requested image and applies Docker Compose
9. verifies the resulting Compose services are running

After a successful Container Release workflow, copy the immutable digest shown in the GitHub Actions step summary into the Production Deployment workflow input. Do not deploy by tag alone.

A real production rollout remains dependent on configuring the protected environment secrets and performing the first deployment against the operator's infrastructure.
