---
name: index-cpp-codebase
description: >-
  Generate or incrementally update an INDEX.md navigation map for a C++ /
  CMake codebase -- a structured map of where things live, with per-module
  summaries and per-header descriptions grounded in actual code. Use this
  skill whenever the user asks to "create an INDEX.md", "index this
  codebase", "generate a navigation map", "produce a map of the repo for
  agents", "build an AI-friendly project index", "update the index",
  "refresh INDEX.md", "what changed since the index was last updated", or
  wants a fresh INDEX.md after substantial structural changes (modules
  added, renamed, restructured). Also use it when the user says "where do
  things live in this project", "give me an orientation map", "summarize
  this C++ project's layout for an agent". Triggers on: INDEX.md, project
  index, codebase index, navigation map, AI-readable project map, module
  map, where things live, orient an agent, update the index, refresh
  index, index changes, what changed in the index. Works on C++/CMake
  projects only. Produces INDEX.md plus a companion INDEX-report.md that
  surfaces ambiguities, README/code conflicts, and (in update mode) the
  changes that drove the partial regeneration.
license: MIT
---

# Index a C++ Codebase

Walk a C++ / CMake codebase and produce a single `INDEX.md` at the project
root: a navigation map for AI agents (and humans) that points to *where
things live*, with enough context per file that a reader can pick the right
one without opening five wrong ones first.

The skill also writes a sibling `INDEX-report.md` that captures everything
the run noticed but deliberately left out of the index -- ambiguities,
README/code conflicts, headers with no includers, files the run could not
parse. The report is for the user; the index is for downstream agents.

## What this skill is for

The index is a **map**. It is not the rulebook, not the design doc, not the
architecture narrative. Conventions belong in `AGENTS.md`, rationale in
`DESIGN.md` / ADRs, per-module context in module READMEs. The skill must
not invent any of those. It must not restate them either: one source of
truth per concern. The index points at headers and modules; everything
else lives where it already lives.

Scope:

- **C++ only. CMake-based projects only.** Non-C++ trees (Python tooling,
  scripts, generated artefacts) are ignored.
- **One language per run.** Multi-language repos are out of scope.
- **Headers only in the file list.** Implementation files (`.cpp`, `.cc`,
  `.cxx`) are read for grounding during discovery but never listed.

## When to (re)run

`INDEX.md` is living documentation. Regenerate it when a structural change
in the session would make the index drift:

- A header is added, removed, renamed, or moved.
- A header's intent or central role changes substantially (a thin wrapper
  grows into the main API; a module's entry point shifts).
- A module is added, removed, renamed, or restructured.
- The directory tree gains or loses a top-level subtree.

Trivial changes (renaming a parameter, fixing a typo, adding a private
helper) do not trigger an update. When in doubt, update -- a stale index
is worse than a touched-too-often one.

## Modes

The skill runs in one of three modes. Pick the mode from the user's
prompt and the state of the project:

| Mode | When to use | What it does |
|------|-------------|--------------|
| **Full** | No `INDEX.md` exists at the project root, or the user explicitly asks to "regenerate" / "rewrite" / "create from scratch". | Runs every phase end-to-end. Writes a brand-new `INDEX.md` and `INDEX-report.md`. |
| **Scoped** | The user names one or more modules ("re-index just `<module>`", "update the `<module>` section"). | Runs discovery + drafting on the named modules only. Splices their sections into the existing `INDEX.md`. Leaves sections 1-3 alone unless the directory tree changed. |
| **Incremental** | `INDEX.md` already exists at the project root and the user asks to "update", "refresh", "rerun", or "see what changed". | Uses git to find files changed since `INDEX.md` was last committed, derives the set of affected modules, and runs the scoped mode against them. Also produces a *changes report* so the user can see what drove the update. |

Mode selection precedence: explicit user instruction > project state. If
the user says "regenerate from scratch" even though `INDEX.md` exists,
honour the instruction and run Full mode.

