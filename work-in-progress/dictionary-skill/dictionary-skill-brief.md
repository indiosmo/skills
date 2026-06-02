# Brief: build a "glossary-cpp-codebase" skill

You are working inside the skills repo (`/home/msi/llm_workspace/skills`, skills
live under `skills/<name>/`). Your task is to create a new skill that generates
and maintains a `GLOSSARY.md` domain glossary for a C++ codebase, then iterate
on it with the `creating-skills` process (draft, write evals, run, review,
improve). The human will review the evals.

This document is the complete spec. You do not need any external context beyond
it and the two repos it points at:

- The skill to model on: `skills/index-cpp-codebase/SKILL.md` (plus its
  `references/`). Read it first and in full -- the glossary skill is its
  sibling and should share its spine (modes, working-folder, parallel
  discovery, verification-then-report).
- A real reference codebase to develop and test against:
  `/home/msi/repos/matching-engine`. It contains a hand-curated root
  `GLOSSARY.md` authored in the exact schema this skill should produce, and an
  `AGENTS.md` showing how the glossary is wired into agent context. Use it as
  the worked example of good output, not a term-by-term answer key.

## Process

Use the `creating-skills` skill. Capture intent (this brief is the intent),
write the `SKILL.md` draft plus reference files, then run the eval loop: 2-3
realistic test prompts, with-skill and baseline runs, the eval viewer for human
review, then improve. The human will look at the evals, so get them in front of
them early (generate the viewer before grading yourself).

Suggested name: `glossary-cpp-codebase`, so it sits beside
`index-cpp-codebase` and reads as its glossary counterpart. Confirm or change
with the human if you prefer another name; keep the directory name and the
`name:` frontmatter in sync.

## What this is: a glossary, not a data dictionary

The artifact is a domain glossary -- the ubiquitous-language layer of a
codebase's docs, in the domain-driven-design sense. Its job is threefold:

- give the team and the agents one shared language for the domain;
- keep naming consistent, so one concept wears one name;
- anchor agent context in domain terms.

It is reference material in the Diataxis sense: neutral, factual, built for quick
lookup, no narrative.

It is a single compact file: a flat, grouped list of terse one-line entries, in
the spirit of an always-loaded agent glossary. It does not split into a verbose
"full" file plus a compact "agent" file; the one file is small enough to load
into agent context and complete enough to be the human reference.

It is emphatically not a data dictionary and not a usage map. Each entry defines
what the term *is* and stops there. It does not record the strong type that
carries the concept, the field width, the per-message field paths, the modules a
term appears in, or how the term is used elsewhere. Those churn, drift, and
duplicate what the code and the index already own. The glossary states meaning;
the code states representation and usage.

## First step: identify the domain (and subdomain)

Before any term work, establish what the application's domain is. Read
`README.md` and `docs/` (and `AGENTS.md` where present) to determine the field
the system operates in -- trading, clinical care, logistics, audio, and so on --
and, in a larger multi-module repo, the subdomain each module occupies. In the
reference repo the domain is order-book trading, with subdomains order routing,
matching, and market-data projection.

This step is load-bearing for everything after it: the domain decides which
authoritative external glossaries to consult, the subdomain decides which
vocabulary each module owns, and the domain and subdomain labels become the
`Domain context:` line and the framing sentence in the assembled glossary. Do
not start surfacing terms until the domain is named. Record the identified domain
and subdomains as a short label list at the top of the working notes so later
phases share the framing and the assembly phase can lift them verbatim into the
header.

## What the skill produces

It runs as a doc tree parallel to the README tree (orientation prose) and the
INDEX tree (navigation map):

- **Root `GLOSSARY.md`** at the project root -- the application-wide glossary:
  every concept shared across subdomains, stated once. This is almost always the
  whole output.
- **Per-subdomain `src/<module>/GLOSSARY.md`** -- only when a module has earned
  one: it owns vocabulary genuinely local to that subdomain, which the root should
  not absorb. Per-subdomain files back-link to the root, mirroring the per-module
  `INDEX.md` shape. Do not create empty module files; bias hard toward the single
  root file.

