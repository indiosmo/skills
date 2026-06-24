---
name: writing-python
description: Write, refactor, and review modern Python (target 3.14, support 3.13) the way a careful team would - domain ownership, parse-at-the-boundary validation, exception-first error handling, a functional core with a runtime shell, typed contracts where they clarify, and pytest that encodes intent. Use whenever authoring, changing, or reviewing Python (.py), shaping packages, types, error paths, async or concurrency, or test structure, or when a task mentions pytest, Pydantic, Pandera, uv, Ruff, Pyright, dataclasses, asyncio/anyio, or Dagster. Also generates a self-contained, committed project-local `<project>-python` skill that maps these guidelines onto a specific codebase's packages, helpers, fixtures, commands, and examples - trigger that on requests to "apply these Python guidelines to this repo", "set up the Python skill for this project", or "generate the project Python skill".
---

# Writing Python

The rules below shape the code you would otherwise write in a modern
Python codebase: domain ownership, dependency direction, types and
validation, exception-first error handling, a functional core with a
runtime shell, concurrency and pipelines, layout, testing, debugging,
and comments. Read them before writing or reviewing Python, then reach
for the references when a rule alone is not enough.

## Progressive disclosure

This file is the always-loaded core. Load deeper material on demand:

- [`references/examples.md`](references/examples.md) -- good/bad code
  pairs keyed to the rule sections below. Open it when the rule alone
  is not enough to shape a concrete edit or review a concrete shape.
- [`references/design-principles/`](references/design-principles/),
  [`references/testing-principles/`](references/testing-principles/),
  [`references/debugging-principles/`](references/debugging-principles/),
  [`references/projects-and-tooling/`](references/projects-and-tooling/)
  -- the long-form guides with the full reasoning, worked discussion,
  and fallbacks. Open the design guide for architecture, types, error
  handling, concurrency, pipelines, performance, and dataframes; the
  testing guide for pytest conventions, helpers, and error-path
  coverage; the debugging guide for root-cause tracing and runtime
  diagnostics; the projects-and-tooling guide for layout, uv workflow,
  Ruff, Pyright, and version policy.
- [`references/overview.md`](references/overview.md) -- reading order,
  suite-wide conventions, and recurring themes.

