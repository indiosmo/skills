# PromQL Deep Reference

## Table of contents

1. [Histogram quantiles](#histogram-quantiles)
2. [SLO queries](#slo-queries)
3. [Time offsets and predictions](#time-offsets-and-predictions)
4. [Recording rules](#recording-rules)
5. [Cardinality and performance](#cardinality-and-performance)
6. [Common monitoring patterns](#common-monitoring-patterns)

---

## Histogram quantiles

### Classic histograms (bucket metrics with `_bucket` suffix)

```promql
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket{job="api"}[5m])) by (le)
)
```

**Multi-service comparison:**

```promql
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
)
```

A common mistake is forgetting `by (le)` in the inner aggregation. Without it,
the bucket boundaries are collapsed and `histogram_quantile` produces NaN.

### Native histograms (Prometheus 2.40+)

Native histograms use a simpler syntax because bucket boundaries are embedded in
the data:

```promql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds[5m])))
```

---

## SLO queries

### Availability over a rolling window

```promql
# Fraction of successful requests over 30 days
1 - (
  sum(increase(http_requests_total{status_code=~"5.."}[30d]))
  /
  sum(increase(http_requests_total[30d]))
)
```

### Error budget burn rate

Used in multi-window alerting. When the burn rate exceeds a threshold, the error
budget is being consumed faster than planned.

```promql
# 1-hour burn rate; fire when burning > 14.4x the allowed rate
(
  sum(rate(http_requests_total{status_code=~"5.."}[1h]))
  /
  sum(rate(http_requests_total[1h]))
)
/
(1 - 0.999)   # replace 0.999 with your SLO target
```

Combine a fast window (1h or 5m) and a slow window (6h or 3d) to catch both
sudden spikes and sustained degradation.

---

## Time offsets and predictions

```promql
# Compare current rate to 1 hour ago
rate(http_requests_total[5m])
-
rate(http_requests_total[5m] offset 1h)

# Day-over-day ratio
rate(http_requests_total[5m])
/
rate(http_requests_total[5m] offset 1d)

# Predict disk exhaustion: linear extrapolation 24h into the future
predict_linear(node_filesystem_avail_bytes{mountpoint="/"}[6h], 24 * 3600) < 0
```

---

## Recording rules

Recording rules pre-compute expensive queries. Store them in rule files loaded
by Prometheus.

```yaml
groups:
  - name: http_request_rates
    interval: 1m
    rules:
      # Per-service request rate
      - record: job:http_requests_total:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)

      # Per-service error ratio
      - record: job:http_errors:ratio5m
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[5m])) by (job)
          /
          sum(rate(http_requests_total[5m])) by (job)

      # Per-service p95 latency (avoids expensive histogram_quantile on dashboards)
      - record: job:http_request_duration_p95:rate5m
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job)
          )
```

**Naming convention:** `<aggregation_level>:<metric_name>:<operation_and_window>`

Load in `prometheus.yml`:

```yaml
rule_files:
  - "/etc/prometheus/rules/*.yml"
```

When to create recording rules:
- Dashboard panels that run the same expensive query across many users
- Queries used in alerts (keeps alert evaluation fast and independent of query complexity)
- Histogram quantiles that aggregate across many series

---

## Cardinality and performance

High cardinality (many unique label combinations) makes queries slow and storage
expensive. The main offenders are labels with unbounded values: user IDs, request
IDs, email addresses, raw URLs.

### Investigate cardinality

```promql
# Top 10 metrics by series count
topk(10, count by (__name__)({__name__=~".+"}))

# Total series count for a specific metric
count(http_requests_total)

# Check how many distinct values a label has
count(count by (user_id)(http_requests_total))
```

### Control cardinality

- Never put high-cardinality values in labels. Use logs or traces for request-level
  detail.
- Group URLs into route patterns: `/api/users/123` becomes `/api/users/{id}`
- Drop problematic labels at scrape time with `metric_relabel_configs`:

```yaml
# In prometheus.yml scrape config
metric_relabel_configs:
  - source_labels: [user_id]
    action: labeldrop
```

---

## Common monitoring patterns

### Service availability

```promql
# Fraction of time the service was up over the last 5 minutes
avg_over_time(up{job="api"}[5m])
```

### CPU saturation

```promql
100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

### Memory usage

```promql
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
/ node_memory_MemTotal_bytes * 100
```

### Disk filling prediction

```promql
# Predict full in < 4 hours based on 1-hour trend
predict_linear(node_filesystem_avail_bytes{mountpoint="/"}[1h], 4 * 3600) < 0
```

### Throughput spike detection

```promql
# Current rate exceeds 3x the 1-hour average
rate(http_requests_total[5m])
>
3 * avg_over_time(rate(http_requests_total[5m])[1h:5m])
```

### Absence detection

```promql
# Alert when a metric disappears entirely
absent(up{job="api"})

# Alert when a metric has not changed (possible stale exporter)
changes(up{job="api"}[5m]) == 0
```
