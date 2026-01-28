# Excalidraw JSON Schema Reference

Complete reference for Excalidraw JSON structure and element types.

---

## File Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "claude-code-excalidraw-skill",
  "elements": [],
  "appState": {
    "gridSize": 20,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `"excalidraw"` |
| `version` | number | Schema version (use `2`) |
| `source` | string | Origin identifier |
| `elements` | array | All diagram elements |
| `appState` | object | Editor configuration |
| `files` | object | Embedded image data (usually empty for architecture diagrams) |

---

## Element Types

| Type | Use For | Arrow Reliability |
|------|---------|-------------------|
| `rectangle` | Services, components, databases, containers, orchestrators, decision points | Excellent |
| `ellipse` | Users, external systems, start/end points | Good |
| `text` | Labels inside shapes, titles, annotations | N/A |
| `arrow` | Data flow, connections, dependencies | N/A |
| `line` | Grouping boundaries, separators | N/A |
| `frame` | Logical groupings with clipping | Good |

### BANNED: Diamond Shapes

**NEVER use `type: "diamond"` in generated diagrams.**

Diamond arrow connections are fundamentally broken in raw Excalidraw JSON:
- Excalidraw applies `roundness` to diamond vertices during rendering
- Visual edges appear offset from mathematical edge points
- No offset formula reliably compensates
- Arrows appear disconnected/floating

**Use styled rectangles instead** for visual distinction:

| Semantic Meaning | Rectangle Style |
|------------------|-----------------|
| Orchestrator/Hub | Coral (`#ffa8a8`/`#c92a2a`) + strokeWidth: 3 |
| Decision Point | Orange (`#ffd8a8`/`#e8590c`) + dashed stroke |
| Central Router | Larger size + bold color |

---

## Required Element Properties

Every element MUST have these base properties:

```json
{
  "id": "unique-id-string",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "angle": 0,
  "strokeColor": "#1971c2",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "seed": 1,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

### Property Reference

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier |
| `type` | string | Element type |
| `x`, `y` | number | Position (top-left corner) |
| `width`, `height` | number | Dimensions |
| `angle` | number | Rotation in radians (usually 0) |
| `strokeColor` | string | Border color (hex) |
| `backgroundColor` | string | Fill color (hex or "transparent") |
| `fillStyle` | string | "solid", "hachure", "cross-hatch" |
| `strokeWidth` | number | Border thickness (1-4 typical) |
| `strokeStyle` | string | "solid", "dashed", "dotted" |
| `roughness` | number | 0=clean, 1=sketchy, 2=very sketchy |
| `opacity` | number | 0-100 |
| `groupIds` | array | Group memberships |
| `frameId` | string/null | Parent frame ID |
| `roundness` | object/null | Corner rounding (type: 3 for rectangles, 2 for ellipses) |
| `seed` | number | Randomization seed |
| `version` | number | Element version |
| `versionNonce` | number | Version identifier |
| `isDeleted` | boolean | Soft delete flag |
| `boundElements` | array/null | Linked elements (text, arrows) |
| `updated` | number | Timestamp |
| `link` | string/null | URL link |
| `locked` | boolean | Edit lock |

---

## Text Binding System

**Every labeled shape requires TWO elements.**

The `label` property does NOT work in raw JSON. You must create:
1. A shape with `boundElements` referencing the text
2. A separate text element with `containerId` referencing the shape

### Shape with boundElements

```json
{
  "id": "api-server",
  "type": "rectangle",
  "x": 500,
  "y": 200,
  "width": 200,
  "height": 90,
  "strokeColor": "#1971c2",
  "backgroundColor": "#a5d8ff",
  "boundElements": [{ "type": "text", "id": "api-server-text" }],
  ...
}
```

### Text with containerId

```json
{
  "id": "api-server-text",
  "type": "text",
  "x": 505,
  "y": 220,
  "width": 190,
  "height": 50,
  "text": "API Server\nExpress.js",
  "fontSize": 16,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "api-server",
  "originalText": "API Server\nExpress.js",
  "lineHeight": 1.25,
  ...
}
```

### Text Positioning Formulas

| Property | Formula |
|----------|---------|
| Text `x` | `shape.x + 5` |
| Text `y` | `shape.y + (shape.height - text.height) / 2` |
| Text `width` | `shape.width - 10` |

### Text Element Properties

| Property | Value |
|----------|-------|
| `fontSize` | 16 (standard), 14 (small), 20 (headers) |
| `fontFamily` | 1 (Virgil/hand-drawn), 2 (Helvetica), 3 (Cascadia/mono) |
| `textAlign` | "left", "center", "right" |
| `verticalAlign` | "top", "middle", "bottom" |
| `lineHeight` | 1.25 (default) |

### ID Naming Convention

Always use pattern: `{shape-id}-text` for text element IDs.

---

## Arrow System

### Basic Arrow Properties

```json
{
  "id": "arrow-api-db",
  "type": "arrow",
  "x": 600,
  "y": 290,
  "width": 0,
  "height": 110,
  "points": [[0, 0], [0, 110]],
  "strokeColor": "#1971c2",
  "roughness": 0,
  "roundness": null,
  "elbowed": true,
  "startBinding": null,
  "endBinding": null,
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "lastCommittedPoint": null,
  ...
}
```

### Elbow Arrow Requirements

For 90-degree corners (not curved), ALL THREE properties are required:

```json
{
  "roughness": 0,        // Clean lines
  "roundness": null,     // Sharp corners
  "elbowed": true        // 90-degree mode
}
```

### Arrow Position

Arrow `x,y` must be at the source shape's edge, NOT the center:

| Edge | Formula |
|------|---------|
| Top | `(shape.x + shape.width/2, shape.y)` |
| Bottom | `(shape.x + shape.width/2, shape.y + shape.height)` |
| Left | `(shape.x, shape.y + shape.height/2)` |
| Right | `(shape.x + shape.width, shape.y + shape.height/2)` |

### Arrow width/height

Must match the bounding box of points:

```
points = [[0, 0], [-440, 0], [-440, 70]]
width = 440  // max(abs(point[0]))
height = 70  // max(abs(point[1]))
```

### Arrowhead Options

| Value | Description |
|-------|-------------|
| `null` | No arrowhead |
| `"arrow"` | Standard arrow |
| `"bar"` | Perpendicular bar |
| `"dot"` | Circle |
| `"triangle"` | Filled triangle |

See `arrows.md` for detailed routing patterns.

---

## Frames

Frames group elements with visual clipping.

### Frame Element

```json
{
  "id": "frame-backend",
  "type": "frame",
  "x": 100,
  "y": 200,
  "width": 400,
  "height": 300,
  "name": "Backend Services",
  ...
}
```

### Frame Children

Elements inside a frame have `frameId` set:

```json
{
  "id": "api-server",
  "type": "rectangle",
  "frameId": "frame-backend",
  ...
}
```

### Ordering Requirement

**Frame children must come BEFORE the frame element in the elements array.**

```json
{
  "elements": [
    { "id": "child-1", "frameId": "frame-1", ... },
    { "id": "child-2", "frameId": "frame-1", ... },
    { "id": "frame-1", "type": "frame", ... }
  ]
}
```

Incorrect ordering causes rendering and clipping issues.

---

## Grouping (Alternative to Frames)

For logical groupings without clipping, use dashed rectangles:

```json
{
  "id": "group-ai-pipeline",
  "type": "rectangle",
  "x": 100,
  "y": 500,
  "width": 1000,
  "height": 280,
  "strokeColor": "#9c36b5",
  "backgroundColor": "transparent",
  "strokeStyle": "dashed",
  "roughness": 0,
  "roundness": null,
  "boundElements": null
}
```

Group labels are standalone text (no containerId) at top-left:

```json
{
  "id": "group-ai-pipeline-label",
  "type": "text",
  "x": 120,
  "y": 510,
  "text": "AI Processing Pipeline",
  "textAlign": "left",
  "verticalAlign": "top",
  "containerId": null,
  ...
}
```

---

## Dynamic ID Generation

Generate IDs from component names discovered in codebase:

| Discovered Component | Generated ID | Generated Label |
|---------------------|--------------|-----------------|
| Express API server | `express-api` | `"API Server\nExpress.js"` |
| PostgreSQL database | `postgres-db` | `"PostgreSQL\nDatabase"` |
| Redis cache | `redis-cache` | `"Redis\nCache"` |
| S3 bucket for uploads | `s3-uploads` | `"S3 Bucket\nuploads/"` |
| Lambda function | `lambda-processor` | `"Lambda\nProcessor"` |
| React frontend | `react-frontend` | `"React App\nFrontend"` |

---

## Critical Caveats Summary

1. **Never use diamond shapes** - Arrow connections are broken
2. **Labels require TWO elements** - Shape + text, not `label` property
3. **Elbow arrows need THREE properties** - `roughness: 0`, `roundness: null`, `elbowed: true`
4. **Arrow x,y is at shape edge** - Not center
5. **Arrow width/height = bounding box** - Of points array
6. **Frame children before frame** - In elements array order
