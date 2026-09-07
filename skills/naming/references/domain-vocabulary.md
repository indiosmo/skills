# Establish the vocabulary of the domain

Choose words that practitioners use for the concept the software implements.
This page explains how to gather that vocabulary, preserve distinctions, and
handle disagreement between a project and an external source. Use the
[foundations](foundations.md) to separate the concept from its current spelling.

## Build a small evidence trail

Begin with the target declaration, its implementation, representative callers,
tests, and nearby documentation. Read applicable project instructions and the
project or subdomain glossary. Callers show how a term participates in the
model; a test can reveal the boundary hidden behind an attractive word.

Then consult an authoritative source for unfamiliar domain meaning: the
protocol being implemented, the relevant standards body's vocabulary, an
official API reference, or a practitioner glossary. Record the source's version
and scope beside the proposed definition. Prefer sources that govern the actual
integration over a broadly related industry description.

Separate observations: "the implementation accepts these states," "the glossary
defines this term," and "the intended contract is this." A conflict between them
needs a decision about the target behavior or boundary. Resolve facts from
available evidence first; ask a domain expert when intent or core meaning
remains material. This read-first procedure is [LOCAL-001](evidence.md#local-001).
Fowler's account of Evans's ubiquitous language supports developing model
vocabulary through discussion and concrete examples
([CON-002](evidence.md#con-002), [source](sources.md#con-fowler-language)).

## Preserve near-neighbors and boundaries

Treat apparent synonyms as candidates for investigation. Two terms can denote
one concept, overlapping concepts, or separate roles. Establish what would make
one applicable while the other is false. The following distinctions come from
the accepted domain sources; each still needs the project's representation and
contract to determine the identifier.

| Context | Distinction to preserve | Naming consequence |
| --- | --- | --- |
| Trading quote | Bid and ask denote buying and selling prices | Preserve the side; generic `price` needs enough enclosing context to identify it |
| Continuous trading | An aggressor matches resting orders and removes liquidity | Identify the incoming and resting roles before naming their prices; fee classifications need their own evidence |
| UN/CEFACT logistics model | Shipment concerns the trade grouping; consignment concerns the transport contract | Check which grouping a collection represents before substituting these terms |
| Audio processing | Frames contain channel samples; duration follows frame count and sample rate | Name the actual quantity; establish the measurement boundary of latency |
| FHIR R5 clinical data | An Observation can carry a measurement; a DiagnosticReport can group observations and context | Distinguish one result from a report containing results |

These scoped distinctions are recorded in [CON-008](evidence.md#con-008),
[CON-009](evidence.md#con-009), [CON-010](evidence.md#con-010),
[CON-011](evidence.md#con-011), and [CON-013](evidence.md#con-013), with primary
sources, inspected versions, and access limits linked from each claim.

For an original quote example, suppose `top_of_book` supplies both sides for one
instrument in the same currency and price unit. The desired result is the ask
minus the bid:

```python
bid_price = top_of_book.bid_price
ask_price = top_of_book.ask_price
spread = ask_price - bid_price
```

`spread` fits that stated calculation; `profit` would require additional facts
about trades and costs. Verify that the actual caller supplies the same
instrument, units, and both sides before endorsing this name. The terminology
comes from [CME's glossary](sources.md#con-cme-glossary); the scenario and
verification procedure are original local applications.

A bounded context is the part of a model within which a term has a coherent
meaning. The same word can be appropriate in two contexts with different
definitions. Fowler's explanation of bounded contexts supports making those
boundaries explicit ([CON-003](evidence.md#con-003)). Record the mapping where
data crosses a real boundary. Include any transformation or loss of detail.
Unifying spelling across contexts requires evidence that their concepts agree.

## Resolve conflicts deliberately

When code, a glossary, and a domain authority disagree, establish which contract
the target artifact serves. An external schema controls its field spelling;
internal code can use a domain term through an explicit mapping. A project term
with a clear, deliberate local definition may remain appropriate in that model.
An accidental inconsistency merits a correction after checking affected uses.

Keep the competing definitions and their evidence visible until that distinction
is settled. If the proposed correction would change interpretation of persisted
values or a public contract, assess it through [renaming](renaming.md). A source
with a different scope supplies context, not automatic authority to migrate the
project. The scoped consistency model and its limits are in
[EMP-005](evidence.md#emp-005).

## Use accepted abbreviations in their context

Default to full words. An abbreviation earns use when practitioners recognize
it and its local scope makes its meaning clear. For example, `http` is an
established protocol abbreviation, whereas shortening `authorization_request`
to `auth_req` merely to save characters loses precision and violates this
package's naming policy. Verify unfamiliar abbreviations in the relevant domain
source or ask about them before naming a core concept.

Consider the audience as well as expansion: a familiar short form can communicate
better than an unusual expansion, and an overloaded short form may need a
qualifier. External spellings retain their contract. Apply the language's casing
rules separately. This is [LOCAL-002](evidence.md#local-002); the
[empirical review](empirical-research.md) explains why abbreviation research
supports conditional guidance rather than a universal length rule.

## Contribute settled terms proportionately

A settled concept merits a glossary contribution when a competent newcomer to
the domain would need it across the codebase. A term useful only for the current
change can stay in the naming brief. Write a concise conceptual definition;
keep concrete code-name mappings and unresolved divergence in the glossary's
report. Follow the project's existing glossary layout and review practice.

The adopted [glossary guidance](../../glossary/SKILL.md#how-meaning-is-derived)
defines this workflow and its review requirements
([adoption boundary](sources.md#local-glossary)). Consuming existing entries and
drafting a scoped contribution are proportionate naming work. Broader glossary
generation follows a separately requested scope. Draft definitions remain
proposals until their required human review is recorded.

Continue with [elicitation](elicitation.md) for unresolved meaning,
[candidate generation](candidate-generation.md) for wording strategies, and
[language conventions](language-conventions.md) for ecosystem spelling.
