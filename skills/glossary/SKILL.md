---
name: glossary
description: >-
  Generate or update a domain glossary (GLOSSARY.md) for a codebase -- the
  ubiquitous-language layer that gives a team and its agents one shared,
  consistent vocabulary for the domain. Use this skill whenever the user wants a
  glossary, a domain dictionary, a terms list, a ubiquitous-language reference,
  or wants to define, standardize, or document the domain terms and naming in a
  codebase -- in any language (C++, Python, TypeScript, ...) -- even if they
  don't say the word "glossary". It surfaces terms from the code's types,
  messages, and boundary translations, aligns each definition with the field's
  authoritative glossaries, and writes a flat compact GLOSSARY.md plus a reviewer
  report. Not for navigation maps (use an index skill), per-field data
  dictionaries, READMEs, or ADRs.
license: MIT
---

# Build a Domain Glossary

Walk a codebase and produce a domain glossary: the ubiquitous-language layer
of its docs, in the domain-driven-design sense. The glossary gives the team and
the agents one shared language for the domain, keeps naming consistent so one
concept wears one name, and anchors agent context in domain terms.

It is reference material in the Diataxis sense -- neutral, factual, built for
quick lookup, no narrative. It is a single compact file: a flat, grouped list of
terse one-line entries, small enough to load into agent context and complete
enough to be the human reference. It does not split into a verbose "full" file
plus a compact "agent" file; one file serves both.

This skill is the glossary counterpart to an index skill. An index is a map --
it points at *where things live*. A glossary is a dictionary -- it says *what the
domain words mean*. They share a spine (modes, working folder, parallel
discovery, verification-then-report) but produce different artifacts.

## A glossary, not a data dictionary

Each entry defines what the term *is* and stops there. The glossary states
meaning; the code states representation and usage. It does not record the type
that carries the concept, the field width, the per-message field paths, the
modules a term appears in, or how the term is used elsewhere -- those churn,
drift, and duplicate what the code already owns.

The litmus test: `symbol` is "an alias that uniquely represents a tradable
product," not "traded instrument; an order book holds one symbol." The good
version captures the essence -- an alias, uniqueness, a tradable product -- and
stops. The bad version drags in the order book; that fact belongs to the
definition of *order book*, not *symbol*. Otherwise every term ends up
redescribing every place that uses it, and the glossary has infinite surface
area.

## Define the concept, not the mechanism

Define a term -- and write the framing paragraph -- by what it *is* and what it
is *for*, not by how it works. Do not describe the steps, the order of
operations, the flow, or the components an input passes through. State the
concept's purpose and the capabilities it provides, and stop.

Three reasons this matters:

- Mechanics drift and are often configurable, so a flow description is fragile
  and quickly wrong.
- Describing mechanics invites factual errors: the more operational detail a
  one-line definition claims, the more chances it has to be wrong.
- A lookup wants meaning, not implementation. The reader who needs the mechanism
  reads the code; the glossary gives them the concept.

**Framing paragraph: capabilities, not a pipeline trace.** Bad, tracing a
configurable pipeline: "...accepts normalized order requests, routes them
through a protocol-agnostic pipeline to venue adapters, checks them against
per-account risk limits before they leave, and tracks the order lifecycle,
positions, and P&L." The routing pipeline is configurable -- stages such as the
firewall may be skipped -- so the flow is not even stable. Good, naming
capabilities: "...provides normalization of inbound and outbound messages,
hierarchical pre-trade risk checks, and order-lifecycle, position, and P&L
tracking."

**Entry: the concept, not the steps.** Bad (mechanism, and factually wrong --
the firewall does not amend):

```
**Firewall**\
The pre-trade risk component that accepts, amends, or rejects each order request
before it reaches the venue.
```

Good (what it is and does, conceptually):

```
**Firewall**\
The pre-trade risk component that evaluates an order against configured risk
limits and either allows or rejects it.
```

## First step: identify the domain (and subdomain)

Before any term work, establish what the application's domain is. Read
`README.md`, `docs/`, and `AGENTS.md` where present to determine the field the
system operates in -- trading, clinical care, logistics, audio, quantitative
research, data reconciliation, and so on -- and, in a larger multi-module repo,
the subdomain each module occupies.

This step is load-bearing for everything after it:

- the domain decides which authoritative external glossaries to consult;
- the subdomain decides which vocabulary each module owns;
- the domain and subdomain labels become the `Domain context:` line and the
  framing sentence in the assembled glossary.

Do not start surfacing terms until the domain is named. Record the identified
domain and subdomains as a short label list at the top of the working notes so
later phases share the framing and the assembly phase can lift them verbatim
into the header.

