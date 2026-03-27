---
name: writing-docs
description: >-
  Guidelines for writing, updating, and reviewing project documentation -- READMEs, architecture
  overviews, runbooks, ADRs, guides, and inline code comments. Use this skill whenever asked to
  create, update, or review documentation of any kind, including when the user says "document this",
  "write a README", "add a runbook", "explain how X works", or wants to improve existing docs.
  Also use it when producing documentation as part of a larger task (adding a new module, finishing
  a feature) even if the user does not explicitly mention documentation. Triggers on: document,
  README, runbook, architecture doc, ADR, guide, explain, write docs, update docs, review docs,
  how does this work, add documentation.
---

# Writing Documentation

## Core principle: document what the code cannot tell you

Code is the authoritative source for implementation details -- config field names, exact routing
conditions, specific metric names, concrete file paths. Documentation exists to provide what code
alone cannot: the **why**, the **mental model**, how pieces **relate to each other**, and the
high-level narrative that helps someone understand the system without reading every file.

When documentation restates implementation details, it creates two sources of truth that inevitably
drift apart. The code always wins that race, leaving the docs as a misleading artifact. Instead,
give the reader enough conceptual grounding that when they do look at the code, they already
understand its purpose and context.

## Structure: general to specific

Documentation reads top-down, from broad context to narrow detail. A reader should be able to stop
at any depth and walk away with a useful understanding proportional to how far they read.

1. **Opening summary** -- what this thing is, why it exists, and the key concepts in a few
   sentences. Someone skimming should get the gist here.
2. **Conceptual sections** -- how the major parts relate to each other, data flow, architectural
   decisions. Use diagrams where they clarify relationships.
3. **Deeper sections** -- drill into each major part, but still at the level of explaining roles,
   relationships, and patterns rather than enumerating every field.

Avoid front-loading with directory trees, file listings, or tables of config values. Those belong
later (if at all) and only in generalized form.

## What belongs in docs vs. in code

**In documentation (README, runbook, architecture doc, guide):**
- What the system or component is and why it exists
- How data flows between components
- Architectural decisions and the reasoning behind them
- The general pattern for how things work, illustrated with one or two examples
- How to extend or add to the system (for example, "adding a new source" steps)
- Concepts that span multiple files or systems

**In code (as comments in source files, config headers, module docstrings):**
- What specific fields, metrics, or tags a particular file produces
- The exact schema or format of a specific output
- Implementation notes that only matter when reading that file
- Anything that must change in lockstep with the code it describes

When writing docs, if you find yourself listing every route, every field, or every config file by
name, that is a signal to step back. Either generalize (describe the pattern with one example) or
move those details into comments in the relevant source files.

## Document hierarchy: avoid restating what a sibling or child doc already covers

Just as a single document flows from general to specific, a tree of documents forms the same
gradient. The root README is the most general; subdirectory READMEs drill into their own area.
When a topic is covered in a child document, the parent should introduce the concept briefly and
point the reader there -- not restate the details.

Before writing or updating a document, check what the parent and child documents already say. If
the parent already explains a concept well, the child can reference it instead of repeating. If
the child covers something in depth, the parent should summarize in a sentence and link down. The
goal is that each piece of information has **one home**, and everything else points to it.

This applies across all documentation types. Runbooks should not restate architecture that lives
in a README. A README should not restate field-level details that live in code comments. An ADR
captures the decision once; other docs reference it rather than re-explaining the reasoning.

## Keeping docs accurate over time

Documentation that drifts from reality is worse than no documentation -- it actively misleads.
These heuristics help docs stay accurate as the codebase evolves:

- **Describe patterns, not instances.** "Each source gets its own config directory with a
  transform and a sink" survives adding new sources. A table listing all four current sources
  does not.
- **Use examples, not exhaustive lists.** A single concrete example illustrates the mechanism
  without committing to a complete enumeration that must be updated every time something is added.
- **Refer to code, do not transcribe it.** "See the header comments in each config file for the
  specific tags and fields" is better than copying those tags and fields into the README.
- **Generalize directory layouts.** Describe the structure and what each level contains, but do
  not list every individual file. The file listing is already available via the filesystem.

## Document types

### README

A README answers: what is this, why does it exist, and how do I get oriented?

Place a README in any directory that a newcomer might land in -- the project root, each major
module or service, and any directory whose purpose is not obvious from its name. Keep each README
focused on its own scope. The root README is the entry point; module READMEs explain their own
area.

**Structure for a root README:**
1. Project name and one-line description
2. Brief overview (what problem this solves, key concepts)
3. Getting started (setup, prerequisites, first run)
4. High-level architecture or repo layout (briefly, linking to deeper docs)
5. Common workflows or commands

**Structure for a module or directory README:**
1. What this module or directory is and why it exists
2. Key concepts and how the parts relate
3. How to extend or modify it
4. Links to deeper documentation if it exists

### Architecture Decision Records (ADRs)

ADRs capture the reasoning behind significant technical decisions. They are permanent records --
not updated after the fact but superseded by new ADRs if a decision changes.

**When to write one:** When a decision is non-obvious, has alternatives worth recording, or will
be questioned by a future developer who was not in the room.

