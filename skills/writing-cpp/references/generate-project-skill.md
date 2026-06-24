# Generate a project-specific C++ skill

This procedure turns the generic `writing-cpp` guidelines into a
committed, self-contained `<project>-cpp` skill living in the target
repository at `.claude/skills/<project>-cpp/`. The generic guides
describe principles in a `lib::` placeholder namespace; the generated
skill says "which header, which macro, which path, which canonical
example in this codebase".

The generated skill is **committed to the project** and **self-contained**:
its reference docs live inside the skill folder, so the project depends
on neither a git submodule nor on the `writing-cpp` skill being installed
on a contributor's machine. The `writing-cpp` skill, when present,
remains the textbook for the generic principles; the generated skill is
the project's index into its own realization of them.

The job is **translation**, not duplication. If a section of the
generated skill reads the same as the generic guide with names swapped,
the section is not earning its place.

## Baseline and inputs

The generic guides are this skill's own references, already available to
you while this skill is loaded:

- [`overview.md`](overview.md) -- reading order, conventions, the
  `lib::` placeholder list, recurring themes.
- [`design-principles/`](design-principles/),
  [`testing-principles/`](testing-principles/),
  [`debugging-principles/`](debugging-principles/) -- the long-form
  guides.
- [`examples.md`](examples.md) -- generic good/bad pairs.
- [`../SKILL.md`](../SKILL.md) -- the condensed always-loaded rules.

Skim these first so you know what generic sections exist and roughly
what each says. You are mapping each into the target codebase.

Then gather, from the target repository:

1. **Project entry points.** `AGENTS.md`, `CLAUDE.md`, `.cursor/`,
   `.claude/`, root `README.md`, root `INDEX.md`. These often already
   name the project's vocabulary -- harvest it.
2. **Directory layout.** Look at `src/`, `include/`, `lib/`, `test/`.
   Note the per-component layout convention (boost-stuttering
   `src/<comp>/<comp>/` is common; flat `include/` + `src/` is the
   other common shape). Note where any runtime / threading split lives.
3. **ADRs.** `docs/adr/`, `docs/decisions/`, or similar. Pull in any
   ADR whose decision is observable in the code (logging backend
   choice, result type, error-code policy).
4. **Build and CI.** `CMakeLists.txt`, `CMakePresets.json`,
   `meson.build`, `Makefile`, `.github/workflows/`, `scripts/`.
   Sanitizer presets, error-code validators, format and lint scripts
   all surface here.
5. **Per-module indexes.** If there's a `src/<comp>/INDEX.md` (or
   equivalent), it usually lists public vs internal headers and the key
   types -- gold for finding canonical examples.

Use `rg` / `grep` and direct reads. Do not hallucinate paths -- every
link in the output must resolve to a real file.

## Goal: the generated skill layout

Produce this tree in the target repository:

```
.claude/skills/<project>-cpp/
  SKILL.md                 # always-loaded: what it is, placeholder mapping table,
                           #   cross-cutting wiring summary, build/test commands, links
  references/
    design.md              # design deltas, additions, consequences for this project
    testing.md             # testing deltas, additions, consequences
    debugging.md           # debugging deltas, additions, consequences
    examples.md            # project-specific good/bad pairs keyed to the rule sections
```

`<project>` is the project's short name (the same token the project
uses elsewhere -- the repo name, the top-level namespace, or the name
already used in `AGENTS.md`). Skip a topical reference file if the
project genuinely has no equivalent surface for it -- but say so
explicitly in `SKILL.md` rather than emit a stub.

In the generated skill, `SKILL.md` plays the role the README plays in a
docs folder: it is the always-loaded entry and the single home of the
placeholder mapping table. The topical files under `references/` are
loaded on demand.

## Discovery: walk the generic guide, ask one question per section

For each section of the generic guide, ask: **"What concrete project
symbol, file, macro, or script realizes this?"** Three possible
answers:

1. **Direct mapping exists.** Project has its own `lib::result<T>`
   equivalent (`mil::result<T>`, `core::result<T>`, `std::expected<T, E>`,
   etc). Record the symbol + the header that defines it.
