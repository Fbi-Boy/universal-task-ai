# Production deployment

The repository provides a protected manual GitHub Actions deployment workflow for a production environment.

Required GitHub Environment secrets:
- `DEPLOY_HOST`
- `DEPLOY_USER`
- `DEPLOY_PATH`
- `DEPLOY_SSH_KEY`
- `DEPLOY_KNOWN_HOSTS`

The workflow:
1. accepts an explicit immutable image tag input
2. runs only against the protected `production` environment
3. uses read-only repository/package permissions
4. requires an SSH known-hosts value rather than disabling host verification
5. fails closed when deployment configuration is missing
6. pulls the requested image and applies Docker Compose
7. verifies the resulting Compose services are running

A real production rollout remains dependent on configuring the protected environment secrets and performing the first deployment against the operator's infrastructure.
