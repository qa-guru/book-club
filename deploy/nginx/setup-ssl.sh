#!/usr/bin/env bash
set -euo pipefail

DOMAIN="book-club.qa.guru"
WEBROOT="/var/www/certbot"
NGINX_SITE="/etc/nginx/sites-available/${DOMAIN}"

if ! command -v nginx >/dev/null; then
  echo "nginx is not installed, skipping SSL setup"
  exit 0
fi

if ! sudo -n true 2>/dev/null; then
  echo "passwordless sudo is required for SSL setup"
  exit 0
fi

sudo mkdir -p /var/www/certbot /etc/nginx/sites-available /etc/nginx/sites-enabled
sudo cp deploy/nginx/book-club-http.conf "$NGINX_SITE"
sudo ln -sf "$NGINX_SITE" "/etc/nginx/sites-enabled/${DOMAIN}"
sudo nginx -t
sudo systemctl reload nginx

if ! command -v certbot >/dev/null; then
  echo "certbot is not installed, skipping certificate issuance"
  exit 0
fi

if [ ! -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]; then
  sudo certbot certonly \
    --webroot -w "$WEBROOT" \
    -d "$DOMAIN" \
    --non-interactive \
    --agree-tos \
    --register-unsafely-without-email \
    --keep-until-expiring
fi

sudo certbot renew --quiet || true

sudo cp deploy/nginx/book-club.conf "$NGINX_SITE"
sudo nginx -t
sudo systemctl reload nginx
