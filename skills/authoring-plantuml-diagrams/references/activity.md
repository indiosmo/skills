# Activity Diagram Reference

Uses the new/beta activity syntax (recommended).

## Basic Activities

Activities are enclosed in `:` and `;`:

```plantuml
start
:First activity;
:Second activity;
stop
```

Use `end` instead of `stop` for an alternative end symbol.

Multi-line and formatting:
```plantuml
:This is on
several lines;
:Use **bold** and //italic//;
```

## Conditionals

```plantuml
if (condition?) then (yes)
  :action A;
elseif (condition B?) then (yes)
  :action B;
else (no)
  :default;
endif
```

### Switch

```plantuml
switch (test?)
case (A)
  :Handle A;
case (B)
  :Handle B;
endswitch
```

## Loops

### While

```plantuml
while (data available?) is (yes)
  :read data;
endwhile (no)
```

### Repeat

```plantuml
repeat
  :process item;
repeat while (more items?) is (yes) not (no)
```

With backward action:
```plantuml
repeat
  :process;
backward :log iteration;
repeat while (more?)
```

### Break

```plantuml
repeat
  :test;
  if (error?) then (yes)
    break
  endif
  :continue;
repeat while (more?)
```

## Fork (Parallel)

```plantuml
fork
  :Task A;
fork again
  :Task B;
fork again
  :Task C;
end fork
```

Use `end merge` to merge without a synchronization bar.

## Swimlanes

```plantuml
|Frontend|
start
:User clicks submit;
|#AntiqueWhite|Backend|
:Validate input;
:Process request;
|Frontend|
:Show result;
stop
```

## Partitions

```plantuml
partition Initialization {
  :Read config;
  :Init variables;
}
partition Processing {
  :Process data;
}
```

## Notes

```plantuml
:Some activity;
note right
  Explanation here
end note

:Another;
note left : short note

floating note left : floating note
```

## Connectors

```plantuml
:Step 1;
(A)
detach
(A)
:Step 2 continues;
```

## Arrow Styling

```plantuml
:Activity 1;
-> label text;
:Activity 2;
-[#blue,dashed]-> styled;
:Activity 3;
```

## Activity Colors

```plantuml
#palegreen:Approved;
#HotPink:Rejected;
```

## Detach

End a flow branch without reaching stop:
```plantuml
fork
  :Action 1;
fork again
  :Action 2;
  detach
end fork
```

## Goto / Label (Experimental)

```plantuml
label retry
:Attempt operation;
if (success?) then (yes)
  stop
endif
goto retry
```
