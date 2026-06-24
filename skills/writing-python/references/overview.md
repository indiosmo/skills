# Modern Python guides

The long-form reference behind the `writing-python` skill. These guides
describe how to shape projects and components, test behavior, and
investigate failures without burying the domain model under incidental
framework or tooling mechanics. They target systems where boundaries,
error paths, concurrency, and testability matter more than isolated
language tricks.

[`../SKILL.md`](../SKILL.md) carries the condensed always-loaded rules.
Read these guides when the rule alone is not enough and you want the
full reasoning, the fallbacks, and the worked discussion behind a
section.

## Reading order

The guides are siblings, not a strict sequence. Start where your task
starts: project setup, component design, writing or repairing tests, or
investigating a bug. When reading broadly, start with the project and
design guides because the testing and debugging guides reuse their
vocabulary.

| Guide | Use it when |
|-------|-------------|
| [`projects-and-tooling/`](projects-and-tooling/) | Setting up repository layout, the uv workflow, Ruff, Pyright, version policy, or the typing stack. |
| [`design-principles/`](design-principles/) | Shaping architecture, types and validation, error handling, invariants, concurrency, pipelines, performance, or dataframes. |
| [`testing-principles/`](testing-principles/) | Writing pytest conventions, encoding test intent, factoring helpers, covering error paths, waiting on conditions, or running approval tests. |
| [`debugging-principles/`](debugging-principles/) | Tracing a failure to its root cause, adding defense in depth, instrumenting logging, applying static analysis, or reading runtime diagnostics. |
| [`examples.md`](examples.md) | Comparing good and bad code pairs keyed to the SKILL.md rule sections. |

## Applying the guides to a project

These guides stay generic: they speak in practitioner vocabulary and
never name a specific codebase. To pin them to a real project, run the
project-skill generator documented in
[`generate-project-skill.md`](generate-project-skill.md). It reads the
target codebase and emits a self-contained, committed `<project>-python`
skill that maps the generic vocabulary onto the project's actual
packages, helpers, fixtures, commands, and example files, and updates
the project's agent entry docs. The generated skill embeds its own
reference docs, so the project depends on neither a submodule nor on the
`writing-python` skill being installed.

## Conventions

Examples target Python 3.14 for new projects. Projects that support
Python 3.13 keep that support visible in package metadata, CI, and
examples.

Code fences use `python`, `toml`, `yaml`, `sh`, or `text` as
appropriate. Examples use practitioner vocabulary and explicit names
rather than generic helpers.

## Themes

A handful of ideas recur across the guide set:

- **Domain ownership.** Domain packages own their vocabulary,
  invariants, errors, and public contracts.
- **Adapters at boundaries.** Adapters translate external shapes into
  domain values at the boundary, so the domain core works in its own
  types.
- **Runtime shells own effects.** Runtime shells own files, sockets,
  settings, event loops, workers, schedulers, logging configuration, and
  framework entry points, leaving inner layers to work in plain values.
- **Typing names contracts, validation guards boundaries.** Static
  typing names stable contracts; runtime validation protects hostile or
  shape-rich boundaries.
- **Exception-first with boundary translation.** Python code is
  exception-first. Boundaries translate failures into HTTP responses,
  CLI exit codes, job states, queue behavior, or UI messages.
- **Tests encode intent.** Tests assert behavior through independent
  oracles and deterministic data, so a passing test reflects the domain
  rather than a re-run of the implementation.
- **Debugging traces values to their origin.** Debugging starts with the
  exact symptom and traces bad values back to their origin before
  changing production code.
