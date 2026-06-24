# Modern C++ guides

The long-form reference behind the `writing-cpp` skill. These guides
describe how to shape components, test behavior, and investigate
failures without burying the domain model in incidental mechanics. They
target systems where ownership boundaries, error paths, threading, and
testability matter more than isolated language tricks.

[`../SKILL.md`](../SKILL.md) carries the condensed always-loaded rules.
Read these guides when the rule alone is not enough and you want the
full reasoning, the fallbacks for older standards, and the worked
discussion behind a section.

## Reading order

The guides are siblings, not a strict sequence. Start where your task
starts: designing a component, writing or repairing tests, or
investigating a bug. When reading broadly, start with the design guide
because the testing and debugging guides reuse its vocabulary.

| Guide | Purpose |
|-------|---------|
| [`design-principles/`](design-principles/) | Architecture, types, error handling, performance. |
| [`testing-principles/`](testing-principles/) | Test intent, Catch2 conventions, error-path coverage. |
| [`debugging-principles/`](debugging-principles/) | Root-cause investigation and structural prevention. |
| [`examples.md`](examples.md) | Good/bad code pairs keyed to the skill's rule sections. |

## Applying the guides to a project

These guides stay generic: they speak in a `lib::` placeholder
namespace and never name a specific codebase. To pin them to a real
project, run the project-skill generator documented in
[`generate-project-skill.md`](generate-project-skill.md). It reads the
target codebase and emits a self-contained, committed `<project>-cpp`
skill that maps every placeholder onto the project's actual headers,
macros, scripts, and example files. The generated skill embeds its own
reference docs, so the project depends on neither a submodule nor on
the `writing-cpp` skill being installed.

## Conventions

Examples use C++26 unless a section says otherwise; the relevant guide
notes drop-in alternatives for C++20 and C++23, and flags the few
features (for example `std::start_lifetime_as`) that have no clean
older-standard equivalent.

Code fences use `cpp` for C++ snippets, examples use `snake_case`
identifiers, and prose uses US English. Catch2 includes use angle brackets.

Use blank lines where they make phases inside C++ examples easier to scan. They
are usually helpful between setup and a loop, after a multi-line control block
before the next independent statement, between non-trivial `switch` case groups,
and before a final `return` that follows a loop or branch. Keep tightly coupled
statements adjacent: assign-and-test pairs, a lookup and the `if` that checks
it, and guard bodies with a log and early `return`. Small helpers that set or
mutate one value and return it can stay compact.

Throughout these guides, `lib::` is a placeholder namespace for small in-house
utilities. Substitute the namespace your codebase uses. The examples rely on a
few recurring helpers:

- `lib::result<T>`: the in-domain result type, treated here as the project
  alias for `boost::leaf::result<T>`.
- `std::expected<T, E>`: the boundary result type when callers must see the
  error value in the signature.
- `lib::scope_exit`: a scope guard for rollback and cleanup.
- `lib::inplace_function`: a fixed-capacity callable wrapper.
- `lib::match` and `lib::match_partial`: variant visitation helpers.
- `lib::error` and `lib::new_error`: structured error construction.

## Themes

A handful of ideas recur across the three guides:

- **Domain ownership.** Each component owns its types, errors, and
  invariants. Cross-domain communication happens through adapters that
  translate at the boundary, never through types shared and mutated across
  component boundaries.
- **Types carry the proof.** A well-typed value is, by construction, a valid
  one. Validation happens once at the parser; downstream code receives refined
  types and trusts them.
- **Push effects to the edge.** The functional core stays free of I/O, threads,
  and timers. The imperative shell composes the pure pieces with the
  surrounding side effects. Inner layers therefore test with plain values.
- **Tests encode intent.** Expected values come from the domain, specification,
  contract, or bug report, not from re-running the implementation. A useful
  test fails for a plausible defect and stays readable enough to serve as a
  behavioral example.
- **Compile-time checks where possible, runtime checks where not.**
  Strong types, exhaustive switches, and designated initializers push
  validation into the compiler. Properties the type system cannot express,
  such as state-dependent invariants, fall back to runtime checks.
- **Code encodes a shared model.** The guides aim to keep that model legible
  and refactorable as the team's understanding of the domain evolves.