The two levels form one hierarchy with a single allocation rule: a term shared
across subdomains lives at the root and is stated once there; a term that only one
subdomain uses, and that a reader of another subdomain would never need, lives in
that subdomain's file. When in doubt, promote to the root -- one source of truth
beats a term duplicated across module files. A subdomain file never redefines a
root term; it adds only what is local to it. The hierarchy follows the domain's
module tree (the subdomains identified in the first phase), so a glossary sits at
each subdomain root that has earned local vocabulary, not under any `vN/` folder.
Most repos are a single root file; a per-subdomain file is the exception a large,
genuinely partitioned domain earns.

It also writes a sibling `GLOSSARY-report.md` at the project root for the human:
ambiguous terms, cross-boundary name divergences worth a unify-or-keep decision
(with the concrete code-name mapping the glossary body deliberately omits),
README/code conflicts about what a term means, terms whose definition leaned on
an external domain glossary (with the source), and anything deliberately left
out. The glossary is for downstream agents and humans alike; the report is for
the human reviewer.

The root `GLOSSARY.md` is the file loaded into agent context. When the project
wires docs into agents via `AGENTS.md`, the skill points that import at
`GLOSSARY.md` directly; there is no separate agent-only glossary file.

## What it is for, and what it is not

One source of truth per concern. The glossary defines concepts; it does not
restate what other artifacts own:

- It is not the rulebook (`AGENTS.md`), not the rationale (ADRs), not the
  orientation prose (README), not the navigation map (INDEX), and not a per-field
  data dictionary with types, constraints, and storage detail.
- An entry may, in the report, point to the ADR that explains a translation; it
  does not reproduce it.

It must not write ADRs or READMEs; it must not invent definitions or
conventions; it must not restate rationale; and it must not document
foundation/tooling libraries while they are out of scope. It may update
`AGENTS.md` only to wire the glossary into agent context: load `GLOSSARY.md` and
state the rule that vocabulary changes update it. It surfaces and defines domain
terms -- nothing else. (Mirror the "What this skill does not do" section of the
index skill.)

## Scope

- **Domain modules only.** In the reference repo those are `order_routing`,
  `matching_engine`, `market_data`. Foundation/vocabulary libraries (`mel`,
  `evl`, `runtime`) are tooling and stay out. Detect domain modules the same way
  the index skill detects modules (subdirs of `src/`, layout per `AGENTS.md` /
  ADRs); let the user scope explicitly when the split is not obvious.
- **Domain-level, version-independent terms.** A term belongs to the domain, not
  a version. Where a repo keeps versioned `vN/` folders, those are implementation
  detail: a `GLOSSARY.md` lives at `src/<module>/` (or the root), never under
  `vN/`. The term is version-stable.

## How meaning is derived

Two derivation sources feed every definition. The codebase says which terms
exist and how this repo wires them; the domain says what each term actually
means.

1. **The codebase**, surfaced from, in priority order:
   - **`types.hpp` per domain** -- strong types and enums name the primary
     terms. Enum values are part of the term; give them inline.
   - **`messages.hpp` / `events.hpp` / state structs** -- field names are concept
     usages and the place a cross-boundary rename shows up.
   - **The boundary converters** -- e.g. `make_order_state` (order_routing to
     matching_engine) and `project*` (matching_engine to market_data). These are
     the authoritative record of which upstream concept maps to which downstream
     name; read the implementation in full, not just signatures.
   - **Module READMEs** -- prose definitions to compress. When a README claim
     contradicts the code, resolve intent from the code, write the
     present-reality definition, and record the conflict in the report with both
     sides quoted.
2. **The domain and its authoritative glossaries.** Once the domain is
   identified, launch research agents to look up the recognized glossaries for
   that field and align each definition with the established industry meaning, so
   the glossary is consistent with the field, not merely self-consistent. For
   trading, that means glossaries such as NASDAQ, CME Group, and the FIX protocol
   field dictionary (FIX is the authority for the quantity and price terms --
   OrderQty, LeavesQty, LastQty, LastPx). Other domains have their own
   authorities (clinical: SNOMED/LOINC and specialty bodies; logistics: Incoterms
   and carrier standards). Prefer the authoritative phrasing; aim for the
   terseness of NASDAQ's definition of a symbol, "an abbreviation assigned to a
   security for trading purposes." Record in the report which terms leaned on an
   external source and which source. A term genuinely local to the repo (an
   internal event type) will not appear in any external glossary; define it from
   the codebase.

