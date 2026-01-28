# Mermaid Layout Patterns

Best practices for organizing complex diagrams with subgraphs, nesting, and layout strategies.

## When to Use Subgraphs

Use subgraphs to:
- Group related nodes logically (e.g., by service, layer, or domain)
- Create visual boundaries between concerns
- Add labels to groups of nodes
- Apply consistent styling to groups

Avoid subgraphs when:
- The diagram has fewer than 6-8 nodes
- Grouping doesn't add clarity
- It creates unnecessary nesting

## Subgraph Best Practices

### Clear Naming

```mermaid
flowchart LR
    %% Good: Descriptive names
    subgraph Frontend["Frontend Layer"]
        UI[User Interface]
    end

    %% Avoid: Generic names
    subgraph Group1
        A[Something]
    end
```

### Direction Within Subgraphs

```mermaid
flowchart LR
    subgraph Services
        direction TB
        api[API]
        auth[Auth]
        db[(DB)]
        api --> auth --> db
    end

    client[Client] --> api
```

### Consistent Grouping Criteria

Pick one grouping strategy:
- By layer (presentation, business, data)
- By domain (users, orders, inventory)
- By deployment (frontend, backend, database)
- By team ownership

## Nesting Depth Guidelines

**Recommended: Maximum 2-3 levels**

```mermaid
flowchart TB
    subgraph System["System"]
        subgraph Backend["Backend"]
            api[API]
            worker[Worker]
        end
        subgraph Data["Data"]
            db[(Database)]
        end
    end
```

**Avoid: Deep nesting (4+ levels)**

Deep nesting causes:
- Rendering issues
- Cramped layouts
- Readability problems

**Solution**: Split into multiple diagrams or flatten hierarchy.

## Cross-Subgraph Connections

### Clean Connections

```mermaid
flowchart LR
    subgraph A["Service A"]
        a1[Component 1]
        a2[Component 2]
    end

    subgraph B["Service B"]
        b1[Component 1]
    end

    %% Connect specific nodes, not subgraphs
    a2 --> b1
```

### Minimize Crossing Lines

Place subgraphs to reduce edge crossings:

```mermaid
flowchart LR
    %% Good: Linear flow
    subgraph Input
        I[Input]
    end
    subgraph Process
        P[Process]
    end
    subgraph Output
        O[Output]
    end

    I --> P --> O
```

## Reducing Edge Crossings

### Strategy 1: Change Direction

If TD has many crossings, try LR:

```mermaid
%% Before: TD with crossings
flowchart TD
    A --> C
    B --> D
    A --> D
    B --> C
```

```mermaid
%% After: LR may be cleaner
flowchart LR
    A --> C
    A --> D
    B --> C
    B --> D
```

### Strategy 2: Reorder Nodes

Node declaration order affects layout:

```mermaid
flowchart LR
    %% Declare in visual order
    A[Start]
    B[Middle 1]
    C[Middle 2]
    D[End]

    A --> B --> D
    A --> C --> D
```

### Strategy 3: Invisible Links

Use invisible links to influence positioning:

```mermaid
flowchart LR
    A --> B
    C --> D
    B ~~~ C  %% Invisible link for spacing
```

## Direction Strategies by Diagram Type

| Diagram Type | Recommended Direction | Reason |
|--------------|----------------------|--------|
| Process flow | LR | Natural reading order |
| Hierarchy/tree | TD | Parent-child relationship |
| Timeline | LR | Chronological order |
| Data flow | LR or TD | Depends on context |
| Architecture | TD or LR | Depends on layers |

## Large Diagram Strategies

### Split by Concern

Instead of one massive diagram, create multiple focused diagrams:
- Overview diagram (high-level components)
- Detail diagrams (each component's internals)

### Use Link Nodes

Reference other diagrams:

```mermaid
flowchart LR
    subgraph Main["Main System"]
        A[Component A]
        B[Component B]
    end

    external[["See: External Systems Diagram"]]

    A --> external
```

### Progressive Disclosure

Show detail levels:

```mermaid
%% Level 1: High-level
flowchart LR
    Client --> Server --> Database

%% Level 2: Expand Server (separate diagram)
flowchart LR
    subgraph Server
        LB[Load Balancer]
        API[API Server]
        Cache[Cache]
    end
```

## Common Layout Mistakes

### Mistake: Everything in One Subgraph

```mermaid
%% Bad: Subgraph doesn't add value
flowchart LR
    subgraph Everything
        A --> B --> C
    end
```

### Mistake: Crossing Subgraph Boundaries Excessively

```mermaid
%% Hard to read: Many cross-boundary connections
flowchart LR
    subgraph A
        a1 & a2 & a3
    end
    subgraph B
        b1 & b2 & b3
    end

    a1 --> b1 & b2 & b3
    a2 --> b1 & b2 & b3
    a3 --> b1 & b2 & b3
```

**Solution**: Group connections or use an intermediary node.

### Mistake: Inconsistent Direction

```mermaid
%% Confusing: Mixed directions
flowchart LR
    A --> B
    B --> C
    D --> B  %% Goes against flow
```

**Solution**: Maintain consistent flow direction.
