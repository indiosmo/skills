# Describe the thing before choosing its name

A useful name lets a reader connect an expression to the concept the program
implements. Start by describing that concept and the evidence for it. This
page supplies the distinctions needed to decide whether a proposed change
improves a name or changes the underlying design.

## Separate meaning, identity, and wording

The following vocabulary is a working adaptation of terminology research to
software. The ISO 704 preview distinguishes objects, concepts, definitions, and
designations; the software applications here are this guide's engineering
judgment. See [CON-001](evidence.md#con-001) and the
[inspected source](sources.md#con-iso704-preview).

| Term | Working meaning | Software example |
| --- | --- | --- |
| Concept | A meaning with distinguishing characteristics | A file awaiting a scheduled import |
| Referent | The particular thing a name denotes in this context | The file selected for this import attempt |
| Role | What a thing contributes to an operation or relationship | The same file can be an import source and an archive entry |
| Definition | An explanation that distinguishes the concept from nearby concepts | An import source is a file whose contents an import operation reads |
| Source-code identifier | A token used to name a program entity within language binding rules | The parameter `source_file` |
| Persistent identifier | A value intended to identify something across a stated lifetime and namespace | An import record key retained across process restarts |
| Label | Wording presented to a reader | `September import` in an operations screen |
| Alias | An additional name that resolves to the same target within a stated scope | A retained command spelling routed to the same operation |
| Context | Information that determines how a name is understood | The import module, parameter type, caller, glossary, and public contract |

Record the lifetime and uniqueness boundary of a persistent identifier. A label
can change while the represented record retains its identity. Conversely, a
human-readable identifier can itself be a stable contract. Choose based on the
actual resolution and persistence rules. SKOS provides one specific model
separating resource identity and lexical labels; the W3C URI guidance also
allows meaningful stable identifiers. These are bounded examples, reflected in
[CON-007](evidence.md#con-007) and [COMP-011](evidence.md#comp-011).

An alias needs a target and resolution scope: a second spelling alone does not
establish equivalence. Before changing one, inspect the places that resolve or
store it. [API and schema naming](apis-schemas-and-configuration.md) and
[renaming](renaming.md) explain the resulting contract checks.

## Define the concept with the distinctions readers need

Write a plain sentence about purpose and behavior. Then test it with a nearby
case. For an import operation, does success mean that parsing completed, that
records passed validation, or that records were committed? Those outcomes can
justify different names even when all three implementations return a boolean.

A definition should make only the commitments the evidence supports. Gruber's
conceptual-design guidance motivates precise definitions with bounded
commitments; applying it to a naming brief is local judgment
([CON-006](evidence.md#con-006)). A small local value may need only a phrase.
A public state or operation benefits from explicit boundary cases, outcomes,
and lifecycle conditions.

Roles can change while the underlying entity persists. An import file can
become the archived copy of that input; whether these are one stored entity or
two requires the program's identity contract. Formal ontology distinguishes
role membership from enduring identity, which offers a useful question for
software modeling. Its formal taxonomy has its own assumptions; a class design
requires software evidence ([CON-004](evidence.md#con-004),
[CON-005](evidence.md#con-005)).

## Separate competing concepts before comparing words

Abstract descriptions often leave the thing's role open. "Coordinates work"
could describe deciding which work is eligible, arranging an execution order, or
running the work through completion. State the plausible responsibilities in
plain language and attach the available evidence to each. Treat missing facts
as questions or explicit hypotheses. A familiar architectural label can suggest
a hypothesis, but its implied behavior needs support from the actual proposal.

Identify the distinction that would change the abstraction: what it owns,
which decisions it makes, what persists, or how it relates to neighboring
objects. One concrete usage or boundary case may settle that distinction. For a
class, consider a creation, operation, and end-of-lifetime example; for a group,
consider what membership means and whether the group has an identity beyond its
current members. Choose only the examples needed to distinguish the live
interpretations. Follow [elicitation](elicitation.md#work-with-sparse-or-abstract-input)
when available evidence leaves that meaning open.

Keep conceptual alternatives separate from lexical alternatives. Two names for
the same supported responsibility can be compared for clarity. Names that imply
different responsibilities express a pending concept decision; score their
wording only after resolving or explicitly conditioning that decision. This is
local engineering guidance under [LOCAL-003](evidence.md#local-003) and
[LOCAL-004](evidence.md#local-004).

## Read the whole expression

Names obtain meaning from receivers, types, modules, argument labels, and nearby
statements. Compare these original use-site sketches, each intended to return
the same committed import record:

```python
import_record = import_repository.load(import_identifier)
import_record = load_import_record(import_identifier)
```

The receiver supplies the first call's storage context. The second function
spells out the returned concept for a reader who encounters it as an imported
function. Choose the form that fits the project's API and the context visible
to its readers. Inspect representative callers, including a caller outside the
implementation module when the symbol is exported.

Google C++ recommends scope-sensitive detail, and Swift emphasizes role and
clarity at use sites. These are attributed design conventions with ecosystem
conditions, recorded in [LANG-01](evidence.md#lang-01) and
[LANG-02](evidence.md#lang-02). They motivate checking the complete expression
rather than choosing an identifier from an isolated list.

## Separate semantic accuracy from surface form

`committed_import_count` and `committedImportCount` can express the same concept
under different casing conventions. `processed_count` could conceal whether
failed records are counted. Resolve the latter question through behavior; use
the project's language convention to settle the spelling.

Full words are this guide's default, with established domain abbreviations
appropriate in local scope ([LOCAL-002](evidence.md#local-002)). Empirical studies
support meaningful words in particular comprehension tasks, while findings for
familiar abbreviations differ from mechanically shortened names. Length alone
cannot settle a choice. See [EMP-002](evidence.md#emp-002),
[EMP-003](evidence.md#emp-003), and [the study explanations](empirical-research.md).

Within a stated context, consistent terms help readers track concepts. Use the
formal naming model as a review question: are two spellings preserving a useful
distinction, and does one spelling hide two meanings? The evidence supports a
scoped modeling discipline, with search completeness requiring separate
inspection of bindings and aliases ([EMP-005](evidence.md#emp-005)).

## Recognize a design question

Suppose `prepare_import` parses a file, commits accepted records, and sends a
completion email. Renaming it to `parse_import` would promise only part of its
observed behavior. A name such as `run_import` may accurately describe the
coordinating operation if the surrounding API defines that lifecycle. Splitting
the operation into parsing, committing, and notification is a separate design
proposal with its own callers and failure behavior to consider.

Difficulty naming a thing is a reason to inspect its responsibilities. The
inspection may reveal a coherent orchestration role, mixed responsibilities, or
simply missing context. A vague word alone proves none of those diagnoses
([EMP-008](evidence.md#emp-008)). Preserve established effects, state transitions,
units, and truth conditions during a rename; handle proposed behavior changes
under their own scope ([COMP-015](evidence.md#comp-015)).

Continue with [domain vocabulary](domain-vocabulary.md) to establish the words,
or [elicitation](elicitation.md) to resolve the concept. Once meaning is settled,
[candidate generation](candidate-generation.md) develops names and
[contextual validation](contextual-validation.md) checks their fit separately.
