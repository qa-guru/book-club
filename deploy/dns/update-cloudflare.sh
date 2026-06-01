#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${1:-book-club.qa.guru}"
TARGET_IP="${2:?target IP required}"
TOKEN="${CLOUDFLARE_API_TOKEN:?CLOUDFLARE_API_TOKEN is required}"

ZONE_NAME="${DOMAIN#*.}"

api() {
  local method="$1"
  local path="$2"
  local data="${3:-}"
  if [ -n "$data" ]; then
    curl -fsS -X "$method" \
      -H "Authorization: Bearer ${TOKEN}" \
      -H "Content-Type: application/json" \
      "https://api.cloudflare.com/client/v4${path}" \
      -d "$data"
  else
    curl -fsS -X "$method" \
      -H "Authorization: Bearer ${TOKEN}" \
      "https://api.cloudflare.com/client/v4${path}"
  fi
}

ZONE_ID="$(api GET "/zones?name=${ZONE_NAME}" | python3 -c "import json,sys; r=json.load(sys.stdin)['result']; print(r[0]['id'] if r else '')")"
if [ -z "$ZONE_ID" ]; then
  echo "Zone ${ZONE_NAME} not found in Cloudflare"
  exit 1
fi

RECORDS="$(api GET "/zones/${ZONE_ID}/dns_records?name=${DOMAIN}")"
read -r RECORD_ID RECORD_TYPE <<<"$(python3 -c "
import json, sys
records = json.load(sys.stdin)['result']
if records:
    print(records[0]['id'], records[0]['type'])
else:
    print('', '')
" <<<"$RECORDS")"

payload="$(python3 -c 'import json, sys; print(json.dumps({"type":"A","name":sys.argv[1],"content":sys.argv[2],"ttl":60,"proxied":False}))' "$DOMAIN" "$TARGET_IP")"

if [ -n "$RECORD_ID" ]; then
  api PATCH "/zones/${ZONE_ID}/dns_records/${RECORD_ID}" "$payload" >/dev/null
  echo "Updated ${RECORD_TYPE} record ${DOMAIN} -> ${TARGET_IP}"
else
  api POST "/zones/${ZONE_ID}/dns_records" "$payload" >/dev/null
  echo "Created A record ${DOMAIN} -> ${TARGET_IP}"
fi
