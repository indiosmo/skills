# Generate a project-specific Python skill

This procedure turns the generic `writing-python` guidelines into a
committed, self-contained `<project>-python` skill living in the target
repository at `.claude/skills/<project>-python/`. The generic guides
describe principles in neutral terms (a domain package, a boundary
parser, a settings facade); the generated skill says "which package,
which validator, which fixture, which command in this codebase".

The generated skill is **committed to the project** and
**self-contained**: its reference docs live inside the skill folder, so
the project depends on neither a git submodule nor on the central
`writing-python` skill being installed on a contributor's machine. The
`writing-python` skill, when present, remains the textbook for the
generic principles; the generated skill is the project's index into its
own realization of them.

The job is **translation**, not duplication. If a section of the
generated skill reads the same as the generic guide with names swapped,
the section is not earning its place.

## Baseline and inputs

The generic guides are this skill's own references, already available to
you while this skill is loaded:

- [`overview.md`](overview.md) -- reading order, conventions, recurring
  themes.
- [`design-principles/`](design-principles/),
  [`testing-principles/`](testing-principles/),
  [`debugging-principles/`](debugging-principles/),
  [`projects-and-tooling/`](projects-and-tooling/) -- the long-form
  guides.
- [`examples.md`](examples.md) -- generic good/bad pairs.
- [`../SKILL.md`](../SKILL.md) -- the condensed always-loaded rules.

Skim these first so you know what generic sections exist and roughly
what each says. You are mapping each into the target codebase.

Then gather, from the target repository:

1. **Project entry docs.** `AGENTS.md`, `CLAUDE.md`, `.cursor/`,
   `.claude/`, root `README.md`, root `INDEX.md`. These often already
   name the project's vocabulary, packages, and command surface --
   harvest it.
2. **Package metadata and tool config.** Root `pyproject.toml` and
   `uv.lock`, plus any child `pyproject.toml` in a uv workspace. Read
   the dependency list, the Python version floor, and the tool tables
   for Ruff, Pyright (or mypy), and pytest. These pin the real command
   surface and the real validation libraries.
3. **Source layout and package names.** Walk `src/`. Note which package
   owns each domain, which package holds adapters, and which holds
   application or orchestration wiring. Record the actual names, not
   placeholders.
4. **Settings and config modules.** Find the Pydantic `BaseSettings`
   object, the config loader, and any context-local facades for clock,
   logger, settings, or tracing.
5. **Adapters and boundary parsers.** The Pydantic models, Pandera
   schemas, and translation functions that turn JSON, CLI input,
   environment, queue messages, database rows, or dataframes into domain
   values.
6. **Runtime and entry points.** CLI commands, FastAPI or Starlette
   routes, Dagster assets, dbt models, workers, schedulers, and the
   `asyncio`/`anyio` `TaskGroup` wiring near the entry point.
7. **Test layout.** `tests/`, `conftest.py` files, fixtures, domain
   factories, fixture factories, dataframe builders, fakes, and the
   marker convention.
8. **CI.** `.github/workflows/`, `pre-commit` config, and any
   project scripts that wrap the tool commands.

Use `rg` / `grep` and direct reads. Do not hallucinate paths -- every
link in the output must resolve to a real file.

## Goal: the generated skill layout

Produce this tree in the target repository:

```
.claude/skills/<project>-python/
  SKILL.md                 # always-loaded: what it is, the package and helper
                           #   mapping tables, cross-cutting wiring summary,
                           #   command surface, links
  references/
    design.md              # design deltas, additions, consequences for this project
    testing.md             # testing deltas, additions, consequences
    debugging.md           # debugging deltas, additions, consequences
    examples.md            # project-specific good/bad pairs keyed to the rule sections
```

`<project>` is the project's short name -- the same token the project
uses elsewhere (the repo name, the top-level package, or the name
already used in `AGENTS.md`). Skip a topical reference file if the
project genuinely has no equivalent surface for it, but say so
explicitly in `SKILL.md` rather than emit a stub.

