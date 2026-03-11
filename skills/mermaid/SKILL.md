---
name: mermaid
description: Create, validate, and optimize Mermaid diagrams for software documentation. Use when asked to visualize, diagram, chart a process, draw a workflow, document architecture, create a system diagram, or produce a data model diagram. Covers flowcharts, sequence diagrams, state diagrams, class diagrams, ER diagrams, and architecture diagrams. Also handles Mermaid syntax validation, diagram aesthetics review, fixing broken Mermaid code, and choosing the right diagram type for a use case.
---

# Mermaid Diagram Skill

Create professional Mermaid diagrams with proper syntax, clear layout, and validated output.

## Prerequisites

**Required: Mermaid CLI** - The `mmdc` command must be available:
```bash
npm install -g @mermaid-js/mermaid-cli
```

**Optional: beautiful-mermaid** - For enhanced theming and ASCII output:
```bash
cd skills/mermaid/scripts && npm install
```

This enables 15 built-in themes (tokyo-night, dracula, github-dark, etc.) and text-based diagram rendering for terminals.

## Workflow Overview

1. **Choose Diagram Type** - Select the appropriate diagram type for your use case
2. **Write Diagram** - Use idiomatic patterns and clear naming
3. **Validate Syntax** - Run through mmdc to catch spec errors
4. **Render Output** - Use beautiful-mermaid for final output (when available)
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

## Validation and Rendering Workflow

### Step 1: Syntax Validation (mmdc)

Save your diagram to a `.mmd` file and validate syntax using mmdc:

```bash
uv run scripts/validate_mermaid.py diagram.mmd --renderer mmdc -o diagram.svg
```

The script will report syntax errors with line numbers. Always use mmdc for syntax validation as it is the authoritative Mermaid spec parser.

The validation script uses a default config (`scripts/mermaid-config.json`) that prevents text clipping by using arial font and increased padding. To use a custom config or disable it:

```bash
# Custom config
uv run scripts/validate_mermaid.py diagram.mmd --renderer mmdc -c my-config.json

# No config (use mmdc defaults)
uv run scripts/validate_mermaid.py diagram.mmd --renderer mmdc --no-config
```

### Step 2: Render with beautiful-mermaid (Preferred)

After syntax validation passes, render the final output with beautiful-mermaid for better theming:

```bash
uv run scripts/validate_mermaid.py diagram.mmd --renderer beautiful --theme github-light -o diagram.svg
```

**Renderer selection rules:**
| Diagram Type | Renderer | Notes |
|--------------|----------|-------|
| Flowchart, Sequence, State, Class, ER | `--renderer beautiful` | Preferred for theming |
| Architecture | `--renderer mmdc` | beautiful-mermaid not supported |

If beautiful-mermaid is not installed, skip this step and use the mmdc output from Step 1.

### Step 3: Visual Quality Review

After syntax validation passes, review the rendered output for:

- [ ] **Readability**: All text is legible, no overlapping labels
- [ ] **Edge Crossings**: Minimized (try different direction if excessive)
- [ ] **Logical Grouping**: Related nodes grouped in subgraphs where beneficial
- [ ] **Consistent Shapes**: Same node shape for similar concepts
- [ ] **Flow Direction**: Consistent and intuitive (usually LR for processes, TD for hierarchies)
- [ ] **Labels**: Edge labels present where needed for clarity
- [ ] **Spacing**: Nodes not too cramped or too spread out
- [ ] **Color Usage**: Styling aids understanding, not just decoration

### Step 4: Common Fixes

If the diagram renders but looks wrong:

| Issue | Fix |
|-------|-----|
| Too many edge crossings | Try different direction (LR vs TD) |
| Nodes too cramped | Add line breaks in labels: `node["Line 1<br/>Line 2"]` |
| Subgraphs overlapping | Reduce nesting depth or split into multiple diagrams |
| Arrows going wrong way | Check connection order: `from --> to` |

## Theming

beautiful-mermaid provides 15 built-in themes (5 light, 10 dark) for professional diagram styling. Themes use a two-color foundation system that derives all diagram colors from background and foreground values.

```bash
# List available themes
uv run scripts/validate_mermaid.py --list-themes

# Render with a specific theme
uv run scripts/validate_mermaid.py diagram.mmd --theme tokyo-night -o diagram.svg

# Custom colors (overrides theme)
uv run scripts/validate_mermaid.py diagram.mmd --bg "#1a1b26" --fg "#c0caf5" -o diagram.svg
```

For the full theme list, color details, selection guide, and custom theme creation, see `references/theming-guide.md`.

## ASCII Output

beautiful-mermaid can render diagrams as text for terminal environments.

### Output Modes

| Mode | Flag | Characters | Best For |
|------|------|------------|----------|
| Unicode | `--unicode` | Box-drawing chars | Modern terminals |
| ASCII | `--ascii` | Basic ASCII only | Legacy terminals, logs |

### Usage

```bash
# Unicode output (recommended)
uv run scripts/validate_mermaid.py diagram.mmd --unicode -o diagram.txt

# ASCII output
uv run scripts/validate_mermaid.py diagram.mmd --ascii -o diagram.txt

# With padding adjustments
uv run scripts/validate_mermaid.py diagram.mmd --unicode --padding-x 2 --padding-y 1 -o diagram.txt
```

### Use Cases

- Terminal-based documentation viewers
- Log file embedding
- Email/plain-text contexts
- Accessibility (screen readers)
- CI/CD pipeline output

### Limitations

ASCII/Unicode output is only available for diagram types supported by beautiful-mermaid:
- Flowcharts
- Sequence diagrams
- State diagrams
- Class diagrams
- ER diagrams

Architecture diagrams are **not supported** - use SVG output with mmdc instead.

## Reference Files

- `references/diagram-types.md` - Full syntax and examples for flowcharts, sequence, state, class, ER, and architecture diagrams
- `references/syntax-quick-ref.md` - Node shapes, arrow types, styling classes, text formatting, and escape sequences
- `references/layout-patterns.md` - Subgraph organization, nesting strategies, and direction optimization
- `references/common-issues.md` - Parse errors, reserved words, text clipping fixes, and debugging steps
- `references/theming-guide.md` - beautiful-mermaid themes, custom colors, and advanced styling

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

3. **Validate syntax** (mmdc):
```bash
uv run scripts/validate_mermaid.py auth-flow.mmd --renderer mmdc -o auth-flow-check.svg
```

4. **Render with theme** (beautiful-mermaid):
```bash
uv run scripts/validate_mermaid.py auth-flow.mmd --renderer beautiful --theme github-dark -o auth-flow.svg
```

5. **Generate ASCII for docs** (optional):
```bash
uv run scripts/validate_mermaid.py auth-flow.mmd --renderer beautiful --unicode -o auth-flow.txt
```

6. **Review**: Check the SVG output for readability

7. **Iterate**: Adjust direction, add styling if needed
