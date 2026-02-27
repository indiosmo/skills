---
name: working-with-vector
description: "Write, review, and debug Vector (vector.dev) observability pipelines: configuration files (TOML/YAML), VRL transforms, source/sink wiring, unit tests, deployment topologies, and production hardening. Use when creating or modifying Vector configs, writing VRL transforms, designing pipeline topologies, troubleshooting Vector pipelines, or reviewing Vector configurations for correctness and best practices."
---

# Working With Vector

Vector is a high-performance observability data pipeline (written in Rust) that collects, transforms, and routes logs, metrics, and traces through a directed acyclic graph (DAG) of sources, transforms, and sinks.

## Pipeline Anatomy

Every Vector config defines a DAG of three component types wired together via `inputs`:

```
sources --> transforms --> sinks
```

- **Sources** ingest data (file, kafka, http_server, vector, kubernetes_logs, ...)
- **Transforms** process data (remap/VRL, filter, route, sample, dedupe, aggregate, log_to_metric, ...)
- **Sinks** deliver data (elasticsearch, aws_s3, kafka, loki, datadog_logs, prometheus_exporter, vector, ...)

Components connect through the `inputs` field forming the DAG. Fan-in and fan-out are both supported. The `route` transform produces named outputs referenced as `component_id.output_name`.

## Workflow

Always validate and test before deploying:

```bash
vector validate config.toml       # check config correctness
vector test config.toml           # run unit tests
vector --config config.toml       # start pipeline
```

Use `vector vrl` to prototype transforms interactively.

## Configuration

Vector supports TOML, YAML, and JSON. Prefer TOML or YAML.

Minimal example (TOML):

```toml
data_dir = "/var/lib/vector"

[sources.app_logs]
type = "file"
include = ["/var/log/app/*.log"]

[transforms.parse]
type = "remap"
inputs = ["app_logs"]
source = '''
  . = parse_json!(.message)
  del(.password)
'''

[sinks.out]
type = "elasticsearch"
inputs = ["parse"]
endpoints = ["https://es:9200"]
bulk.index = "app-%Y.%m.%d"
```

Key global options:
- `data_dir` -- persistent state directory (checkpoints, disk buffers). Must persist across restarts.
- `[api]` -- enable the management API (`/health`, GraphQL, `vector top`/`vector tap`)
- `[log_schema]` -- override default field names (host, message, timestamp)
- Environment variable interpolation: `${VAR}`, `${VAR:-default}`, `${VAR:?error}`

Multi-file configs: `vector --config-dir /etc/vector/` or `vector -c sources.toml -c transforms.toml -c sinks.toml`. Wildcard inputs are supported: `inputs = ["parse_*"]`.

## VRL (Vector Remap Language)

VRL is the primary transform language. It compiles at config load time (no runtime interpretation), is safe (no loops, no I/O, guaranteed termination), and requires explicit error handling.

### Core syntax

```coffee
# Access/set fields
.new_field = "value"
.nested.field = 42
del(.unwanted)

# Variables
my_var = parse_json!(.message)

# Error handling -- fallible functions require one of:
result = parse_json!(.msg)           # ! = abort on error (event goes to .dropped)
result, err = parse_json(.msg)       # explicit error capture
result = parse_json(.msg) ?? {}      # coalesce with default

# Conditionals
if .status >= 500 { .severity = "error" } else { .severity = "info" }

# Null coalescing
.host = .hostname ?? .host ?? "unknown"

# Abort (drop event when drop_on_abort = true)
if .level == "debug" { abort }
```

### Key functions

Standard string, type-check, and encoding functions work as expected (`downcase`, `contains`, `to_int!`, `is_string`, `encode_json`, etc.). These are Vector-specific or commonly needed:

| Category | Functions |
|----------|-----------|
| Parsing | `parse_json!`, `parse_syslog!`, `parse_key_value!`, `parse_regex!`, `parse_grok!`, `parse_logfmt!`, `parse_timestamp!` |
| Enrichment | `get_enrichment_table_record!` |
| Time | `now()`, `format_timestamp!`, `to_unix_timestamp` |
| Object | `del`, `merge`, `compact`, `flatten` |
| Debug | `log` (rate-limited), `assert!`, `assert_eq!` |

Prototype complex `parse_regex!` and `parse_grok!` patterns interactively with `vector vrl` before embedding in config.

### VRL constraints (by design)

- No general-purpose loops (single-pass transforms only)
- No I/O (no file/network access)
- No custom functions
- No recursion
- No cross-event state
- Metric events are restrictive -- only tags and certain fields can be modified

### Idiomatic VRL patterns

Parse-and-restructure:
```coffee
. = parse_json!(.message)
.timestamp = parse_timestamp!(.timestamp, format: "%Y-%m-%dT%H:%M:%S%.fZ")
.severity = if .status >= 500 { "error" } else if .status >= 400 { "warn" } else { "info" }
del(.raw_body)
```

Redact sensitive data:
```coffee
.message = replace(.message, r'[\w.+-]+@[\w-]+\.[\w.]+', "[REDACTED]")
del(.password)
del(.api_key)
```

Dead-letter routing (use `reroute_dropped = true` on the remap transform):
```coffee
parsed, err = parse_json(.message)
if err != null { abort }  # sends to <transform>.dropped output
. = parsed
```

## Unit Testing

Test transforms inline in config files. Run with `vector test <config>`.

```toml
[[tests]]
name = "parse_app_logs"

[[tests.inputs]]
insert_at = "parse"
type = "log"
[tests.inputs.log_fields]
message = '{"user":"alice","action":"login","ts":"2024-01-15T10:00:00Z"}'

[[tests.outputs]]
extract_from = "parse"
[[tests.outputs.conditions]]
type = "vrl"
source = '''
  assert_eq!(.user, "alice")
  assert_eq!(.action, "login")
  assert!(is_timestamp(.timestamp))
  assert!(!exists(.password))
'''
```

Use `no_outputs_from` to verify a filter drops events:

```toml
[[tests]]
name = "filter_drops_debug"
no_outputs_from = ["debug_filter"]

[[tests.inputs]]
insert_at = "debug_filter"
type = "log"
[tests.inputs.log_fields]
level = "debug"
```

Test chains by setting `insert_at` to the first transform and `extract_from` to the last.

## Pipeline Design Patterns

See [references/patterns.md](references/patterns.md) for detailed pipeline patterns:
- Agent + Aggregator topology
- Routing and fan-out
- Dead-letter queues
- Sampling and cost reduction
- Metrics derivation from logs
- Multi-tenant routing
- Enrichment tables

## Production Deployment

See [references/production.md](references/production.md) for:
- Deployment topologies (distributed, centralized, stream-based)
- Sizing and capacity planning
- Buffering strategies (memory vs disk vs overflow)
- Hardening (TLS, secrets, non-root, disk encryption)
- High availability patterns
- Monitoring Vector itself (`internal_metrics`, `internal_logs`)
- Troubleshooting workflow

## Common Mistakes

Avoid these frequent pitfalls (see [references/production.md](references/production.md) for detailed production guidance):

- Generic component IDs (`transform_1`, `sink_2`) -- use descriptive names like `parse_nginx_logs`, `route_by_severity`
- Hardcoded secrets -- always use `${ENV_VAR}` interpolation
- Deploying without running `vector validate` and `vector test`
- Using Lua when VRL can handle the use case
- Blindly using `!` on every fallible function instead of handling errors explicitly
- Placing filters late in the pipeline after expensive transforms
- Using memory buffers for data you cannot afford to lose
- Ephemeral `data_dir` (loses checkpoints and disk buffers on restart)
- Running without self-monitoring (`internal_metrics` source)
