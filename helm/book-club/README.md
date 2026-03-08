# Book Club Helm Chart

This Helm chart deploys the Book Club application to Kubernetes.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- HashiCorp Vault Secrets Operator (if using Vault integration)
- Ingress controller (nginx recommended)
- Cert-manager (for TLS certificates)

## Installation

### Quick Install

```bash
helm install book-club . --namespace book-club --create-namespace
```

### Custom Values

```bash
helm install book-club . \
  --namespace book-club \
  --create-namespace \
  --set image.registry=harbor.example.com \
  --set image.tag=v1.0.0 \
  --set ingress.hosts[0].host=bookclub.example.com
```

### Using Custom Values File

```bash
helm install book-club . \
  --namespace book-club \
  --create-namespace \
  --values custom-values.yaml
```

## Configuration

### Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.registry` | Harbor registry URL | `harbor.example.com` |
| `image.project` | Harbor project name | `book-club` |
| `image.tag` | Image tag to deploy | `latest` |
| `backend.replicaCount` | Number of backend replicas | `2` |
| `frontend.replicaCount` | Number of frontend replicas | `2` |
| `postgres.enabled` | Deploy PostgreSQL | `true` |
| `postgres.storage` | PostgreSQL storage size | `10Gi` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class | `nginx` |
| `vault.enabled` | Enable Vault integration | `true` |

### Example Custom Values

```yaml
image:
  registry: harbor.mycompany.com
  tag: v1.2.3

backend:
  replicaCount: 3
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi

ingress:
  hosts:
    - host: bookclub.mycompany.com
      paths:
        - path: /api
          pathType: Prefix
          backend: backend
        - path: /
          pathType: Prefix
          backend: frontend
  tls:
    - secretName: bookclub-tls
      hosts:
        - bookclub.mycompany.com

vault:
  address: https://vault.mycompany.com
  role: book-club-prod
```

## Upgrading

```bash
helm upgrade book-club . --namespace book-club
```

## Uninstalling

```bash
helm uninstall book-club --namespace book-club
```

## Vault Integration

This chart uses the Vault Secrets Operator to fetch secrets from HashiCorp Vault.

### Required Vault Setup

1. Enable Kubernetes auth method
2. Create a policy for the book-club role
3. Create secrets at the configured path

See the main [README.md](../../README.md) for detailed Vault setup instructions.

## Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n book-club
```

### View Logs

```bash
# Backend logs
kubectl logs -n book-club -l app.kubernetes.io/component=backend

# Frontend logs
kubectl logs -n book-club -l app.kubernetes.io/component=frontend

# PostgreSQL logs
kubectl logs -n book-club -l app.kubernetes.io/component=postgres
```

### Check Secrets

```bash
kubectl get secrets -n book-club
kubectl describe secret book-club-secrets -n book-club
```

### Test Connectivity

```bash
# Port forward to backend
kubectl port-forward -n book-club svc/book-club-backend 8000:8000

# Port forward to frontend
kubectl port-forward -n book-club svc/book-club-frontend 8080:80
```
