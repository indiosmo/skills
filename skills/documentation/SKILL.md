---
name: documentation
description: >-
  Guidelines for writing, updating, and reviewing project documentation -- READMEs, architecture
  overviews, runbooks, ADRs, guides, and inline code comments. Use this skill whenever asked to
  create, update, or review documentation of any kind, including when the user says "document this",
  "write a README", "add a runbook", "explain how X works", "write an ADR", "document this
  decision", or wants to improve existing docs. Also use when producing documentation as part of a
  larger task (adding a new module, finishing a feature) even if the user does not explicitly mention
  documentation. Use it when a significant technical choice is being made and should be captured as
  an ADR, even if the user does not say "ADR" explicitly. Triggers on: document, README, runbook,
  architecture doc, ADR, decision record, guide, explain, write docs, update docs, review docs,
  how does this work, add documentation, record this decision, why did we choose X.
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

## Which document type?

Different situations call for different document types. Use this to decide:

| If the reader needs to...                              | Write a...   | Reference                        |
|--------------------------------------------------------|--------------|----------------------------------|
| Understand what something is and get oriented          | README       | `references/readme.md`           |
| Understand why a technical decision was made           | ADR          | `references/adr.md`              |
| Follow steps to perform an operational task            | Runbook      | `references/runbooks.md`         |
| Learn how something works or how to do a class of task | Guide        | See "Guides and references" below |

Some signals to help route:

- **"Why did we choose X?"** or a significant technical choice is being made --> ADR
- **"How do I set up / deploy / rotate / migrate X?"** --> Runbook
- **"What is this project / module / directory?"** --> README
- **"How does X work?"** --> Could be a README section (if it's about orienting someone to a
  component) or a guide (if it's about teaching a technique or pattern)

When in doubt, start with a README. Most documentation needs are orientation needs.

Read the corresponding reference file before writing that document type. Each reference file
contains the structure, conventions, and examples specific to that type.

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

## Guides and references

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