## What the skill produces

A doc tree parallel to the README tree (orientation prose) and any INDEX tree
(navigation map):

- **Root `GLOSSARY.md`** at the project root -- the application-wide glossary:
  every concept shared across subdomains, stated once. This is almost always the
  whole output.
- **Per-subdomain `<module-path>/GLOSSARY.md`** -- only when a module has earned
  one: it owns vocabulary genuinely local to that subdomain, which the root
  should not absorb. Per-subdomain files back-link to the root. Do not create
  empty module files; bias hard toward the single root file.

The two levels form one hierarchy with a single allocation rule: a term shared
across subdomains lives at the root and is stated once there; a term only one
subdomain uses, and that a reader of another subdomain would never need, lives
in that subdomain's file. **When in doubt, promote to the root** -- one source of
truth beats a term duplicated across module files. A subdomain file never
redefines a root term; it adds only what is local to it. Most repos are a single
root file; a per-subdomain file is the exception a large, genuinely partitioned
domain earns.

It also writes a sibling **`GLOSSARY-report.md`** at the project root for the
human reviewer: ambiguous terms, cross-boundary name divergences worth a
unify-or-keep decision (with the concrete code-name mapping the glossary body
deliberately omits), README/code conflicts about what a term means, terms whose
definition leaned on an external glossary (with the source), and anything
deliberately left out. The glossary is for downstream agents and humans alike;
the report is for the human.

When the project wires docs into agents via `AGENTS.md`, the skill points that
import at `GLOSSARY.md` directly; there is no separate agent-only glossary file.

## What it is for, and what it is not

One source of truth per concern. The glossary defines concepts; it does not
restate what other artifacts own. It is not the rulebook (`AGENTS.md`), not the
rationale (ADRs), not the orientation prose (README), not the navigation map
(INDEX), and not a per-field data dictionary with types, constraints, and
storage detail. An entry may, *in the report*, point to the ADR that explains a
translation; it does not reproduce it.

This skill does not:

- write ADRs, READMEs, or design docs;
- invent definitions or conventions;
- restate rationale;
- document foundation/tooling libraries that are out of scope;
- rename code (it surfaces naming questions; the human decides).

It may update `AGENTS.md` only to wire the glossary into agent context: load
`GLOSSARY.md`, and state the rule that vocabulary changes update it. It surfaces
and defines domain terms -- nothing else.

## Scope

- **Domain modules only.** Foundation and vocabulary libraries (generic
  containers, logging, an event loop, a result type, build tooling) are
  infrastructure, not domain, and stay out. Detect domain modules from the
  project layout (subdirectories of `src/`, top-level packages, the structure
  `AGENTS.md` / ADRs describe). Let the user scope explicitly when the split is
  not obvious.
- **Domain-level, version-independent terms.** A term belongs to the domain, not
  a version or an implementation variant. Where a repo keeps versioned `vN/`
  folders, benchmark variants, or generated code, those are implementation
  detail: a `GLOSSARY.md` lives at the module root (or the project root), never
  under a `vN/` folder. The term is version-stable.

## How meaning is derived

Two derivation sources feed every definition. **The codebase says which terms
exist and how this repo wires them; the domain says what each term actually
means.** A definition grounded only in the code is self-consistent but may drift
from the field; a definition grounded only in the field may not match what this
repo built. Use both.

### 1. The codebase

Surface terms from these source kinds, in priority order. The kinds are
language-agnostic; the concrete files differ per language. Read the bullets for
your language and treat the rest as analogues.

1. **Type and vocabulary definitions** -- where the language declares the
   domain's named types, enums, and constants. These name the primary terms, and
   **enum values are part of the term -- give them inline.**
   - C++: `types.hpp` per domain, `enum`/`enum class`, strong-typed wrappers.
   - Python: dataclasses, `Enum` subclasses, Pydantic models, `NewType`,
     `Literal`/`TypeAlias`, `TypedDict`, SQLAlchemy/ORM models, dbt `schema.yml`.
   - TypeScript: `type`/`interface`, string-literal unions, `enum`, Zod schemas.
2. **Message / event / schema / record definitions** -- field names are concept
   *usages* and the place a cross-boundary rename shows up.
   - C++: `messages.hpp` / `events.hpp`, state structs.
   - Python: request/response models, table columns, protobuf/avro/JSON schemas,
     API response shapes.
3. **Boundary and translation code** -- functions that convert one domain
   representation into another (constructors, mappers, adapters, ETL transforms,
   serializers, e.g. a `make_order_state` or a `project*` projector). These are
   the authoritative record of which upstream concept maps to which downstream
   name. **Read the implementation in full, not just signatures** -- a rename
   lives in the body.
