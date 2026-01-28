# Mermaid Diagram Types Reference

Detailed syntax, examples, and guidance for each supported diagram type.

## 1. Flowchart

**Purpose**: Visualize processes, decisions, algorithms, and workflows.

**When to Use**:
- Documenting step-by-step processes
- Decision trees and branching logic
- Algorithm visualization
- User journey flows

**Basic Syntax**:
```mermaid
flowchart LR
    A[Hard] -->|Text| B(Round)
    B --> C{Decision}
    C -->|One| D[Result 1]
    C -->|Two| E[Result 2]
```

**Direction Options**:
- `flowchart TD` - Top to bottom (default)
- `flowchart LR` - Left to right
- `flowchart BT` - Bottom to top
- `flowchart RL` - Right to left

**Key Features**:
- Multiple node shapes for different meanings
- Subgraphs for logical grouping
- Edge labels for conditions
- Styling with classes

**Complete Example**:
```mermaid
flowchart TD
    subgraph Input["Input Processing"]
        start([Start]) --> readData[Read Input Data]
        readData --> validate{Valid Format?}
    end

    subgraph Processing
        transform[Transform Data]
        enrich[Enrich with Metadata]
    end

    subgraph Output
        save[(Save to DB)]
        notify[Send Notification]
        done([End])
    end

    validate -->|Yes| transform
    validate -->|No| error[Log Error]
    error --> done
    transform --> enrich
    enrich --> save
    save --> notify
    notify --> done
```

**vs Sequence Diagram**: Use flowchart when focus is on process steps; use sequence diagram when focus is on communication between actors.

---

## 2. Sequence Diagram

**Purpose**: Show interactions between components over time.

**When to Use**:
- API call documentation
- Message passing between services
- Request/response flows
- Protocol documentation

**Basic Syntax**:
```mermaid
sequenceDiagram
    Alice->>John: Hello John, how are you?
    loop HealthCheck
        John->>John: Fight against hypochondria
    end
    John-->>Alice: Great!
```

**Arrow Types**:
| Arrow | Description |
|-------|-------------|
| `->` | Solid line without arrow |
| `-->` | Dotted line without arrow |
| `->>` | Solid line with arrow |
| `-->>` | Dotted line with arrow |
| `-x` | Solid line with cross |
| `--x` | Dotted line with cross |
| `-)` | Solid line with open arrow (async) |
| `--)` | Dotted line with open arrow (async) |

**Key Features**:
- Participant declaration and aliases
- Activation/deactivation boxes
- Notes (left, right, over)
- Loops, alternatives, optionals, parallels

**Complete Example**:
```mermaid
sequenceDiagram
    participant Client
    participant API as API Gateway
    participant Auth as Auth Service
    participant DB as Database

    Client->>+API: POST /login
    API->>+Auth: Validate credentials
    Auth->>+DB: Query user
    DB-->>-Auth: User data
    Auth-->>-API: JWT token
    API-->>-Client: 200 OK + token

    Note over Client,API: Subsequent requests include token

    Client->>+API: GET /profile (with token)
    API->>Auth: Verify token
    Auth-->>API: Valid
    API->>+DB: Get profile
    DB-->>-API: Profile data
    API-->>-Client: 200 OK + profile
```

**Control Structures**:
```mermaid
sequenceDiagram
    %% Alternative paths
    alt Successful login
        Client->>Server: Login success
    else Failed login
        Client->>Server: Login failed
    end

    %% Optional
    opt Extra logging
        Server->>Logger: Log event
    end

    %% Parallel
    par Notification
        Server->>Email: Send email
    and
        Server->>SMS: Send SMS
    end
```

---

## 3. State Diagram

**Purpose**: Model state machines, lifecycles, and status transitions.

**When to Use**:
- Object lifecycle documentation
- Workflow states
- UI component states
- Protocol states

**Basic Syntax**:
```mermaid
stateDiagram-v2
    [*] --> Still
    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]
```

