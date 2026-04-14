---
name: grafana-stack
description: >-
  Build Grafana dashboards, write PromQL and Flux queries, provision data sources
  and dashboards as code, configure alerting, and manage an on-premises Grafana +
  Prometheus + InfluxDB observability stack. Use this skill whenever the user
  mentions Grafana dashboards, PromQL queries, Prometheus metrics, recording rules,
  alert rules, dashboard provisioning, dashboard JSON, panel configuration, template
  variables, Flux queries for InfluxDB in Grafana, time series visualization,
  Grafana alerting, or observability stack setup. Also use when the user wants to
  add a panel, create a stat or gauge, write a rate() or histogram_quantile()
  query, set up dashboard folders, configure a Prometheus or InfluxDB data source,
  or export/import dashboard JSON -- even if they do not say "Grafana" explicitly.
  This skill covers self-hosted, open-source Grafana only (not Grafana Cloud).
---

# Grafana Observability Stack

On-premises patterns for Grafana OSS with Prometheus and InfluxDB. Everything here
targets self-hosted, open-source deployments -- no Grafana Cloud, no enterprise
features.

For detailed references beyond what is covered here, read the appropriate file
from the `references/` directory:

| Reference file | When to read it |
|---|---|
| `references/promql.md` | Deep PromQL patterns: histograms, SLOs, cardinality, recording rules |
| `references/dashboards.md` | Dashboard JSON deep dive: transformations, linking, annotations, library panels |
| `references/alerting.md` | Alert rules, contact points, notification policies, silences, notification templates |
| `references/datasources.md` | Full data source provisioning for Prometheus, InfluxDB (Flux), and Elasticsearch |
| `references/panels.md` | All visualization types, field configuration, overrides, value mappings |

---

## Provisioning as Code

Provisioning is the recommended way to manage Grafana resources in version control.
Place YAML files in the provisioning directory and Grafana loads them on startup.

### Data source provisioning

```yaml
# provisioning/datasources/datasources.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true

  - name: InfluxDB
    type: influxdb
    access: proxy
    url: http://influxdb:8086
    jsonData:
      version: Flux
      organization: my-org
      defaultBucket: default
    secureJsonData:
      token: $INFLUXDB_TOKEN

  - name: Elasticsearch
    type: elasticsearch
    access: proxy
    url: http://elasticsearch:9200
    jsonData:
      timeField: "@timestamp"
```

Environment variables (like `$INFLUXDB_TOKEN`) are interpolated at startup from
the Grafana container's environment.

### Dashboard provider provisioning

Dashboard providers tell Grafana where to find dashboard JSON files on disk.

```yaml
# provisioning/dashboards/dashboards.yml
apiVersion: 1

providers:
  - name: my-service
    orgId: 1
    type: file
    disableDeletion: true
    editable: true
    options:
      path: /var/lib/grafana/dashboards/my-service
      foldersFromFilesStructure: false
```

- `disableDeletion: true` prevents accidental removal through the UI
- `editable: true` allows UI edits for experimentation, but changes are lost on
  container restart unless saved back to the JSON files
- Each provider maps to a Grafana folder; add one provider per logical grouping

Store dashboard JSON files in the directory pointed to by `options.path`, then
mount that directory into the container as a read-only volume.

---

## Dashboard JSON Authoring

Every dashboard is a JSON document. The essential structure:

```json
{
  "title": "Service Overview",
  "uid": "service-overview-v1",
  "tags": ["production", "my-service"],
  "time": { "from": "now-1h", "to": "now" },
  "refresh": "30s",
  "timezone": "browser",
  "schemaVersion": 41,
  "templating": { "list": [] },
  "annotations": { "list": [] },
  "panels": []
}
```

- `uid` is a stable identifier used in URLs and API calls; keep it short and
  meaningful
- `schemaVersion` 41 is appropriate for Grafana 11+
- `time.from` / `time.to` support relative expressions (`now-1h`, `now-7d`) and
  absolute ISO timestamps
- `refresh` sets the auto-refresh interval (`"30s"`, `"1m"`, `""` for off)

### Panel structure

```json
{
  "id": 1,
  "type": "timeseries",
  "title": "Request Rate",
  "gridPos": { "x": 0, "y": 0, "w": 12, "h": 8 },
  "datasource": { "type": "prometheus", "uid": "prometheus" },
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{job=\"api\"}[5m])) by (status_code)",
      "legendFormat": "{{status_code}}",
      "refId": "A"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "reqps",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          { "color": "green", "value": null },
          { "color": "yellow", "value": 500 },
          { "color": "red", "value": 1000 }
        ]
      }
    },
    "overrides": []
  },
  "options": {
    "legend": { "calcs": ["mean", "max", "last"], "displayMode": "table", "placement": "bottom" },
    "tooltip": { "mode": "multi", "sort": "desc" }
  }
}
```