When a project already has a committed `<project>-python` skill (see
[Generate a project-specific skill](#generate-a-project-specific-skill)),
prefer it: it names the concrete packages, helpers, fixtures,
commands, and example files that realize these generic rules in that
codebase.

Before writing code, search for the local abstraction that already
expresses the idea. Prefer project helpers, package conventions, and
command surfaces over new utilities unless the same missing shape
recurs.

## Core Lens

Code is the working theory of the domain. Preserve that theory in
names, package boundaries, types, validation, errors, and tests.
Before adding behavior, ask:

- Which domain owns this concept?
- Which boundary parses untrusted input into domain values?
- Which type or validator carries the proof that the value is valid?
- Which adapter translates between external and local vocabulary?
- Which runtime effect can move outward toward the shell?
- Which invariant must remain true if a middle step fails?

If the answer is unclear, make ownership, inputs, outputs, and failure
modes visible in the signature before adding more behavior.

## Project Layout

Use the project's existing layout. The common shape is a root
`pyproject.toml` and `uv.lock`, package code under `src/`, tests under
`tests/`, benchmarks under `benchmarks/`, and infrastructure outside
importable package trees. Reusable libraries, applications,
orchestration code, and data pipelines live in packages whose names
describe the domain or layer they own.

Avoid generic package names such as `common`, `shared`, `helpers`, and
`utils` for core concepts. Use practitioner vocabulary such as
`market_data`, `portfolio_rebalance`, `specimen_processing`,
`shipment_routing`, or `audio_rendering` when those are the real
domains.

## Domain Ownership

Domain packages own vocabulary, values, invariants, errors, and public
contracts. Adapter packages translate vendor SDKs, wire formats,
database rows, CLI inputs, queue messages, UI inputs, and dataframe
schemas into domain values. Application and orchestration packages own
settings, logging configuration, event loops, worker pools, database
sessions, schedulers, and framework entry points.

Keep import arrows acyclic. When two packages need the same concept,
move that concept to a named package both can import. Peers do not
reach into each other; an adapter or a shared package mediates.

## Types And Validation

Use type annotations where they clarify stable contracts: public APIs,
domain values, adapters after parsing, settings, reusable helpers,
fixtures, fakes, and dataframe boundary objects. Keep dynamic Python
where runtime validation or native dataframe operations are clearer
than elaborate static types.

Parse hostile input at boundaries. Use Pydantic v2 for JSON, CLI,
environment, config, queue, and cross-process shapes. Use Pandera for
dataframe schemas. Use frozen slotted dataclasses for internal values
built from validated parts. Use `NewType` or small validated classes
when primitive identity matters. Inside the domain, trust the refined
types; re-parse only when data re-enters from an untyped source.

Let `Any` stop at adapters. Use `object` when a value is unknown and
only runtime checks permit operations. Use `cast` only after a nearby
runtime check, a trusted library contract, or a named invariant.

## Functional Core And Runtime Shell

Domain functions accept values and return values. Runtime code reads
environment variables, opens files, configures logging, creates
clients, starts workers, and calls framework APIs. Framework routes,
CLI commands, Dagster assets, scheduled jobs, and UI handlers
translate framework inputs to domain values, call the core, and
translate the result back.

This is the most important design pressure in the guide. The core
expresses domain rules over plain values; the shell decides where
inputs come from, which concrete services are installed, and which
task or worker runs each consumer. A domain function that reads the
environment, opens a socket, constructs its own concrete client, or
knows its downstream consumer has pulled runtime composition into the
domain.

Use explicit parameters for domain-specific collaborators such as
repositories, pricing clients, carriers, or codecs. Use context-local
facades for truly cross-cutting services such as logger, clock,
settings, tracing context, and timers when scoped overrides are
useful.

## Error Handling

Python code is exception-first. Use built-in exceptions when the name
communicates the failure. Add small custom domain exceptions when
callers need to distinguish a meaningful failure class, when
structured attributes support logging or tests, or when a boundary
needs a stable translation target.

Translate failures at HTTP, CLI, job, queue, worker, event-loop, and
UI boundaries into the caller's vocabulary: HTTP responses, CLI exit
codes, job states, queue behavior, or UI messages. Use exception
chaining (`raise ... from ...`) when adding context. Use
`ExceptionGroup` and `except*` for grouped concurrent failures. Use
warnings for recoverable conditions that callers may escalate. Use
sentinel values when absence is the normal API contract.

Result-shaped values fit bulk item status, best-effort partial
processing, and serialized per-item outcomes. Exceptions remain the
default failure channel.

## Invariants And Rollback

Put invariant ownership with the object, package, transaction, or
pipeline stage that can maintain it. Build new state in locals and
commit at the end when possible. Use context managers, `ExitStack`,
database transactions, atomic file replacement, idempotency keys,
durable markers, and compensating actions for effects that must remain
coherent.

Tests for rollback assert the observable state after failure, not only
the raised exception.

## Concurrency And Pipelines

Runtime ownership belongs near the entry point. Use
`asyncio.TaskGroup` for structured async work. Use anyio when cancel
scopes, timeout composition, or trio compatibility earn the
dependency. Use queues to cross ownership boundaries. Keep shared
mutable state owned by one task, thread, process, or object.

Pipeline stages expose explicit inputs and outputs. Use callbacks,
queues, async channels, Dagster assets, dbt models, or graph tools
when the graph shape has operational meaning. Keep runtime wiring
close to the shell, where the topology is visible in one place.

## Testing

Tests assert behavior through independent evidence from the domain,
contract, specification, bug report, or public example. Do not derive
the expected value from the implementation under test; that only
proves the code does what the code does. Tests fail for plausible
defects and stay readable as examples of the intended behavior.

Use pytest. Prefer clear test names, direct assertions, parametrization
with meaningful `ids`, domain factories, fixture factories, dataframe
builders, fakes that implement protocols, and condition-based waits.
Drive the domain surface with values and capture observable outputs;
keep benchmarks out of the normal correctness loop.

For bug fixes, reproduce the failure, write or tighten the regression
test that fails for the observed bug and passes for the intended
behavior, then fix the production cause.

## Debugging

Do not patch symptoms. Reproduce the failure, read the whole traceback
or diagnostic output, trace the bad value or state backward to where
it originated, state one hypothesis, run one focused experiment, write
the regression test, and fix the origin.

Use logs, probes, `pytest -k`, warning escalation, Pyright, Ruff,
Python development mode, asyncio debug mode, `faulthandler`,
`tracemalloc`, memray, and py-spy as evidence sources. Compare the
broken path against a nearby working path before inventing a new
pattern. When a fix attempt fails, treat that as new evidence and
return to investigation instead of stacking another guess on top.

Once the root cause is understood, ask what type, parser, boundary
validation, assertion, context manager, or error path would make the
bug class harder to reintroduce.

## Comments And Docs

Write comments and docstrings in present tense. Explain what the code
does and why the why is non-obvious. Prefer positive statements about
current behavior. Delete refactor notes, history notes, commented-out
code, and lists of absent responsibilities.

Use comments for non-obvious grouping, invariants, preconditions,
algorithmic rationale, or domain rules. If a precondition matters,
phrase it as the invariant the code relies on, not as a chore the
caller has been assigned. Keep field-level and variable documentation
close to the code that defines the field or variable.

## Tooling

Use the repository command surface. The default shape is:

```sh
uv sync
uv run ruff format .
uv run ruff check .
uv run pyright
uv run pytest
```

Run the narrowest useful command while editing, then run the broader
command that verifies the changed surface before calling the work
complete.

## Generate a project-specific skill

These rules stay generic on purpose. To pin them to a real codebase,
generate a committed, self-contained `<project>-python` skill that maps
the generic vocabulary onto the project's actual packages, helpers,
fixtures, commands, and example files, and updates the project's agent
entry docs (AGENTS.md / CLAUDE.md) to point at it.

Trigger this on requests such as "apply these Python guidelines to
this repo", "set up the Python skill for this project", or "generate
the project Python skill". Follow the full procedure in
[`references/generate-project-skill.md`](references/generate-project-skill.md).