4. **Module READMEs and docstrings** -- prose definitions to compress. When a
   README claim contradicts the code, resolve intent from the code, write the
   present-reality definition, and record the conflict in the report with both
   sides quoted.

### 2. The domain and its authoritative glossaries

Once the domain is identified, launch research agents to look up the recognized
glossaries for that field and align each definition with the established industry
meaning, so the glossary is consistent with the field, not merely with itself.

- Trading: NASDAQ, CME Group, the FIX protocol field dictionary (FIX is the
  authority for quantity and price terms -- OrderQty, LeavesQty, LastQty, LastPx).
- Clinical: SNOMED CT, LOINC, specialty bodies.
- Logistics: Incoterms, carrier standards.
- Other fields have their own authorities; find them.

Prefer the authoritative phrasing; aim for the terseness of NASDAQ's definition
of a symbol: "an abbreviation assigned to a security for trading purposes."
Record in the report which terms leaned on an external source and which source. A
term genuinely local to the repo (an internal event type, a project-specific
pipeline stage) will not appear in any external glossary; define it from the
codebase.

### Decompose composite terms

A composite term implies its components, and each component is its own entry.
"Aggressor side" requires both "aggressor" and "side"; "best bid" requires "bid".
Surface the atomic vocabulary, not only the compound, so a reader can look up the
part they do not know. When surfacing terms, split every multi-word concept into
its parts and check each part has an entry.

### Surface domain acronyms and proper names

Protocol and standard names, venue and feed codes, and vendor or component
shorthand are first-class terms -- they are exactly what a newcomer cannot
decode. Surface them, expand the abbreviation, and define it conceptually.
Trading examples: `FIX`, `SBE`, `BOE`, `UMDF` (protocols and message encodings),
`B3` (a venue), and product or component codenames. Keep their canonical casing
(`FIX`, not `fix`) -- the proper-casing rule for headwords never lowercases an
acronym or a proper name.

### Inclusion filter: a glossary, not an English dictionary

Include a term only when its domain meaning diverges enough from plain English to
warrant an entry. Keep genuine jargon, acronyms, and precise domain terms
(`aggressor`, `leaves quantity`, `FIX`). Drop words used in their ordinary
English sense, even when they appear in identifiers: a `tie` meaning "two
securities sharing the same score" and an `untie` step that "perturbs tied
scores" are ordinary English (and `untie` is mechanism, not a concept) -- leave
them out. This also drops terms whose meaning is just the everyday technical word
with no domain-specific twist: in a protocol glossary, `logon` and `logout` say
exactly what they are -- omit them. The test: would a competent newcomer to the
domain, already fluent in English, have to look this up? If not, it is not a
glossary entry.

## Entry schema

Each entry is a headword on its own line, then its essential definition on the
next line, with a blank line between entries:

```
**Term**\
Essential definition.

**Next term**\
Essential definition.
```

The trailing backslash is a Markdown hard line break, so the headword renders on
its own line above the definition.

- **headword** -- the concept in plain-English words, spaced, not a type name
  (`engine event`, not `engine_event`). Use proper casing: capitalize the first
  word, and keep acronyms and proper names in their canonical casing wherever
  they appear (`Order type`, `Best bid`, `FIX session`, `B3 connectivity`,
  `SBE`). One entry per concept; do not give a concept two names (no
  "user / user_id").
- **essential definition** -- one sentence stating what the term *is*, derived
  from the codebase and aligned with the domain's authoritative glossary. It is
  self-contained and conceptual: it defines the term itself, by what it is and
  what it is for -- not where it is used, what consumes it, or the steps by which
  it is mechanically processed (see "Define the concept, not the mechanism").

There are no anchor links, no `related` field, no `not to be confused with`
field, and no "carried by" field; the compact list carries definitions only.
Representation is deliberately omitted.

### Be concise

The root glossary is loaded into agent context on every run, so every word costs
tokens on every load. Keep each definition to the concept itself, in as few words
as carry the meaning.

**Do not enumerate.** A definition states what the term is, not the full set of
values it can take or fields it contains. Name the concept; add one or two
illustrative examples only when they aid understanding and the definition is not
already long, never the whole list. The glossary is the map, not the terrain: it
points at the concept, it does not reproduce the value set the code already
holds.

- Bad (lists every value): "how long an order stays in effect: a day order lasts
  until the end of the session, an immediate-or-cancel order fills what it can at
  once and cancels any remainder, a fill-or-kill order must fill in full or
  cancel, good-till-cross rests until it would cross, ..."
