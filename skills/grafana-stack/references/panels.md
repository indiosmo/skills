# Panels and Visualizations Reference

## Table of contents

1. [Panel editor layout](#panel-editor-layout)
2. [Visualization types](#visualization-types)
3. [Field configuration](#field-configuration)
4. [Field overrides](#field-overrides)
5. [Query options](#query-options)
6. [Panel inspect](#panel-inspect)
7. [Performance tips](#performance-tips)

---

## Panel editor layout

Open the panel editor by clicking a panel title then Edit, or by clicking "Add
visualization" for a new panel.

- **Center:** Live visualization preview
- **Table view toggle:** Shows raw query results as a table (useful for debugging)
- **Right sidebar tabs:**
  1. Query -- configure data sources and write queries
  2. Transform -- apply data transformations
  3. Alert -- create alert rules from this panel
  4. Below the tabs: visualization-specific options and field config

---

## Visualization types

### Time series (default)

The go-to panel for any metric over time.

- Renders as lines, points, or bars
- Graph styles: Lines, Bars, Points (can mix per series via overrides)
- Stacking: None, Normal, 100%
- Supports dual Y-axes (left and right)
- Threshold lines or colored background regions
- Annotation overlay

### Stat

Single important value displayed as large text.

- Optional sparkline background showing recent trend
- Color modes: value text, background fill, or none
- Reduce function: last, mean, sum, max, min
- Good for KPI dashboards (uptime, current throughput, active users)

### Gauge

Value shown against a min/max range as a circular arc.

- Thresholds set the arc colors
- Best for percentages (disk usage, SLO budget remaining)

### Bar gauge

Multiple values as horizontal or vertical bars.

- Display modes: gradient, retro LCD, basic
- Good for comparing many items (top 10 services by latency)

### Bar chart

Categorical comparison.

- Horizontal or vertical orientation
- Grouped or stacked
- Supports labels on bars

### Table

Multi-column tabular data.

- Sortable columns
- Cell display modes: color text, color background, gradient gauge, sparkline
- Pagination for large datasets
- Column width customization

### Heatmap

Distribution over time.

- X-axis: time; Y-axis: buckets; Color: density or value
- Supports pre-bucketed data (Prometheus histogram) and raw values
- Tooltip shows exact bucket counts

### Histogram

Value distribution analysis.

- Groups values into configurable bucket sizes
- Can combine multiple series

### Pie chart

Part-to-whole proportions.

- Pie or donut style
- Labels show name, value, or percentage

### Logs

Log data from Elasticsearch, Loki, or other log sources.

- Timestamp and raw log lines
- Log level coloring (info/warn/error)
- Search and filter within results
- Deduplication
- JSON prettify option

### State timeline

State changes over time.

- Horizontal bands showing state duration
- Each series is one row
- Color per state value
- Good for on/off, healthy/degraded/critical status

### Status history

Periodic state checks over time.

- Grid layout: Y-axis is services, X-axis is time buckets
- Color per state

### Node graph

Service dependency maps and network topology.

- Nodes and edges
- Node color and size configurable by metric

### Geomap

Geographic data visualization.

- Layer types: markers, heatmap, route
- Base maps: OpenStreetMap, CARTO
- Supports GeoJSON

### Canvas

Custom layouts and process diagrams.

- Drag-and-drop element placement
- Elements: text, metric value, rectangle, ellipse, icon, image, connections
- Dynamic data binding per element

### XY chart

Correlation between two metrics (scatter plot).

- X and Y from different fields
- Bubble size from a third field

### Text

Documentation and header panels.

- Renders Markdown or HTML

### Alert list

Overview of currently firing alerts.

### Dashboard list

Navigation panel linking to other dashboards.

---

## Field configuration

Standard options available for most visualization types.

| Option | Purpose |
|---|---|
| Unit | Display unit (bytes, seconds, percent, requests per second, etc.) |
| Min / Max | Override auto-detected scale boundaries |
| Decimals | Number of decimal places |
| Display name | Override the series or field name |
| Color scheme | Fixed, thresholds-based, or palette |
| No value | Text shown when the value is null |

### Thresholds

Define color-coded boundaries. Two modes:

- **Absolute:** Fixed numeric values (for example, green below 70, yellow 70-90, red above 90)
- **Percentage:** Relative to min/max

```json
"thresholds": {
  "mode": "absolute",
  "steps": [
    { "color": "green", "value": null },
    { "color": "yellow", "value": 70 },
    { "color": "red", "value": 90 }
  ]
}
```

### Value mappings

Transform raw values into readable labels:

- **Value to text:** `1` becomes "Up", `0` becomes "Down"
- **Range to text:** `0-50` becomes "Low", `51-100` becomes "High"
- **Regex to text:** Match patterns for dynamic mapping

### Data links

Create clickable links from panel values to other dashboards or external systems:

```json
"links": [
  {
    "title": "View in detail dashboard",
    "url": "/d/detail?var-instance=${__field.labels.instance}&from=${__from}&to=${__to}",
    "targetBlank": false
  }
]
```

Available interpolation variables: `${__value.raw}`, `${__field.name}`,
`${__field.labels.label_name}`, `${__from}`, `${__to}`.

---

## Field overrides

Apply specific options to individual series or columns rather than all data.

1. In the panel editor, go to the Overrides section
2. Click "Add field override"
3. Choose the target:
   - Fields with name (exact match)
   - Fields with name matching regex
   - Fields with type (number, string, time)
   - Fields returned by a specific query (A, B, C...)
4. Add properties to override (unit, color, thresholds, display name, etc.)

Example: In a table with `cpu_idle` and `cpu_used` columns, set `cpu_used` to
display as percentage with red/yellow/green thresholds while leaving `cpu_idle`
with default styling.

---

## Query options

### Multiple queries

Add queries A, B, C... to one panel. They are overlaid in the visualization.
Useful for comparing metrics or showing multiple services on one graph.

### Server-side expressions

Combine query results with server-side math:

- **Math:** `$A + $B`, `$A / $B * 100`
- **Reduce:** Collapse a series to a scalar (Last, Mean, Sum, Max, Min)
- **Resample:** Change time resolution
- **Classic conditions:** Threshold logic (used in alerting)

### Important query variables

| Variable | Purpose |
|---|---|
| `$__interval` | Auto-calculated interval based on time range and resolution |
| `$__rate_interval` | Interval safe for `rate()` (at least 4x the scrape interval) |
| `$__from` | Start of time range as millisecond epoch |
| `$__to` | End of time range as millisecond epoch |
| `$__range` | Duration of the current time range (for example, "6h") |
| `$__range_s` | Duration in seconds |

### Per-panel time override

In query options, set "Relative time" to override the dashboard time range for a
specific panel. For example, set a panel to always show the last 24 hours
regardless of the dashboard time picker.

"Time shift" offsets the time range (for example, show the same panel but shifted
back one week for comparison).

---

## Panel inspect

Click the panel menu (three-dot icon) then Inspect to access:

- **Data:** Raw table view of the data powering the panel
- **Stats:** Query performance (execution time, row count)
- **JSON:** The panel's JSON model
- **Query:** Raw query and response (useful for debugging)

---

## Performance tips

1. Limit max data points to avoid over-fetching for wide time ranges
2. Use recording rules in Prometheus for expensive queries that appear on
   frequently-viewed dashboards
3. Set longer min intervals for historical dashboards
4. Use `$__interval` in queries to align with the panel's time resolution
5. Use `$__rate_interval` instead of hardcoded intervals for `rate()` queries
6. Keep dashboards under 20 panels where possible; use collapsible rows to
   organize larger dashboards