**Grid layout:** The dashboard uses a 24-column grid. Common widths: full=24,
half=12, third=8, quarter=6. Height is in grid units (roughly 30px each).

### Panel types at a glance

| Panel | When to use |
|---|---|
| **Time series** | Any metric over time -- counters, rates, gauges (the default) |
| **Stat** | Single current value with optional sparkline (uptime, current throughput) |
| **Gauge** | Value against a min/max range (disk usage percent, SLO budget) |
| **Bar gauge** | Compare multiple values side by side (top 10 services by request rate) |
| **Table** | Multi-column data, sortable (alert list, instance inventory) |
| **Heatmap** | Distribution over time (request duration histogram) |
| **Logs** | Log stream viewer (Elasticsearch, Loki) |
| **Text** | Markdown documentation panels |
| **State timeline** | State changes over time (on/off, healthy/degraded) |

Read `references/panels.md` for the full list and field configuration details.

### Common unit identifiers

```
"reqps"        requests per second
"ops"          operations per second
"bytes"        bytes (auto-scales to KB/MB/GB)
"percentunit"  0.0-1.0 displayed as percentage
"ms"           milliseconds
"s"            seconds
"short"        compact number (1.2k, 3.4M)
"none"         raw number
```

### Template variables

Variables make dashboards reusable across environments and services.

**Query variable** (populated from Prometheus labels):

```json
{
  "name": "job",
  "type": "query",
  "datasource": { "type": "prometheus", "uid": "prometheus" },
  "query": { "query": "label_values(up, job)", "refId": "A" },
  "refresh": 2,
  "includeAll": true,
  "multi": true,
  "label": "Service"
}
```

**Datasource variable** (switch between Prometheus instances without editing queries):

```json
{
  "name": "datasource",
  "type": "datasource",
  "pluginId": "prometheus",
  "label": "Prometheus"
}
```

**Chained variables** (second variable filters based on the first):

```json
{
  "name": "instance",
  "query": "label_values(up{job=\"$job\"}, instance)"
}
```

Use variables in PromQL: `rate(http_requests_total{job=~"$job"}[$interval])`

When a multi-value variable like `$job` has multiple selections, Grafana
automatically produces a regex alternation: `job=~"api|worker"`.

---

## PromQL Essentials

PromQL is a functional query language for Prometheus time-series data. Every
query returns either an instant vector (one value per label set), a range vector
(a sliding window of samples), or a scalar.

### Rate and counters

The golden rule: `rate()` and `increase()` require a range vector. The range
should be at least 4x the scrape interval to avoid gaps.

```promql
# Per-second rate over 5 minutes
rate(http_requests_total[5m])

# Always rate first, then aggregate -- never the reverse
sum(rate(http_requests_total{job="api"}[5m])) by (status_code)

# Total increase over a window (not per-second)
increase(http_requests_total[1h])
```

`rate()` gives a smooth average -- use it for both dashboards and alerts. It is
the correct default for almost every panel and recording rule. `irate()` uses
only the last two samples to capture brief spikes, but it is too volatile for
alerting and produces noisy graphs on most dashboard panels. Reach for `irate()`
only when you specifically need to see sub-second spikes that `rate()` would
smooth away.

### Aggregation

```promql
# Sum across instances, keep the service label
sum(rate(http_requests_total[5m])) by (service)

# 95th percentile latency from a histogram
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
)

# Top 5 services by request rate
topk(5, sum(rate(http_requests_total[5m])) by (service))
```

### Error rate

```promql
# Error ratio
sum(rate(http_requests_total{status_code=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))

# Avoid division by zero
sum(rate(errors_total[5m]))
/
(sum(rate(requests_total[5m])) > 0)
```

### Absence and staleness

```promql
# Alert when a job stops reporting
absent(up{job="api"})

# Detect stale exporters
changes(up{job="api"}[5m]) == 0
```

### Useful built-in query variables

Use these in Grafana panel queries instead of hardcoding intervals:

| Variable | Purpose |
|---|---|
| `$__rate_interval` | Safe interval for `rate()` -- at least 4x the scrape interval |
| `$__interval` | Auto-calculated interval matching the current time range and resolution |
| `$__range` | Duration of the current time range (e.g. `"6h"`) |

```promql
rate(http_requests_total[$__rate_interval])
```

Read `references/promql.md` for histograms, SLOs, cardinality management,
recording rules, time offsets, and prediction queries.

---

## Flux Queries for InfluxDB

When a panel targets an InfluxDB data source configured with Flux:

```flux
from(bucket: "my-bucket")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "events")
  |> filter(fn: (r) => r._field == "latency_us")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```

Grafana provides `v.timeRangeStart`, `v.timeRangeStop`, and `v.windowPeriod` as
built-in variables that sync with the dashboard time picker and panel resolution.