### Decompose composite terms

A composite term implies its components, and each component is its own entry.
"Aggressor side" requires both "aggressor" and "side"; "best bid" requires "bid".
Surface the atomic vocabulary, not only the compound, so a reader can look up the
part they do not know. When surfacing terms, split every multi-word concept into
its parts and check each part has an entry.

## Entry schema

The file is a flat list of one-line entries:

```
- **term** -- essential definition.
```

Do not group by default. A small glossary is a single flat list. Introduce
`##` groups only when the term count is large enough that coarse buckets aid
lookup, and keep any buckets coarse: if a term plausibly belongs in two groups,
the groups are too fine -- collapse them. The reference repo's glossary uses no
groups at all.

- **term** -- the concept in plain-English words, lowercase, spaced
  (`engine event`, not `engine_event`, not a type name). One entry per concept;
  do not give a concept two names (no "user / user_id").
- **essential definition** -- one sentence stating what the term *is*, derived
  from the codebase and aligned with the domain's authoritative glossary. It is
  self-contained: it defines the term itself and nothing else. It does not say
  where the term is used, what consumes it, or how it is mechanically processed.

The litmus test: `symbol` is "an alias that uniquely represents a tradable
product," not "traded instrument; an order book holds one symbol." The good
version captures the essence -- an alias, uniqueness, a tradable product -- and
stops; the bad version drags in the order book. The fact that an order book holds
one symbol belongs to the definition of *order book*, not *symbol* -- otherwise
every term ends up redescribing every place that uses it, and the glossary has
infinite surface area.

There are no anchor links, no `related` field, and no `not to be confused with`
field; the compact list carries definitions only. There is no "carried by" field:
representation is deliberately omitted. Give enum-like terms their values inline
(order type: limit, market; time in force: day, immediate-or-cancel).

Cross-boundary naming differences do not appear in the glossary body. The
glossary defines each concept once under its canonical name; renames and
inconsistencies are recorded in the report.

## Divergence handling

The glossary body keeps one essential definition per concept and does not carry a
naming table. Cross-boundary naming differences are recorded in
`GLOSSARY-report.md`:

- **Deliberate boundary rename** (e.g. the execution price is the engine's trade
  price and prints on the public feed in FIX vocabulary as the last price) ->
  the glossary defines the concept once under its canonical name; the report
  records the concrete code-name mapping.
- **A name unified across the boundary** -> a single concept, one entry, nothing
  special to say. Do not invent a divergence for a name the domains share.
- **Accidental divergence** -> define the concept once under its canonical name,
  and flag it in the report as a unify-or-keep decision. The skill does not
  rename code; it surfaces the choice.

The skill cannot always tell deliberate from accidental. Default to defining the
concept once and raising the naming question in the report when intent is
unclear.

## Output formats

Model the shapes on the index skill's "Output format" sections, adapted to
vocabulary:

