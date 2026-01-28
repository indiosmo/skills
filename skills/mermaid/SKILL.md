---
name: mermaid
description: Create, validate, and optimize Mermaid diagrams for software documentation. Use when Claude needs to: (1) Create flowcharts, sequence diagrams, state diagrams, class diagrams, ER diagrams, or architecture diagrams, (2) Validate Mermaid syntax, (3) Review and improve diagram aesthetics, (4) Fix broken Mermaid code, or (5) Choose the right diagram type for a use case.
---

# Mermaid Diagram Skill

Create professional Mermaid diagrams with proper syntax, clear layout, and validated output.

## Prerequisites

Check that the Mermaid CLI is available:

```bash
mmdc --version
```

If not installed, install via npm:
```bash
npm install -g @mermaid-js/mermaid-cli
```

## Workflow Overview

1. **Choose Diagram Type** - Select the appropriate diagram type for your use case
2. **Write Diagram** - Use idiomatic patterns and clear naming
3. **Validate Syntax** - Run through mmdc to catch syntax errors
4. **Review Diagram Code** - Check for common issues
5. **Visual Review** - Check the rendered output for layout issues
6. **Iterate** - Refine based on feedback

## Diagram Type Selection

| Type | Best For | Key Indicator |
|------|----------|---------------|
| **Flowchart** | Processes, decisions, algorithms, workflows | "How does X flow?" or "What are the steps?" |
| **Sequence Diagram** | API calls, message passing, interactions over time | "How do components communicate?" |
| **State Diagram** | State machines, object lifecycles, status transitions | "What states can X be in?" |
| **Class Diagram** | OOP design, type relationships, inheritance | "What are the types and their relationships?" |
| **ER Diagram** | Database schemas, data models, table relationships | "What data do we store and how is it related?" |
| **Architecture** | System components, services, infrastructure | "What are the high-level components?" |

For detailed syntax and examples of each type, see `references/diagram-types.md`.

## Idiomatic Patterns

### Use Self-Explanatory Node IDs

Good - IDs describe the node:
```mermaid
flowchart LR
    userInput[User Input] --> validation{Valid?}
    validation -->|Yes| processData[Process Data]
    validation -->|No| showError[Show Error]
```

Bad - Cryptic IDs:
```mermaid
flowchart LR
    A[User Input] --> B{Valid?}
    B -->|Yes| C[Process Data]
    B -->|No| D[Show Error]
```

### Declare Nodes Before Connections

For complex diagrams, declare nodes first, then define connections:

```mermaid
flowchart TD
    %% Node declarations
    start[Start Process]
    validate{Validate Input}
    process[Process Data]
    error[Handle Error]
    done[Complete]

    %% Connections
    start --> validate
    validate -->|Valid| process
    validate -->|Invalid| error
    process --> done
    error --> validate
```

### Use Subgraphs for Logical Grouping

```mermaid
flowchart LR
    subgraph Frontend
        ui[UI Layer]
        state[State Management]
    end

    subgraph Backend
        api[API Server]
        db[(Database)]
    end

    ui --> api
    state --> api
    api --> db
```

### Direction Guidelines

| Direction | Code | Best For |
|-----------|------|----------|
| Top to Bottom | `TD` or `TB` | Hierarchies, decision trees |
| Left to Right | `LR` | Timelines, processes, pipelines |
| Bottom to Top | `BT` | Bottom-up flows |
| Right to Left | `RL` | Reverse flows |

## Validation Workflow

### Step 1: Syntax Validation

Save your diagram to a `.mmd` file and validate:

```bash
uv run scripts/validate_mermaid.py diagram.mmd --output diagram.svg
```

The script will report syntax errors with line numbers.

### Step 2: Visual Quality Review

After syntax validation passes, review the rendered output for:

- [ ] **Readability**: All text is legible, no overlapping labels
- [ ] **Edge Crossings**: Minimized (try different direction if excessive)
- [ ] **Logical Grouping**: Related nodes grouped in subgraphs where beneficial
- [ ] **Consistent Shapes**: Same node shape for similar concepts
- [ ] **Flow Direction**: Consistent and intuitive (usually LR for processes, TD for hierarchies)
- [ ] **Labels**: Edge labels present where needed for clarity
- [ ] **Spacing**: Nodes not too cramped or too spread out
- [ ] **Color Usage**: Styling aids understanding, not just decoration

### Step 3: Common Fixes

If the diagram renders but looks wrong:

| Issue | Fix |
|-------|-----|
| Too many edge crossings | Try different direction (LR vs TD) |
| Nodes too cramped | Add line breaks in labels: `node["Line 1<br/>Line 2"]` |
| Subgraphs overlapping | Reduce nesting depth or split into multiple diagrams |
| Arrows going wrong way | Check connection order: `from --> to` |

## Common Gotchas

| Problem | Cause | Solution |
|---------|-------|----------|
| `Parse error` on node text | Reserved word or special character | Wrap in quotes: `node["end"]` |
| Arrows not rendering | Wrong arrow syntax | Use `-->` not `->` for flowcharts |
| Subgraph not grouping | Missing `end` keyword | Ensure every `subgraph` has `end` |
| Direction ignored | Direction after nodes | Put direction first: `flowchart LR` |
| Sequence diagram timeline wrong | Participants not declared | Declare participants in order |

### Reserved Words to Quote

These words must be quoted when used as node labels:
- `end`, `graph`, `subgraph`, `direction`
- `click`, `style`, `class`, `classDef`
- `default`, `linkStyle`

```mermaid
flowchart LR
    start[Start] --> finish["end"]  %% "end" must be quoted
```

## Quick Syntax Reference

### Node Shapes

```
node[Rectangle]
node(Rounded)
node([Stadium])
node[[Subroutine]]
node[(Database)]
node((Circle))
node{Diamond}
node{{Hexagon}}
node[/Parallelogram/]
node[\Parallelogram Alt\]
node[/Trapezoid\]
node[\Trapezoid Alt/]
```

### Arrow Types

```
A --> B       Solid arrow
A --- B       Solid line (no arrow)
A -.-> B      Dotted arrow
A -.- B       Dotted line
A ==> B       Thick arrow
A === B       Thick line
A --text--> B Arrow with label
A -->|text| B Arrow with label (alt)
```

### Styling

```mermaid
flowchart LR
    %% Define styles
    classDef primary fill:#4CAF50,stroke:#2E7D32,color:#fff
    classDef warning fill:#FF9800,stroke:#F57C00,color:#000

    %% Apply styles
    nodeA[Primary Node]:::primary
    nodeB[Warning Node]:::warning

    nodeA --> nodeB
```

## Reference Files

- `references/diagram-types.md` - Detailed syntax and examples for each diagram type
- `references/syntax-quick-ref.md` - Complete node shapes, arrows, and styling reference
- `references/layout-patterns.md` - Subgraphs, nesting, and layout strategies
- `references/common-issues.md` - Troubleshooting guide and quality checklist

## Example: Complete Workflow

Creating an authentication flow diagram:

1. **Choose type**: Flowchart (it's a process with decisions)

2. **Write diagram**:
```mermaid
flowchart TD
    subgraph Client
        request[Login Request]
        storeToken[Store Token]
        retry[Retry Login]
    end

    subgraph AuthServer["Auth Server"]
        validate{Valid Credentials?}
        generateToken[Generate JWT]
        logFailure[Log Failed Attempt]
    end

    request --> validate
    validate -->|Yes| generateToken
    validate -->|No| logFailure
    generateToken --> storeToken
    logFailure --> retry
    retry --> request
```

3. **Validate**:
```bash
uv run scripts/validate_mermaid.py auth-flow.mmd --output auth-flow.svg
```

4. **Review**: Check the SVG output for readability

5. **Iterate**: Adjust direction, add styling if needed
