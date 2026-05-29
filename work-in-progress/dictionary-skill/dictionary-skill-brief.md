# Brief: build a "dictionary-cpp-codebase" skill

You are working inside the skills repo (`/home/msi/llm_workspace/skills`, skills
live under `skills/<name>/`). Your task is to create a new skill that generates
and maintains a `DICTIONARY.md` domain glossary for a C++ codebase, then iterate
on it with the `creating-skills` process (draft, write evals, run, review,
improve). The human will review the evals.

This document is the complete spec. You do not need any external context beyond
it and the two repos it points at:

- The skill to model on: `skills/index-cpp-codebase/SKILL.md` (plus its
  `references/`). Read it first and in full -- the dictionary skill is its
  sibling and should share its spine.
- A real reference codebase to develop and test against:
  `/home/msi/repos/matching-engine`. It already contains a hand-written root
  `DICTIONARY.md` (the target shape) and an `AGENTS.md` describing how the
  dictionary fits the docs. Use both as ground truth for what good output looks
  like, and as the corpus for evals.

## Process

Use the `creating-skills` skill. Capture intent (this brief is the intent),
write the `SKILL.md` draft plus reference files, then run the eval loop: 2-3
realistic test prompts, with-skill and baseline runs, the eval viewer for human
review, then improve. The human will look at the evals, so get them in front of
them early (generate the viewer before grading yourself).

Suggested name: `dictionary-cpp-codebase`, so it sits beside
`index-cpp-codebase` and reads as its glossary counterpart. Confirm or change
with the human if you prefer another name; keep the directory name and the
`name:` frontmatter in sync.

## What the skill produces

A domain glossary -- the ubiquitous-language layer of a codebase's docs. It
states what each domain term means, how terms relate, and where the same concept
is named differently across a domain boundary. It is reference material in the
Diataxis sense: neutral, factual, built for quick lookup, no narrative.

It runs as a doc tree parallel to the README tree (orientation prose) and the
INDEX tree (navigation map), and is hybrid like the index:

- **Root `DICTIONARY.md`** at the project root -- every shared concept stated
  once, with the cross-boundary renames captured as inline aliases on the
  concept entry. This is almost always the whole output.
- **Per-module `src/<module>/DICTIONARY.md`** -- only when a module has earned
  one: it owns genuinely local vocabulary, or an inbound-translation table too
  substantial for inline aliases. Per-module files back-link to the root,
  mirroring the per-module `INDEX.md` shape. Do not create empty module files;
  bias hard toward the single root file.

It also writes a sibling `DICTIONARY-report.md` at the project root for the
human: ambiguous terms, cross-domain name divergences worth a unify-or-keep
decision, README/code conflicts about what a term means, and anything
deliberately left out. The dictionaries are for downstream agents; the report is
for the human.

For projects that load docs into agent context, the skill also writes a compact
agent glossary, conventionally `AGENT_DICTIONARY.md`, beside the root
`DICTIONARY.md`. This file is the always-loaded vocabulary layer: the domain
flow, canonical terms, and important aliases compressed enough for every agent
session. The full dictionary remains the human reference and the on-demand
drill-down.

## What it is for, and what it is not

One source of truth per concern. The dictionary defines concepts; it does not
restate what other artifacts own:

- It is not the rulebook (`AGENTS.md`), not the rationale (ADRs), not the
  orientation prose (README), not the navigation map (INDEX), and not a
  per-field data dictionary with constraints and storage detail.
- An entry may link to the ADR that explains a translation; it does not
  reproduce it.

