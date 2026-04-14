# Data Source Configuration Reference

## Table of contents

1. [Prometheus](#prometheus)
2. [InfluxDB (Flux)](#influxdb-flux)
3. [Elasticsearch](#elasticsearch)
4. [MySQL](#mysql)
5. [PostgreSQL](#postgresql)
6. [Provisioning patterns](#provisioning-patterns)

---

## Prometheus

Native support, no plugin required.

### Provisioning YAML

```yaml
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    jsonData:
      timeInterval: "15s"
      queryTimeout: "60s"
      httpMethod: POST
```

- `timeInterval` should match your Prometheus scrape interval
- `httpMethod: POST` is recommended because it supports longer queries than GET

### Key options

| Option | Purpose |
|---|---|
| Scrape interval | Should match Prometheus config (default: 15s) |
| Query timeout | Default: 60s |
| HTTP method | POST recommended |
| Exemplars | Enable to link metrics to traces (requires a tracing data source) |

### Template variables with Prometheus

```
label_values(metric_name, label_name)    All values of a label for a metric
label_values(label_name)                  All values across all metrics
metrics(prefix)                           All metric names matching a prefix
query_result(promql_expression)           PromQL result as variable values
```

---

## InfluxDB (Flux)

### Provisioning YAML

```yaml
datasources:
  - name: InfluxDB
    type: influxdb
    access: proxy
    url: http://influxdb:8086
    jsonData:
      version: Flux
      organization: my-org
      defaultBucket: default
    secureJsonData:
      token: $INFLUXDB_ADMIN_TOKEN
```

The `version: Flux` setting tells Grafana to use the Flux query editor instead
of InfluxQL.

### Flux query basics in Grafana

```flux
from(bucket: "my-bucket")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "events")
  |> filter(fn: (r) => r._field == "latency_us")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```

### Grafana-provided Flux variables

| Variable | Purpose |
|---|---|
| `v.timeRangeStart` | Dashboard time range start |
| `v.timeRangeStop` | Dashboard time range end |
| `v.windowPeriod` | Auto-calculated aggregation window for the current panel resolution |

### Common Flux patterns

```flux
// Filter by tag (using a Grafana template variable)
|> filter(fn: (r) => r.host == "${host}")

// Multiple fields
|> filter(fn: (r) => r._field == "sent" or r._field == "received")

// Pivot fields into columns for cross-field math
|> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
|> map(fn: (r) => ({ r with ratio: r.errors / r.total * 100.0 }))

// Group and aggregate
|> group(columns: ["host"])
|> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)

// Last value (for stat panels)
|> last()

// Sort and limit (for table panels showing top N)
|> sort(columns: ["_value"], desc: true)
|> limit(n: 10)
```

### Template variables with InfluxDB Flux

Use a Flux query as the variable source:

```flux
import "influxdata/influxdb/schema"
schema.tagValues(bucket: "my-bucket", tag: "host")
```

---

## Elasticsearch

### Provisioning YAML

```yaml
datasources:
  - name: Elasticsearch
    type: elasticsearch
    access: proxy
    url: http://elasticsearch:9200
    jsonData:
      timeField: "@timestamp"
      esVersion: "9.0.0"
      logMessageField: message
      logLevelField: level
```

### Derived fields

Extract values from log lines and create links to other data sources:

```yaml
jsonData:
  derivedFields:
    - name: TraceID
      matcherRegex: "traceID=(\\w+)"
      url: ""
      datasourceUid: tempo
```

### Query examples

```
# Simple text filter
message: "error"

# Field-specific filter
level: "ERROR" AND service: "api"

# Lucene query syntax
status:[500 TO 599] AND NOT path:"/health"
```

### Template variables with Elasticsearch

The query editor supports term aggregations for variable values. Configure a
variable with type "Query" and the Elasticsearch data source.

---

## MySQL

Built-in support for MySQL 5.7+ and compatible databases (MariaDB, Percona).

### Provisioning YAML

```yaml
datasources:
  - name: MySQL Production
    type: mysql
    url: mysql:3306
    database: mydb
    user: grafana
    secureJsonData:
      password: $MYSQL_PASSWORD
    jsonData:
      maxOpenConns: 100
      maxIdleConns: 100
      connMaxLifetime: 14400
```

### Time series query

```sql
SELECT
  $__timeGroup(created_at, $__interval) AS time,
  status,
  count(*) AS count
FROM orders
WHERE $__timeFilter(created_at)
GROUP BY 1, 2
ORDER BY 1
```

### SQL macros

| Macro | Purpose |
|---|---|
| `$__timeFilter(column)` | WHERE clause for the dashboard time range |
| `$__timeGroup(column, interval)` | Group by time interval |
| `$__timeFrom()` | Start of dashboard time range as Unix timestamp |
| `$__timeTo()` | End of dashboard time range as Unix timestamp |
| `$__interval` | Auto-calculated interval for the current time range |

---

## PostgreSQL

### Provisioning YAML

```yaml
datasources:
  - name: PostgreSQL
    type: postgres
    url: postgres:5432
    database: mydb
    user: grafana
    secureJsonData:
      password: $PG_PASSWORD
    jsonData:
      sslmode: disable
      postgresVersion: 1500
```

### Time series query (with TimescaleDB time_bucket)

```sql
SELECT
  time_bucket('$__interval', time) AS time,
  avg(value)
FROM metrics
WHERE time BETWEEN $__timeFrom() AND $__timeTo()
GROUP BY 1
ORDER BY 1
```

---

## Provisioning patterns

### Environment variable interpolation

Data source YAML files support environment variable substitution. Reference
variables with `$VARIABLE_NAME` (no curly braces). Sensitive values should go in
`secureJsonData`:

```yaml
secureJsonData:
  password: $DATABASE_PASSWORD
  token: $INFLUXDB_ADMIN_TOKEN
```

Set these variables in the Grafana container's environment (Docker Compose
`environment` section or `.env` file).

### Multiple environments

For multi-environment setups, use the same provisioning YAML with different
environment variables per deployment. Alternatively, use Grafana template
variables (datasource type) to let users switch between environments at the
dashboard level.

### Disabling edits

Set `editable: false` on a provisioned data source to prevent UI modifications:

```yaml
datasources:
  - name: Prometheus
    type: prometheus
    editable: false
    ...
```
