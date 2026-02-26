# Compose Production and Multi-File Patterns

Patterns for production deployment and multi-file Compose configuration.

## Table of Contents

- [Production Checklist](#production-checklist)
- [Production Overlay](#production-overlay)
- [Targeted Redeployment](#targeted-redeployment)
- [Remote Deployment](#remote-deployment)
- [Multiple Compose Files](#multiple-compose-files)

## Production Checklist

When moving from development to production:

1. **Remove volume bindings for code** -- source must stay inside the container
2. **Set `restart: always`** to recover from crashes
3. **Bind to production ports** (e.g., 80/443 instead of dev ports)
4. **Reduce logging verbosity** (remove DEBUG flags, lower log levels)
5. **Configure external services** via environment variables
6. **Add supplementary services** (log aggregators, monitoring)

## Production Overlay

Never modify the base `compose.yaml` for production. Use an overlay file:

```yaml
# compose.prod.yaml
services:
  app:
    build:
      target: production
    restart: always
    volumes: []                   # Remove dev bind mounts
    ports:
      - "80:3000"
    environment:
      - NODE_ENV=production
      - LOG_LEVEL=warn
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M

  db:
    ports: []                     # No host-exposed ports
    restart: always
```

```bash
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

## Targeted Redeployment

Rebuild and redeploy a single service without restarting its dependencies:

```bash
docker compose build app
docker compose up --no-deps -d app
```

The `--no-deps` flag prevents cascading container restarts.

## Remote Deployment

Deploy to a remote Docker host via environment variables:

```bash
export DOCKER_HOST=tcp://remote-host:2376
export DOCKER_TLS_VERIFY=1
export DOCKER_CERT_PATH=/path/to/certs
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

For multi-node scaling, use Docker Swarm or Kubernetes.

## Multiple Compose Files

### Auto-Detection

Compose automatically merges `compose.yaml` + `compose.override.yaml` when running `docker compose up` with no `-f` flags. This enables zero-configuration dev overrides.

### Merge Rules

| Category | Behavior | Examples |
|----------|----------|----------|
| Single-value | Later file replaces | `image`, `command`, `mem_limit` |
| Lists | Concatenated | `ports`, `expose`, `dns`, `tmpfs` |
| Key-value | Merged by key; later wins per-key | `environment`, `labels` |
| Volumes/devices | Merged by container mount path | `volumes`, `devices` |

Always verify the merged result:

```bash
docker compose config
docker compose -f compose.yaml -f compose.prod.yaml config
```

### Path Resolution

All relative paths resolve relative to the **first** (base) Compose file. This matters in monorepo setups.

### extends: Service Reuse

Reuse properties from another service without including it in the final project:

```yaml
# common-services.yaml
services:
  webapp:
    build: .
    environment:
      - NODE_ENV=production

# compose.yaml
services:
  web:
    extends:
      file: common-services.yaml
      service: webapp
    ports:
      - "3000:3000"

  worker:
    extends:
      file: common-services.yaml
      service: webapp
    command: ["node", "worker.js"]
```

The source service (`webapp`) does not appear in the final project. Only `web` and `worker` do.

### include: Modular Composition

Pull in entire Compose files, each maintaining its own path resolution:

```yaml
# compose.yaml
include:
  - infra/compose.yaml
  - monitoring/compose.yaml

services:
  app:
    build: .
    depends_on:
      - db            # from infra/compose.yaml
```

- Supports recursive includes
- Each included file resolves paths relative to its own directory
- Supports inline overrides per include:
  ```yaml
  include:
    - path:
        - third-party/compose.yaml
        - third-party-overrides.yaml
  ```