**Key Features**:
- Start `[*]` and end `[*]` states
- Composite states (nested)
- Forks and joins
- Notes and descriptions
- Choice pseudostates

**Complete Example**:
```mermaid
stateDiagram-v2
    [*] --> Draft

    Draft --> PendingReview: Submit
    PendingReview --> Draft: Request Changes
    PendingReview --> Approved: Approve

    state Approved {
        [*] --> Scheduled
        Scheduled --> Publishing
        Publishing --> Published
        Published --> [*]
    }

    Approved --> Rejected: Reject
    Rejected --> Draft: Revise
    Approved --> Archived: Archive
    Draft --> Archived: Discard

    Archived --> [*]

    note right of PendingReview
        Requires at least
        2 reviewer approvals
    end note
```

**Composite States**:
```mermaid
stateDiagram-v2
    [*] --> Active

    state Active {
        [*] --> Idle
        Idle --> Processing: Start
        Processing --> Idle: Complete
    }

    Active --> Suspended: Suspend
    Suspended --> Active: Resume
    Active --> [*]: Terminate
```

**vs Flowchart**: Use state diagram when modeling states of a single entity; use flowchart when modeling a process with multiple actors.

---

## 4. Class Diagram

**Purpose**: Document object-oriented design, type relationships, and class structure.

**When to Use**:
- OOP design documentation
- API type hierarchies
- Domain modeling
- Interface documentation

**Basic Syntax**:
```mermaid
classDiagram
    Class01 <|-- AveryLongClass : Cool
    Class01 : size()
    Class01 : int chipiChiworque
    Class01 : equals()
    Class07 : equals()
    Class07 : Object[] elementData
    Class01 "1" --> "0..*" Class07 : contains
```

**Relationship Types**:
| Symbol | Type |
|--------|------|
| `<\|--` | Inheritance |
| `*--` | Composition |
| `o--` | Aggregation |
| `-->` | Association |
| `--` | Link (solid) |
| `..>` | Dependency |
| `..\|>` | Realization |
| `..` | Link (dashed) |

**Cardinality**:
- `"1"` - Exactly one
- `"0..1"` - Zero or one
- `"*"` - Many
- `"1..*"` - One or more
- `"n"` - n instances
- `"0..n"` - Zero to n

**Visibility Modifiers**:
- `+` Public
- `-` Private
- `#` Protected
- `~` Package/Internal

**Complete Example**:
```mermaid
classDiagram
    class User {
        +String id
        +String email
        -String passwordHash
        +Profile profile
        +login(password) bool
        +logout() void
        #hashPassword(plain) String
    }

    class Profile {
        +String displayName
        +String avatarUrl
        +Date createdAt
        +update(data) void
    }

    class Post {
        +String id
        +String title
        +String content
        +User author
        +publish() void
        +archive() void
    }

    class Comment {
        +String id
        +String text
        +User author
        +Post post
    }

    User "1" --> "1" Profile : has
    User "1" --> "0..*" Post : writes
    Post "1" --> "0..*" Comment : has
    User "1" --> "0..*" Comment : writes
```

**Abstract and Interface**:
```mermaid
classDiagram
    class Animal {
        <<abstract>>
        +String name
        +makeSound()* void
    }

    class Serializable {
        <<interface>>
        +serialize() String
        +deserialize(data) void
    }

    class Dog {
        +makeSound() void
        +fetch() void
    }

    Animal <|-- Dog
    Serializable <|.. Dog
```

---

## 5. Entity Relationship Diagram

**Purpose**: Model database schemas and data relationships.

**When to Use**:
- Database design documentation
- Data modeling
- Schema visualization
- Migration planning

