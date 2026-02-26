# Dockerfile Best Practices

Advanced build patterns from the official Docker documentation.

## Table of Contents

- [Base Image Selection](#base-image-selection)
- [RUN Instruction Patterns](#run-instruction-patterns)
- [User Creation](#user-creation)
- [COPY vs ADD](#copy-vs-add)
- [Layer Caching](#layer-caching)
- [CMD and ENTRYPOINT](#cmd-and-entrypoint)
- [Environment Variables in Builds](#environment-variables-in-builds)

## Base Image Selection

- Choose minimal base images (Alpine is under 6 MB)
- Prefer Docker Official Images, Verified Publishers, and Docker-Sponsored Open Source
- Pin images by digest for supply-chain integrity:
  ```dockerfile
  FROM alpine:3.21@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
  ```
- Rebuild images regularly to incorporate security patches
- Use `docker build --pull` to fetch the latest base image
- Use `--no-cache` to rebuild all layers from scratch

## RUN Instruction Patterns

### Combine package operations

```dockerfile
# GOOD: Single layer, clean cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# BAD: Separate RUN causes stale package lists
RUN apt-get update
RUN apt-get install -y curl
```

### Use pipefail for piped commands

`/bin/sh` silently swallows failures in the middle of a pipe. Switch to bash:

```dockerfile
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -fsSL https://example.com/setup.sh | bash
```

### Heredocs for multi-command blocks

```dockerfile
RUN <<EOF
set -e
apt-get update
apt-get install -y --no-install-recommends curl git
rm -rf /var/lib/apt/lists/*
EOF
```

### Temporary build-time file access

Avoid COPY + cleanup. Use a bind mount instead -- the file is available during the RUN step but never persisted as a layer:

```dockerfile
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip install -r /tmp/requirements.txt
```

## User Creation

```dockerfile
# Debian/Ubuntu
RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser
USER appuser

# Alpine
RUN addgroup -g 1001 -S appgroup && adduser --no-log-init -S appuser -u 1001
USER appuser
```

- Always use `--no-log-init` to prevent sparse file issues that bloat image layers
- For privilege dropping in entrypoint scripts, use `gosu` instead of `sudo`:

```bash
#!/bin/bash
set -e
# ... setup tasks as root ...
exec gosu appuser "$@"
```

## COPY vs ADD

| Use case | Instruction |
|----------|-------------|
| Copy local files | `COPY` (always preferred) |
| Auto-extract local tar | `ADD archive.tar.gz /dest` |
| Fetch remote URL | `ADD https://example.com/file /dest` |
| Temporary build files | `RUN --mount=type=bind` |

Default to COPY. Only use ADD when you need tar extraction or remote URL fetching.

## Layer Caching

- Order instructions from least to most frequently changed
- Copy dependency manifests before source code:
  ```dockerfile
  COPY package.json package-lock.json ./
  RUN npm ci
  COPY . .
  ```
- Version-pin packages to force cache busting when needed: `package=1.3.*`
- Sort multi-line arguments alphanumerically for readability and diff clarity

## CMD and ENTRYPOINT

- Always use exec form: `CMD ["executable", "param1"]`
- Shell form (`CMD executable param1`) runs under `/bin/sh -c`, preventing signal propagation to the process
- ENTRYPOINT helper scripts should end with `exec "$@"` to hand off PID 1:
  ```bash
  #!/bin/bash
  set -e
  # run migrations, wait for deps, etc.
  exec "$@"
  ```
- Avoid combining CMD + ENTRYPOINT unless the interaction is well understood

## Environment Variables in Builds

- Use `ENV` for persistent runtime variables (like PATH updates)
- For build-only variables, use inline assignment to prevent persistence across layers:
  ```dockerfile
  RUN export DEBIAN_FRONTEND=noninteractive && \
      apt-get update && apt-get install -y pkg && \
      unset DEBIAN_FRONTEND
  ```
- Or use `ARG` for build-time-only values (not available at runtime)
