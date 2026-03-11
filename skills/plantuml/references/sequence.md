# Sequence Diagram Reference

## Participants

Declare participants upfront to control ordering:

```plantuml
participant Alice
participant Bob
actor User
database DB #LightBlue
participant "Long Name" as LN
```

Types: `participant`, `actor`, `boundary`, `control`, `entity`, `database`, `collections`, `queue`.

Order override: `participant Alice order 10`

Group participants:
```plantuml
box "Backend" #LightYellow
  participant API
  participant Worker
end box
```

## Messages

```plantuml
Alice -> Bob   : synchronous (solid, filled arrow)
Alice --> Bob  : return / response (dashed)
Alice ->> Bob  : async (thin/open arrow)
Alice ->x Bob  : lost message
Alice <-> Bob  : bidirectional
```

Self-message:
```plantuml
Alice -> Alice : internal call
```

### Coloring arrows

```plantuml
Alice -[#red]> Bob : urgent
Alice -[#blue,dashed]-> Bob : optional
```

## Numbering

```plantuml
autonumber
autonumber 10 5          ' start at 10, increment 5
autonumber "<b>[000]"    ' formatted
autonumber stop           ' pause
autonumber resume         ' resume
```

## Activation / Deactivation

Explicit:
```plantuml
Alice -> Bob : request
activate Bob
Bob --> Alice : response
deactivate Bob
```

Shortcut:
```plantuml
Alice -> Bob++ : request      ' activate
Bob --> Alice-- : response    ' deactivate
Alice -> Bob** : create
Alice -> Bob!! : destroy
```

Return shorthand:
```plantuml
activate Bob
Alice -> Bob : request
return response
```

## Grouping

```plantuml
alt Success
  Bob -> Alice : 200
else Failure
  Bob -> Alice : 500
end

opt Optional
  Alice -> Log : write
end

loop 1000 times
  Alice -> Bob : ping
end

par
  Alice -> Bob : task A
else
  Alice -> Carol : task B
end

break Emergency
  Alice -> Bob : abort
end

group Custom [label]
  Alice -> Bob : message
end
```

## Notes

```plantuml
note left of Alice : short note
note right of Bob
  multi-line
  note
end note
note over Alice, Bob : spanning note
note across : all participants
```

## Dividers and Delays

```plantuml
== Section Title ==
...
...5 minutes later...
|||                  ' extra space
||45||               ' 45px space
```

## Incoming / Outgoing

```plantuml
[-> Alice : from outside
Alice ->] : to outside
```

## Hide Footbox

```plantuml
hide footbox
```

## Reference

```plantuml
ref over Alice, Bob : See other diagram
```