- Good (the concept): "how long an order remains active before it expires."
- Bad (lists every field): "the static record of a security: symbol, asset,
  security type and subtype, contract multiplier, tick size, and venue."
- Good: "a security's static descriptive record, such as its symbol and tick
  size."

The same restraint applies to mechanism and components (see "Define the concept,
not the mechanism"): "a control that stops an account's orders from trading
against each other" needs neither the id that identifies it nor the
cancel-instruction that governs it.

Cross-boundary naming differences **do not appear in the glossary body**. The
glossary defines each concept once under its canonical name; renames and
inconsistencies go in the report.

### Ordering

Sort entries alphabetically by term. A glossary is a lookup reference: a reader
who knows the word but not the meaning scans for it, and alphabetical order is
the only ordering they can predict without reading the whole file. Do not order
by concept, by pipeline stage, or by the order terms were discovered. When the
glossary is grouped (see below), sort alphabetically *within* each group.

### Grouping

**Do not group by default.** A small glossary is a single flat list. Introduce
`##` groups only when the term count is large enough that coarse buckets aid
lookup, and keep any buckets coarse: if a term plausibly belongs in two groups,
the groups are too fine -- collapse them. A calibration-sized glossary uses no
groups at all.

## Divergence handling

The glossary body keeps one essential definition per concept and carries no
naming table. Cross-boundary naming differences are recorded in
`GLOSSARY-report.md`:

- **Deliberate boundary rename** (e.g. the execution price is the engine's trade
  price and prints on the public feed in FIX vocabulary as the last price) -> the
  glossary defines the concept once under its canonical name; the report records
  the concrete code-name mapping.
- **A name unified across the boundary** -> a single concept, one entry, nothing
  special to say. Do not invent a divergence for a name the domains share.
- **Accidental divergence** -> define the concept once under its canonical name,
  and flag it in the report as a unify-or-keep decision. The skill does not
  rename code; it surfaces the choice.

The skill cannot always tell deliberate from accidental. Default to defining the
concept once and raising the naming question in the report when intent is
unclear.

## Output formats

See `references/output-template.md` for a complete worked example -- the root
file, an earned per-subdomain file, the `AGENTS.md` wiring, and the report,
against a realistic layout. The shapes in brief:

**Root `GLOSSARY.md`:**

```
# <System or domain name>

<one short framing paragraph: what the system is, at a high level>

Domain context: <domain and subdomain labels>.

**Term**\
Essential definition.

**Next term**\
Essential definition.
```

- **Title** names the system or domain (`# Matching Engine`, not `# GLOSSARY` --
  the file is a glossary, but its heading names the subject).
- **Framing paragraph** reads like a README's opening sentence: a high-level
  description of what the system is, naming the major capabilities at the level a
  newcomer needs to place the terms. It does *not* trace the pipeline or data
  flow, describe the architecture, explain what the glossary file is, or name
  source libraries, folder layout, or the build/lab structure -- those are too
  specific and drift (see "Define the concept, not the mechanism").
- **`Domain context:` line** lists the domain and subdomain labels established in
  the identify-the-domain phase, grounding the framing in the same terms.
- Then the entries, as a flat list. No per-entry fields, no links, no
  cross-domain-naming section, no maintenance section, and no groups unless the
  term count makes coarse buckets worthwhile.

**Per-subdomain `GLOSSARY.md`** (only when earned): a title naming the subdomain,
a framing paragraph that says what the subdomain is at a high level the same way
the root frames the whole system, a back-link to the root
(`Part of the [project glossary](../../GLOSSARY.md).` -- adjust the relative depth
to the module's actual location), and the subdomain's genuinely local terms in
the same compact form.

**`GLOSSARY-report.md`:** grouped by category -- ambiguities, divergences
(unify-or-keep, with the concrete cross-boundary name mapping), README/code
conflicts (both sides quoted), external-source notes (term -> glossary used),
decisions, and skipped. **Keep empty sections with a "none" note** so the human
knows the run checked.

**`AGENTS.md` integration:** when the project has `AGENTS.md`, add `@GLOSSARY.md`
to the always-loaded context and the sync instruction that `GLOSSARY.md` changes
when domain vocabulary changes. Reference any per-subdomain files as on-demand
drill-downs.

Drafting follows the project's documentation conventions: have subagents consult
the `documentation` skill for structure and `writing-clearly-and-concisely` for
prose (active voice, no hedging, no filler). Plain text only -- no glyphs or
icons, including in any ASCII trees or tables.

The glossary is markdown read through a rendered view. Navigation uses what
markdown gives: `##` theme headings for grouping and browser find for search. The
skill produces no separate HTML view and no generated site.

## Modes and workflow

Three modes, with explicit user instruction taking precedence over project state:

- **Full**: no root `GLOSSARY.md`, or the user asks to regenerate. Identify the
  domain, surface all terms, write the root file, any earned subdomain files, the
  report, and the `AGENTS.md` wiring when present.
- **Scoped**: the user names modules or a term set. Re-surface only those; splice
  the root only where entries changed.
- **Incremental**: root `GLOSSARY.md` exists; use git to find the
  vocabulary-bearing files changed since it was last committed (the type/enum
  definitions, the message/event/schema definitions, state structs, and the
  boundary translators -- a changed translator can introduce or retire a
  cross-boundary rename even when no type changed), derive the affected terms,
  and run scoped against them. Produce a changes report.

### Phases

Parallelized one subagent per domain module (use `dispatching-parallel-agents`
when the source does not fit one context; dispatch all subagents in a single
message so they run concurrently):

1. **Working folder.** Create `/tmp/glossary-<YYYYMMDD-HHMMSS>-<short-id>/` and
   use it as the spine of phase-to-phase communication. Every phase writes its
   full output there; subagent return messages only compress what the agent
   learned. Every subagent prompt names the exact file the subagent must write,
   so assembly is a predictable glob. Suggested layout:
   ```
   /tmp/glossary-<run-id>/
   |-- manifest.md            skill name, start time, args, project root, mode
   |-- run.log                append-only log of phase events
   |-- domain.md              identified domain + subdomain labels (load-bearing)
   |-- sources/<module>.md    located vocabulary-bearing files + translators
   |-- research/<domain>.md   authoritative-glossary findings
   |-- terms/<module>.md      surfaced terms + draft definitions
   `-- report-fragments/<module>.md
   ```
   The folder is not cleaned on completion; final artifacts go to the repo
   (`GLOSSARY.md`, `GLOSSARY-report.md`, any `<module>/GLOSSARY.md`).
2. **Identify the domain and subdomains** from `README.md`, `docs/`, and
   `AGENTS.md`. Write `domain.md`. Do not proceed until the domain is named.
3. **Locate the vocabulary-bearing files and translators**, and **launch
   research agents to look up the domain's authoritative glossaries.** These run
   in parallel -- code location and domain research do not depend on each other.
4. **Surface terms** (decomposing composites) and **write essential,
   domain-aligned definitions.** One subagent per module; each writes its terms
   to `terms/<module>.md` and findings to `report-fragments/<module>.md`.
5. **Assemble** the single compact root file (plus any earned subdomain files)
   from the working folder, the report from the fragments, and the `AGENTS.md`
   wiring when present.
6. **Verify** (below), then stop and report.

### Verification

Before declaring done, check:

- the identified domain is recorded;
- the root file is titled with the system/domain name (not `GLOSSARY`), opens
  with a high-level framing paragraph that says what the system is (not the
  pipeline, the architecture, the glossary file, or the build/lab structure) and
  a `Domain context:` line whose labels match the identified domain and
  subdomains, and the framing names no source libraries or folder layout;
- the framing paragraph names the system's capabilities conceptually and does
  not trace the data flow or pipeline (no "routes X through Y to Z" description);
- every per-module file opens the same way for its subdomain, back-links to the
  root, and corresponds to a real module;
- no empty sections;
- the root states every shared concept exactly once;
- entries use the headword-on-its-own-line format (a bolded headword, a hard
  line break, then the definition), with proper casing and acronyms/proper names
  in canonical casing;
- entries are sorted alphabetically by term (within each group, when grouped);
- every composite term's components have their own entries;
- domain acronyms and proper names are surfaced, expanded, and defined;
- no entry is a plain-English word used in its ordinary sense (the glossary is
  not an English dictionary);
- each definition is self-contained and conceptual: it defines what the term is
  and is for, not its consumers, and not the steps, flow, or order of operations
  -- and makes no claim a different configuration would falsify;
- `AGENTS.md`, when present, loads `GLOSSARY.md` and states the sync rule.

If verification fails, stop and report -- do not hand-wave. The glossary is
consumed as ground truth by downstream agents.

### Manual review gate

The skill drafts; the human reviews and edits before the glossary is treated as
ground truth. State this explicitly when handing off: the report exists so the
reviewer can confirm the ambiguities, divergences, and external-source calls the
run made.

## Reference files

- `references/output-template.md` -- a complete worked example of the root
  `GLOSSARY.md`, an earned per-subdomain `GLOSSARY.md`, the `AGENTS.md` wiring,
  and `GLOSSARY-report.md`, so a subagent drafting the glossary has the target
  shape in front of it.