2. **Mapping exists but is structured differently.** Project owns the
   concept but splits it across more files or wraps it differently
   (e.g. a three-file domain triad `error_code.hpp + errors.hpp +
   error_handlers.hpp` where the generic guide describes one of those).
   Record the shape, not just the symbol.
3. **No equivalent.** The project genuinely lacks the pattern (e.g. no
   inplace-function wrapper, no scope-guard library). Note it
   explicitly in the placeholder table as "n/a; project uses X instead"
   or "absent; prefer Y pattern". Do not invent.

## Discovery: walk the project for patterns the generic guide does NOT name

The second source of content is the project's own recurring patterns.
Look for shapes the generic guide does not cover but that recur often
enough to deserve a name:

- Adapter naming conventions (`<dom1>_<dom2>/`,
  `adapters/<external>/`, `clients/<vendor>/`).
- Wiring helpers (functions that bulk-connect callback fields, no-op
  wirings for tests, proxy stages).
- Cross-cutting service registration patterns (variant-backed globals,
  service locator, dependency-injection roots).
- Error-code numeric allocation schemes (`601xxx` for `aor`, etc.) and
  the validator script that enforces them.
- Macros that abstract recurring expressions (`MIL_PLUCK`,
  `MIL_CONTINUE_ON_ERROR`, `MIL_REQUIRE_LEAF`).
- Per-domain `types.hpp` conventions plus any local namespace-alias
  shorthand (`namespace at = aor::types;`).
- Per-module navigation files (root `INDEX.md` + per-module `INDEX.md`
  with public/internal tagging).
- JSON-config-driven runtime composition pipelines.
- Test-side singleton-sandboxing helpers.

`rg` for recurring tokens. Read a handful of the most-cited headers from
`INDEX.md`. Skim `AGENTS.md` -- if a pattern is repeated there as a
warning ("non-defaulted callback type X asserts on destruction"), that
is signal it bites often and belongs in the generated skill.

## Writing discipline: the three-bucket filter

Every section, paragraph, and bullet in a topical reference file
(`design.md`, `testing.md`, `debugging.md`) must fit one of three
buckets. If a candidate sentence does not fit any bucket, delete it.

1. **Additions** -- something the project has that the generic guide
   does not name at all. Examples: a numeric-prefix scheme for error
   codes plus the validator script that enforces it; a wiring-helper
   family that bulk-connects callback fields; an adapter recipe of
   "abstract codec + per-counterparty impl + runtime layer"; a JSON
   config + PFR-reflection macro pair.
2. **Deltas** -- something the project does differently from the
   generic guide's default shape. Examples: the generic guide describes
   a single `errors.hpp`, but the project splits into a triad
   (`error_code.hpp + errors.hpp + error_handlers.hpp`); the generic
   guide names a generic `lib::scope_exit`, but the project uses
   `ricab/scope_guard` directly with no wrapper.
3. **Consequences** -- a non-obvious project-specific outcome of
   following a generic rule. Examples: callback fields are
   `mil::inplace_function`, which is non-defaulted, so tests must
   wire every callback or trip a destruction assert; handler order
   in `std::tuple_cat` matters because `boost::leaf` walks the tuple
   linearly.

If a candidate paragraph reads like "the generic guide says X; in
this project, X looks like Y", it is almost certainly restatement.
Strip the "generic guide says X" half. The generic textbook lives in
the `writing-cpp` skill; the reader can open it.

### Tells of restatement

- A paragraph framing or motivating a rule before stating the
  project's realisation. ("The generic guide pushes strong typing,
  exhaustive enum switches, ...") Delete the framing; jump to the
  project specifics.
- A code example that demonstrates a generic-guide rule with no
  project-specific helper, `N` choice, or gotcha.
- A description of what `lib::strong_type`, `lib::match`,
  `BOOST_LEAF_CHECK`, or `std::variant` does.
- A "reserve this pattern for genuine X" sentence (rationale belongs
  in the generic guide).
