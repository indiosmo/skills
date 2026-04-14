# Grafana Alerting Reference

## Table of contents

1. [Core concepts](#core-concepts)
2. [Creating alert rules](#creating-alert-rules)
3. [Contact points](#contact-points)
4. [Notification policies](#notification-policies)
5. [Notification templates](#notification-templates)
6. [Silences and mute timings](#silences-and-mute-timings)
7. [Common alert rule examples](#common-alert-rule-examples)
8. [Connecting alerts to dashboards](#connecting-alerts-to-dashboards)
9. [High availability alerting](#high-availability-alerting)
10. [Grafana configuration for alerting](#grafana-configuration-for-alerting)

---

## Core concepts

### Alert states

| State | Meaning |
|---|---|
| Normal | Condition not met |
| Pending | Condition met but pending period has not elapsed |
| Firing | Condition met and pending period elapsed; notifications sent |
| Resolved | Previously firing alert returned to normal |
| No Data | Query returned no data (behavior is configurable) |
| Error | Query failed (behavior is configurable) |

### Evaluation groups

Alert rules are organized into evaluation groups. All rules in a group share the
same evaluation interval and are evaluated sequentially.

### Pending period

How long the condition must be continuously met before the alert fires.
`0s` fires immediately. `5m` requires 5 continuous minutes of breach.

### Keep firing for

How long an alert continues firing after the condition resolves. Prevents brief
recoveries from prematurely clearing an alert.

---

## Creating alert rules

Navigate to Alerting then Alert rules then New alert rule.

### Step 1: Define query and condition

Write one or more queries (labeled A, B, C...). Then add expressions:

- **Reduce** -- collapse a time series to a single value (Last, Mean, Sum, Max, Min)
- **Math** -- `$A > 80` or `($A + $B) / 2`
- **Threshold** -- set the firing threshold
- **Classic conditions** -- multiple threshold conditions with AND/OR

### Step 2: Set evaluation behavior

| Setting | Purpose |
|---|---|
| Folder | Organize rules; folder is the RBAC boundary |
| Evaluation group | Group name (all rules in the group share its interval) |
| Evaluation interval | How often the rule runs (for example, 1m) |
| Pending period | How long condition must hold before firing (for example, 5m) |
| Keep firing for | How long alert stays firing after recovery |

### Step 3: Configure labels and notifications

**Labels** are key-value pairs for routing and grouping:

```
severity=critical
team=infrastructure
service=database
```

**Annotations** provide context for notification messages:

```
Summary: CPU usage above 80% on {{ $labels.instance }}
Description: CPU usage is {{ $values.A.Value | humanize }}% on {{ $labels.instance }}
Runbook URL: https://wiki.example.com/runbooks/cpu-high
```

### Step 4: No data and error handling

| Situation | Options |
|---|---|
| No data | Alerting, OK, No Data state, Keep last state |
| Query error | Alerting, OK, Error state, Keep last state |

---

## Contact points

Contact points define notification destinations. Navigate to Alerting then
Contact points.

### On-premises integrations

| Integration | Configuration needed |
|---|---|
| Email | SMTP settings via `GF_SMTP_*` environment variables |
| Slack | Incoming webhook URL |
| PagerDuty | Integration key |
| Microsoft Teams | Incoming webhook URL |
| Telegram | Bot token and chat ID |
| Webhook | Any HTTP endpoint accepting POST |

### Email SMTP configuration

Set these environment variables on the Grafana container:

```
GF_SMTP_ENABLED=true
GF_SMTP_HOST=smtp.example.com:587
GF_SMTP_USER=alerts@example.com
GF_SMTP_PASSWORD=app-password
GF_SMTP_FROM_ADDRESS=alerts@example.com
GF_SMTP_FROM_NAME=Grafana Alerts
```

### Webhook payload format

Grafana POSTs JSON to webhook endpoints:

```json
{
  "receiver": "webhook-receiver",
  "status": "firing",
  "alerts": [
    {
      "status": "firing",
      "labels": { "alertname": "HighCPU", "instance": "server1" },
      "annotations": { "summary": "CPU above 80%" },
      "startsAt": "2024-01-15T10:00:00Z",
      "generatorURL": "http://grafana/alerting/..."
    }
  ],
  "groupLabels": { "alertname": "HighCPU" },
  "externalURL": "http://grafana"
}
```

---

## Notification policies

Policies route alerts to contact points based on label matchers. Navigate to
Alerting then Notification policies.

### Routing structure

The root policy catches all alerts that do not match a more specific child policy.
Child policies match on labels:

```
severity = critical    -->  pagerduty contact point
team = infrastructure  -->  slack-infra contact point
environment = staging  -->  email-dev contact point
```

### Policy settings

| Setting | Purpose |
|---|---|
| Contact point | Where to send matching alerts |
| Continue matching | If true, also evaluate subsequent sibling policies |
| Group by | Labels used to batch alerts into single notifications |
| Group wait | Wait before sending the first notification for a new group (default: 30s) |
| Group interval | Wait before sending updates for an existing group (default: 5m) |
| Repeat interval | Wait before re-sending for still-firing alerts (default: 4h) |

### Grouping to prevent notification storms

When many alerts share the same "group by" labels, they are batched into one
notification. For example, if 50 hosts fire HighCPU simultaneously and you group
by `[alertname, datacenter]`, you get one notification per datacenter containing
all affected hosts.

---

## Notification templates

Customize notification messages using Go templating. Navigate to Alerting then
Contact points then Notification templates.

### Built-in variables

```
{{ $labels }}          Alert labels as a map
{{ $values }}          Query values as a map
{{ $labels.instance }} Specific label value
{{ $values.A.Value }}  Specific query result value
{{ $status }}          "firing" or "resolved"
{{ $startsAt }}        When the alert started firing
```

### Example Slack template

```
{{ define "slack_message" }}
{{ if eq .Status "firing" }}FIRING{{ else }}RESOLVED{{ end }} -- {{ .Labels.alertname }}

Status: {{ .Status }}
Severity: {{ .Labels.severity }}

{{ range .Alerts }}
Instance: {{ .Labels.instance }}
Value: {{ .Values.A.Value | humanize }}
Summary: {{ .Annotations.summary }}
{{ end }}
{{ end }}
```

### Humanize functions

```
{{ $value | humanize }}           "12.3k"
{{ $value | humanize1024 }}       "12.3Ki"
{{ $value | humanizeBytes }}      "12.3 kB"
{{ $value | humanizeDuration }}   "3h 2m 1s"
{{ $value | humanizePercentage }} "12.3%"
```

---

## Silences and mute timings

### Silences

Silences temporarily suppress notifications without stopping alert evaluation.
Navigate to Alerting then Silences.

1. Set start and end time (or duration)
2. Add label matchers:
   ```
   alertname = HighCPU
   instance =~ ".*staging.*"
   severity != critical
   ```
3. Add a comment explaining why

From a firing alert detail view, click Silence to pre-populate label matchers.

### Mute timings

Mute timings are recurring schedules when notifications are suppressed (unlike
silences, which are one-time).

```
Name: no-alerts-weekends
  Weekdays: Saturday, Sunday

Name: business-hours-only
  Weekdays: Monday-Friday
  Times: 09:00-17:00
```

Attach mute timings to notification policies in the policy settings.

---

## Common alert rule examples

### CPU usage above threshold

```
Query A: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
Threshold: A > 80
Pending: 5m
Labels: severity=warning
```

### Memory usage

```
Query A: (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
Threshold: A > 90
```

### HTTP error rate

```
Query A: sum(rate(http_requests_total{status=~"5.."}[5m]))
Query B: sum(rate(http_requests_total[5m]))
Expression C (Math): $A / $B * 100
Threshold: C > 5
```

### Disk space

```
Query A: (1 - (node_filesystem_free_bytes{fstype!="tmpfs"} / node_filesystem_size_bytes{fstype!="tmpfs"})) * 100
Threshold: A > 85
```

### Service down

```
Query A: up{job="my-service"}
Threshold: A < 1
No data handling: Alerting (treat absence as firing)
```

---

## Connecting alerts to dashboards

### Create alert from a panel

1. Open the panel editor
2. Click the Alert tab
3. Click "Create alert rule from this panel"
4. The query is pre-populated from the panel

### Link an alert to a dashboard panel

In the alert rule definition, set the Dashboard and Panel fields. The alert state
badge appears on the panel, and clicking it navigates to the alert rule.

---

## High availability alerting

When running multiple Grafana instances behind a load balancer, configure HA to
prevent duplicate notifications:

```
GF_UNIFIED_ALERTING_HA_PEERS=grafana-1:9094,grafana-2:9094,grafana-3:9094
GF_UNIFIED_ALERTING_HA_ADVERTISE_ADDRESS=${POD_IP}:9094
GF_UNIFIED_ALERTING_HA_PEER_TIMEOUT=15s
```

---

## Grafana configuration for alerting

Relevant environment variables:

```
GF_UNIFIED_ALERTING_ENABLED=true
GF_UNIFIED_ALERTING_EVALUATION_TIMEOUT=30s
GF_UNIFIED_ALERTING_MIN_INTERVAL=10s
GF_UNIFIED_ALERTING_MAX_ANNOTATIONS_TO_KEEP=100
```
