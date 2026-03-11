---
name: dockerizing-services
description: >-
  Practical Docker and Docker Compose patterns for local development, container
  security, networking, volume strategies, and multi-service orchestration. Use
  when setting up Docker Compose for local dev with hot-reload and service
  dependencies, designing multi-container architectures with service discovery
  and network isolation, hardening container images and runtime policies,
  troubleshooting container networking/DNS/volume issues, reviewing Dockerfiles
  for security and size, or migrating local dev workflows to container-based
  CI/CD pipelines. Trigger phrases: "containerize my app", "microservices",
  "run alongside Postgres", "dev environment with services", "run my app with
  a database", "Docker Compose setup", "multi-container", "add a Redis
  container", "Dockerize". This skill is NOT for Kubernetes orchestration,
  Helm charts, cloud-native deployment (ECS/Cloud Run/Fly.io), or container
  registries and CI image publishing.
---

# Docker Patterns

Actionable Docker and Docker Compose patterns for containerized development and deployment.

Docker is the right tool when you need reproducible service dependencies (databases, caches, queues) alongside your application, when "works on my machine" problems keep recurring, or when you want to mirror a multi-service production topology locally. If you only run a single process with no service dependencies, running natively is simpler.

This skill has permission to fetch from `docs.docker.com` via WebFetch. Use it to look up current reference documentation when needed.

## Docker Compose for Local Development

### Standard Web App Stack

```yaml
# compose.yaml
services:
  app:
    build:
      context: .
      target: dev                     # Use dev stage of multi-stage Dockerfile
    ports:
      - "3000:3000"
    volumes:
      - .:/app                        # Bind mount for hot reload
      - /app/node_modules             # Anonymous volume -- see note below
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/app_dev
      - REDIS_URL=redis://redis:6379/0
      - NODE_ENV=development
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    command: npm run dev

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app_dev
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data

  mailpit:                            # Local email testing
    image: axllent/mailpit
    ports:
      - "8025:8025"                   # Web UI
      - "1025:1025"                   # SMTP

volumes:
  pgdata:
  redisdata:
```

The `/app/node_modules` anonymous volume prevents the bind mount (`.:/app`) from clobbering the `node_modules` directory that was installed inside the container during the image build. Without it, the host's `node_modules` (which may be empty, or built for a different OS/architecture) would shadow the container's copy, causing missing or incompatible dependencies at runtime.

### Multi-Stage Dockerfile

```dockerfile
# Stage: dependencies
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# Stage: dev (hot reload, debug tools)
FROM node:22-alpine AS dev
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

# Stage: build
FROM node:22-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build && npm prune --production

# Stage: production (minimal image)
FROM node:22-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 -S appgroup && adduser --no-log-init -S appuser -u 1001
USER appuser
COPY --from=build --chown=appuser:appgroup /app/dist ./dist
COPY --from=build --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=build --chown=appuser:appgroup /app/package.json ./
ENV NODE_ENV=production
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

For advanced build patterns (digest pinning, RUN mounts, pipefail, layer caching), see [references/dockerfile-best-practices.md](references/dockerfile-best-practices.md).

### Override Files

Compose auto-loads `compose.override.yaml` alongside `compose.yaml` with no flags needed.

```yaml
# compose.override.yaml (auto-loaded, dev-only settings)
services:
  app:
    environment:
      - DEBUG=app:*
      - LOG_LEVEL=debug
    ports:
      - "9229:9229"                   # Node.js debugger
```

```yaml
# compose.prod.yaml (explicit for production)
services:
  app:
    build:
      target: production
    restart: always
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
```

```bash
# Development (auto-loads compose.override.yaml)
docker compose up

# Production
docker compose -f compose.yaml -f compose.prod.yaml up -d

# Verify merged result
docker compose -f compose.yaml -f compose.prod.yaml config
```

For production deployment, `extends`, `include`, and merge rules, see [references/compose-production.md](references/compose-production.md).

## Environment Variables

### Precedence (highest to lowest)

1. `docker compose run -e` CLI flag
2. Shell / `.env` interpolation in `environment:` or `env_file:`
3. `environment:` attribute (hardcoded in compose.yaml)
4. `env_file:` attribute (external .env files)
5. Image `ENV` directive (Dockerfile)

### Variable Interpolation

Use `${VAR:-default}` in compose files for dynamic configuration:

```yaml
services:
  app:
    image: myapp:${APP_VERSION:-latest}
    ports:
      - "${HOST_PORT:-3000}:3000"
```

### The .env Dual Role

The `.env` file at the project root serves two distinct purposes:
- **Compose interpolation**: substitutes `${VAR}` placeholders in compose.yaml at parse time
- **`env_file:` attribute**: injects variables directly into the running container

These are different mechanisms. Use separate `.env` files per environment (`.env.development`, `.env.production`) for flexible configuration across stages.

## Networking

### Service Discovery

Services in the same Compose network resolve by service name:

```
# From "app" container:
postgres://postgres:postgres@db:5432/app_dev    # "db" resolves to the db container
redis://redis:6379/0                             # "redis" resolves to the redis container
```

### Custom Networks

```yaml
services:
  frontend:
    networks: [frontend-net]

  api:
    networks: [frontend-net, backend-net]

  db:
    networks: [backend-net]              # Only reachable from api, not frontend