Read `references/datasources.md` for more Flux patterns (pivoting, cross-field
math, tag filtering, template variables with Flux).

---

## Alerting

Grafana unified alerting (enabled by default since Grafana 9) lets you define
alert rules that query any configured data source.

### Alert rule structure

1. **Query** -- one or more data queries (A, B, C...)
2. **Expression** -- reduce, math, or threshold applied to query results
3. **Evaluation interval** -- how often the rule runs
4. **Pending period** -- how long the condition must hold before firing
5. **Keep firing for** -- how long the alert stays firing after the condition
   resolves (prevents notification flapping during unstable recoveries)
6. **Labels** -- route alerts to the right contact point
7. **Annotations** -- context included in notifications (summary, description, runbook URL)

### Prometheus alert rule example

```
Query A: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
Expression B (Threshold): A > 80
Pending period: 5m
Labels: severity=warning, team=infrastructure
Annotation summary: CPU usage above 80% on {{ $labels.instance }}
```

### Contact points and notification policies

Contact points define where notifications go (Email via SMTP, Slack webhooks,
PagerDuty, Microsoft Teams, generic HTTP webhooks). Notification policies route
alerts to the right contact point based on label matchers like
`severity=critical` or `team=infrastructure`.

Alert rules, contact points, and notification policies can all be provisioned
as YAML files in the Grafana provisioning directory, just like data sources and
dashboard providers. This keeps the entire alerting configuration in version
control alongside your dashboards.

Read `references/alerting.md` for the full reference on contact points,
notification policies, silences, mute timings, notification templates, and
provisioning alerting resources as code.

---

## Recording Rules

Recording rules pre-compute expensive PromQL queries, improving dashboard load
times and reducing Prometheus query load. Define them in a rules file loaded by
Prometheus.

```yaml
# prometheus-rules/http-rates.yml
groups:
  - name: http_request_rates
    interval: 1m
    rules:
      - record: job:http_requests_total:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)

      - record: job:http_errors:ratio5m
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[5m])) by (job)
          /
          sum(rate(http_requests_total[5m])) by (job)
```

Naming convention: `<aggregation_level>:<metric_name>:<operation_and_window>`

Load rules files in `prometheus.yml`:

```yaml
rule_files:
  - "/etc/prometheus/rules/*.yml"
```

---

## Grafana HTTP API

Useful for scripting dashboard management and CI/CD integration.

```bash
# Search dashboards
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://grafana:3000/api/search?query=service&type=dash-db"

# Get dashboard by UID
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://grafana:3000/api/dashboards/uid/service-overview-v1" | jq '.dashboard'

# Create or update a dashboard
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "http://grafana:3000/api/dashboards/db" \
  -d '{
    "dashboard": { ... },
    "folderUid": "my-folder",
    "overwrite": true,
    "message": "Updated via API"
  }'

# Create a folder
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "http://grafana:3000/api/folders" \
  -d '{"uid": "my-team", "title": "My Team"}'

# Create annotation (mark a deploy on dashboards)
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "http://grafana:3000/api/annotations" \
  -d '{
    "dashboardUID": "service-overview-v1",
    "time": 1706745600000,
    "tags": ["deploy", "v2.0"],
    "text": "Deployed v2.0"
  }'
```

## Grafana Server Configuration

For on-premises Docker deployments, configure Grafana through environment
variables in Docker Compose rather than editing `grafana.ini` directly:

```yaml
environment:
  - GF_SECURITY_ADMIN_USER=${GRAFANA_ADMIN_USER}
  - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}
  - GF_USERS_ALLOW_SIGN_UP=false
  - GF_SECURITY_ALLOW_EMBEDDING=true       # if embedding dashboards
  - GF_FEATURE_TOGGLES_ENABLE=publicDashboards
  # SMTP for email alerts
  - GF_SMTP_ENABLED=true
  - GF_SMTP_HOST=smtp.example.com:587
  - GF_SMTP_USER=alerts@example.com
  - GF_SMTP_PASSWORD=secret
  - GF_SMTP_FROM_ADDRESS=alerts@example.com
```

Every `grafana.ini` setting maps to an environment variable following the pattern
`GF_<SECTION>_<KEY>` in uppercase. For example, `[server] http_port` becomes
`GF_SERVER_HTTP_PORT`.

---

## RBAC (Built-in Roles)

| Role | Permissions |
|---|---|
| Viewer | Read dashboards and alerts |
| Editor | Create and edit dashboards and alerts, create silences |
| Admin | Manage data sources, users, plugins, contact points, notification policies |
| Server Admin | Server-wide superuser (set via `GF_SECURITY_ADMIN_USER`) |

For more granular access, organize dashboards into folders -- folder permissions
are the primary RBAC boundary in OSS Grafana.