- **Root `GLOSSARY.md`**: a top-level title that names the system or domain
  (`# Matching Engine`, not `# GLOSSARY` -- the file is a glossary, but its
  heading names the subject), then a short framing paragraph that says what the
  system is at a high level, then a one-line `Domain context:` list, then the
  entries as a flat list of one-line `- **term** -- definition.` items. The
  framing paragraph reads like a README's opening sentence: a high-level
  description of what the system is (in the reference repo: "A full trading
  exchange implementation, including order routing, the matching engine, and
  market data publication."). It names the major capabilities at the level a
  newcomer needs to place the terms, and stops there. It does not trace the
  pipeline or the data flow, does not describe the architecture, does not explain
  what the glossary file is, and does not name source libraries, folder layout,
  or the project's build/lab structure -- those are too specific and drift. The
  `Domain context:` line lists the domain and subdomain labels established in the
  identify-the-domain phase (in the reference repo: trading, financial markets,
  order routing, matching engine, market data), giving a reader the field at a
  glance and grounding the framing sentence in the same terms. No per-entry
  fields, no links, no cross-domain-naming section, no maintenance section, and
  no groups unless the term count makes coarse buckets worthwhile.
- **Per-subdomain `GLOSSARY.md`** (only when earned): a title naming the subdomain,
  a framing paragraph that says what the subdomain is at a high level the same way
  the root frames the whole system (and a `Domain context:` line scoped to the
  subdomain when it aids the reader), a back-link to the root
  (`Part of the [project glossary](../../GLOSSARY.md).`), and the subdomain's
  genuinely local terms in the same compact form.
- **`GLOSSARY-report.md`**: grouped by category -- ambiguities, divergences
  (unify-or-keep, with the concrete cross-boundary name mapping), README/code
  conflicts (both sides quoted), external-source notes (term -> glossary used),
  decisions, and skipped. Keep empty sections with a "none" note so the human
  knows the run checked.
- **`AGENTS.md` integration**: when the project has `AGENTS.md`, add
  `@GLOSSARY.md` to the always-loaded context and the sync instruction that
  `GLOSSARY.md` changes when domain vocabulary changes.

Drafting follows the project's documentation conventions: have subagents consult
the `documentation` skill for structure and `writing-clearly-and-concisely` for
prose (active voice, no hedging, no filler). Avoid glyphs and icons; plain text
only, including in any ASCII trees or tables.

### Navigation and rendering

The glossary is markdown read through GitHub's rendered view. Navigation uses
what markdown gives: the `##` theme headings for grouping and browser find for
search. The skill produces no separate HTML view and no generated site; the
markdown is both the source the agent imports and the artifact a human reads.

## Modes and workflow

Mirror the index skill -- same three modes, same precedence (explicit user
instruction over project state), same working-folder spine under `/tmp`, same
parallel discovery, same verification-then-report:

- **Full**: no root `GLOSSARY.md`, or the user asks to regenerate. Identify the
  domain, surface all terms, write the root file, any earned module files, the
  report, and the `AGENTS.md` wiring when present.
- **Scoped**: the user names modules or a term set. Re-surface only those; splice
  the root only where entries changed.
- **Incremental**: root `GLOSSARY.md` exists; use git to find the
  vocabulary-bearing files changed since it was last committed (per-domain
  `types.hpp`, `messages.hpp`/`events.hpp`, state structs, and the boundary
  converters -- a changed converter can introduce or retire a cross-boundary
  rename even when no type changed), derive the affected terms, and run scoped
  against them. Produce a changes report.

Phases, parallelized one subagent per domain (use `dispatching-parallel-agents`
when the source does not fit one context):

1. working folder
2. **identify the domain and subdomains** from `README.md` and `docs/`
3. locate the vocabulary-bearing files and converters, and **launch research
   agents to look up the domain's authoritative glossaries**
4. surface terms (decomposing composites) and write essential, domain-aligned
   definitions
5. assemble the single compact file
6. verify

Every phase writes its full output to the working folder; subagent prompts name
the exact file to write. Verification checks: the identified domain is recorded;
the root file is titled with the system/domain name (not `GLOSSARY`), opens with
a high-level framing paragraph that says what the system is (not the pipeline, not
the architecture, not the glossary file, not the build/lab structure) and a
`Domain context:` line whose labels match the identified domain and subdomains,
and the framing names no source libraries or folder layout; every per-module file
opens the same way for its subdomain, back-links to the root, and corresponds to
a real module; no empty
sections; the root states every shared concept exactly once; every composite
term's components have their own entries; each definition is self-contained
(defines the term, not its consumers or mechanics); `AGENTS.md`, when present,
loads `GLOSSARY.md` and states the sync rule.

Manual review gate: the skill drafts; the human reviews and edits before the
glossary is treated as ground truth. State this explicitly, as the index skill
states its verification phase.

## Reference codebase and how evals work

`/home/msi/repos/matching-engine` is a clean, small target, used for development
and as the worked example of the target schema. Its hand-curated `GLOSSARY.md`
is a single compact file: a flat list (no groups) of lowercase spaced terms,
one essential self-contained definition each, no links or per-entry fields,
definitions aligned with trading-industry usage. Use it as the reference
shape -- match its structure, density, and definitional style -- not as a
term-for-term answer key.

The plan for evaluation: develop the skill against matching-engine (self-check
its output against the curated example), then run it on a much larger repo the
human names, and judge that output on schema conformance and definitional
quality (essential, self-contained, domain-aligned), optionally comparing its
structure against the curated matching-engine glossary. The larger repo is the
real test; matching-engine is the calibration target.

The instructive cases the skill must handle, illustrated by matching-engine:

- **Essential, self-contained definitions**: `symbol` defines the identifier
  itself, not the order book that holds it. A run that writes "an order book
  holds one symbol" into the `symbol` entry has failed the litmus test.
- **Domain-aligned definitions**: the standard trading terms (maker, taker,
  aggressor, top of book, leaves quantity, last quantity) match how NASDAQ, CME,
  and FIX define them, not an ad-hoc paraphrase. The report names which source
  each leaned on.
- **A genuine boundary rename**: the execution price is the engine's trade price
  and prints on the public feed as the FIX last price. The glossary defines the
  concept once; the report records the code-name mapping; the skill does not
  create a second entry.
- **A name unified across the boundary**: the quantity lifecycle stages (order
  quantity, leaves quantity, last quantity) share names across the engine and the
  feed -- one entry each, no divergence. The skill must not invent a rename for a
  shared name.
- **A README/code conflict worth flagging**: the README says the public feed
  never carries identity, but the projected book-delta messages currently carry
  user and order id. The glossary states meaning and does not enumerate fields,
  but the skill reads the messages and converters, notices the contradiction, and
  flags it in the report with both sides quoted.
- **A negative check on a healed divergence**: the repo unified an `instrument`
  field name to `symbol`. A run today should produce `symbol` as a single concept
  with no divergence, and must not invent an `instrument`/`symbol` rename.
- **Composite decomposition**: the curated glossary lists `aggressor`, `side`,
  `bid`, `ask`, and `liquidity` as their own entries, not only the compounds.

## Suggested eval prompts

Realistic, the kind of thing the human would actually type. The full-mode prompt
can run against matching-engine for calibration and against the larger eval repo
for the real grade.

1. "Build a domain glossary for the matching-engine repo at
   `/home/msi/repos/matching-engine` -- I want a glossary of the domain terms
   across order_routing, matching_engine, and market_data." (Full mode. Assert:
   the run first identifies the trading domain from the README/docs; a single
   compact root `GLOSSARY.md` titled with the system name (not `GLOSSARY`),
   opening with a high-level framing paragraph that says what the system is (not
   the pipeline, the architecture, the glossary file, or the repo's lab structure)
   and a `Domain context:` line (trading, financial markets, order routing,
   matching engine, market data), with lowercase spaced terms and one
   self-contained definition each; `AGENTS.md` loads `GLOSSARY.md`; no "carried by" field, no
   links; one entry per concept (no combined "user / user_id"); composites
   decomposed (`aggressor`, `bid`, `ask`, `liquidity` present); `symbol` defines
   the identifier itself, not the order book; standard terms align with
   NASDAQ/CME/FIX usage; `symbol` is one concept with no rename; the report flags
   the market_data identity question and names external sources used. Compare
   structure and definitional style against the curated `GLOSSARY.md`.)
2. "I just renamed a field and added an enum in matching_engine -- refresh the
   glossary." (Incremental mode. Assert: it diffs the vocabulary-bearing files
   since the last commit, touches only affected terms, and writes a changes
   report.)
3. "Add a glossary just for the market_data module." (Scoped mode. Assert: it
   only emits a module file if market_data has earned local vocabulary;
   otherwise it explains why the root file still carries everything.)

## Deliverables

- `skills/glossary-cpp-codebase/SKILL.md`
- `skills/glossary-cpp-codebase/references/output-template.md` -- a worked
  example of the root file, an earned per-module file, the `AGENTS.md` wiring,
  and the report, against a realistic layout (model on the index skill's
  `references/output-template.md`).
- `evals/evals.json` and the eval workspace, per the `creating-skills` process.

Confirm the name and the scope-detection approach with the human, run the evals,
and put the results in front of them before iterating.