**Basic Syntax**:
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER }|..|{ DELIVERY-ADDRESS : uses
```

**Relationship Notation**:
| Left | Right | Meaning |
|------|-------|---------|
| `\|o` | `o\|` | Zero or one |
| `\|\|` | `\|\|` | Exactly one |
| `}o` | `o{` | Zero or more |
| `}\|` | `\|{` | One or more |

**Line Types**:
- `--` Solid (identifying)
- `..` Dashed (non-identifying)

**Complete Example**:
```mermaid
erDiagram
    USER ||--o{ POST : creates
    USER ||--o{ COMMENT : writes
    USER ||--|| PROFILE : has
    POST ||--o{ COMMENT : has
    POST }o--o{ TAG : tagged_with
    CATEGORY ||--o{ POST : contains

    USER {
        uuid id PK
        string email UK
        string password_hash
        datetime created_at
        datetime updated_at
    }

    PROFILE {
        uuid id PK
        uuid user_id FK
        string display_name
        string bio
        string avatar_url
    }

    POST {
        uuid id PK
        uuid author_id FK
        uuid category_id FK
        string title
        text content
        enum status
        datetime published_at
    }

    COMMENT {
        uuid id PK
        uuid post_id FK
        uuid author_id FK
        text content
        datetime created_at
    }

    TAG {
        uuid id PK
        string name UK
        string slug UK
    }

    CATEGORY {
        uuid id PK
        string name
        string slug UK
        uuid parent_id FK
    }
```

**Attribute Types**:
- Include data types after attribute name
- Use `PK` for primary key
- Use `FK` for foreign key
- Use `UK` for unique constraint

---

## 6. Architecture Diagram (C4/Block)

**Purpose**: Visualize system architecture, components, and their interactions.

**When to Use**:
- System design documentation
- Service architecture
- Infrastructure diagrams
- Component relationships

**Using Block Diagram**:
```mermaid
block-beta
    columns 3

    Browser["Web Browser"]
    space
    Mobile["Mobile App"]

    space:3

    block:backend["Backend Services"]:3
        API["API Gateway"]
        Auth["Auth Service"]
        Core["Core Service"]
    end

    space:3

    block:data["Data Layer"]:3
        DB[("PostgreSQL")]
        Cache[("Redis")]
        Queue[("RabbitMQ")]
    end

    Browser --> API
    Mobile --> API
    API --> Auth
    API --> Core
    Core --> DB
    Core --> Cache
    Auth --> Cache
    Core --> Queue
```

**Using Flowchart for Architecture**:
```mermaid
flowchart TB
    subgraph Clients
        web[Web App]
        mobile[Mobile App]
        cli[CLI Tool]
    end

    subgraph Gateway["API Gateway"]
        lb[Load Balancer]
        auth[Auth Middleware]
    end

    subgraph Services
        users[User Service]
        orders[Order Service]
        inventory[Inventory Service]
        notifications[Notification Service]
    end

    subgraph Data
        postgres[(PostgreSQL)]
        redis[(Redis)]
        kafka>Kafka]
    end

    subgraph External
        email[Email Provider]
        payment[Payment Gateway]
    end

    web & mobile & cli --> lb
    lb --> auth
    auth --> users & orders & inventory

    users --> postgres
    orders --> postgres
    inventory --> postgres

    users & orders --> redis
    orders --> kafka
    kafka --> notifications
    notifications --> email
    orders --> payment
```

**Key Architecture Patterns**:

1. **Layered Architecture**:
```mermaid
flowchart TB
    subgraph Presentation
        UI[User Interface]
    end
    subgraph Business
        Logic[Business Logic]
    end
    subgraph Data
        DAL[Data Access Layer]
    end
    subgraph Storage
        DB[(Database)]
    end

    UI --> Logic
    Logic --> DAL
    DAL --> DB
```

2. **Microservices**:
```mermaid
flowchart LR
    subgraph Gateway
        API[API Gateway]
    end

    subgraph Services
        S1[Service A]
        S2[Service B]
        S3[Service C]
    end

    subgraph Messaging
        MQ[Message Queue]
    end

    API --> S1 & S2 & S3
    S1 --> MQ
    MQ --> S2 & S3
```

**vs Other Diagrams**: Use architecture diagrams for high-level system overview; use sequence diagrams for detailed interactions; use class diagrams for code-level design.
