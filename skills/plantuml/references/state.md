# State Diagram Reference

## Declaring States

Declare states upfront for readability:

```plantuml
state Idle
state Running
state Stopped
state "Long Name" as LN
```

With description lines (entry/do/exit actions):
```plantuml
Running : on_entry / start_timer()
Running : do / process()
Running : on_exit / cleanup()
```

## Start and End

```plantuml
[*] --> Idle        ' start pseudostate
Stopped --> [*]     ' end pseudostate
```

## Transitions

```plantuml
Idle --> Running : start
Running --> Stopped : Event [guard] / action
Running -left-> Paused : pause    ' directional arrow
```

Direction hints: `-up->`, `-down->`, `-left->`, `-right->` (or short form `-u->`, `-d->`, `-l->`, `-r->`).

## Composite / Nested States

```plantuml
state Active {
  [*] --> Running
  Running --> Paused : pause
  Paused --> Running : resume
}

Idle --> Active : start
Active --> Idle : stop
```

Deeper nesting:
```plantuml
state Active {
  state Running {
    [*] --> Processing
    Processing --> Waiting : yield
    Waiting --> Processing : resume
  }
}
```

## Concurrent Regions

Horizontal separator `--` stacks regions vertically:

```plantuml
state Active {
  [*] --> NumLockOff
  NumLockOff --> NumLockOn : toggle
  NumLockOn --> NumLockOff : toggle
  --
  [*] --> CapsLockOff
  CapsLockOff --> CapsLockOn : toggle
  CapsLockOn --> CapsLockOff : toggle
}
```

## Fork / Join

```plantuml
state fork_state <<fork>>
state join_state <<join>>

[*] --> fork_state
fork_state --> TaskA
fork_state --> TaskB

TaskA --> join_state
TaskB --> join_state
join_state --> Done
```

## Choice Pseudostate

```plantuml
state choice <<choice>>
Idle --> choice
choice --> SmallPath : [size < 10]
choice --> LargePath : [size >= 10]
```

## Entry / Exit Points

```plantuml
state Module {
  state ep <<entryPoint>>
  state ex <<exitPoint>>
  ep --> Internal
  Internal --> ex
}

[*] --> ep
ex --> [*]
```

## History

```plantuml
state component {
  [*] --> A
  A --> B : next
  state h <<history>>
}
Outside --> h : restore
```

Deep history: `<<history*>>`

## Notes

```plantuml
state Foo
note left of Foo : short note

note right of Bar
  multi-line
  note
end note

Foo --> Bar
note on link
  transition note
end note
```

## Hide Empty Description

Makes states compact (no description area shown):
```plantuml
hide empty description
```

## Inline Styling

```plantuml
state Error #FFaaaa
state Active #palegreen;line:green;text:green
```
