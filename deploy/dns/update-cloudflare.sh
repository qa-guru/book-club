#!/usr/bin/env bash
# Upsert grey A record for a FQDN in Cloudflare.
# Default: dry-run. Pass --apply to mutate.
# Token SSOT: CLOUDFLARE_API_TOKEN or ~/.config/cloudflare-dns.token
set -euo pipefail

APPLY=0
DOMAIN=""
TARGET_IP=""

usage() {
  echo "Usage: $0 [--dry-run|--apply] <fqdn> <target-ip>" >&2
  echo "  Default is dry-run. Zone resolved by longest CF zone suffix match." >&2
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) APPLY=1; shift ;;
    --dry-run) APPLY=0; shift ;;
    -h|--help) usage ;;
    *)
      if [[ -z "$DOMAIN" ]]; then
        DOMAIN="$1"
      elif [[ -z "$TARGET_IP" ]]; then
        TARGET_IP="$1"
      else
        usage
      fi
      shift
      ;;
  esac
done

[[ -n "$DOMAIN" && -n "$TARGET_IP" ]] || usage

if [[ -n "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  TOKEN="$CLOUDFLARE_API_TOKEN"
elif [[ -f "${HOME}/.config/cloudflare-dns.token" ]]; then
  TOKEN="$(tr -d '[:space:]' <"${HOME}/.config/cloudflare-dns.token")"
else
  echo "Cloudflare token missing: set CLOUDFLARE_API_TOKEN or ~/.config/cloudflare-dns.token" >&2
  exit 2
fi

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

PYTHON="$(command -v python3 || command -v python || true)"
if [[ -z "$PYTHON" ]]; then
  echo "python3 (or python) is required for Cloudflare JSON parsing" >&2
  exit 127
fi

# Longest-suffix zone match (book-club.qa.guru → qa.guru; api.niffler.qa.guru → qa.guru).
ZONES_JSON="$(api GET "/zones?per_page=50")"
ZONE_ID="$(DOMAIN="$DOMAIN" "$PYTHON" -c "
import json, os, sys
fqdn = os.environ['DOMAIN'].rstrip('.').lower()
zones = json.load(sys.stdin).get('result') or []
best_id, best_len = '', -1
for z in zones:
    name = (z.get('name') or '').rstrip('.').lower()
    if fqdn == name or fqdn.endswith('.' + name):
        if len(name) > best_len:
            best_id, best_len = z.get('id') or '', len(name)
print(best_id)
" <<<"$ZONES_JSON")"

if [ -z "$ZONE_ID" ]; then
  echo "No Cloudflare zone matched for ${DOMAIN}" >&2
  exit 1
fi

ZONE_NAME="$(DOMAIN="$DOMAIN" "$PYTHON" -c "
import json, os, sys
fqdn = os.environ['DOMAIN'].rstrip('.').lower()
zones = json.load(sys.stdin).get('result') or []
best_name, best_len = '', -1
for z in zones:
    name = (z.get('name') or '').rstrip('.').lower()
    if fqdn == name or fqdn.endswith('.' + name):
        if len(name) > best_len:
            best_name, best_len = name, len(name)
print(best_name)
" <<<"$ZONES_JSON")"

# zone-guard: FQDN must belong to resolved zone (always true after suffix match, assert anyway)
"$PYTHON" -c "
fqdn='${DOMAIN}'.rstrip('.').lower()
zone='${ZONE_NAME}'.rstrip('.').lower()
assert fqdn == zone or fqdn.endswith('.' + zone), (fqdn, zone)
"

RECORDS="$(api GET "/zones/${ZONE_ID}/dns_records?name=${DOMAIN}")"
read -r RECORD_ID RECORD_TYPE RECORD_CONTENT <<<"$("$PYTHON" -c "
import json, sys
records = json.load(sys.stdin)['result']
if records:
    r = records[0]
    print(r['id'], r['type'], r.get('content', ''))
else:
    print('', '', '')
" <<<"$RECORDS")"

payload="$("$PYTHON" -c 'import json, sys; print(json.dumps({"type":"A","name":sys.argv[1],"content":sys.argv[2],"ttl":60,"proxied":False}))' "$DOMAIN" "$TARGET_IP")"

plan() {
  if [ -n "$RECORD_ID" ] && [ "$RECORD_TYPE" = "A" ]; then
    echo "would_update A ${DOMAIN}: ${RECORD_CONTENT} -> ${TARGET_IP} (zone ${ZONE_NAME})"
  elif [ -n "$RECORD_ID" ]; then
    echo "would_replace ${RECORD_TYPE} with A ${DOMAIN} -> ${TARGET_IP} (zone ${ZONE_NAME})"
  else
    echo "would_create A ${DOMAIN} -> ${TARGET_IP} (zone ${ZONE_NAME})"
  fi
}

if [ "$APPLY" -eq 0 ]; then
  plan
  exit 0
fi

if [ -n "$RECORD_ID" ] && [ "$RECORD_TYPE" = "A" ]; then
  api PATCH "/zones/${ZONE_ID}/dns_records/${RECORD_ID}" "$payload" >/dev/null
  echo "Updated A record ${DOMAIN} -> ${TARGET_IP}"
elif [ -n "$RECORD_ID" ]; then
  api DELETE "/zones/${ZONE_ID}/dns_records/${RECORD_ID}" >/dev/null
  api POST "/zones/${ZONE_ID}/dns_records" "$payload" >/dev/null
  echo "Replaced ${RECORD_TYPE} record with A ${DOMAIN} -> ${TARGET_IP}"
else
  api POST "/zones/${ZONE_ID}/dns_records" "$payload" >/dev/null
  echo "Created A record ${DOMAIN} -> ${TARGET_IP}"
fi
