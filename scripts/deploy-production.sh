#!/usr/bin/env bash
set -euo pipefail

: "${IMAGE:?IMAGE is required}"
: "${DEPLOY_HOST:?DEPLOY_HOST is required}"
: "${DEPLOY_USER:?DEPLOY_USER is required}"
: "${DEPLOY_PATH:?DEPLOY_PATH is required}"

ssh -o BatchMode=yes -o StrictHostKeyChecking=yes "${DEPLOY_USER}@${DEPLOY_HOST}" \
  "cd '${DEPLOY_PATH}' && UTA_IMAGE="${IMAGE}" docker compose -f docker-compose.prod.yml pull && UTA_IMAGE="${IMAGE}" docker compose -f docker-compose.prod.yml up -d --remove-orphans"

ssh -o BatchMode=yes -o StrictHostKeyChecking=yes "${DEPLOY_USER}@${DEPLOY_HOST}" \
  "cd '${DEPLOY_PATH}' && docker compose -f docker-compose.prod.yml ps"