Inputs:

- **Full mode**: no required arguments. Run from the project root.
- **Scoped mode**: one or more module names (or paths). The skill
  resolves them against the detected module list.
- **Incremental mode**: no required arguments. The skill discovers the
  scope from git. Optional: an explicit baseline commit / tag to diff
  against if the user wants a different anchor than "last commit that
  touched `INDEX.md`".

---

## Workflow

Five phases, in order: preflight, detection, discovery, drafting,
verification. Everything important from every phase is written to an
on-disk working folder so the run is auditable after the fact.

### Phase 0: Working folder

At the start of every run, create a working folder under `/tmp` and use
it as the spine of phase-to-phase communication. Subagent return messages
compress what the agent learned; the on-disk files are the source of
truth.

Path: `/tmp/index-cpp-codebase-<YYYYMMDD-HHMMSS>-<short-id>/`

Layout:

```
/tmp/index-cpp-codebase-<run-id>/
|-- manifest.md                  skill name, start time, args, project root, mode
|-- run.log                      timestamped append-only log of phase events
|-- preflight.md                 preflight checks + their results
|-- consumer-map.json            cross-module includer edges (built once up front)
|-- changes-since-index.md       (incremental mode only) git diff summary + affected modules
|-- discovery/
|   |-- <module>.md              per-module discovery output
|   `-- <module>.tests.md        nested test-intent summaries
|-- drafting/
|   `-- <module>.md              per-module draft of the INDEX section
`-- report-fragments/
    `-- <module>.md              per-module findings for the companion report
```

Rules:

- **Every phase writes its full output to the folder.** Nothing important
  lives only in a subagent return message.
- **Every subagent prompt names the working folder path and the exact
  file the subagent must write to.** Subagents do not pick their own
  paths -- this thread decides the layout so assembly stays a predictable
  glob.
- **File naming is flat and predictable** -- `<module>.md`,
  `<module>.tests.md`, etc. Nested subagents follow the same conventions
  so their parent can find their output without threading paths back
  through messages.
- **The folder is not cleaned on completion.** It survives the run for
  debugging; `/tmp` self-cleans on a system schedule.
- **Final artifacts go to the project root**, not the working folder.
  `INDEX.md` and `INDEX-report.md` live in the repo.
- **`run.log` is append-only.** Each phase logs its start and end with a
  timestamp so a post-mortem can see where the run spent time.

When the skill produces a wrong description, the working folder is the
audit trail: open `discovery/<module>.md` and see exactly what the
subagent had in front of it before it wrote the line.

### Phase 1: Preflight

Verify the environment before doing any indexing work:

- A `CMakeLists.txt` exists at the project root.
- `clangd` is on `PATH`.
- A `compile_commands.json` exists where the project's build presets put
  it (typically `_build/<preset>/` or a top-level symlink).
- The `compile_commands.json` was generated within the last 60 seconds.

If any check fails, stop and tell the user exactly what to do (run the
project's build command to regenerate `compile_commands.json`, install
clangd, fix the missing root marker). **Do not fall back to grep-only
mode.** The structural information clangd provides is load-bearing for
accurate descriptions and visibility tags. A "best effort" index without
it is worse than no index, because downstream agents will trust it.

Write the preflight result to `preflight.md` and append a line to
`run.log`.

### Phase 2: Detection