**Format:**
```
# NNN. Title

**Status:** Proposed | Accepted | Deprecated | Superseded by [NNN]

## Context
Neutral description of the forces and constraints at play.

## Decision
What was decided, stated in active voice.

## Consequences
All outcomes -- positive, negative, and neutral.
```

Keep ADRs short (one to two pages). They are a "conversation with a future developer" -- write
in full sentences, include enough context that the decision makes sense without external knowledge.

### Runbooks

Runbooks are step-by-step operational procedures. They answer: how do I do this specific task?

**When to write one:** When a procedure involves multiple steps, touches production or shared
systems, or is performed infrequently enough that the steps will be forgotten between occurrences.

**Principles:**
- Lead with prerequisites (tools, access, environment)
- Number every step
- Include the exact commands to run, with placeholders for variable parts
- State what success looks like after each non-trivial step (expected output, status to verify)
- Keep the scope narrow -- one procedure per runbook

### Guides and references

Guides explain how something works or how to accomplish a class of tasks. References document
schemas, configuration options, or API surfaces. These are less common than READMEs and runbooks
but valuable when a topic is too large for a README section yet not a step-by-step procedure.

Organize guides by topic (for example, `error_handling.md`, `testing.md`). Include code examples
that show both the correct pattern and the pattern to avoid, with a brief explanation of why.

## Tone and style

Apply the `/writing-clearly-and-concisely` skill when drafting or editing documentation prose.
That skill provides concrete rules for clear, concise writing -- active voice, positive form,
omitting needless words, and other principles from Strunk's *Elements of Style*. Use it alongside
the guidelines below.

- Write in plain, direct prose. No marketing language, no filler, no throat-clearing ("It should
  be noted that...", "In order to...").
- Use the same terminology the codebase uses. If the code calls it a "transform", the docs call
  it a "transform" -- not a "processor" or "handler" or "middleware".
- Keep sentences short. If a paragraph exceeds four or five sentences, consider splitting it or
  moving some content elsewhere.
- Use imperative mood for procedures and instructions ("Run the setup script", "Add a new entry").
- Use present tense for descriptions ("The router dispatches events", not "The router will
  dispatch events").
- Avoid glyphs and icons. Use regular text.
- Avoid abbreviations. Prefer explicit names (`playbook_file`, not `pb_file`).

## Diagrams

Use diagrams when they clarify relationships, data flow, or architecture that would be tedious to
describe in prose alone. Do not add diagrams for simple structures that a few sentences can convey.

- **Mermaid** (`mermaid` fenced code blocks) is the default. It renders natively in GitHub
  markdown, stays inline as diffable text, and needs no exported images or build steps. Use the
  `/mermaid` skill when producing Mermaid diagrams.
- **ASCII art** is acceptable for simple flows where Mermaid would be overkill.
- Avoid binary image files (PNG, SVG) when a text-based diagram would do. Images cannot be
  diffed, are easy to forget to update, and require external tools.

## DO and DO NOT

**DO:**
- Explain the why behind decisions, architecture, and non-obvious patterns
- Start every document with a summary that gives the reader the gist in seconds
- Use one concrete example to illustrate a pattern instead of listing every instance
- Link to child or sibling documents rather than restating their content
- Put implementation details in code comments where they stay in sync with the code
- Check existing docs before writing -- extend or update, do not duplicate
- Match the project's existing documentation conventions (heading style, file placement, naming)

**DO NOT:**
- Transcribe code into documentation -- the diff will always be fresher
- List every file, field, route, or config value -- describe the pattern and give one example
- Front-load documents with directory trees, exhaustive tables, or boilerplate
- Write documentation that requires updating every time a new instance of something is added
- Use vague or generic language ("various components", "different things") -- be specific
- Add documentation for things that are self-evident from well-named code and types
- Create a new document when an existing one covers the same scope -- update it instead

**Example -- describing a pattern vs. listing instances:**

Bad (fragile, must be updated for every new source):
```markdown
## Sources
| Source | Config | Description |
|--------|--------|-------------|
| fix_gateway | sources/fix/config.toml | FIX protocol events |
| market_data | sources/md/config.toml | Market data ticks |
| risk_engine | sources/risk/config.toml | Risk calculation results |
```

Good (durable, survives adding new sources):
```markdown
## Sources

Each observed system gets its own directory under `sources/` containing a config file
that defines the collection pipeline. For example, `sources/fix/` handles FIX protocol
events. See the README in each source directory for specifics.
```

**Example -- explaining why vs. restating what:**

Bad (restates the code):
```markdown
The `validate()` function checks that `quantity > 0`, `price > 0`, and
`symbol` is not empty.
```

Good (explains the purpose):
```markdown
Orders are validated at the gateway boundary before entering the matching engine.
See `validate()` in `order.py` for the specific checks.
```

## Working with project-specific skills

This skill provides general documentation guidelines. Individual projects may have a companion
skill that adds project-specific conventions -- preferred diagram types, domain terminology,
directory layout rules, or doc templates. When a project-specific skill is present, follow
both: this skill for the general principles, and the project skill for local conventions.
Where they conflict, the project-specific skill takes precedence.
