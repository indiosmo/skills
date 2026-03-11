# Layout Optimization Reference

Techniques for improving visual layout of PlantUML diagrams, organized by scope.

## Contents

- [Universal Techniques](#universal-techniques) -- direction, spacing, line type, layout engines, arrow control, hidden/norank links, together blocks, scale
- [Sequence Diagrams](#sequence-diagrams) -- participant ordering, vertical/horizontal spacing, box grouping, compact messages
- [Activity Diagrams](#activity-diagrams) -- swimlanes, partitions, vertical if branches, arrow styling
- [State Diagrams](#state-diagrams) -- arrow directions, composite states, concurrent regions

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

