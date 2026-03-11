# Vector Pipeline Patterns

## Table of Contents

- [Agent + Aggregator Topology](#agent--aggregator-topology)
- [Routing and Fan-out](#routing-and-fan-out)
- [Dead-Letter Queue](#dead-letter-queue)
- [Sampling and Cost Reduction](#sampling-and-cost-reduction)
- [Metrics Derivation from Logs](#metrics-derivation-from-logs)
- [Multi-Tenant Routing](#multi-tenant-routing)
- [Enrichment Tables](#enrichment-tables)
- [Parsing Pipeline](#parsing-pipeline)
- [Vector-to-Vector Communication](#vector-to-vector-communication)

## Agent + Aggregator Topology

The most common production pattern. Agents do lightweight collection/filtering on each host, aggregators do heavy processing centrally.

Agent config:
```toml
[sources.app_logs]
type = "file"
include = ["/var/log/app/*.log"]

[transforms.light_parse]
type = "remap"
inputs = ["app_logs"]
source = '. = parse_json!(.message)'

[sinks.to_aggregator]
type = "vector"
inputs = ["light_parse"]
address = "aggregator.internal:6000"
buffer.type = "disk"
buffer.max_size = 536870912  # 512 MB
```

Aggregator config:
```toml
[sources.from_agents]
type = "vector"
address = "0.0.0.0:6000"

[transforms.enrich]
type = "remap"
inputs = ["from_agents"]
source = '''
  .datacenter = get_env_var("DATACENTER") ?? "unknown"
  .team = if starts_with!(.service, "auth") { "security" } else { "platform" }
'''

[transforms.router]
type = "route"
inputs = ["enrich"]
[transforms.router.route]
errors = '.level == "ERROR" || .level == "FATAL"'
security = 'starts_with!(.service, "auth")'

[sinks.elasticsearch]
type = "elasticsearch"
inputs = ["enrich"]
endpoints = ["https://es:9200"]
bulk.index = "logs-%Y.%m.%d"

[sinks.alerts]
type = "http"
inputs = ["router.errors"]
uri = "https://alerts.example.com/v1/events"
encoding.codec = "json"

[sinks.siem]
type = "kafka"
inputs = ["router.security"]
bootstrap_servers = "kafka:9092"
topic = "security-logs"
encoding.codec = "json"
```

Use the native `vector` source/sink pair for agent-to-aggregator communication -- it uses gRPC, supports end-to-end acknowledgements, and is the most efficient protocol.

## Routing and Fan-out

Use `route` to split traffic by condition. Unmatched events go to `<route_id>._unmatched`.

```toml
[transforms.by_severity]
type = "route"
inputs = ["parsed_logs"]
[transforms.by_severity.route]
errors = '.level == "error" || .level == "fatal"'
warnings = '.level == "warn"'

[sinks.error_pager]
inputs = ["by_severity.errors"]
type = "http"
uri = "https://pagerduty.example.com/v2/enqueue"
encoding.codec = "json"

[sinks.all_logs]
inputs = ["parsed_logs"]  # all logs, not just routed ones
type = "aws_s3"
bucket = "log-archive"
key_prefix = "logs/%Y/%m/%d/"
encoding.codec = "ndjson"
compression = "gzip"
```

Fan-out: a single source/transform can feed multiple downstream components. Fan-in: a single transform/sink can accept inputs from multiple upstream components.

## Dead-Letter Queue

Route parsing/processing failures to a separate sink for later inspection.

```toml
[transforms.parse]
type = "remap"
inputs = ["raw_source"]
reroute_dropped = true
source = '''
  parsed, err = parse_json(.message)
  if err != null {
    log("Parse failed: " + to_string(err), level: "warn")
    abort
  }
  . = parsed
'''

[sinks.main]
type = "elasticsearch"
inputs = ["parse"]
endpoints = ["https://es:9200"]
bulk.index = "app-%Y.%m.%d"

[sinks.dead_letter]
type = "aws_s3"
inputs = ["parse.dropped"]
bucket = "dead-letter-queue"
key_prefix = "failed/%Y/%m/%d/"
encoding.codec = "ndjson"
```

The `abort` in VRL sends events to the `.dropped` output when `reroute_dropped = true` (otherwise they are silently dropped when `drop_on_abort = true`).

## Sampling and Cost Reduction

Filter noise early, sample non-critical logs.

```toml
[transforms.drop_noise]
type = "filter"
inputs = ["all_logs"]
condition = '.level != "debug" || .service == "critical-app"'

[transforms.sample_info]
type = "sample"
inputs = ["drop_noise"]
rate = 10  # keep 1 in 10
exclude = '.level == "error" || .level == "fatal"'  # never sample out errors
```

Use `throttle` for rate-limiting per key:
```toml
[transforms.rate_limit]
type = "throttle"
inputs = ["all_logs"]
threshold = 100
window_secs = 60
key_field = "service"
```

## Metrics Derivation from Logs

```toml
[transforms.http_metrics]
type = "log_to_metric"
inputs = ["parsed_http_logs"]

[[transforms.http_metrics.metrics]]
type = "counter"
field = "method"
name = "http_requests_total"
tags.method = "{{method}}"
tags.status = "{{status}}"

[[transforms.http_metrics.metrics]]
type = "histogram"
field = "response_time_ms"
name = "http_response_duration_ms"
tags.method = "{{method}}"

[sinks.prometheus]
type = "prometheus_exporter"
inputs = ["http_metrics"]
address = "0.0.0.0:9598"
```

**Missing fields are silently skipped.** If a `[[metrics]]` block references a `field` that doesn't exist in an event, no metric is emitted for that block -- no error, no empty metric. This means you can define the superset of all possible metrics and each event will only produce what it actually contains.

**The `name` field supports [template syntax](https://vector.dev/docs/reference/configuration/template-syntax/).** This enables fully dynamic metrics when combined with VRL fan-out. Instead of adding a static `[[metrics]]` block per metric type, fan-out the log into one event per metric key, then use a single templated block:

```toml
# Step 1: fan-out payload keys into individual events
[transforms.counters_expanded]
type = "remap"
inputs = ["counters_filtered"]
source = '''
tags = {}
tags.host = string!(.host)
tags.component = string!(.component)
tags.counter_set = string!(.name)

payload = object!(.payload)
events = []
for_each(payload) -> |key, value| {
  event = {}
  for_each(tags) -> |tk, tv| {
    event = set!(event, [tk], tv)
  }
  event.timestamp = .timestamp
  event.counter_name = key
  event.counter_value = value
  events = push(events, event)
}
. = events
'''

# Step 2: single dynamic metric block handles all counter types
[transforms.counters_metrics]
type = "log_to_metric"
inputs = ["counters_expanded"]

  [[transforms.counters_metrics.metrics]]
  type = "counter"
  field = "counter_value"
  name = "app_{{counter_name}}_total"
  namespace = "app"
  increment_by_value = true
    [transforms.counters_metrics.metrics.tags]
    host = "{{host}}"
    component = "{{component}}"
    counter_set = "{{counter_set}}"
```

New payload keys automatically become metrics without config changes.

Use `tag_cardinality_limit` to protect downstream systems from high-cardinality tags:
```toml
[transforms.limit_tags]
type = "tag_cardinality_limit"
inputs = ["http_metrics"]
mode = "exact"
value_limit = 500
```

## Multi-Tenant Routing

```toml
[transforms.tenant_router]
type = "route"
inputs = ["all_events"]
[transforms.tenant_router.route]
tenant_a = '.metadata.tenant == "a"'
tenant_b = '.metadata.tenant == "b"'

[sinks.tenant_a]
type = "kafka"
inputs = ["tenant_router.tenant_a"]
topic = "tenant-a-logs"
bootstrap_servers = "kafka:9092"
encoding.codec = "json"

[sinks.tenant_b]
type = "kafka"
inputs = ["tenant_router.tenant_b"]
topic = "tenant-b-logs"
bootstrap_servers = "kafka:9092"
encoding.codec = "json"

[sinks.unrouted]
type = "aws_s3"
inputs = ["tenant_router._unmatched"]
bucket = "unmatched-events"
key_prefix = "unrouted/%Y/%m/%d/"
encoding.codec = "ndjson"
```

## Enrichment Tables

Use CSV or GeoIP files to enrich events at processing time.

Config:
```toml
[enrichment_tables.hosts]
type = "file"
[enrichment_tables.hosts.file]
path = "/etc/vector/hosts.csv"
encoding.type = "csv"
[enrichment_tables.hosts.schema]
hostname = "string"
team = "string"
tier = "string"

[enrichment_tables.geoip]
type = "geoip"
path = "/etc/vector/GeoLite2-City.mmdb"
```

VRL usage:
```coffee
# CSV lookup
row, err = get_enrichment_table_record("hosts", {"hostname": .host})
if err == null {
  .team = row.team
  .tier = row.tier
}

# GeoIP lookup
.geo = get_enrichment_table_record!("geoip", {"ip": .client_ip})
.country = .geo.country_name
.city = .geo.city_name
```

Enrichment happens on-premise -- sensitive lookup data never leaves your network.

## Parsing Pipeline

Chain parsing, enrichment, and restructuring:

```toml
[transforms.parse]
type = "remap"
inputs = ["raw"]
source = '''
  . = parse_json!(.message)
  .timestamp = parse_timestamp!(.ts, format: "%Y-%m-%dT%H:%M:%S%.fZ")
  del(.ts)
  .status = to_int!(.status)
  .duration_ms = to_float!(.duration) * 1000.0
  del(.duration)
  .environment = get_env_var("ENVIRONMENT") ?? "unknown"
'''
```

For multi-format sources, use conditional parsing:
```coffee
if starts_with!(.message, "{") {
  . = parse_json!(.message)
} else if match(.message, r'^\<\d+\>') {  # syslog PRI header
  . = parse_syslog!(.message)
} else {
  . = parse_key_value!(.message)
}
```

## Vector-to-Vector Communication

Use the native `vector` source/sink pair. It uses gRPC, supports compression, and integrates with end-to-end acknowledgements.

Upstream (sender):
```toml
[sinks.forward]
type = "vector"
inputs = ["processed"]
address = "downstream:6000"
compression = true
buffer.type = "disk"
buffer.max_size = 1073741824  # 1 GB
acknowledgements.enabled = true
```

Downstream (receiver):
```toml
[sources.upstream]
type = "vector"
address = "0.0.0.0:6000"
```

Prefer this over Kafka/HTTP for Vector-to-Vector links unless you specifically need stream durability.