The `SKILL.md` wrapper is the project's always-loaded layer. It maps the
generic `writing-python` vocabulary onto this codebase's real surface:

- the real packages that own each domain, and which package holds
  adapters versus application wiring;
- the real validation libraries and their aliases (Pydantic base
  classes, Pandera schema registry, the `NewType` family, the frozen
  slotted dataclass conventions);
- the real settings, clock, and logger facades, and how runtime code
  reaches them;
- the real test fixtures, factories, dataframe builders, and fakes,
  and where they live;
- the real command surface (the project's `uv`, `ruff`, `pyright`, and
  `pytest` invocations, plus any wrapper scripts).

The wrapper points at the embedded `references/`, which carry only the
project's deltas, additions, and consequences on top of the generic
guidance, plus the project's own canonical examples -- enough that the
skill stands alone.

In the generated skill, `SKILL.md` plays the role the README plays in a
docs folder: it is the always-loaded entry and the single home of the
mapping tables. The topical files under `references/` are loaded on
demand.

## Discovery: walk the generic guides, ask one question per section

For each section of the generic guides, ask the three-bucket question:
**what does this project ADD that the generic guide does not name, do
DIFFERENTLY, or suffer a non-obvious CONSEQUENCE from?** Three possible
answers:

1. **Direct mapping exists.** The project has its own realization of the
   concept (a `Settings` object for the settings facade, a domain
   exception base for the error model, a `tests/factories/` package for
   domain factories). Record the symbol and the module that defines it.
2. **Mapping exists but is structured differently.** The project owns
   the concept but splits it across more files or wraps it differently
   (for example, domain errors split across `errors.py` plus
   `error_codes.py` where the generic guide describes one module).
   Record the shape, not just the symbol.
3. **No equivalent.** The project genuinely lacks the pattern (no
   dataframe layer, no async runtime, no result-shaped bulk API). Note
   it explicitly in the mapping table as "n/a; project uses X instead"
   or "absent". Do not invent.

Walk the guides one tree at a time -- `design-principles/` for
`design.md`, `testing-principles/` for `testing.md`,
`debugging-principles/` and `projects-and-tooling/` for `debugging.md`
and the command surface. Reference the real generic section names so the
walk is concrete: `architecture.md`, `types-and-correctness.md`,
`error-handling.md`, `runtime-and-concurrency.md`,
`cross-cutting-services.md`, `data-pipeline-and-dataframes.md`,
`pytest-conventions.md`, `test-helpers.md`, `error-path-testing.md`,
`condition-based-waiting.md`, `root-cause-tracing.md`, `logging.md`,
`tooling-baseline.md`, and the rest.

A generic section that yields zero bullets produces nothing in the
generated skill.

## Discovery: walk the project for patterns the generic guides do NOT name

The second source of content is the project's own recurring patterns.
Look for shapes the generic guides do not cover but that recur often
enough to deserve a name:

- adapter naming conventions (`adapters/<vendor>/`,
  `<domain>_ingest.py`, `clients/<service>.py`);
- settings and facade patterns (the `Settings` singleton, a
  `ContextVar`-backed clock or logger, a `get_settings()` accessor);
- result-shaped bulk APIs (a `BulkResult` or per-item `Outcome` dataclass
  the project returns instead of raising for partial success);
- dataframe schema conventions (the Pandera schema registry plus the
  validator that enforces it at ingest);
- fixture, factory, and fake families (a `tests/factories/` package,
  `make_<value>` builders, protocol-implementing fakes);
- condition-wait helpers (a `wait_until` predicate-wait, an event-based
  readiness probe);
- task-group and anyio runtime wiring (the entry-point `TaskGroup`,
  cancel-scope helpers, queue typedefs);
- error-translation boundaries (the FastAPI exception handler, the CLI
  exit-code mapper, the worker retry classifier).

