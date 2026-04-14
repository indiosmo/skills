# Dashboard JSON Deep Reference

## Table of contents

1. [Transformations](#transformations)
2. [Dashboard linking](#dashboard-linking)
3. [Annotations](#annotations)
4. [Library panels](#library-panels)
5. [Sharing and embedding](#sharing-and-embedding)
6. [Rows and layout](#rows-and-layout)
7. [Playlists and kiosk mode](#playlists-and-kiosk-mode)
8. [Dashboard versioning](#dashboard-versioning)
9. [Keyboard shortcuts](#keyboard-shortcuts)

---

## Transformations

Transformations reshape data client-side after queries return, without changing
the queries themselves. Apply them in the panel editor under the Transform tab.

### Common transformations

```json
"transformations": [
  {
    "id": "merge",
    "options": {}
  },
  {
    "id": "organize",
    "options": {
      "renameByName": { "Value #A": "Request Rate", "Value #B": "Error Rate" },
      "excludeByName": { "Time": true }
    }
  },
  {
    "id": "calculateField",
    "options": {
      "alias": "Error Percent",
      "binary": {
        "left": "errors",
        "right": "total",
        "operator": "/"
      }
    }
  },
  {
    "id": "filterByValue",
    "options": {
      "filters": [
        {
          "fieldName": "Error Percent",
          "config": { "id": "greater", "options": { "value": 0.01 } }
        }
      ],
      "type": "include",
      "match": "any"
    }
  },
  {
    "id": "sortBy",
    "options": { "sort": [{ "field": "Error Percent", "desc": true }] }
  }
]
```

### Transformation reference

| ID | Purpose |
|---|---|
| `merge` | Combine multiple query results into one table |
| `organize` | Rename, reorder, or hide fields |
| `calculateField` | Add a computed column from existing columns |
| `filterByValue` | Keep or exclude rows matching a condition |
| `groupBy` | Group rows and aggregate (count, sum, mean) |
| `sortBy` | Sort rows by a field |
| `limit` | Keep only first N rows |
| `labelsToFields` | Convert Prometheus labels into separate columns |
| `seriesToRows` | Pivot time series into a row-oriented table |
| `partitionByValues` | Split one series into many based on a label value |
| `joinByField` | SQL-style join on a common field (often time) |
| `renameByRegex` | Batch rename fields using a regex pattern |
| `extractFields` | Parse JSON or regex from a string field |
| `convertFieldType` | Change a field's data type |

Enable the "Debug" toggle on any transformation to see its input and output,
which is helpful when chaining multiple transformations.

---

## Dashboard linking

### Panel links

Click a panel to navigate somewhere, passing data from the current context:

```json
"links": [
  {
    "title": "Go to details",
    "url": "/d/details-dashboard?var-service=${__field.labels.service}",
    "targetBlank": false
  }
]
```

### Dashboard-level links

Appear in the top-right corner of the dashboard:

```json
"links": [
  {
    "title": "Runbook",
    "url": "https://wiki.example.com/runbook/${job}",
    "icon": "external link",
    "targetBlank": true,
    "type": "link"
  }
]
```

### Built-in link variables

| Variable | Value |
|---|---|
| `${__value.raw}` | Current data point value |
| `${__field.labels.job}` | Label value from the current series |
| `${__url.params}` | Current URL query parameters (pass-through) |
| `${__from}` / `${__to}` | Current time range as Unix milliseconds |

---

## Annotations

Annotations overlay event markers on time series panels -- deployments,
incidents, maintenance windows.

### Query annotation from Prometheus

```json
{
  "datasource": { "type": "prometheus", "uid": "prometheus" },
  "expr": "changes(kube_deployment_status_observed_generation{namespace=\"production\"}[5m]) > 0",
  "step": "60s",
  "name": "Deployments",
  "iconColor": "blue",
  "titleFormat": "Deploy: {{deployment}}"
}
```

### Query annotation from Elasticsearch

```json
{
  "datasource": { "type": "elasticsearch", "uid": "elasticsearch" },
  "query": "event_type:deploy",
  "name": "Deployments",
  "iconColor": "blue",
  "timeField": "@timestamp",
  "titleFormat": "{{service}} deployed {{version}}"
}
```

### Manual annotations

Hold Ctrl and click on a time series panel to add a note at a specific time.
These are stored in Grafana's internal database.

### API annotations

Create annotations programmatically (useful in CI/CD pipelines):

```bash
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

---

## Library panels

Library panels are reusable panel definitions shared across multiple dashboards.

- **Create:** Panel menu (three-dot) then "Create library panel"
- **Use:** When adding a panel, choose "Add from panel library"
- **Update:** Edit the source panel and all dashboards using it reflect the change
- **Unlink:** Detach a library panel to make it independent in a specific dashboard

Library panels are useful for standardizing common visualizations (like a
"service health" stat panel) across team dashboards.

---

## Sharing and embedding

### Share link

Click the Share icon on a dashboard, then the Link tab. Options:
- Lock time range (embed the current time window in the URL)
- Include template variable values

### Snapshot

Creates a read-only copy of the dashboard with rendered data at share time. No
live data source access is needed to view a snapshot. Snapshots can expire after
1 hour, 1 day, 7 days, or never.

### Export and import JSON

Export: Share then Export to download the dashboard JSON.
Import: Dashboards then New then Import. Paste JSON, upload a file, or enter a
grafana.com dashboard ID.

### Embed via iframe

Share then Embed generates an iframe HTML snippet. Requires anonymous access
enabled in Grafana configuration:

```
GF_AUTH_ANONYMOUS_ENABLED=true
GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer
```

### Public dashboards (Grafana 10+)

Make a specific dashboard publicly accessible without login. Enable per-dashboard
via Share then Public dashboard.

---

## Rows and layout

- **Add a row:** Use Add then Row to insert a collapsible section
- **Collapse rows:** Click the row header to collapse all panels within it
- **Move panels:** Drag the panel header
- **Resize panels:** Drag the panel corners
- **Duplicate:** Panel menu then Duplicate

---

## Playlists and kiosk mode

Playlists cycle through dashboards automatically.

1. Go to Dashboards then Playlists then New playlist
2. Add dashboards by name or tag
3. Set the rotation interval (for example, 5 minutes)
4. Append `?kiosk=1` to the URL for TV/kiosk mode (hides menus and navigation)

---

## Dashboard versioning

Access via Dashboard Settings then Versions. You can:
- See who saved what and when
- Compare two versions with a diff view
- Restore any previous version

---

## Keyboard shortcuts

| Key | Action |
|---|---|
| `Ctrl+S` | Save dashboard |
| `e` | Open panel editor (when a panel is focused) |
| `v` | Toggle panel fullscreen |
| `d r` | Refresh all panels |
| `d s` | Open dashboard settings |
| `d k` | Toggle kiosk mode |
| `?` | Show all shortcuts |
