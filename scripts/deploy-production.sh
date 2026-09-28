#!/usr/bin/env bash
set -euo pipefail

: "${IMAGE:?IMAGE is required}"
: "${DEPLOY_HOST:?DEPLOY_HOST is required}"
: "${DEPLOY_USER:?DEPLOY_USER is required}"
: "${DEPLOY_PATH:?DEPLOY_PATH is required}"

if [[ ! "${IMAGE}" =~ ^ghcr\.io/fbi-boy/universal-task-ai@sha256:[a-f0-9]{64}$ ]]; then
  echo "IMAGE must be the approved GHCR repository pinned to a sha256 digest." >&2
  exit 2
fi
if [[ ! "${DEPLOY_USER}" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "DEPLOY_USER contains unsupported characters." >&2
  exit 2
fi
if [[ ! "${DEPLOY_HOST}" =~ ^[A-Za-z0-9.-]+$ ]]; then
  echo "DEPLOY_HOST must be a DNS name or IPv4 address." >&2
  exit 2
fi
if [[ ! "${DEPLOY_PATH}" =~ ^/[A-Za-z0-9._/-]+$ || "${DEPLOY_PATH}" == *".."* ]]; then
  echo "DEPLOY_PATH must be an absolute path without spaces, quotes, or parent traversal." >&2
  exit 2
fi

printf -v remote_deploy 'cd -- %q && UTA_IMAGE=%q docker compose -f docker-compose.prod.yml pull && UTA_IMAGE=%q docker compose -f docker-compose.prod.yml up -d --remove-orphans' "$DEPLOY_PATH" "$IMAGE" "$IMAGE"
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes "${DEPLOY_USER}@${DEPLOY_HOST}" "$remote_deploy"

printf -v remote_status 'cd -- %q && docker compose -f docker-compose.prod.yml ps' "$DEPLOY_PATH"
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes "${DEPLOY_USER}@${DEPLOY_HOST}" "$remote_status"
