# Mermaid Syntax Quick Reference

Quick lookup for node shapes, arrows, styling, and common syntax patterns.

## Node Shapes (Flowchart)

| Shape | Syntax | Use Case |
|-------|--------|----------|
| Rectangle | `A[Text]` | Process, action, step |
| Rounded | `A(Text)` | Start/end, general node |
| Stadium | `A([Text])` | Terminal, start/end |
| Subroutine | `A[[Text]]` | Subprocess, function call |
| Database | `A[(Text)]` | Database, storage |
| Circle | `A((Text))` | Connector, junction |
| Diamond | `A{Text}` | Decision, condition |
| Hexagon | `A{{Text}}` | Preparation, setup |
| Parallelogram | `A[/Text/]` | Input |
| Parallelogram Alt | `A[\Text\]` | Output |
| Trapezoid | `A[/Text\]` | Manual operation |
| Trapezoid Alt | `A[\Text/]` | Manual input |
| Double Circle | `A(((Text)))` | Stop |

**Visual Reference**:
```mermaid
flowchart LR
    rect[Rectangle]
    round(Rounded)
    stadium([Stadium])
    sub[[Subroutine]]
    db[(Database)]
    circle((Circle))
    diamond{Diamond}
    hex{{Hexagon}}
```

## Arrow Types (Flowchart)

| Arrow | Syntax | Description |
|-------|--------|-------------|
| Solid arrow | `A --> B` | Standard connection |
| Solid line | `A --- B` | Connection without arrow |
| Dotted arrow | `A -.-> B` | Optional or async |
| Dotted line | `A -.- B` | Weak relationship |
| Thick arrow | `A ==> B` | Emphasized connection |
| Thick line | `A === B` | Strong relationship |
| With label | `A -->|label| B` | Labeled connection |
| With label alt | `A --label--> B` | Alternative label syntax |
| Multidirectional | `A <--> B` | Bidirectional |

**Arrow Length**:
```
A --> B      Normal
A ---> B     Longer
A ----> B    Even longer
```

**Combined Example**:
```mermaid
flowchart LR
    A -->|normal| B
    B -.->|optional| C
    C ==>|important| D
    D <-->|bidirectional| E
```

## Sequence Diagram Arrows

| Arrow | Syntax | Description |
|-------|--------|-------------|
| Solid with arrow | `->>` | Synchronous message |
| Dotted with arrow | `-->>` | Response, return |
| Solid with cross | `-x` | Lost message |
| Dotted with cross | `--x` | Lost async |
| Solid open arrow | `-)` | Async message |
| Dotted open arrow | `--)` | Async response |

## Direction Keywords

| Keyword | Direction | Best For |
|---------|-----------|----------|
| `TD` or `TB` | Top to Down | Hierarchies, trees |
| `LR` | Left to Right | Processes, timelines |
| `BT` | Bottom to Top | Bottom-up flows |
| `RL` | Right to Left | Reverse processes |

## Subgraph Syntax

```mermaid
flowchart LR
    subgraph GroupName["Display Title"]
        direction TB
        A[Node A]
        B[Node B]
    end

    subgraph Another
        C[Node C]
    end

    A --> C
```

**Nested Subgraphs**:
```mermaid
flowchart TB
    subgraph Outer["Outer Group"]
        subgraph Inner["Inner Group"]
            A[Node]
        end
        B[Other]
    end
```

## Styling

### Class Definitions

```mermaid
flowchart LR
    classDef default fill:#f9f9f9,stroke:#333
    classDef primary fill:#4CAF50,stroke:#2E7D32,color:#fff
    classDef warning fill:#FF9800,stroke:#F57C00
    classDef error fill:#f44336,stroke:#c62828,color:#fff

    A[Default]
    B[Primary]:::primary
    C[Warning]:::warning
    D[Error]:::error

    A --> B --> C --> D
```

### Inline Styles

```mermaid
flowchart LR
    A[Styled Node]
    style A fill:#bbf,stroke:#333,stroke-width:2px
```

### Link Styles

```mermaid
flowchart LR
    A --> B --> C
    linkStyle 0 stroke:#ff3,stroke-width:4px
    linkStyle 1 stroke:#3f3,stroke-width:2px,stroke-dasharray:5
```

### Subgraph Styling

```mermaid
flowchart LR
    subgraph sub1[Styled Subgraph]
        A[Node]
    end
    style sub1 fill:#ffe,stroke:#aa0
```

## Text Formatting

### Line Breaks

```mermaid
flowchart LR
    A["Line 1<br/>Line 2<br/>Line 3"]
```

### Special Characters

Characters that need quoting: `()[]{}|<>` and reserved words

```mermaid
flowchart LR
    A["Node with (parens)"]
    B["Node with [brackets]"]
    C["Reserved: end"]
```

### Unicode and Emoji

```mermaid
flowchart LR
    A["Check completed"]
    B["Warning sign"]
```

## Comments

```mermaid
flowchart LR
    %% This is a comment
    A[Node A] --> B[Node B]
    %% Comments can appear anywhere
```

## Common Patterns

### Decision Tree

```mermaid
flowchart TD
    Q{Question?}
    Q -->|Yes| Y[Yes Path]
    Q -->|No| N[No Path]
```

### Pipeline

```mermaid
flowchart LR
    I[Input] --> P1[Process 1] --> P2[Process 2] --> O[Output]
```

### Parallel Processing

```mermaid
flowchart TD
    S[Start]
    S --> A & B & C
    A & B & C --> E[End]
```

### Loop Back

```mermaid
flowchart LR
    A[Start] --> B[Process]
    B --> C{Done?}
    C -->|No| B
    C -->|Yes| D[End]
```

## Escape Sequences

| Character | Escape |
|-----------|--------|
| `#` | `#35;` |
| `;` | `#59;` |
| Quote in string | Use different quotes |

## Configuration (Directives)

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': {'primaryColor': '#ff0000'}}}%%
flowchart LR
    A --> B
```

Common themes: `default`, `dark`, `forest`, `neutral`
