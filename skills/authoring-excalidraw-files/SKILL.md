---
name: authoring-excalidraw-files
description: Generate architecture diagrams as .excalidraw files. Use when the user asks to create architecture diagrams, system diagrams, visualize codebase structure, infrastructure diagrams, or generate excalidraw files.
---

# Excalidraw Architecture Diagram Generator

Generate architecture diagrams as `.excalidraw` files from codebase analysis or user specifications.

---

## Prerequisites

- No prerequisites - generates raw JSON
- For visual inspection: Open `.excalidraw` files in [excalidraw.com](https://excalidraw.com) or VS Code extension

---

## Quick Start

**User asks:**
```
"Generate an architecture diagram for this project"
"Create an excalidraw diagram of the system"
"Visualize this codebase structure"
"Draw the infrastructure architecture"
```

**Claude will:**
1. Analyze the codebase (any language/framework)
2. Identify components, services, databases, APIs
3. Map relationships and data flows
4. Generate valid `.excalidraw` JSON
5. Validate the structure
6. User opens in excalidraw.com or VS Code for visual inspection

---

## Critical Rules

### 1. NEVER Use Diamond Shapes

Diamond arrow connections are broken in raw Excalidraw JSON. Use styled rectangles instead:

| Semantic Meaning | Rectangle Style |
|------------------|-----------------|
| Orchestrator/Hub | Coral (`#ffa8a8`/`#c92a2a`) + strokeWidth: 3 |
| Decision Point | Orange (`#ffd8a8`/`#e8590c`) + dashed stroke |

### 2. Labels Require TWO Elements

The `label` property does NOT work in raw JSON. Every labeled shape needs:

```json
// 1. Shape with boundElements reference
{
  "id": "my-box",
  "type": "rectangle",
  "boundElements": [{ "type": "text", "id": "my-box-text" }]
}

// 2. Separate text element with containerId
{
  "id": "my-box-text",
  "type": "text",
  "containerId": "my-box",
  "text": "My Label"
}
```

### 3. Elbow Arrows Need Three Properties

For 90-degree corners (not curved):

```json
{
  "type": "arrow",
  "roughness": 0,        // Clean lines
  "roundness": null,     // Sharp corners
  "elbowed": true        // 90-degree mode
}
```

### 4. Arrow Position at Shape Edge

Arrows must start/end at shape edges, not centers:

| Edge | Formula |
|------|---------|
| Top | `(x + width/2, y)` |
| Bottom | `(x + width/2, y + height)` |
| Left | `(x, y + height/2)` |
| Right | `(x + width, y + height/2)` |

### 5. Arrow width/height = Bounding Box

```
points = [[0, 0], [-440, 0], [-440, 70]]
width = 440   // max(abs(point[0]))
height = 70   // max(abs(point[1]))
```

---

## Workflow

### Step 1: Analyze Codebase

Discover components by looking for:

| Codebase Type | What to Look For |
|---------------|------------------|
| Monorepo | `packages/*/package.json`, workspace configs |
| Microservices | `docker-compose.yml`, k8s manifests |
| IaC | Terraform/Pulumi resource definitions |
| Backend API | Route definitions, controllers, DB models |
| Frontend | Component hierarchy, API calls |

**Use tools:**
- `Glob` for `**/package.json`, `**/Dockerfile`, `**/*.tf`
- `Grep` for `app.get`, `@Controller`, `CREATE TABLE`
- `Read` for README, config files, entry points

### Step 2: Plan Layout

**Vertical flow (most common):**
```
Row 1: Users/Entry points (y: 100)
Row 2: Frontend/Gateway (y: 250)
Row 3: Orchestration (y: 400)
Row 4: Services (y: 550)
Row 5: Data layer (y: 700)

Columns: x = 100, 300, 500, 700, 900
Element size: 160-200px x 80-90px
```

### Step 3: Generate Elements

For each component:
1. Create shape with unique `id`
2. Add `boundElements` referencing text
3. Create text with `containerId`
4. Choose color based on type (see `references/colors.md`)

### Step 4: Add Connections

For each relationship:
1. Calculate source edge point
2. Calculate target edge point
3. Determine routing pattern
4. Create arrow with `points` array
5. Set width/height from bounding box

See `references/arrows.md` for routing patterns.

### Step 5: Validate

Run validation script before finalizing:

```bash
uv run scripts/validate_excalidraw.py diagram.excalidraw
```

Checks performed:
- Valid JSON structure
- boundElements/containerId pairs match
- No duplicate IDs
- No diamond shapes
- Elbow arrows have required properties
- Arrow width/height matches points

### Step 6: Visual Inspection and Iterate

Open the `.excalidraw` file for visual inspection:
- **Web**: Drag file to [excalidraw.com](https://excalidraw.com)
- **VS Code**: Install "Excalidraw" extension and open file

If issues found:
1. Identify the problem element
2. Fix the JSON
3. Re-validate
4. Re-inspect
5. Repeat until correct

---

## Element Reference

### Shapes

| Component Type | Element Type | Background | Stroke |
|----------------|--------------|------------|--------|
| Frontend/UI | rectangle | `#a5d8ff` | `#1971c2` |
| Backend/API | rectangle | `#d0bfff` | `#7048e8` |
| Database | rectangle | `#b2f2bb` | `#2f9e44` |
| Storage | rectangle | `#ffec99` | `#f08c00` |
| Cache | rectangle | `#ffe8cc` | `#fd7e14` |
| Message Queue | rectangle | `#fff3bf` | `#fab005` |
| External API | rectangle | `#ffc9c9` | `#e03131` |
| Orchestrator | rectangle | `#ffa8a8` | `#c92a2a` |
| User/Actor | ellipse | `#e7f5ff` | `#1971c2` |

### Arrow Patterns

| Pattern | Points | Use Case |
|---------|--------|----------|
| Down | `[[0,0], [0,h]]` | Vertical connection |
| Right | `[[0,0], [w,0]]` | Horizontal connection |
| L-shape | `[[0,0], [dx,0], [dx,dy]]` | Offset connection |
| U-turn | `[[0,0], [50,0], [50,dy], [dx,dy]]` | Callback |

### Staggering Multiple Arrows

When N arrows leave from same edge:
- 2 arrows: 20%, 80% across edge
- 3 arrows: 20%, 50%, 80%
- 5 arrows: 20%, 35%, 50%, 65%, 80%

---

## Validation Checklist

Before writing file:
- [ ] Every shape with label has boundElements + text element
- [ ] Text elements have containerId matching shape
- [ ] Multi-point arrows have `elbowed: true`, `roundness: null`, `roughness: 0`
- [ ] Arrow x,y = source shape edge point
- [ ] Arrow final point offset reaches target edge
- [ ] Arrow width/height = bounding box of points
- [ ] No diamond shapes
- [ ] No duplicate IDs
- [ ] File is valid JSON

---

## Common Issues

| Issue | Fix |
|-------|-----|
| Labels don't appear | Use TWO elements (shape + text), not `label` property |
| Arrows curved | Add `elbowed: true`, `roundness: null`, `roughness: 0` |
| Arrows floating | Calculate x,y from shape edge, not center |
| Arrows overlapping | Stagger start positions across edge |
| Arrows clipped | Set width/height to bounding box of points |

---

## Reference Files

| File | Contents |
|------|----------|
| `references/schema.md` | JSON format, element types, text bindings, frames |
| `references/arrows.md` | Routing algorithm, patterns, bindings, staggering |
| `references/colors.md` | Default, AWS, Azure, GCP, Kubernetes palettes |

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/validate_excalidraw.py` | Validate JSON structure before saving |

Usage:
```bash
# Validate
uv run scripts/validate_excalidraw.py diagram.excalidraw

# Validate with verbose arrow checks
uv run scripts/validate_excalidraw.py diagram.excalidraw --verbose

# Output as JSON
uv run scripts/validate_excalidraw.py diagram.excalidraw --json
```

---

## Output

- **Location:** `docs/architecture/` or user-specified
- **Filename:** Descriptive, e.g., `system-architecture.excalidraw`
- **Testing:** Open in https://excalidraw.com or VS Code extension