It must not write ADRs or READMEs; it must not invent definitions or
conventions; it must not restate rationale; and it must not document
foundation/tooling libraries while they are out of scope. It may update
`AGENTS.md` only to wire the dictionary artifacts into agent context: load
`AGENT_DICTIONARY.md`, keep full `DICTIONARY.md` on demand, and state the sync
rule. It surfaces and defines domain terms -- nothing else. (Mirror the "What
this skill does not do" section of the index skill.)

## Scope

- **Domain modules only.** In the reference repo those are `order_routing`,
  `matching_engine`, `market_data`. Foundation/vocabulary libraries (`mel`,
  `evl`, `runtime`) are tooling and stay out. Detect domain modules the same way
  the index skill detects modules (subdirs of `src/`, layout per `AGENTS.md` /
  ADRs); let the user scope explicitly when the split is not obvious.
- **Domain-level, version-independent terms.** A term belongs to the domain, not
  a version. Where a repo keeps versioned `vN/` folders, those are
  implementation detail: a `DICTIONARY.md` lives at `src/<module>/` (or the
  root), never under `vN/`. The type a term cites is the current representative
  one; the term itself is version-stable.

## Where the vocabulary lives (term-surfacing inputs)

This is the discovery core and the main thing that differs from the index skill.
Unlike a file-by-file index, the vocabulary is concentrated in a few
human-readable headers, so reading them directly is reliable; use clangd/LSP to
enumerate symbols accurately when available, but it is not as load-bearing as it
is for the index. Surface terms from, in priority order:

1. **`types.hpp` per domain** -- strong types and enums are the primary term
   source. Enum values are part of the term (give them inline).
2. **`messages.hpp` / `events.hpp` / state structs** -- field names are concept
   usages and the place aliases show up (the same `types::symbol` may be a field
   named `symbol` in one domain and something else in another).
3. **The boundary converters** -- e.g. `make_order_state` (order_routing to
   matching_engine) and `project*` (matching_engine to market_data). These are
   the authoritative record of which upstream concept maps to which downstream
   name; mine the translation table from them, reading the implementation in
   full, not just signatures.
4. **Module READMEs** -- prose definitions to compress (not paraphrase). When a
   README claim contradicts the code, resolve intent from the code, write the
   present-reality definition, and record the conflict in the report with both
   sides quoted.

## Entry schema

Each term is one entry. Keep the fields lightweight:

- **term** -- the concept name (canonical, lower_snake as it reads in the
  domain).
- **definition** -- one or two neutral sentences. No narrative, no rationale.
- **carried by** -- the strong type(s) and domain(s) that express it (e.g.
  `types::price` in all three domains). Name the type and the owning domain, not
  the per-message field paths or an exhaustive list of call sites -- those churn
  and make the field drift. When one concept has a different strong type per
  domain, list each (e.g. `types::quantity` (`matching_engine`),
  `types::leaves_qty` (`market_data`)).
- **aliases** -- the bare alias name(s) only, no domain tag or gloss (e.g.
  `last_px`). An alias appears when a concept keeps a genuinely different name on
  one side of a boundary. When the domains instead share the name, the concept is
  a single term carried by both -- no alias.
- **related** -- see-also links to sibling terms.
- **not to be confused with** -- the polysemy guard (e.g. an order's `side` vs a
  trade's `aggressor_side`; an order's limit `price` vs the execution price
  `trade_price`).

Give enum-like terms their valid values inline (e.g. `order_type`: limit,
market; `time_in_force`: day, ioc).

The `related` and `not to be confused with` fields, and any inline term mention
that has its own entry, render as intra-document links to that entry, not as
plain text. A reader on GitHub clicks `order_qty` in a `related` line and jumps
to that entry. The `aliases` field carries bare names; link one only if that
alias is itself a term entry (usually it is not, so it stays plain text).
Link to GitHub's auto-generated heading anchor: lowercase the heading, replace
spaces with hyphens, drop punctuation -- `### user, user_id` becomes
`#user-user_id`, so the link is `[user_id](#user-user_id)`. When a target term is
one of several names on a shared heading (`### order_id, user_order_id`), link to
that combined anchor. Cross-references that point outside the dictionary (an ADR,
a header) use ordinary relative links.

## Divergence handling (the heart of the skill)

The dictionary's distinctive value is exposing where one concept wears different
names across the boundary. Two outcomes, and the skill must distinguish them:

- **Deliberate boundary rename** -> record as an inline bare **alias** on the
  concept entry. Example: the public feed re-expresses the execution price in FIX
  vocabulary (`trade_price` -> `last_px`). That is intentional; the dictionary
  documents it, it does not flag it for change. (If the team instead unifies the
  name across the boundary -- as the quantity stages now share `order_qty` /
  `leaves_qty` / `last_qty` between engine and feed, differing only in strong type
  -- the concept becomes one term carried by both domains, with no alias.)
- **Accidental divergence** (the same concept named inconsistently with no
  deliberate reason) -> document the current state factually, and flag it in
  `DICTIONARY-report.md` as a unify-or-keep decision for the human. The skill
  does not rename code; it surfaces the choice.

The skill cannot always tell which is which. Default to recording the alias and
raising it in the report when intent is unclear. Let the human decide.

## Output formats

Model the precise shapes on the index skill's "Output format" sections, adapted
to vocabulary:

- **Root `DICTIONARY.md`**: a short framing paragraph that states what the file
  is (reference material, scope, version-independence), a "how to read an entry"
  note naming the schema fields, then the entries grouped by theme (identity,
  order attributes, quantities, prices, matching/event stream, etc.). No
  cross-domain-naming section and no maintenance section: a rename shows up as a
  bare alias on the concept entry, and maintenance rules live in `AGENTS.md`, not
  the glossary. The theme groups are `##` headings and each term is a `###`
  heading, so GitHub renders a usable section structure and every term gets a
  linkable anchor. Cross-references between entries are real anchor links (see
  entry schema).
- **Per-module `DICTIONARY.md`** (only when earned): title, back-link to the
  root (`Part of the [project dictionary](../../DICTIONARY.md).`), the module's
  genuinely local terms, and the inbound-translation table for the seam it
  consumes.
- **`AGENT_DICTIONARY.md`**: a compressed, always-loaded glossary for agents.
  Include the domain flow, canonical identity/order terms, order attributes,
  quantity aliases, and matching/event-stream vocabulary. Keep it terse enough
  to replace loading the full dictionary into every agent session. Add a
  sentence that vocabulary changes update both `DICTIONARY.md` and
  `AGENT_DICTIONARY.md`.
- **`DICTIONARY-report.md`**: grouped by category -- ambiguities, divergences
  (unify-or-keep), README/code conflicts (both sides quoted), decisions, and
  skipped. Keep empty sections with a "none" note so the human knows the run
  checked.
- **`AGENTS.md` integration**: when the project has `AGENTS.md`, add
  `@AGENT_DICTIONARY.md` to the always-loaded context, describe full
  `DICTIONARY.md` as an on-demand drill-down, and add the sync instruction that
  `DICTIONARY.md` and `AGENT_DICTIONARY.md` change together when domain
  vocabulary changes.

Drafting follows the project's documentation conventions: have subagents consult
the `documentation` skill for structure and `writing-clearly-and-concisely` for
prose (active voice, no hedging, no filler). Avoid glyphs and icons; plain text
only, including in any ASCII trees or tables.

### Navigation and rendering

The dictionary is markdown, read through GitHub's rendered view. Navigation uses
what markdown and GitHub already give: heading anchors for jump-to-term, the
rendered section structure for grouping, browser find for search, and the
intra-document cross-reference links above for following relations between terms.
The skill produces no separate HTML view and no generated site; the markdown is
both the source the agent imports and the artifact a human reads. Keep heading
text stable, since a renamed heading changes its anchor and breaks inbound
cross-reference links -- the verification phase checks for this.

## Modes and workflow

Mirror the index skill exactly here -- same three modes, same precedence
(explicit user instruction over project state), same working-folder spine under
`/tmp`, same parallel discovery, same verification-then-report:

- **Full**: no root `DICTIONARY.md`, or the user asks to regenerate. Surface all
  terms, write the root file, `AGENT_DICTIONARY.md`, any earned module files,
  the report, and the `AGENTS.md` wiring when present.
- **Scoped**: the user names modules or a term set. Re-surface only those;
  splice the root only where entries changed.
- **Incremental**: root `DICTIONARY.md` exists; use git to find the
  vocabulary-bearing files changed since it was last committed (the per-domain
  `types.hpp`, `messages.hpp`/`events.hpp`, state structs, and the boundary
  converters -- a changed converter can introduce or retire an alias even when
  no type changed), derive the affected terms, and run scoped against them.
  Produce a changes report. Keep the system-overview framing sticky. When any
  root or module dictionary entry changes, refresh `AGENT_DICTIONARY.md` if its
  compressed vocabulary is affected.

Phases, parallelized one subagent per domain (use `dispatching-parallel-agents`
when the source does not fit one context): working folder -> detect domain
modules and locate the vocabulary-bearing files and converters -> discover terms
-> draft and assemble -> verify. Every phase writes its full output to the
working folder; subagent prompts name the exact file to write. Verification
checks: every per-module file back-links and corresponds to a real module; every
"carried by" type exists; no empty sections; the root states every shared
concept once; every intra-document cross-reference link resolves to a real
heading anchor (no dangling `related`/`aliases`/`not to be confused with` link);
`AGENT_DICTIONARY.md` is present and names only terms backed by the full
dictionary; and `AGENTS.md`, when present, loads `AGENT_DICTIONARY.md` rather
than the full dictionary and states that the two dictionary files stay in sync.

Manual review gate: the skill drafts; the human reviews and edits before the
dictionary is treated as ground truth. State this explicitly, as the index skill
states its verification phase.

## Reference codebase: concrete material for development and evals

`/home/msi/repos/matching-engine` is a clean, small target. Its hand-written
root `DICTIONARY.md` is the gold output -- diff your skill's output against it.
The vocabulary, as it stands, so you can sanity-check term surfacing and build
realistic evals:

Shared concepts (each domain owns its own `types::` version): `symbol` (an
8-char fixed string; the field is named `symbol` in all three domains), `order`,
`side` (buy/sell), `price`, `quantity`, `user`/`user_id`,
`order_id`/`user_order_id`, `order_type` (limit/market), `time_in_force`
(day/ioc), and the engine's `order_key` (user_id + order_id).

Quantity stages: `order_quantity` (the size submitted on a new order), and the
shared engine/feed names `order_qty` (size that rests after any immediate fill),
`leaves_qty` (residual after a partial fill), and `last_qty` (size filled in a
match).

Matching and the event stream: `maker`/`taker`, `aggressor_side`, `resting
order`, `book delta` (order_added/order_updated/order_removed), `trade`/`trade
tape`, `engine_event`, `order_book` and `top of book`/`best bid`/`best ask`.

The instructive divergences (your skill must handle every kind):

- **A genuine boundary alias**: the execution price is `trade_price` in the
  engine and `last_px` on the public feed, performed by the `project*` converter
  in `market_data`. This is the one surviving cross-boundary rename; record it as
  a bare alias on the concept entry, not as a problem.
- **A name unified across the boundary**: the quantity lifecycle stages
  (`order_qty` on the add, `leaves_qty` on an update, `last_qty` on a trade) now
  use the same names in `matching_engine` and `market_data`, differing only in
  the strong type each domain owns (`types::quantity` vs `types::order_qty` and
  friends). Each is a single term carried by both domains, with no alias. The
  skill must not invent an alias for a name the domains share.
- **A README/code conflict worth flagging**: the repo README says the public
  market_data feed never carries identity, but the projected book-delta messages
  currently carry `user`/`user_order_id`. A good run documents what the messages
  carry, and flags the discrepancy in `DICTIONARY-report.md` rather than papering
  over it. This is an ideal eval assertion -- it tests whether the skill catches
  intent-vs-code drift.

Note one historical detail for realism: this repo recently unified an
`instrument` field name to `symbol`, so the type and field now agree
(`types::symbol symbol`). A dictionary run today should produce `symbol` as a
single concept with no divergence -- useful as a negative check (the skill should
not invent an `instrument`/`symbol` alias that no longer exists).

## Suggested eval prompts

Realistic, the kind of thing the human would actually type. Develop assertions
around the points above.

1. "Build a domain dictionary for the matching-engine repo at
   `/home/msi/repos/matching-engine` -- I want a glossary of the domain terms
   across order_routing, matching_engine, and market_data." (Full mode. Assert:
   single root file, compact `AGENT_DICTIONARY.md`, no empty module files;
   `AGENTS.md` loads the compact file and keeps the full dictionary on demand;
   `symbol` is one concept with no alias; `last_px` is recorded as a bare alias
   on `trade_price`/`price`, while the quantity FIX names `order_qty` /
   `leaves_qty` / `last_qty` are terms carried by both `matching_engine` and
   `market_data` (not aliases); `carried by` names types and domains, not field
   paths; no cross-domain-naming or maintenance section; the report flags the
   market_data identity question. Diff against the existing `DICTIONARY.md` and
   `AGENT_DICTIONARY.md`.)
2. "I just renamed a field and added an enum in matching_engine -- refresh the
   dictionary." (Incremental mode. Assert: it diffs the vocabulary-bearing files
   since the last commit, touches only affected terms, and writes a changes
   report.)
3. "Add a dictionary just for the market_data module." (Scoped mode. Assert: it
   only emits a module file if market_data has earned local vocabulary;
   otherwise it explains why the root file still carries everything.)

## Deliverables

- `skills/dictionary-cpp-codebase/SKILL.md`
- `skills/dictionary-cpp-codebase/references/output-template.md` -- a worked
  example of the root file, `AGENT_DICTIONARY.md`, an earned per-module file,
  the `AGENTS.md` wiring, and the report, against a realistic layout (model on
  the index skill's `references/output-template.md`).
- `evals/evals.json` and the eval workspace, per the `creating-skills` process.

Confirm the name and the scope-detection approach with the human, run the evals,
and put the results in front of them before iterating.