`rg` for recurring tokens. Read a handful of the most-cited modules from
`INDEX.md` or `AGENTS.md`. If a pattern shows up as a warning in
`AGENTS.md` ("frozen slotted dataclasses are kw-only; construct through
the factory"), that is signal it bites often and belongs in the
generated skill.

## Writing discipline: the three-bucket filter

Every section, paragraph, and bullet in a topical reference file
(`design.md`, `testing.md`, `debugging.md`) must fit one of three
buckets. If a candidate sentence does not fit any bucket, delete it.

1. **Additions** -- something the project has that the generic guide
   does not name at all. Example: a Pandera schema registry plus the
   validator that enforces every dataframe at ingest; a `BulkResult`
   dataclass the project returns from batch endpoints; a
   `tests/factories/` package with one builder per domain value.
2. **Deltas** -- something the project does differently from the generic
   guide's default shape. Example: the generic guide describes a single
   error module, but the project splits domain errors across `errors.py`
   (the exception classes) and `error_codes.py` (the stable string codes
   the HTTP boundary maps); the project uses `anyio` cancel scopes where
   the generic guide reaches first for `asyncio.TaskGroup`.
3. **Consequences** -- a non-obvious project-specific outcome of
   following a generic rule. Example: domain values are frozen slotted
   dataclasses with keyword-only fields, so a test that constructs one
   positionally or omits a field trips a `TypeError` -- tests must build
   through the factory; Pydantic models are `model_config =
   ConfigDict(frozen=True)`, so an adapter that mutates a parsed model
   in place raises instead of silently updating.

If a candidate paragraph reads like "the generic guide says X; in this
project, X looks like Y", it is almost certainly restatement. Strip the
"generic guide says X" half. The generic textbook lives in the
`writing-python` skill; the reader can open it.

### Tells of restatement

- A paragraph framing or motivating a rule before stating the project's
  realization. ("Python is exception-first, so the project translates
  failures at boundaries...") Delete the framing; jump to the project
  specifics.
- A code example that demonstrates a generic-guide rule with no
  project-specific helper, library choice, or gotcha.
- A description of what Pydantic, Pandera, `dataclasses.dataclass`,
  `asyncio.TaskGroup`, or `match`/`assert_never` does.
- A "reserve this pattern for genuine X" sentence (rationale belongs in
  the generic guide).
- A sentence listing what something is *not* responsible for ("this
  parser does not validate the database row"), unless the boundary is
  load-bearing and non-obvious from the signature.

### Worked example

A pipelines section that fails the test:

> ## Pipeline stages and wiring
>
> The generic guide describes pipeline stages as components with
> explicit inputs and outputs, wired near the runtime shell. The
> canonical realization lives in `src/ingest/pipeline.py`. A stage
> exposes a `process(batch)` method and emits results through a
> callback the shell assigns. The generic guide pushes keeping shared
> mutable state owned by one task...

The first sentences restate the generic guide's pipeline shape; only the
project-specific detail earns its place. The trimmed version reads:

> ## Pipeline wiring
>
> Stages follow the generic explicit-input/output shape. Project
> additions live in `src/ingest/wiring.py`: `build_pipeline` connects
> stages to the `anyio` memory-object stream pair the shell owns.
>
> **Non-obvious consequence.** A stage that forgets to close its send
> stream leaves the downstream `TaskGroup` blocked forever; the shell's
> `aclose()` in the `finally` is the only place that unblocks it.

One sentence pointing at the generic shape, then the addition and the
consequence. Everything else is gone.

### Section-length smell

If a topical-file section runs longer than five or six short sentences
or bullets, suspect restatement. The generated skill is an index; a
section that needs two paragraphs of prose is almost always doing the
generic guide's job too.

## Writing discipline: one canonical example per pattern

The generic writing rules ban listing every module that follows a rule.
Apply the same rule to code snippets inside a section: pick the single
file most worth reading and link there. Do not paste two or three
near-identical snippets to illustrate the same shape -- the reader will
copy the first one and never reach the second.

When two examples really do illustrate different things (one shows the
Pydantic boundary model, the other shows the frozen dataclass it parses
into), keep both but say what each adds.

## Writing discipline: the mapping tables live only in SKILL.md

The **mapping tables** -- the ones whose rows pair a generic concept
(domain package, result type, settings facade, factory family) with a
project symbol and its defining module -- belong in **one** place: the
generated `SKILL.md`. Topical files (`design.md`, `testing.md`,
`debugging.md`) reference symbols freely and trust the reader to consult
the table for module paths.

This matters because mapping rows are the highest-velocity drift hazard
in the deliverable -- a module gets moved, the row updates, and if the
same row is duplicated three files away it silently rots.

When `design.md` needs to name a symbol that already lives in the table,
write the symbol name plain (`Settings`, `ShipmentSchema`,
`make_shipment`) without re-linking to the defining module. Add a module
link only when the section is the canonical reading-order entry for that
symbol.

The rule is narrow. **Other project-internal tables are fine in topical
files.** Tables of Pandera schema-to-domain mappings, error-code string
allocations, pytest marker meanings, fixture-to-fake substitutions, and
similar project-only information belong next to the section that uses
them. The signal that a table is a mapping table is the presence of a
generic concept in the left column, not the presence of project symbols
on the right.

## File shape: SKILL.md

Start with YAML frontmatter. The `name` is `<project>-python`; the
`description` must trigger whenever an agent writes, changes, or reviews
Python in this project. Use a description shaped like:

```yaml
---
name: <project>-python
description: Write, change, and review Python in the <project> codebase using its real packages, validators, and conventions - <one clause naming the project's domain packages, error model, and runtime shell>. Use whenever editing or reviewing <project> Python under src/ or tests/, parsing inputs at adapters, adding domain values or error codes, wiring runtime tasks, or writing pytest tests. Maps the generic writing-python guidelines onto <project>'s actual symbols.
---
```

Then the body, opening with one paragraph naming what this skill is and
its relationship to the generic `writing-python` skill. Then:

1. **Progressive-disclosure links.** Point to `references/design.md`,
   `references/testing.md`, `references/debugging.md`,
   `references/examples.md`, each with a "use it when" hook. Note that
   the generic textbook lives in the installed `writing-python` skill
   when present.
2. **Mapping tables.** A package-ownership table (domain, owning
   package, layer) and a helper table (generic concept, project symbol,
   defining module) covering the result type or error base, the settings
   and clock and logger facades, the validation libraries, the factory
   and fake families, and the runtime entry points. After the tables, a
   short "absent / different" list for concepts that have no project
   equivalent.
3. **Cross-cutting wiring summary.** Three to five bullets naming the
   conventions that shape almost every module in `src/` (domain
   ownership, boundary parsing, the settings or facade pattern, the
   runtime shell split). Each bullet is one or two sentences -- the
   topical files carry the detail.
4. **Command surface.** The project's real invocations for sync,
   format, lint, type-check, and test (`uv sync`, `uv run ruff format`,
   `uv run ruff check`, `uv run pyright`, `uv run pytest`, plus any
   wrapper scripts or narrowed markers the project uses). Point at
   `pyproject.toml` as the source of truth for tool config rather than
   transcribing every option.
5. **Relation to other docs.** Short bullets pointing at `AGENTS.md`,
   `INDEX.md`, ADRs.

## Writing procedure: extract bullets first, then prose

Do not draft prose top to bottom. Each topical file is built in three
passes:

1. **Topic walk.** Go through the matching generic guide tree
   (`design-principles/` for `design.md`, and so on) one file at a time.
   For each generic file, ask only the three-bucket questions: does the
   project add anything here, do anything differently, or suffer any
   non-obvious consequence? Capture each answer as a single bullet with
   the concrete package, symbol, fixture, or command attached. If a
   generic file yields zero bullets, write nothing for it.

2. **Group into sections.** Cluster the bullets that share a topic
   (error handling, adapters, runtime, dataframes, ...). Each cluster
   becomes one section. A cluster with one bullet is a fine section --
   write the bullet plus its routing sentence and stop. A topic that
   produced zero bullets does not appear in the file at all.

3. **Prose only as needed.** For each section, write the minimum routing
   prose to introduce the bullets -- usually one sentence. No framing, no
   motivation, no rationale. If the routing sentence restates the generic
   guide, delete it; the bullets are enough.

The order of sections in the final file follows whichever cluster the
reader is most likely to need first; the topic walk in pass 1 is
discovery scaffolding, not the output order.

## What the topical files actually contain

The three topical files are not "everything about design / testing /
debugging in this project". They are the project's deltas, additions,
and consequences on top of the generic guides. Anything the generic
guide already covers without project specifics belongs to the generic
guide.

Common categories of content (use as a checklist during the topic walk;
do not turn into mandatory sections):

**design.md typically contains, when the project has them:**

- the package layout -- which domain package owns what, where adapters
  live, where application and orchestration wiring lives, and the
  project's stance on generic package names;
- the boundary-parsing recipe (Pydantic model at the edge, frozen
  slotted dataclass inside, the `NewType` family for primitive
  identity), and the consequence that kw-only frozen dataclasses force
  construction through factories;
- the error model -- the domain exception base, whether errors split
  across `errors.py` and `error_codes.py`, the boundary translation
  functions, and any result-shaped bulk return type;
- the settings and cross-cutting facade pattern (the `Settings` object,
  the `ContextVar`-backed clock or logger, the accessor functions) and
  how tests substitute them;
- the runtime shell split (functional core plus an application package
  that owns the event loop, clients, and workers), the `TaskGroup` or
  anyio wiring, and queue typedefs;
- the dataframe layer, when present: the Pandera schema registry, the
  ingest validator, the mutation-ownership convention, and the choice of
  pandas, Polars, or ibis;
- pipeline and stage conventions, adapter naming, and any
  framework-entry recipe (FastAPI router, Dagster asset, CLI command);
- per-module `INDEX.md` or `README.md` conventions.

**testing.md typically contains:**

- the test-target layout (mirroring `src/`), the `conftest.py`
  placement, and the marker convention;
- where domain factories, presets, fixture factories, dataframe
  builders, and fakes live, plus the naming pattern (`make_<value>`,
  `Fake<Protocol>`);
- error-path helpers (the project's `pytest.raises` wrappers, stable
  message and attribute assertions, the rollback-state assertions);
- condition-wait helpers (the `wait_until` predicate-wait, event-based
  readiness, async timeout composition);
- integration-test boundaries -- which markers or directories signal
  "this boots a real client, socket, worker, or database";
- approval-test scaffolding (renderers, scrubbers, output directory
  layout), when present;
- the "construct through the factory, not the constructor" recipe for
  frozen slotted dataclasses.

**debugging.md typically contains:**

- the logging stack and the project's event-shaped message convention,
  level toggles, and disabled-level cost notes;
- the static-analysis surface -- the Pyright (or mypy) mode, the Ruff
  rule set, the warning-escalation policy, and Python development mode;
- runtime diagnostics the project wires (`faulthandler`, asyncio debug
  mode, `tracemalloc`, memray, py-spy) and how to turn them on;
- defense-in-depth boundaries -- which parser, validator, assertion, or
  error path closes a given bug class;
- domain-specific replay or capture tools;
- where to look first when investigating a class of bug.

These are categories to scan during discovery, not headings to
guarantee. A project with no dataframe layer simply does not get a
dataframe section.

## File shape: references/examples.md

Project-specific good/bad pairs that complement the generic
`examples.md`. Cover only shapes that appear once the generic vocabulary
maps to the project -- the project's own helpers, validators, factories,
and gotchas. Match section titles to the rule sections in `design.md` /
`testing.md` / `debugging.md` so a reader can slice the file by section
name. Lead with the good form; add a `Bad:` block only where the
project-specific tell is not evident from the good form, reduced to the
fragment that carries the tell, followed immediately by the corrected
good form.

## Wire the skill into the project's agent docs

A committed skill is only useful if agents find it on the first pass.
After writing the skill:

- If the project has `AGENTS.md`, `CLAUDE.md`, or an equivalent
  agent-entry doc, add a short pointer: name the `<project>-python`
  skill and say to use it when writing or reviewing Python in this repo.
  Place the pointer where the doc already routes tasks to tools or
  conventions; match the doc's existing voice and format.
- If no such doc exists, note to the user that the skill will still be
  discovered by Claude Code's skill loader from `.claude/skills/`, and
  offer to add a brief `AGENTS.md` pointer if they want non-Claude
  agents to find it too.
- If the project keeps skills somewhere other than `.claude/skills/`,
  follow the project's convention and put the skill where its loader
  already looks.

Do not duplicate the skill's content into the agent doc -- one or two
sentences and the path are enough.

## Refresh: re-running on an existing skill

When the codebase or the generic `writing-python` guidance moves, update
the existing `<project>-python` skill rather than regenerating it from
scratch. Diff the inputs against what the skill already records:

- If a package, validator, facade, or factory was renamed or moved,
  update the affected mapping rows in `SKILL.md` and re-resolve every
  link the topical files point at.
- If the project grew a new recurring pattern (a new adapter family, a
  new result-shaped API), run the second discovery pass on the changed
  area and add bullets only for the new additions, deltas, and
  consequences.
- If the generic guides changed, re-walk only the affected generic
  section and adjust the project deltas it implies. A generic change
  with no project-specific consequence produces no edit.
- Re-run the self-review pass on every section you touched.

Keep the refresh additive and surgical. Rewriting unchanged sections
risks reintroducing restatement that an earlier pass already removed.

## Self-review pass (before declaring done)

Walk every section of every topical file and apply the three-bucket
filter sentence by sentence. For each sentence, classify it:

- (A) an **addition** -- project pattern the generic guide does not name;
- (D) a **delta** -- project does this differently from the generic default;
- (C) a **consequence** -- non-obvious outcome of following a generic rule;
- (R) a routing sentence pointing at a file, symbol, or section
      (allowed once or twice per section to introduce bullets);
- (X) anything else (framing, rationale, restatement, motivation).

Every (X) is a defect. Delete it. If a section is all (R)s and (X)s
after the pass, the section has no content and should disappear.

Then run the mechanical checks:

- Does the skill have valid frontmatter with `name: <project>-python`
  and a triggering `description`?
- Does this link resolve? (`ls` every path you wrote.)
- Did I cite a real example file, not a generic shape? (Open it and
  confirm the symbol is at the cited line.)
- Does this row appear in the `SKILL.md` mapping table and also in a
  topical file? (Delete the topical-file restatement.)
- Is any section longer than ~6 short sentences or bullets? (Suspect
  restatement; rerun the bucket filter on that section.)
- Is the skill self-contained -- no link reaching into a submodule path
  or assuming the `writing-python` skill is installed?

## Anti-patterns

- Writing framing or rationale prose before getting to the
  project-specific bullet. The generic guide owns rationale; jump
  straight to additions, deltas, and consequences.
- Drafting topical files top to bottom in prose rather than extracting
  bullets first. The bullet-first procedure exists because prose-first
  drafting reliably produces restatement padding.
- Treating the content categories above as a checklist of required
  sections. A project with no async runtime does not get a `TaskGroup`
  section.
- Writing prose that explains why parse-at-the-boundary or
  exception-first error handling is good. The generic guide owns
  rationale.
- Pasting the generic guide's `match`/`assert_never`, Pydantic, or
  Pandera examples with project names swapped in.
- Inventing a project helper because the generic guide mentions one and
  the project lacks an equivalent. Say it is absent and move on.
- Listing every adapter, every schema, every error code. Generalize and
  point at the package.
- Front-loading topical files with directory trees. The root `INDEX.md`
  is the project map.
- Duplicating the mapping tables across topical files.
- Linking the generated skill to a submodule or to the `writing-python`
  references by path. The committed skill must stand alone.

## Tone

Plain, direct, present tense. No marketing voice. No glyphs. Imperative
mood for procedures, declarative for descriptions. Match the project's
existing documentation voice -- if the project writes British spelling,
match it; if it qualifies every name with its package, match that too.

The generated skill is an index. The generic `writing-python` guides are
the textbook. Write accordingly.