- **Modules** are subdirectories of `src/` (or whatever layout the
  project's ADRs / `AGENTS.md` specify). A common convention is that
  each module's headers live under `<module>/<module>/`; treat whatever
  directory matches that pattern as the header root for the module.
- **Test root** (`test/`) and **vendored trees** (`libs/`,
  `third_party/`, `vendor/`) are located but not recursed into -- they
  get one line in the directory tree.
- **Build / generated directories** (`_build/`, `build/`,
  `cmake-build-*/`) are skipped entirely. Mention once in a "skipped"
  footnote if their presence is worth knowing.

Headers (`.hpp`, `.h`) are the files of interest. Implementation files
(`.cpp`, `.cc`, `.cxx`) are read for context during discovery but never
listed.

Before dispatching discovery, run **one pre-pass** in this thread: sweep
`#include "..."` edges across the repo, produce a consumer map keyed by
header, and write it to `consumer-map.json`. The map is small (edges
only) so it fits even when the source itself does not. Each discovery
subagent receives the slice of the map that touches its module.

### Phase 3: Discovery (parallelized)

This phase is parallelizable and **should** be parallelized in any project
large enough that the full source set doesn't fit a single context
window. Use the `dispatching-parallel-agents` skill: one subagent per
module, each doing its own discovery + drafting end to end. Dispatch all
subagents in a single message so they run concurrently.

For each module the subagent:

1. **Reads context READMEs in widening rings** -- any parent README
   (project root, `src/README.md` if it exists), the module's own README,
   every README nested under the module. This places the module inside
   the system before drilling into files.
2. **Gathers test-intent context.** Tests show the module's public API in
   representative use: which entry points matter, which combinations are
   exercised, which edge cases the authors thought worth pinning. The
   discovery subagent **does not** read raw test files itself -- a
   module's test directory can run to thousands of lines and would swamp
   its context window. Instead it dispatches a **nested subagent** whose
   only job is to produce a short intent-summary of the module's tests
   and write it to `discovery/<module>.tests.md`. The discovery subagent
   then reads that summary and uses it as input for per-header
   descriptions.
3. **Enumerates headers in the module** (git-tracked only).
4. **For each header, collects:**
   - The file's top-of-file comment.
   - The declared symbols (types, free functions, constants) via
     clangd / LSP.
   - The corresponding implementation file(s), **read in full for
     grounding** -- descriptions must reflect what the code actually
     does, not what the header declares.
   - The cross-module includer list, from the consumer-map slice this
     thread supplied.
   - A visibility tag (`P` / `I`) inferred from where the includers live:
     external includers -> `(P)`; module-only includers -> `(I)`;
     ambiguous -> `(P)` per the bias rule below.

Each subagent writes its full discovery output to
`discovery/<module>.md` and its drafted INDEX section to
`drafting/<module>.md`, plus any findings to
`report-fragments/<module>.md`.

### Phase 4: Drafting and assembly

Each subagent produces its module's section in the exact format specified
under "Output format" below. Writing follows the project's documentation
conventions: subagents should consult the `documentation` skill for
structure and section choices, and `writing-clearly-and-concisely` for
prose-level conventions (active voice, no hedging, no filler).

When all subagents complete, this thread assembles `INDEX.md`:

1. System overview, tech stack, directory tree (sections 1-3).
2. Module sections in a **stable, dependency-aware order**: shared /
   utility libraries first, then leaf domains, then composition domains,
   then runtime / application shells. This matches the natural dependency
   order and the order a new reader would want.
3. Write `INDEX.md` to the project root.

This thread also assembles `INDEX-report.md` from `report-fragments/*.md`.

### Phase 5: Verification

Before declaring done:

- Every file path in `INDEX.md` resolves to a real file (`test -f` each
  one).
- Every module listed in section 4 corresponds to a real directory.
- The directory tree in section 3 matches the actual top-level layout
  (`tree -d -L 2` diff).
- No section is empty.

If verification fails, stop and report. Do not hand-wave or skip the
failure -- the index is consumed as ground truth by downstream agents.

---

## Incremental mode details

Incremental mode is a scoped run whose scope is computed from git. It
exists because re-indexing a large codebase from scratch on every
structural change is wasteful: most modules did not change, and
regenerating their sections risks gratuitous churn in descriptions that
were already accurate. The git diff is the source of truth for "what
might be stale."

### Preconditions

- The project is a git repository.
- `INDEX.md` exists at the project root and is tracked by git.
- The working tree is in a reasonable state (no unresolved merge
  conflicts in the files we want to read).

If `INDEX.md` exists but is untracked or uncommitted, the skill cannot
locate a baseline. Stop and tell the user: "INDEX.md is uncommitted; I
can't compute a diff. Commit it (or pass an explicit baseline), or rerun
with full-mode regeneration." Do not silently fall back -- the user
asked for an incremental update; surface the prerequisite.

### Computing the change set

1. **Resolve the baseline commit**:
   ```
   git log -1 --format=%H -- INDEX.md
   ```
   If the user supplied an explicit baseline (commit, tag, or ref), use
   it instead.
2. **Collect committed changes** between baseline and `HEAD`:
   ```
   git diff --name-status <baseline> HEAD -- <project-source-paths>
   ```
3. **Collect working-tree changes** since `HEAD` (unstaged + staged):
   ```
   git status --porcelain -- <project-source-paths>
   ```
4. **Union** the two sets. Each entry has a path and a status
   (`A`/`M`/`D`/`R`).

Filter to the file kinds the index depends on:

- **Headers** (`.hpp`, `.h`): direct -- they appear in the file list. An
  add/remove/rename/modify flags the owning module.
- **Implementation** (`.cpp`, `.cc`, `.cxx`): indirect -- they ground
  descriptions. A modified `.cpp` flags its matching header for a
  description refresh, even if the header is unchanged.
- **`CMakeLists.txt`**, **`CMakePresets.json`**, top-level
  `vcpkg.json` / `conanfile.txt`: structural -- changes here may shift
  the tech stack section. Flag section 2 for refresh.
- **READMEs**: any `README.md` under `src/` or a module root -- changes
  here may shift a module's summary. Flag the owning module.
- **Top-level directory adds/removes** under `src/`: flag section 3
  (directory tree) for refresh; a new directory may be a new module
  that needs its own section.

Everything else (docs, tests, scripts, generated files) is irrelevant
to the index and is ignored.

### Mapping files to modules

Walk up from each changed file to the nearest module root (the
`<module>/` directory directly under `src/`). The set of affected
modules is the union. Headers in vendored / `third_party/` trees are
ignored -- those aren't indexed.

### The changes report

Before running discovery, write the report to
`changes-since-index.md` in the working folder. Group by category, then
by module:

```
# Changes since INDEX.md was last updated

Baseline: <commit-sha> (<short subject>, <author date>)
Current:  HEAD + working tree

## Modules with structural changes (file added / removed / renamed)

### <module>

- A submission/src/<module>/<module>/new_header.hpp
- D submission/src/<module>/<module>/old_header.hpp
- R submission/src/<module>/<module>/{old => new}.hpp

## Modules with description-impacting changes (implementation or README)

### <module>

- M submission/src/<module>/src/foo.cpp        -- flagged foo.hpp for refresh
- M submission/src/<module>/README.md          -- module summary may shift

## Top-level structural changes

- A submission/src/<new-module>/                -- new module; needs a section
- (none for `src/` removals)

## Tech-stack-impacting changes

- M CMakeLists.txt                              -- new `find_package(...)`
- (none)

## Affected modules (final scope)

- <module-a>
- <module-b>
```

Print the *Affected modules* list back to the user in the chat message
that follows discovery dispatch, so they know what got re-run before
the new INDEX.md lands.

### Update strategy

Once the change set is computed:

1. **If only existing modules are affected**: run discovery + drafting
   on each affected module, then splice the resulting sections into the
   existing `INDEX.md`. Replace the old section for each affected
   module; leave every other module's section byte-for-byte alone.
2. **If a new module appeared**: run discovery on it as if in full
   mode, then insert its section in the right place in the dependency-
   aware order. Also re-derive section 3 (directory tree) to include
   it.
3. **If a module disappeared**: drop its section from `INDEX.md` and
   re-derive section 3.
4. **If tech-stack-impacting files changed**: re-derive section 2 from
   the current `CMakeLists.txt` and other manifests. Diff against the
   old section 2 and record any added / removed dependencies in
   `INDEX-report.md`.
5. **Section 1 (system overview) is sticky**: never auto-rewrite it in
   incremental mode. If the user wants the overview refreshed, they
   ask for a Full run. The overview is short, opinionated, and
   sensitive to phrasing -- re-deriving it on every nudge would churn
   wording for no gain.

### Updating INDEX-report.md

Append a `## Changes since last index` section to `INDEX-report.md`
containing the changes report from above. Keep prior content (the
ambiguities / inconsistencies / decisions from earlier runs) -- the
report is a running log, not a snapshot. If a previous "Changes since
last index" section exists, replace it with the new one; the latest
update only needs the most recent diff.

### Verification (incremental)

The standard verification still applies, plus:

- Every module that was *not* in the affected set must have an
  identical section in the new `INDEX.md` (byte-for-byte). If you see
  drift in an untouched module's section, you spliced incorrectly --
  abort and report.
- The new `INDEX.md` must still have every module listed in section 3
  (directory tree) and vice versa.

---

## Output format: INDEX.md

Four sections, in this order. The format is precise on purpose:
downstream agents grep for the section headers and the `(P|I) path -- desc`
line shape.

**Each section MUST use the exact `##` heading shown.** The file opens
with a `# INDEX` title; the four sections follow under it. An opening
paragraph that fills the role of "System overview" without the heading
is not acceptable -- downstream tooling greps for `## System overview`
specifically.

Skeleton:

```
# INDEX

## System overview

<2-3 sentences>

## Tech stack

<inventory bullets>

## Directory structure

<annotated tree>

## Modules

### <module-1>
...
### <module-2>
...
```

### 1. `## System overview`

Two to three sentences under the literal heading `## System overview`.
What the project is, what it does, what shape it has (library, service,
CLI, multi-binary workspace). No history, no rationale -- just
orientation.

### 2. `## Tech stack`

Inventory only:

- C++ standard / version (e.g. C++23).
- Build system (CMake, with presets if any).
- External libraries actually used in the source. **Name + origin URL**
  per entry. The URL resolves ambiguity for libraries that share a name
  (there are multiple `expected` implementations) and gives the agent a
  documentation anchor.
- Test framework.

Bullets, no prose. Example:

```
- C++23
- CMake (presets: debug, release, asan, tsan)
- Boost.LEAF -- https://github.com/boostorg/leaf
- fmt -- https://github.com/fmtlib/fmt
- Catch2 (tests) -- https://github.com/catchorg/Catch2
```

### 3. `## Directory structure`

`tree -d`-style output, annotated. One line per directory with a short
purpose tag. Depth up to 5 levels so nested submodules show up.

Per-directory depth exceptions:

- `test/` -- list once, no recursion. The test tree mirrors the source
  tree by convention; spelling it out wastes lines.
- `libs/` / `third_party/` / `vendor/` -- list once, no recursion. The
  index focuses on this project's surface; vendored trees are reference,
  not surface.
- Build / generated directories -- skipped entirely. Note once in a
  "skipped" footnote if useful.

Example shape (placeholders -- substitute real module names):

```
<project>/
|-- src/
|   |-- <util-lib>/
|   |   `-- <util-lib>/        general-purpose vocabulary headers
|   |       `-- <subsystem>/   nested submodule
|   |-- <input-domain>/        inbound boundary translator
|   |-- <output-domain>/       outbound boundary translator
|   |-- <core-domain>/         composition domain
|   `-- <runtime>/             runtime shell + main
`-- test/                      per-module unit tests (not expanded)
```

### 4. `## Modules`

The `## Modules` heading opens section 4. Below it, one `### <module>`
sub-section per logical unit. Each module section has:

**Header** -- the module name and a **2-4 sentence summary** of *what
the module does*: its responsibility, the abstractions it owns, the
problem it solves inside the system.

**The summary is 2-4 sentences. Hard cap. Count them.** Five sentences
is over the limit even if every sentence is good. Split content out into
the per-header lines, or cut.

**Dependencies and consumers are NOT part of the summary** -- they're
input the agent uses while writing it, not output the reader needs to
see. A dependency graph in every summary would dominate the file, and
common libraries would carry a consumer list the length of the project.

The rule applies to *any* phrasing that names other modules to
describe role-in-the-system. The smell-words are: "consumes", "emits",
"depends on", "used by", "called from", "feeds into", "produced by",
"composed in". If a sentence in your draft contains one of those words
followed by a module name, rewrite it.

Bad (names peer modules):

> Order-book matching domain. Consumes `order_routing` requests, emits
> `market_data` events. Depends on `kraken` for vocabulary helpers.
> Composed in the `kraken_submission` runtime shell.

Good (says what it does in its own terms):

> Order-book matching domain. Matches incoming requests against resting
> orders and produces trade events. Maintains per-instrument bid/ask
> ladders with pool-backed intrusive nodes and a flat resting-order
> index.

The good version describes the module's job; the reader can find out
*who* it talks to by reading section 3 (directory tree) and the file
lines themselves. The bad version turns the index into a dependency
diagram, which is `DESIGN.md`'s job, not the index's.

The summary is informed by reading the module's README if one exists,
plus a full read of the module's headers **and** implementation files.
The header list is what ends up in `INDEX.md`; the implementation files
are read for context so the descriptions are grounded.

**Resolving README/code conflicts.** When a README claim contradicts what
the code actually does, the agent resolves intent from the surrounding
code and writes the description that reflects present reality. Every
such conflict is recorded in `report-fragments/<module>.md` with both
sides quoted so the user can confirm which was right.

**The summary should not paraphrase the README -- it should compress it.**

**Base path** -- stated once at the top of the section:

```
Base path: `<project>/src/<module>/<module>/`
```

**File list** -- one line per header. Both public and internal headers
are listed; working on the module itself requires knowing where internal
helpers live too.

Format per file line:

```
- (P|I) <relative path>  -- <description>
```

Each line is tagged with visibility:

- `(P)` -- public, included from outside the module.
- `(I)` -- internal, only included within the module.

**Visibility ambiguity rule.** When visibility is unclear (no clear
convention in this codebase, header sits in a public-looking directory
but only internal includers, etc.), list as `(P)`. The cost of an
over-public tag is a reader trying to use a stable-looking header; the
cost of an over-internal tag is a reader skipping the right file. Bias
toward the cheaper mistake. Record the ambiguity in the report.

Full shape (placeholders -- real output uses real module and file names):

```
### <core-domain>

Base path: `<project>/src/<core-domain>/<core-domain>/`

Two-to-four-sentence summary of what this module does, the abstractions
it owns, and the problem it solves inside the system. No dependency
list, no consumer list.

Headers:

- (P) entry.hpp            -- module entry point; dispatches inputs to typed handlers
- (P) types.hpp            -- domain vocabulary (ids, primitives, strong-typed wrappers)
- (I) detail/state.hpp     -- internal mutable state owned by the entry point
- (I) detail/algorithm.hpp -- core algorithm implementation
```

See `references/output-template.md` for a complete worked example
against a realistic project layout.

---

## How to write file descriptions

This is where the skill earns its keep. A naive description reads the
file in isolation and produces something like "header declaring class
Foo." That's worse than `tree`.

The output is a description of *what the file does*. The agent gets there
by drawing on four contexts during exploration -- but these are inputs to
understanding, not content to enumerate in the line itself.

1. **The file itself, plus its implementation.** What it declares:
   types, free functions, constants, the central abstraction. **Read the
   matching `.cpp` in full** -- public surface plus implementation
   together produces a grounded description. A description built from
   declarations alone is shallow.
2. **Its neighbors.** What other files sit next to it in the same
   directory/module, so the description can position the file against
   its peers when that disambiguates ("bid-side ladder" vs "ask-side
   ladder").
3. **The module's role.** The same `types.hpp` means different things in
   an inbound-boundary module (request vocabulary) and an outbound-
   boundary module (event vocabulary). The module context picks the
   framing.
4. **Consumers.** Where the file's exports are used elsewhere in the
   repo. Useful as a sanity check (a header included only by tests is a
   test helper; one that crosses domain boundaries is a contract). The
   consumer list itself does not appear in the line.

The line says what the file does. The four contexts are how the agent
figures out what to say.

### Length

Strive for terseness; **target around 100 characters**. Going longer is
fine when the file genuinely needs it (a header that anchors a small
subsystem, a vocabulary file whose entries don't share a single theme).
The hard upper limit is **300 characters** -- past that the line becomes
its own paragraph and the listing stops being scannable. Split into a
follow-up note in the report rather than letting one line dominate.

### Examples

Bad (declares-only, worse than `tree`):

```
- (P) entry.hpp -- declares the engine class
```

Bad (drags consumer info into the line):

```
- (P) entry.hpp -- declares engine; used by the runtime, included by tests/engine_test.cpp
```

Bad (consumer phrasing leaks at the end of an otherwise-fine line):

```
- (P) overload.hpp -- variadic overload set for std::visit, used by `match`
```

The `, used by X` tail is the leak. Same rule as module summaries: who
uses it is reachable via the directory tree and is logged in the
working folder, but it does not belong on the line. **Smell-words to
strip from header lines: "used by", "called from", "consumed by",
"included from", "composed in", "exposed to".**

Good (says what the file does):

```
- (P) entry.hpp     -- module entry point; matches incoming requests and emits result events
- (P) overload.hpp  -- variadic overload set for std::visit; tagging building block for variant dispatch
```

---

## Companion report: INDEX-report.md

Alongside `INDEX.md`, write `INDEX-report.md` at the project root. The
report is for the user, not the agent -- it captures everything the run
noticed that deserves human attention.

Contents, grouped by category:

- **Ambiguities** -- headers where visibility could not be determined
  cleanly, where the role inside the module was unclear, where two
  plausible descriptions both fit.
- **Inconsistencies** -- README claims that don't match the code (every
  case where the agent resolved a conflict by trusting one side over the
  other, with both sides quoted so the user can confirm), modules with
  no README where peers have one, headers in public-looking locations
  with no external includers (or vice versa), dead headers (no
  includers anywhere), duplicate declarations across modules.
- **Errors** -- files the run could not parse, files with malformed
  includes, headers that wouldn't compile in isolation (if the run
  checked).
- **Decisions** -- non-obvious calls the run made (which module a
  borderline header was assigned to, which of two candidate descriptions
  was chosen). Briefly, so the user can audit.
- **Skipped** -- anything intentionally not indexed (non-C++ trees,
  vendored directories, generated code) and the reason.

Format: plain markdown, grouped by category, with file paths as anchors
so the user can navigate from the report into the source. **Keep empty
sections with a "none" note** so the user knows the run actually checked
rather than skipped.

---

## What this skill does *not* do

- It does not write `AGENTS.md`, `DESIGN.md`, ADRs, or READMEs.
- It does not invent conventions.
- It does not summarize implementation files.
- It does not document tests (beyond mentioning the test directory in
  the tree).
- It does not call out "interesting" code, suggest refactors, or rate
  quality.
- It does not enumerate consumers or dependencies in module summaries or
  per-header descriptions.

The index is a map. The map is not the territory; the map is not the
rulebook; the map is not the design doc. Keep it a map.

---

## Reference files

- `references/path-format-tradeoff.md` -- why module-relative paths
  under a stated base path were chosen over full repo-root paths on
  every line. Read this if asked to switch the format or if you're
  tempted to redesign the file-list format.
- `references/output-template.md` -- a complete worked example of
  `INDEX.md` and `INDEX-report.md`, so a subagent drafting a section
  has the target shape in front of it.
