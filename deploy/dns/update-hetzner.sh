#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${1:-book-club.qa.guru}"
TARGET_IP="${2:?target IP required}"
TOKEN="${HETZNER_DNS_TOKEN:?HETZNER_DNS_TOKEN is required}"

ZONE_NAME="${DOMAIN#*.}"
RECORD_NAME="${DOMAIN%%.*}"

api() {
  local method="$1"
  local path="$2"
  local data="${3:-}"
  if [ -n "$data" ]; then
    curl -fsS -X "$method" \
      -H "Auth-API-Token: ${TOKEN}" \
      -H "Content-Type: application/json" \
      "https://dns.hetzner.com/api/v1${path}" \
      -d "$data"
  else
    curl -fsS -X "$method" \
      -H "Auth-API-Token: ${TOKEN}" \
      "https://dns.hetzner.com/api/v1${path}"
  fi
}

ZONE_ID="$(api GET "/zones?name=${ZONE_NAME}" | jq -r '.zones[0].id // empty')"
if [ -z "$ZONE_ID" ]; then
  echo "Zone ${ZONE_NAME} not found in Hetzner DNS"
  exit 1
fi

RECORDS="$(api GET "/records?zone_id=${ZONE_ID}&name=${RECORD_NAME}")"
RECORD_ID="$(echo "$RECORDS" | jq -r ".records[] | select(.name==\"${RECORD_NAME}\") | .id" | head -1)"
RECORD_TYPE="$(echo "$RECORDS" | jq -r ".records[] | select(.name==\"${RECORD_NAME}\") | .type" | head -1)"

if [ -n "$RECORD_ID" ] && [ "$RECORD_TYPE" = "A" ]; then
  api POST "/records/${RECORD_ID}" "$(jq -nc \
    --arg zone_id "$ZONE_ID" \
    --arg name "$RECORD_NAME" \
    --arg value "$TARGET_IP" \
    '{zone_id:$zone_id,type:"A",name:$name,value:$value,ttl:60}')"
  echo "Updated A record ${DOMAIN} -> ${TARGET_IP}"
elif [ -n "$RECORD_ID" ]; then
  api DELETE "/records/${RECORD_ID}"
  api POST "/records" "$(jq -nc \
    --arg zone_id "$ZONE_ID" \
    --arg name "$RECORD_NAME" \
    --arg value "$TARGET_IP" \
    '{zone_id:$zone_id,type:"A",name:$name,value:$value,ttl:60}')"
  echo "Replaced ${RECORD_TYPE} record with A ${DOMAIN} -> ${TARGET_IP}"
else
  api POST "/records" "$(jq -nc \
    --arg zone_id "$ZONE_ID" \
    --arg name "$RECORD_NAME" \
    --arg value "$TARGET_IP" \
    '{zone_id:$zone_id,type:"A",name:$name,value:$value,ttl:60}')"
  echo "Created A record ${DOMAIN} -> ${TARGET_IP}"
fi
