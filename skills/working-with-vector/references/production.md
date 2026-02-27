# Vector Production Guide

## Table of Contents

- [Deployment Topologies](#deployment-topologies)
- [Sizing and Capacity Planning](#sizing-and-capacity-planning)
- [Buffering Strategies](#buffering-strategies)
- [Backpressure Handling](#backpressure-handling)
- [High Availability](#high-availability)
- [Hardening](#hardening)
- [Monitoring Vector Itself](#monitoring-vector-itself)
- [Troubleshooting](#troubleshooting)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Configuration Management](#configuration-management)

## Deployment Topologies

### Distributed (Agent-only)

Agents ship directly to sinks. Simple, but no centralized processing, higher connection fan-out, no cross-host aggregation.

Use when: simple environments, few sinks, no durability requirements.

### Centralized (Agent + Aggregator)

Agents forward to aggregators via `vector` source/sink. Aggregators do heavy transforms and fan-out to sinks.

Use when: most production environments. Recommended default.

- Agents: lightweight parsing/filtering, deployed per-node
- Aggregators: enrichment, routing, aggregation, deployed on dedicated nodes
- Use `vector` source/sink (native gRPC) for agent-to-aggregator links
- Front aggregators with a load balancer using DNS/service discovery

### Stream-Based

Insert Kafka/Pulsar between agents and aggregators for maximum durability.

Use when: large deployments with existing stream infrastructure, strict durability requirements.

## Sizing and Capacity Planning

### Throughput estimates (per vCPU, conservative)

| Event type | Avg size | Throughput |
|------------|----------|------------|
| Unstructured logs | ~256 bytes | ~10 MiB/s |
| Structured logs | ~768 bytes | ~25 MiB/s |
| Metrics | ~256 bytes | ~25 MiB/s |
| Trace spans | ~1 KB | ~25 MiB/s |

### Resource recommendations

- **Agent**: min 2 vCPUs
- **Aggregator**: min 4 vCPUs
- **Memory**: 2 GiB per vCPU as starting point. Increase for many sinks or large buffers.
- **Disk buffers**: provision for 10 minutes of throughput; 2x headroom recommended
- **Instance types**: compute-optimized (c6i, c6g on AWS; c2 on GCP; f8 on Azure). ARM64 preferred.
- No single node should handle >33% of total volume (HA headroom)

### Scaling

- **Vertical**: Vector auto-uses all vCPUs, no config change needed. Set `VECTOR_THREADS` to limit.
- **Horizontal (aggregators)**: load balancer + multiple instances. Use consistent hashing for stateful transforms (aggregate, dedupe). Autoscale on avg CPU (85% target, 5-min stabilization).
- **Kubernetes agents**: DaemonSet scales with nodes automatically.

## Buffering Strategies

### Memory buffer (default)

```toml
[sinks.out.buffer]
type = "memory"
max_events = 500
when_full = "block"
```

Fast, low-latency. Data lost on crash. Use for non-critical/analytics data.

### Disk buffer

```toml
[sinks.out.buffer]
type = "disk"
max_size = 536870912  # 512 MB
when_full = "block"
```

Survives crashes. Use for critical data (audit, security, billing). Size for expected burst duration (e.g., 10 min outage at 100 MB/min = 1 GB min).

### Overflow (hybrid)

Memory-speed normally, spills to disk during bursts:
```toml
[sinks.out.buffer]
type = "disk"
max_size = 1073741824
when_full = "overflow"
```

### `when_full` behavior

- `block` (default): backpressure upstream. Safe, no data loss, may slow sources.
- `drop_newest`: drops new events. Use for metrics/telemetry where freshness > completeness.
- `overflow`: spill to disk (disk buffer only).

### End-to-end acknowledgements

Enable for at-least-once delivery. Sources won't advance checkpoints until all downstream sinks confirm delivery:

```toml
[sinks.critical_sink]
acknowledgements.enabled = true
buffer.type = "disk"
buffer.max_size = 5368709120  # 5 GB
```

Requires source support (file, kafka, vector, etc. -- not stdin).

## Backpressure Handling

Backpressure cascades backward through the DAG: full sink buffer -> transforms pause -> sources pause (file pauses reading, TCP causes backpressure, etc.).

- Use `block` for critical paths
- Monitor buffer utilization to detect backpressure early
- Size buffers to absorb expected burst duration
- Add capacity when buffers are consistently full

## High Availability

- Deploy aggregators across multiple availability zones
- No single node should process >33% of volume
- Front aggregators with load balancers; maintain standby LBs via DNS/service discovery
- Enable end-to-end acknowledgements for at-least-once delivery
- Use disk buffers at sinks to absorb downstream outages
- Route dropped/failed events to backup destinations (dead-letter pattern)
- Use platform-level self-healing (Kubernetes controllers, systemd restart)
- Adaptive Request Concurrency (ARC) automatically throttles during downstream failures

## Hardening

### Data at rest
- Enable whole-disk encryption at OS/filesystem level
- Disable swap (`swapoff -a`)
- Restrict `data_dir` permissions to Vector's service account
- Disable core dumps (`LimitCORE=0` in systemd, or `RLIMIT_CORE=0`)

### Data in transit
- TLS on all sources and sinks, including internal Vector-to-Vector traffic
- Use TLS 1.3+ where supported
- Firewall rules: only allow authorized agent-to-aggregator and aggregator-to-sink

### Process security
- Never run Vector as root
- Dedicated unprivileged service account
- Never hardcode secrets -- use `${ENV_VAR}` interpolation
- Restrict `/etc/vector` directory permissions
- Prevent service account from modifying Vector binary or config

### Secrets management
- Use `${VAR}` interpolation for all credentials
- Integrate with secrets managers (AWS Secrets Manager, Vault, etc.)
- Redact sensitive fields in VRL before routing to sinks

## Monitoring Vector Itself

Always include self-monitoring in your pipeline:

```toml
[sources.internal_metrics]
type = "internal_metrics"
scrape_interval_secs = 30

[sources.internal_logs]
type = "internal_logs"

[sinks.vector_monitoring]
type = "prometheus_exporter"
inputs = ["internal_metrics"]
address = "0.0.0.0:9598"
```

### Key metrics to monitor and alert on

| Metric | Alert condition |
|--------|----------------|
| `component_errors_total` | Any increase |
| `buffer_byte_size` / `buffer_events` | Approaching configured max |
| `buffer_discarded_events_total` | Any increase |
| `component_received_events_total` | Drops to 0 (source stopped) |
| `utilization` (per component) | Sustained > 0.9 |

### Diagnostic tools

- `vector top` -- live throughput/error dashboard (requires API enabled)
- `vector tap <component_id>` -- live-stream events at any pipeline point
- `vector validate <config>` -- check config correctness before deploy
- `vector vrl` -- interactive VRL REPL for prototyping transforms

## Troubleshooting

Follow this order:

1. **Check known issues**: search Vector GitHub issues by component label
2. **Inspect logs**: `journalctl -fu vector` (systemd) or `/var/log/vector.log`
3. **Enable debug logging**: `VECTOR_LOG=debug vector ...` (safe for production, rate-limited)
4. **Enable backtraces**: `RUST_BACKTRACE=full` if exceptions appear in logs
5. **Use `vector top`**: identify components with errors, low throughput, or high utilization
6. **Use `vector tap`**: inspect actual events at any pipeline point
7. **Check metrics**: `component_errors_total`, buffer utilization, throughput deltas

### Common issues

| Symptom | Investigation |
|---------|---------------|
| High memory usage | Reduce buffer `max_events`, check stateful transforms (reduce, dedupe) |
| Events dropped | Check `buffer_discarded_events_total`, increase buffer or use disk |
| High CPU | Profile transforms with `vector top`, check complex regex in VRL |
| Slow sink | Check ARC metrics, verify downstream health, increase batch size |
| File source not reading | Check include/exclude globs, file permissions, checkpoint in `data_dir` |
| Data duplicates after restart | Expected with at-least-once; use idempotent writes downstream |

## Kubernetes Deployment

### DaemonSet (recommended for agents)

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: vector-agent
spec:
  template:
    spec:
      containers:
        - name: vector
          image: timberio/vector:latest-alpine
          args: ["--config-dir", "/etc/vector/"]
          resources:
            requests: { cpu: "200m", memory: "256Mi" }
            limits: { cpu: "1", memory: "512Mi" }
          volumeMounts:
            - name: data
              mountPath: /var/lib/vector
            - name: config
              mountPath: /etc/vector/
          livenessProbe:
            httpGet: { path: /health, port: 8686 }
            initialDelaySeconds: 5
          readinessProbe:
            httpGet: { path: /health, port: 8686 }
            initialDelaySeconds: 5
      terminationGracePeriodSeconds: 60
      volumes:
        - name: data
          hostPath: { path: /var/lib/vector }
        - name: config
          configMap: { name: vector-agent-config }
```

### Aggregator Deployment

Use a Deployment with HPA. Autoscale on CPU (85% target). Use PersistentVolumeClaims for disk buffers. Set `terminationGracePeriodSeconds` >= 60 (more for large disk buffers).

## Configuration Management

- Version control all configs
- Validate in CI: `vector validate /path/to/config`
- Run unit tests in CI: `vector test /path/to/config`
- Use `--watch-config` or `SIGHUP` for hot-reload (some changes need restart)
- Use `vector generate` to scaffold new component chains
- Use multi-file organization: split by function (sources, transforms, sinks) or by team/service