- A sentence that lists what something is *not* responsible for
  ("this is not a thread-safe component"), unless the boundary is
  load-bearing and non-obvious from the type.

### Worked example

A pipelines section that fails the test:

> ## Pipelines and callbacks
>
> The generic guide describes pipeline stages as components with
> `on_*` callback fields and `send` overloads. The canonical
> realisation lives in `src/aor/aor/pipeline_stage.hpp`. A stage
> exposes:
>
> - one virtual `send(Message&&)` per message type;
> - one public `mil::inplace_function<void(Message&&)>` callback
>   field per message type.
>
> Wiring near `main` assigns the callbacks. Non-obvious consequence:
> these callbacks are non-defaulted and assert on destruction in
> debug builds...

The first three paragraphs restate the generic guide's pipeline
shape; only the consequence-bullet earns its place. The trimmed
version reads:

> ## Pipelines and callback wiring
>
> Pipeline interfaces follow the generic on_* + send shape. Project
> additions live in `src/aor/aor/wiring.hpp`: `wire_requests`,
> `wire_responses`, `wire`, `wire_proxy`.
>
> **Non-obvious consequence.** Callback fields are
> `mil::inplace_function`, which is non-defaulted and asserts on
> destruction if it was never assigned. `scripts/wirecheck.sh`
> catches most production omissions; tests must wire noops by hand.