networks:
  frontend-net:
  backend-net:
```

### Exposing Only What's Needed

```yaml
services:
  db:
    ports:
      - "127.0.0.1:5432:5432"   # Only accessible from host, not network
    # Omit ports entirely in production -- accessible only within Docker network
```

## Volume Strategies

```yaml
volumes:
  # Named volume: persists across container restarts, managed by Docker
  pgdata:

  # Bind mount: maps host directory into container (for development)
  # - ./src:/app/src

  # Anonymous volume: preserves container-generated content from bind mount override
  # - /app/node_modules
```

### Common Patterns

```yaml
services:
  app:
    volumes:
      - .:/app                   # Source code (bind mount for hot reload)
      - /app/node_modules        # Protect container's node_modules from host
      - /app/.next               # Protect build cache

  db:
    volumes:
      - pgdata:/var/lib/postgresql/data          # Persistent data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql  # Init scripts
```

## Container Security

### Dockerfile Hardening

```dockerfile
# 1. Pin specific tags; use digest for supply-chain security
FROM node:22.12-alpine3.20
# Or: FROM node:22.12-alpine3.20@sha256:abcdef...

# 2. Run as non-root (--no-log-init prevents sparse file issues)
RUN addgroup -g 1001 -S app && adduser --no-log-init -S app -u 1001
USER app

# 3. Prefer COPY over ADD (ADD auto-extracts tars and fetches URLs)
COPY . .

# 4. Use exec form for CMD so the process becomes PID 1 and receives signals
CMD ["node", "server.js"]
```

### Compose Security

```yaml
services:
  app:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
      - /app/.cache
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE          # Only if binding to ports < 1024
```

`no-new-privileges` prevents a process inside the container from gaining additional privileges via setuid/setgid binaries or filesystem capabilities. This limits the blast radius if an attacker achieves code execution: they cannot escalate from the application user to root. `cap_drop: ALL` removes every Linux capability (mount, chown, raw sockets, etc.) from the container, then `cap_add` grants back only the specific capabilities the application actually requires. Together, these settings enforce least-privilege: even if the container is compromised, the attacker has almost no kernel-level powers to exploit.

### Secret Management

```yaml
# GOOD: Docker secrets (Swarm / orchestrator mode)
secrets:
  db_password:
    file: ./secrets/db_password.txt

services:
  db:
    secrets:
      - db_password

# OK for non-sensitive config: env_file
# env_file is NOT secure for secrets -- values visible via docker inspect
services:
  app:
    env_file:
      - .env                     # Never commit to git
    environment:
      - LOG_LEVEL                # Inherits from host environment

# BAD: Hardcoded in image
# ENV API_KEY=sk-proj-xxxxx      # NEVER DO THIS
```

## .dockerignore

Every file in the build context is sent to the Docker daemon before the build starts. Without a `.dockerignore`, this includes the `.git` directory (often hundreds of megabytes), `node_modules`, test fixtures, and -- critically -- `.env` files that may contain secrets. A proper `.dockerignore` keeps the build context small (faster builds, less memory) and prevents accidental secret leakage into image layers.

```
node_modules
.git
.env
.env.*
dist
coverage
*.log
.next
.cache
compose*.yaml
Dockerfile*
README.md
tests/
```

## Debugging

```bash
# Logs
docker compose logs -f app           # Follow app logs
docker compose logs --tail=50 db     # Last 50 lines from db

# Shell into running container
docker compose exec app sh
docker compose exec db psql -U postgres

# Inspect
docker compose ps                     # Running services
docker compose top                    # Processes in each container
docker stats                          # Resource usage

# Verify compose file merge
docker compose config
docker compose -f compose.yaml -f compose.prod.yaml config

# Rebuild
docker compose up --build             # Rebuild images
docker compose build --no-cache app   # Force full rebuild

# Targeted redeploy (skip recreating dependencies)
docker compose up --no-deps -d app

# Clean up
docker compose down                   # Stop and remove containers
docker compose down -v                # Also remove volumes (DESTRUCTIVE)
docker system prune                   # Remove unused images/containers
```

### Debugging Network Issues

```bash
# Check DNS resolution inside container
docker compose exec app nslookup db

# Check connectivity
docker compose exec app wget -qO- http://api:3000/health

# Inspect network
docker network ls
docker network inspect <project>_default
```

## Anti-Patterns

```
# Using :latest or unpinned tags
Pin to specific versions; use digest pinning for production supply-chain integrity

# Running as root
Always create and use a non-root user

# Storing data in containers without volumes
Containers are ephemeral -- all data lost on restart without volumes

# One giant container with all services
Separate concerns: one process per container

# Secrets in compose files, Dockerfiles, or env_file for sensitive data
Use Docker secrets, an orchestrator secret mechanism, or an external secret manager

# Bind-mounting source code in production
Code must stay inside the container; remove volume bindings for app code in production

# Using ADD when COPY suffices
Prefer COPY; use ADD only for tar extraction or remote URLs
```
