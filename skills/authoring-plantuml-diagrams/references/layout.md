# Layout Optimization Reference

Techniques for improving visual layout of PlantUML diagrams, organized by scope.

## Universal Techniques

### Global Direction

```plantuml
top to bottom direction   ' default vertical flow
left to right direction   ' horizontal flow -- better for wide architectures, use cases
```

### Spacing

```plantuml
skinparam nodesep 60      ' horizontal spacing between nodes (px)
skinparam ranksep 40      ' vertical spacing between ranks (px)
```

### Line Type

```plantuml
skinparam linetype ortho      ' right-angle connections (can cause label overlap)
skinparam linetype polyline   ' segmented paths
```

### Layout Engines

```plantuml
!pragma layout smetana    ' Java Graphviz port -- straighter arrows
!pragma layout elk         ' Eclipse Layout Kernel -- orthogonal only
' Default: Graphviz dot (no pragma needed)
```

### Arrow Direction Keywords

```plantuml
A -down-> B     ' (or -d->) push B below A
A -up-> B       ' (or -u->) push B above A
A -left-> B     ' (or -l->) push B left of A
A -right-> B    ' (or -r->) push B right of A
```

With `left to right direction`, directions rotate 90 degrees: `-down->` becomes rightward, `-right->` becomes upward.

### Arrow Length

More dashes = more distance between connected nodes:

```plantuml
A -> B        ' short
A --> B       ' medium
A ---> B      ' long
```

### Hidden Links

Invisible edges that influence layout without rendering:

```plantuml
A -[hidden]-> B              ' hidden link
A -[hidden]right-> B         ' directional hidden link
```

### norank Links

Arrow renders but does not affect layout rank:

```plantuml
A -[norank]-> B
```

### together Blocks

Group elements so the layout engine places them close together:

```plantuml
together {
  class Foo
  class Bar
}
```

### Scale

```plantuml
scale 1.5
scale 200 width
scale max 300*200
skinparam dpi 150
```

## Sequence Diagrams

### Participant Ordering

Participants appear left-to-right in declaration order. Override with `order`:

```plantuml
participant "API Gateway" as GW order 10
participant "Auth Service" as Auth order 20
participant "Database" as DB order 30
```

### Vertical Spacing

```plantuml
|||               ' small vertical gap
||45||            ' 45px vertical gap
```

### Horizontal Spacing

```plantuml
skinparam ParticipantPadding 20
```

### Box Grouping

```plantuml
box "Frontend" #LightBlue
  participant Browser
  participant MobileApp
end box
```

### Compact Messages

```plantuml
skinparam responseMessageBelowArrow true
skinparam maxMessageSize 150           ' auto-wrap long text
```

### Hide Footer

```plantuml
hide footbox
```

## Activity Diagrams

### Swimlanes

Swimlanes implicitly organize flow into columns:

```plantuml
|Customer|
:Place order;
|#LightBlue|System|
:Validate order;
```

### Partitions

```plantuml
partition "Authentication" {
  :Enter credentials;
  :Validate token;
}
```

### Vertical If Branches

By default, `elseif` branches spread horizontally. Force vertical:

```plantuml
!pragma useVerticalIf on
```

### Arrow Styling

```plantuml
-[#blue]->            ' colored arrow
-[#green,dashed]->    ' dashed green arrow
```

## State Diagrams

### Arrow Directions (Primary Layout Tool)

Arrow directions are the main way to control state diagram layout. Plan a spatial grid and assign directions explicitly:

```plantuml
[*] -down-> Idle
Idle -down-> Active : start
Active -right-> Paused : pause
Paused -left-> Active : resume
Active -down-> Completed : finish
```

### Composite States for Grouping

```plantuml
state "Connection" as Conn {
  [*] --> Connecting
  Connecting --> Authenticating
  Authenticating --> Ready
}
```

### Concurrent Regions

```plantuml
state Active {
  state "Network" {
    [*] --> Connected
  }
  --
  state "UI" {
    [*] --> Rendering
  }
}
```

## Class Diagrams

### Package Grouping

```plantuml
package "Domain" {
  class Order
  class Customer
}
```

### together Blocks

```plantuml
together {
  class Order
  class OrderLine
}
```

### Link Direction Strategy

Draw links from parent to child (top to bottom). For upward links, reverse the endpoints:

```plantuml
Parent <-- Child    ' keeps Parent above Child
```

### Uniform Width

```plantuml
skinparam minClassWidth 120
skinparam sameClassWidth true
```

## Component / Deployment Diagrams

### Container Types

Use different keywords for different visual shapes: `node`, `cloud`, `database`, `frame`, `folder`, `storage`, `queue`, `stack`, `card`.

### Left-to-Right for Architecture

```plantuml
left to right direction

[Client] --> [API Gateway] --> [Service]
```

### Nesting for Grouping

```plantuml
node "Production" {
  node "Web Server" {
    [Nginx]
    [App]
  }
  database "PostgreSQL"
}
```

## Use Case Diagrams

### Left-to-Right (Recommended)

```plantuml
left to right direction
```

### Rectangle Boundaries

```plantuml
rectangle "System" {
  usecase "Login" as UC1
  usecase "Register" as UC2
}
```

### Actor Placement via Direction

```plantuml
Customer -right-> (Place Order)
(Place Order) <-left- Admin
```