One sentence pointing at the generic shape ("follow the generic on_* +
send shape"), then the additions and the consequence. Everything
else is gone.

### Section-length smell

If a topical-file section runs longer than five or six short
sentences or bullets, suspect restatement. The generated skill is an
index; a section that needs two paragraphs of prose is almost
always doing the generic guide's job too.

## Writing discipline: one canonical example per pattern

The generic writing rules ban listing every module that follows a rule.
Apply the same rule to code snippets inside a section: pick the single
file most worth reading and link there. Do not paste two or three
near-identical snippets to illustrate the same shape -- the reader will
copy the first one and never reach the second.

When two examples really do illustrate different things (e.g. one
shows the abstract interface, the other shows the per-counterparty
implementation), keep both but say what each adds.

## Writing discipline: the placeholder mapping table lives only in SKILL.md

The **placeholder mapping table** -- the one whose rows pair a generic
`lib::*` placeholder with a project symbol and its defining header --
belongs in **one** place: the generated `SKILL.md`. Topical files
(`design.md`, `testing.md`, `debugging.md`) reference symbols freely
and trust the reader to consult the table for header paths.

This matters because mapping rows are the highest-velocity drift hazard
in the deliverable -- a header gets moved, the row updates, and if the
same row is duplicated three files away it silently rots.

When `design.md` needs to name a macro or symbol that already lives in
the table, write the symbol name plain (`mil::strong_type`, `MIL_PLUCK`)
without re-linking to the defining header. Add a header link only when
the section is the canonical reading-order entry for that symbol.

The rule is narrow. **Other project-internal tables are fine in topical
files.** Tables of `fixed_string<N>` size choices, error-code numeric
prefix allocations, sanitizer presets, test-target layout, variant
singleton alternatives, and similar project-only information belong
next to the section that uses them and do not need to migrate to
`SKILL.md`. The signal that a table is the placeholder mapping is the
presence of `lib::*` (or "generic placeholder") in the left column --
not the presence of project symbols on the right.

## File shape: SKILL.md

Start with YAML frontmatter. The `name` is `<project>-cpp`; the
`description` must trigger whenever an agent writes, changes, or reviews
C++ in this project. Use a description shaped like:

```yaml
---
name: <project>-cpp
description: Guidelines for writing C++ in the <project> codebase.
---
```

Then the body, opening with one paragraph naming what this skill is and
its relationship to the generic `writing-cpp` skill. Then:

1. **Progressive-disclosure links.** Point to `references/design.md`,
   `references/testing.md`, `references/debugging.md`,
   `references/examples.md`, each with a "use it when" hook. Note that
   the generic textbook lives in the installed `writing-cpp` skill when
   present.
2. **Placeholder mapping table.** Three columns: generic placeholder,
   project symbol, defining header. Add rows for every recurring
   placeholder used by the project examples. After the table, a short
   "absent / different" list for placeholders that have no project
   equivalent.
3. **Cross-cutting wiring summary.** Three to five bullets naming the
   conventions that shape almost every file in `src/` (domain
   ownership, pipeline callback wiring, cross-cutting services,
   runtime split). Each bullet is one or two sentences -- the topical
   files carry the detail.
4. **Build, test, verification commands.** Point to the relevant script
   or preset for each (build presets, sanitizer wrapper, error-code
   validator, flaky-test bisector). Do not list every preset name --
   `CMakePresets.json` is the source of truth.
5. **Relation to other docs.** Short bullets pointing at `AGENTS.md`,
   `INDEX.md`, ADRs.

## Writing procedure: extract bullets first, then prose

Do not draft prose top to bottom. Each topical file is built in three
passes:

1. **Topic walk.** Go through the generic guide's matching tree
   (`design-principles/` for `design.md`, etc.) one file at a time.
   For each generic file, ask only the three-bucket questions: does the
   project add anything here, do anything differently, or suffer any
   non-obvious consequence? Capture each answer as a single bullet with
   the concrete symbol, path, or script attached. If a generic file
   yields zero bullets, write nothing for it.

2. **Group into sections.** Cluster the bullets that share a topic
   (error handling, pipelines, runtime, ...). Each cluster becomes
   one section. A cluster with one bullet is a fine section -- write
   the bullet plus its routing sentence and stop. A topic that
   produced zero bullets does not appear in the file at all.

3. **Prose only as needed.** For each section, write the minimum
   routing prose to introduce the bullets -- usually one sentence.
   No framing, no motivation, no rationale. If the routing sentence
   restates the generic guide, delete it; the bullets are enough.

The order of sections in the final file follows whichever cluster
the reader is most likely to need first; the topic walk in pass 1 is
discovery scaffolding, not the output order.

## What the topical files actually contain

The three topical files are not "everything about design / testing /
debugging in this project". They are the project's deltas, additions,
and consequences on top of the generic guide. Anything the generic
guide already covers without project specifics belongs to the generic
guide.

Common categories of content (use as a checklist during the topic
walk; do not turn into mandatory sections):

**design.md typically contains, when the project has them:**

- the component directory layout (boost-stuttering, flat, or
  whatever the project uses), including where runtime wrappers and
  test helpers live, and how adapter modules are named;
- recurring `mil::fixed_string<N>` / `mil::inplace_function<Sig, N>`
  size tables;
- the X-macro / reflection-macro tricks the project uses
  (`MIL_AUTO_JSON_PFR_NAMESPACE`, X-macro composite enums);
- the error-handling triad (`error_code.hpp` + `errors.hpp` +
  `error_handlers.hpp`), the numeric-prefix scheme, the catch-macro
  family, the `make_error` shortcut, the validator script;
- the wiring-helper family (`wire`, `wire_proxy`, `wire_noop`) and
  its consequence: callbacks that assert on destruction;
- the runtime layer split (functional core + `<domain>/runtime/`),
  marshalled adapters, message-queue typedefs and their capacity
  tuning;
- the cross-cutting singleton pattern realised by the project's
  variant-backed globals, plus how tests sandbox them;
- the adapter recipe (abstract interface + per-X impls + runtime
  layer);
- hot-path helper choices and "do not adopt X -- broken" notes;
- per-module `INDEX.md` / `README.md` conventions.

**testing.md typically contains:**

- the test-target layout (mirroring `src/`), the test framework
  invocation glue (`catch_discover_tests`, etc.), and the tag
  convention;
- result-aware assertion helpers
  (`mil::testing::require_error`, equivalents);
- where factories, fixtures, and probes live and the naming pattern;
- singleton-sandboxing RAII guards;
- the deterministic-clock helper, plus the predicate-wait family;
- integration-test boundaries (which tags or directories signal
  "this boots a real vendor engine / socket / thread");
- approval-test scaffolding (scrubbers, output directory layout);
- the "wire every callback in tests too" recipe.

**debugging.md typically contains:**

- the logging-macro family, level-toggle, throttle variants, and
  logger backends;
- stack-trace integration (`cpptrace`, `boost::stacktrace`),
  always-on stacktrace toggles, full-details helpers;
- the sanitizer-preset table and suppression file locations;
- flaky-test bisection invocation and reproducibility tools;
- error-code validators and wiring validators;
- domain-specific replay or capture tools;
- where to look first when investigating a class of bug.

These are categories to scan during discovery, not headings to
guarantee. A project that has no flaky-test bisector simply does
not get a flaky-test section.

## File shape: references/examples.md

Project-specific good/bad pairs that complement the generic
`examples.md`. Cover only shapes that appear once the placeholders map
to the project vocabulary -- the project's own helpers, `N` choices,
macros, and gotchas. Match section titles to the rule sections in
`design.md` / `testing.md` / `debugging.md` so a reader can slice the
file by section name. Lead with the good form; add a `Bad:` block only
where the project-specific tell is not evident from the good form,
reduced to the fragment that carries the tell, followed immediately by
the corrected good form.

## Wire the skill into the project's agent docs

A committed skill is only useful if agents find it on the first pass.
After writing the skill:

- If the project has `AGENTS.md`, `CLAUDE.md`, or an equivalent
  agent-entry doc, add a short pointer: name the `<project>-cpp` skill
  and say to use it when writing or reviewing C++ in this repo. Place
  the pointer where the doc already routes tasks to tools or
  conventions; match the doc's existing voice and format.
- If no such doc exists, note to the user that the skill will still be
  discovered by Claude Code's skill loader from `.claude/skills/`, and
  offer to add a brief `AGENTS.md` pointer if they want non-Claude
  agents to find it too.

Do not duplicate the skill's content into the agent doc -- one or two
sentences and the path are enough.

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

- Does the skill have valid frontmatter with `name: <project>-cpp` and
  a triggering `description`?
- Does this link resolve? (`ls` every path you wrote.)
- Did I cite a real example file, not a generic shape? (Open it and
  confirm the symbol is at the cited line.)
- Does this row appear in the `SKILL.md` mapping table and also in a
  topical file? (Delete the topical-file restatement.)
- Is any section longer than ~6 short sentences or bullets? (Suspect
  restatement; rerun the bucket filter on that section.)
- Is the skill self-contained -- no link reaching into a submodule path
  or assuming the `writing-cpp` skill is installed?

## Anti-patterns

- Writing framing or rationale prose before getting to the
  project-specific bullet. The generic guide owns rationale; jump
  straight to additions, deltas, and consequences.
- Drafting topical files top to bottom in prose rather than
  extracting bullets first. The bullet-first procedure exists because
  prose-first drafting reliably produces restatement padding.
- Treating the content categories above as a checklist of required
  sections. A project that has no flaky-test bisector does not get a
  flaky-test section.
- Writing prose that explains why strong types are good. The generic
  guide owns rationale.
- Pasting the generic guide's enum-switch / variant-match /
  state-machine examples with project names.
- Inventing a project utility because the generic guide mentions one
  and the project lacks an equivalent. Say it is absent and move on.
- Listing every adapter, every codec, every error code. Generalize and
  point at the directory.
- Front-loading topical files with directory trees. The root `INDEX.md`
  is the project map.
- Duplicating the placeholder mapping table across topical files.
- Linking the generated skill to a submodule or to the `writing-cpp`
  references by path. The committed skill must stand alone.

## Tone

Plain, direct, present tense. No marketing voice. No glyphs. Imperative
mood for procedures, declarative for descriptions. Match the project's
existing documentation voice -- if the project uses British spelling,
match it; if it writes `std::` qualifiers everywhere, match that too.

The generated skill is an index. The generic `writing-cpp` guides are
the textbook. Write accordingly.
