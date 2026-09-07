# Evidence and claim register

## Contents

- [Evidence classes and decisions](#evidence-classes-and-decisions)
- [Empirical and seed claim audit](#empirical-and-seed-claim-audit)
- [Concepts and domain claims](#concepts-and-domain-claims)
- [Language and artifact claims](#language-and-artifact-claims)
- [Compatibility claims](#compatibility-claims)
- [Local policy and engineering judgment](#local-policy-and-engineering-judgment)
- [Disagreement resolutions](#disagreement-resolutions)
- [Verification and use](#verification-and-use)

Use this register to check what a naming recommendation establishes and where
its reasoning applies. [Sources](sources.md) records author, version, access,
sections and reuse status; [empirical research](empirical-research.md) explains
study designs and disagreements. Research inspected on 2026-09-06 underlies the
claim decisions recorded here.

## Evidence classes and decisions

Empirical results describe measured tasks and populations. Formal models state
conceptual constraints under their assumptions. Standards and implementation
references establish rules within their named protocol or product. Practitioner
conventions express attributed design judgment. Local policy states this
package's chosen workflow and project constraints.

Adopted means the stated scoped claim has inspected support. Qualified means its
conditions or access boundaries govern use. Replaced preserves the original
citation while choosing an inspected primary source. Excluded means the stronger
claim supplies no adopted advice. Unresolved records a precise evidence gap.
Rejection records necessarily identify the disputed proposition; positive
recommendations and source-specific limits remain explicit beside them.

## Empirical and seed claim audit

Evidence kinds: EMP-002 and the bounded study findings in EMP-014 are empirical;
EMP-005/006 draw on a formal model and observational account; other rows audit
unsupported empirical extensions, reclassifying useful guidance as convention or
local judgment. The source register preserves every original study's methods.

| Claim ID | Audited claim | Disposition and exact support | Consuming references |
| --- | --- | --- | --- |
| <a id="emp-001"></a>EMP-001 | Synonymy/polysemy directly correlate with defect rates; abbreviations increase defects, attributed to Deissenboeck/Pizka | Exclude quantitative/causal claim. [B06](sources.md#b06) and inspected [B07](sources.md#b07) contain no defect-incidence comparison. [EMP-hofmeister-2017](sources.md#emp-hofmeister-2017) measures finding seeded defects. | [evidence](evidence.md), [empirical-research](empirical-research.md) |
| <a id="emp-002"></a>EMP-002 | Full words help comprehension | Adopt with task conditions in [EMP-hofmeister-2017](sources.md#emp-hofmeister-2017) IV-VII and [EMP-lawrie-2007](sources.md#emp-lawrie-2007) 2/4. Use the distinct tasks, abbreviation construction and outcomes in the linked source records. | [foundations](foundations.md), [selection](selection.md), [contextual-validation](contextual-validation.md) |
| <a id="emp-003"></a>EMP-003 | Every abbreviation harms comprehension; research establishes universal full-word consensus | Exclude universal claim. [EMP-lawrie-2007](sources.md#emp-lawrie-2007) 4.1 preserves uncertainty for familiar abbreviations. The project's full-word default and domain/local-scope exception are explicit policy. | [language-conventions](language-conventions.md), [foundations](foundations.md) |
| <a id="emp-004"></a>EMP-004 | Longer names are always better | Exclude. Semantic content, familiarity, scope and recall differ; length by itself is an inadequate selection criterion. The syllable association belongs specifically to [EMP-lawrie-2007](sources.md#emp-lawrie-2007)'s recognition model. | [selection](selection.md), [candidate-generation](candidate-generation.md) |
| <a id="emp-005"></a>EMP-005 | Strict one-to-one naming prevents logical collisions and guarantees exhaustive searches | Qualify as scoped modeling discipline and local review heuristic; [B07](sources.md#b07) 3.2 supplies formal definitions. Search completeness needs aliases, scope and affected-use inspection. | [foundations](foundations.md), [domain-vocabulary](domain-vocabulary.md), [renaming](renaming.md) |
| <a id="emp-006"></a>EMP-006 | Naming dictionaries empirically reduce cognitive load/maintenance costs | Adopt dictionary as a proposed tool/design aid ([B07](sources.md#b07) 5); exclude measured cost reduction. | [domain-vocabulary](domain-vocabulary.md), [evidence](evidence.md) |
| <a id="emp-007"></a>EMP-007 | Implementation details change more often than concepts; embedding them reduces stability, creates immediate rot or migration debt | Exclude empirical frequency/causation claim under [B06](sources.md#b06)/[B07](sources.md#b07). Evaluate accuracy under the actual representation contract as engineering judgment; see [compatibility claims](#compatibility-claims). | [variables-and-state](variables-and-state.md), [renaming](renaming.md) |
| <a id="emp-008"></a>EMP-008 | Generic names prove failure to classify; `data` may become `activeSubscription` | Exclude diagnostic certainty and invented state. Clarify actual meaning and use sites. A generic name may fit a small, clear scope. | [elicitation](elicitation.md), [contextual-validation](contextual-validation.md), [examples](../examples/README.md) |
| <a id="emp-009"></a>EMP-009 | Boolean negatives require mental inversion; positive capability names are instantly comprehensible, [B24](sources.md#b24) | Exclude empirical attribution and universal superiority. [B24](sources.md#b24) IV evaluates tagging. Describe truth conditions accurately as a scoped convention/local judgment; establish policy/capability distinction and truth tables. | [variables-and-state](variables-and-state.md), [examples](../examples/README.md), [local-rename fixture](renaming.md) |
| <a id="emp-010"></a>EMP-010 | Consistent Rust morphology drastically reduces cognitive load; local casing empirically always outweighs alternatives | Classify ecosystem rule as convention under [language claims](#language-and-artifact-claims); exclude magnitude/universal empirical claim. [EMP-sharif-2010](sources.md#emp-sharif-2010) supports a narrow recognition comparison. | [language-conventions](language-conventions.md) |
| <a id="emp-011"></a>EMP-011 | Hidden units are a primary source of catastrophic failures; a unit suffix prevents errors | Exclude general incidence claim from empirical evidence. Adopt explicit dimensional contracts as engineering judgment, supported by [quantity conventions](#lang-10) and [audio terminology](#con-011) and behavioral checks. | [variables-and-state](variables-and-state.md), [examples](../examples/README.md) |
| <a id="emp-012"></a>EMP-012 | Wrapper nouns cause god classes; action verbs prevent obscurity | Practitioner/design guidance subject to observed responsibilities; see [practitioner perspectives](#lang-14). Exclude causal proof from [B06](sources.md#b06)/[B07](sources.md#b07). | [functions-and-methods](functions-and-methods.md), [modules-packages-and-files](modules-packages-and-files.md) |
| <a id="emp-013"></a>EMP-013 | Evolution necessarily creates semantic debt, concept splits cause massive corruption, overloaded project names restrict growth | Exclude inevitable outcomes. Compatibility/design risk depends on actual contracts. [B06](sources.md#b06) 4.4 offers contrary evidence to monotonic naming-violation growth. See [bounded contexts](#con-003) and [compatibility](#compatibility-claims). | [renaming](renaming.md), [contextual-validation](contextual-validation.md) |
| <a id="emp-014"></a>EMP-014 | An explanatory intermediate variable always improves comprehension | Exclude universal claim; [EMP-cates-2021](sources.md#emp-cates-2021) V/VI preserves mixed results. Judge whether the name identifies a useful sub-result at its use site. | [variables-and-state](variables-and-state.md), [selection](selection.md) |
| <a id="emp-015"></a>EMP-015 | Identifier names constitute 70% of every program | Exclude universal scope. If needed, attribute corpus counts specifically to [B07](sources.md#b07) 1.1/4.2 and named Java versions. The guide does not need this statistic. | [empirical-research](empirical-research.md) |

## Concepts and domain claims

| Claim | Wording | Evidence and support | Disposition, conditions, and limits | Consuming references |
| --- | --- | --- | --- | --- |
| <a id="con-001"></a>CON-001 | Objects, concepts, definitions and designations have distinct roles. | Terminology standard preview; [CON-iso704-preview](sources.md#con-iso704-preview), introduction 0.1. | Qualified: software behavior briefs adapt this distinction; normative full-standard requirements remain uninspected. | [foundations](foundations.md), [elicitation](elicitation.md) |
| <a id="con-002"></a>CON-002 | Develop domain vocabulary through model discussion and examples with practitioners. | Practitioner guidance; [CON-fowler-language](sources.md#con-fowler-language), main paragraphs 1-2. | Adopted: inspect the project glossary and behavior; attribute Evans through Fowler. | [domain-vocabulary](domain-vocabulary.md), [elicitation](elicitation.md) |
| <a id="con-003"></a>CON-003 | Keep terminology coherent within a stated model boundary and explain cross-boundary mappings. | Practitioner guidance; [CON-fowler-context](sources.md#con-fowler-context), opening and multiple canonical models. | Adopted: two contexts may use one word differently; mapping depends on actual contracts. | [domain-vocabulary](domain-vocabulary.md), [modules-packages-and-files](modules-packages-and-files.md) |
| <a id="con-004"></a>CON-004 | An anti-rigid parent property constrains its child to be anti-rigid; identity and unity concern different modeling questions. | Formal ontology; [B15](sources.md#b15) sections 8.1-8.3. | Qualified: Human under Student violates the stated constraint; Student under Human is permitted by this constraint. Apply to software as a modeling analogy. | [foundations](foundations.md), [types-and-messages](types-and-messages.md) |
| <a id="con-005"></a>CON-005 | Role membership and enduring identity require distinct conditions. | Formal ontology; [B16](sources.md#b16) property taxonomy, PDF pages 5-6. | Qualified: class design and persistence choices require their own software contracts. | [types-and-messages](types-and-messages.md), [apis-schemas-and-configuration](apis-schemas-and-configuration.md) |
| <a id="con-006"></a>CON-006 | Use precise definitions and make only necessary commitments about the modeled world. | Conceptual design argument; [CON-gruber](sources.md#con-gruber) section 3, 1993 manuscript revision. | Qualified: minimal commitment means bounded assertions about reality; semantic precision remains useful. | [foundations](foundations.md), [elicitation](elicitation.md) |
| <a id="con-007"></a>CON-007 | SKOS separates resource identity and lexical labels, with at most one preferred label per language tag. | W3C Recommendation; [CON-skos](sources.md#con-skos) sections 3 and 5, S14. | Qualified to SKOS. Scoped canonical software terms and explicit aliases are local adaptation. | [domain-vocabulary](domain-vocabulary.md), [apis-schemas-and-configuration](apis-schemas-and-configuration.md) |
| <a id="con-008"></a>CON-008 | Bid and ask identify buying and selling prices; spread compares the prices. | Practitioner terminology; [CON-cme-glossary](sources.md#con-cme-glossary) named entries. | Adopted: state instrument, units and availability of both sides in an example. | [domain-vocabulary](domain-vocabulary.md), [variables-and-state](variables-and-state.md) |
| <a id="con-009"></a>CON-009 | An aggressor matches resting orders and removes liquidity in the documented continuous-trading setting. | Protocol documentation; [CON-cme-orders](sources.md#con-cme-orders) Order Aggressor Indicator. | Qualified by trading state and instrument. Incoming limit and resting price identify different roles; fee classifications need separate evidence. | [domain-vocabulary](domain-vocabulary.md), [variables-and-state](variables-and-state.md) |
| <a id="con-010"></a>CON-010 | UN/CEFACT vocabulary distinguishes trade shipment from transport-contract consignment. | Project vocabulary; [CON-uncefact-vocabulary](sources.md#con-uncefact-vocabulary) Classes table. | Qualified: inspected test-site version is unversioned; preserve the chosen context and project glossary. BRS excerpts offer access-limited corroboration. | [domain-vocabulary](domain-vocabulary.md), [types-and-messages](types-and-messages.md) |
| <a id="con-011"></a>CON-011 | Audio frames, channel samples, sample rate, buffer duration, and latency preserve different quantities. | API reference; [CON-portaudio](sources.md#con-portaudio) V19 Pa_OpenStream; Burk V18 latency explanation. | Qualified: 480 frames at 48,000 frames/second last 0.010 seconds; stereo supplies 960 scalar samples. Latency needs a measurement boundary. | [domain-vocabulary](domain-vocabulary.md), [variables-and-state](variables-and-state.md) |
| <a id="con-012"></a>CON-012 | FHIR Encounter represents healthcare interactions and their lifecycle and settings. | Standard vocabulary; [CON-fhir-encounter](sources.md#con-fhir-encounter) R5 Scope and Usage. | Qualified to R5 data modeling. Example transitions specify software state and timestamp. | [domain-vocabulary](domain-vocabulary.md), [types-and-messages](types-and-messages.md) |
| <a id="con-013"></a>CON-013 | FHIR Observation carries measurements/assertions; DiagnosticReport can group observations with context. | Standard vocabulary; [CON-fhir-observation](sources.md#con-fhir-observation) R5 Scope and Usage. | Qualified: choose a single lab-result name or grouped report name from actual representation and cardinality. | [domain-vocabulary](domain-vocabulary.md), [types-and-messages](types-and-messages.md) |
| <a id="con-014"></a>CON-014 | FHIR Specimen represents sampled material. | Standard vocabulary; [CON-fhir-specimen](sources.md#con-fhir-specimen) R5 Scope and Usage. | Qualified: receipt records and events require stipulated software behavior; vocabulary describes a data model. | [domain-vocabulary](domain-vocabulary.md), [functions-and-methods](functions-and-methods.md) |

## Language and artifact claims

<a id="lang-01"></a>

### LANG-01: Meaning and scope in Google C++

Recommend intent-bearing names whose detail fits visible context. Recognizable
abbreviations have scoped exceptions. Google casing is policy: types and ordinary
functions use capitalized words; variables use snake case; class data members have
a trailing underscore; namespaces use snake case. File and namespace names aid
discovery and collision avoidance. Source: [LANG-google-cpp](sources.md#lang-google-cpp), named sections in the source register.

Condition: code adopting Google's C++ guide. A standard-library-shaped API can
have different spelling. A local name need not repeat its enclosing operation;
a public name must work for readers beyond its implementation. Evidence class:
practitioner convention. Adopt with qualification; consume in [foundations](foundations.md)/[variables and state](variables-and-state.md)/[modules packages and files](modules-packages-and-files.md)/[language conventions](language-conventions.md).

<a id="lang-02"></a>

### LANG-02: Swift use-site grammar

Judge the complete call, including argument labels. Name values by role and
preserve established terms. Swift distinguishes imperative effectful methods
from value-oriented queries, and pairs mutation with derived-value forms such as
`sort`/`sorted`. Nonmutating boolean uses should read as assertions; `intersects`
shows that `is` is optional. Types/protocols use UpperCamelCase; other names use
lowerCamelCase. Capability protocol suffixes and acronym casing are Swift rules.
Source: [LANG-swift](sources.md#lang-swift), named sections in the source register. Adopt/qualified; [domain vocabulary](domain-vocabulary.md)/[variables and state](variables-and-state.md), [functions and methods](functions-and-methods.md), [types and messages](types-and-messages.md)/[language conventions](language-conventions.md).

Counterexample to universal verb naming: a query can be a noun phrase. Transferring
Swift's participle rule mechanically into another ecosystem is local policy,
not evidence-based necessity. Assertion grammar establishes neither positive
polarity nor permission to change a predicate's truth conditions.

<a id="lang-03"></a>

### LANG-03: Python names and error types

PEP 8 uses snake case for functions, variables and methods, CapWords for most
classes, and uppercase underscore constants. Module names are lowercase;
package underscores are discouraged. `self`, `cls`, underscore visibility and
name-mangling conventions have specific meanings. Error exceptions take an
`Error` suffix; signaling exceptions can differ. Existing project consistency
can override the defaults. Source: [LANG-python](sources.md#lang-python) naming subsections.

Adopt/qualified language convention; [variables and state](variables-and-state.md), [functions and methods](functions-and-methods.md), [types and messages](types-and-messages.md), [modules packages and files](modules-packages-and-files.md)/[language conventions](language-conventions.md). A `StopIteration`-like signaling
exception defeats an unconditional Error-suffix rule. A name is not a substitute
for checking the raised exception and caller handling. PEP 8 supplies no universal
boolean prefix or unit suffix prescription.

<a id="lang-04"></a>

<a id="lang-05"></a>

### LANG-04 and LANG-05: Rust document ownership

[RFC 430](sources.md#lang-rfc430) owns the historical casing table and discussion distinguishing panicking
`unwrap` from conversions. Its crate row prefers single-word snake case. The
current [API Guidelines](sources.md#b21) C-CASE marks crate casing unclear; do not publish the RFC
row as settled current crate policy. Adopt both with dates and this qualification.

C-CONV owns the detailed conversion cost/ownership table: `as_` for free borrowed
views; `to_` for conversions involving work or copied/borrowed inputs; `into_` for
consuming owned non-Copy inputs. `into_` can be cheap or costly. C-GETTER usually
omits `get_`, with exceptions including unambiguous getters and checked indexing.
C-ITER applies `iter`/`iter_mut`/`into_iter` to homogeneous collection methods;
text iteration and free functions provide explicit counterexamples.

Evidence: ecosystem convention, verified/qualified. Consumers [functions and methods](functions-and-methods.md)/[modules packages and files](modules-packages-and-files.md)/[language conventions](language-conventions.md).
Preserve ownership, cost and method-category conditions; a generic claim that
`to_` always allocates or `into_` always means cheap is unsupported.

<a id="lang-06"></a>

<a id="lang-07"></a>

<a id="lang-08"></a>

### LANG-06, LANG-07 and LANG-08: JavaScript/TypeScript scope

Google JavaScript names types with UpperCamelCase and methods/fields/parameters
with lowerCamelCase. Method verbs and type nouns are tendencies, with adjective
interfaces permitted. Boolean accessors may use `get`, `is`, or `has`. Private
trailing underscores are optional; constant case depends on constant semantics,
not merely the presence of `const`. Source: [LANG-javascript](sources.md#lang-javascript) 6.2. Adopt/qualified.

Google TypeScript uses UpperCamelCase types, lowerCamelCase values and module
aliases, and snake-case filenames. It avoids type decorations and private
underscores, permits established framework conventions, and treats Observable
`$` suffixes as a team decision. Its constant rule permits intended immutability,
where the JavaScript guide asks for stronger observable immutability. Source:
[LANG-typescript](sources.md#lang-typescript) Naming. Adopt/qualified; [variables and state](variables-and-state.md), [functions and methods](functions-and-methods.md), [types and messages](types-and-messages.md), [modules packages and files](modules-packages-and-files.md)/[language conventions](language-conventions.md).

Microsoft's contributor guide chooses PascalCase enum values; Google's chooses
constant case. Both are organizational guidance. [LANG-typescript-contributors](sources.md#lang-typescript-contributors)
explicitly disclaims a community-wide prescription. Adoption: use to demonstrate
scope, not to rank ecosystems. Language validity and project convention require
separate checks. A legal TypeScript namespace is not automatically Google-style.

<a id="lang-09"></a>

### LANG-09: API/schema fields

AIP-140 asks for precise fields, plural repeated fields, compatible generated
spellings and reserved-word avoidance. Boolean fields omit `is`, with keyword
exceptions, and `disabled` is valid. Fields describe state; operations describe
actions. Familiar abbreviations are favored in that API convention.

Adopt/qualified Google API convention; [variables and state](variables-and-state.md)/[API contracts](apis-schemas-and-configuration.md)/[language conventions](language-conventions.md). It contradicts a universal
`is_` requirement or positive-predicate rule. Project full-word policy takes
precedence for new local examples; preserve established external field spelling
when it is a contract. A scalar count and a collection express different things.
Uniformity is a scoped goal, not a mathematical one-name/one-concept guarantee.

<a id="lang-10"></a>

### LANG-10: Quantities and configuration

AIP-141 gives unit suffixes for quantity fields, `_count` for item counts, and
rules for inverse units. It also supports specialized quantity messages and
variable units. Adopt/qualified for that API ecosystem; [variables and state](variables-and-state.md)/[API contracts](apis-schemas-and-configuration.md). Generalizing to
configuration is local judgment: establish the parser's unit, allowed values and
defaults before choosing a key. An explicit duration type or a unit-bearing
configuration value can carry information that would otherwise need a suffix.

Original example: a configuration key `buffer_size_samples` can describe a raw
integer measured in samples. If the input represents frames, that proposed name
fails regardless of its suffix clarity. Domain verification owns the distinction.
A suffix is evidence of intended units, not evidence that arithmetic is correct.

<a id="lang-11"></a>

### LANG-11: Queries and commands in APIs

AIP-136 gives custom operations verb/noun names and a custom verb after `:` in
the URI. Standard methods are preferred when their semantics fit; custom methods
express other intent. GET retrieves state; POST supports mutations and specified
retrieval exceptions. Adopt/qualified; [functions and methods](functions-and-methods.md)/[API contracts](apis-schemas-and-configuration.md). This directly rejects universal
verb-free URL advice. Match the API's design contract before judging grammar.
An operation's attractive name cannot establish its actual effects or billing.

<a id="lang-12"></a>

### LANG-12: Schemas, files and namespace collisions

Protobuf uses snake-case files/fields, capitalized message names, plural repeated
fields and project-based package names. Identifier transformations can merge
distinct source spellings; package conventions also consider generated languages.
Adopt/qualified format guidance; [modules packages and files](modules-packages-and-files.md), [API contracts](apis-schemas-and-configuration.md), [language conventions](language-conventions.md). Check generated names as well as source
names. Distinct case-sensitive schema identifiers can collide after generation.
The package naming advice applies to protobuf packages, not every distribution
registry. Link to [LANG-protobuf](sources.md#lang-protobuf)'s precise sections in the register.

<a id="lang-13"></a>

### LANG-13: Events, commands and state

Microsoft's domain-event guide uses past-tense event classes because they record
occurrences. Vogel's Handling Commands and Events describes imperative command
names and past-tense event names as conventions, with conceptual distinctions
and queue-based counterexamples. Adopt/qualified DDD guidance; [types and messages](types-and-messages.md). Applied naming
judgment: distinguish an imperative request `StartEncounter` from an occurrence `EncounterStarted` and
a current state `started`. These are original software examples, not clinical
workflow claims. Verify dispatch and transition behavior before selecting them.
A cancellation request is not proof that cancellation completed. Framework event
names can have their own grammar. Past tense alone proves neither persistence
nor successful transaction commit; inspect the event's publication contract.

<a id="lang-14"></a>

<a id="lang-15"></a>

### LANG-14 and LANG-15: Practitioner perspectives

[Hilton's Naming smells](sources.md#lang-hilton-smells) supplies useful prompts about vague names, unexplained
numeric suffixes, ambiguity, and disagreements with documentation. Adopt those as
review questions. His opposition to boolean prefixes and short names is a
practitioner position, not a universal result. His relationship renames require
domain evidence: a relationship does not establish an employment role. Replacing
a collection with a richer domain noun requires the richer concept to be true.
Consumers [foundations](foundations.md)/[candidate generation](candidate-generation.md)/[types and messages](types-and-messages.md)/[contextual validation](contextual-validation.md); verified/qualified.

[Yegge's satire](sources.md#b20) criticizes forcing actions through excessive noun-based wrappers.
Adopt only as an attributed design perspective for [functions and methods](functions-and-methods.md)/[types and messages](types-and-messages.md): a naming struggle
can invite review of an abstraction. It does not prove that classes, managers,
or nouns are intrinsically defective. No empirical claim is adopted from it.

## Compatibility claims

All source-supported rows are adopted within the conditions below. COMP-014 and
COMP-015 are adopted local engineering policy.

| Claim | Scoped wording | Kind and support | Conditions, limits, and consuming references |
| --- | --- | --- | --- |
| <a id="comp-001"></a>COMP-001 | A refactoring preserves observable behavior; a rename may be a small refactoring | Practitioner definition, [COMP-refactoring](sources.md#comp-refactoring) | Establish observable boundaries first. [renaming](renaming.md) |
| <a id="comp-002"></a>COMP-002 | Source, wire, and semantic compatibility require separate assessment | Official policy, [COMP-aip180](sources.md#comp-aip180) | Its concrete restrictions apply to its API scope. Local systems state their own release promise. [API contracts](apis-schemas-and-configuration.md)/[renaming](renaming.md) |
| <a id="comp-003"></a>COMP-003 | Renaming a published component can act as removal plus addition; aliases require conflict semantics | Official policy, [COMP-aip180](sources.md#comp-aip180) | Old clients, generated imports, defaults, and field presence can remain contractual. [API contracts](apis-schemas-and-configuration.md)/[renaming](renaming.md) |
| <a id="comp-004"></a>COMP-004 | A protobuf field number and its JSON spelling serve different encoding roles | Format specification, [COMP-proto3](sources.md#comp-proto3) and [COMP-protojson](sources.md#comp-protojson) | Preserve reserved numbers/names where required; inspect every format actually used. [API contracts](apis-schemas-and-configuration.md)/[renaming](renaming.md) |
| <a id="comp-005"></a>COMP-005 | ProtoJSON allows explicit JSON names and enum aliases; serializer ordering and rollout affect emitted names | Format specification, [COMP-protojson](sources.md#comp-protojson) | Its enum sequence requires compatible readers before writers and accounts for persisted data and rollback. These mechanics do not establish arbitrary JSON alias behavior. [API contracts](apis-schemas-and-configuration.md)/[renaming](renaming.md) |
| <a id="comp-006"></a>COMP-006 | A string may select a runtime attribute even when ordinary static references do not show it | Language reference, [COMP-python-runtime](sources.md#comp-python-runtime) | Check actual lookup paths, registries, imports, and configured targets. [renaming](renaming.md) |
| <a id="comp-007"></a>COMP-007 | Renaming a Python module, function or class can affect stored pickle data | Language reference, [COMP-python-pickle](sources.md#comp-python-pickle) | Test previously serialized objects using trusted data and the real import environment. [renaming](renaming.md) |
| <a id="comp-008"></a>COMP-008 | A CLI option may keep its spelling while its internal destination changes | Language reference, [COMP-python-cli](sources.md#comp-python-cli) | Example: `--retry-limit` can populate `retry_limit`; mapping and parser precedence stay explicit. [API contracts](apis-schemas-and-configuration.md) |
| <a id="comp-009"></a>COMP-009 | Configuration structures and CLI elements can carry published compatibility promises | Project policy, [COMP-kubernetes](sources.md#comp-kubernetes) | Copying Kubernetes' exact durations into unrelated projects would require a local decision. [API contracts](apis-schemas-and-configuration.md) |
| <a id="comp-010"></a>COMP-010 | A direct database column rename is one available mechanism | Official implementation reference, [COMP-postgresql](sources.md#comp-postgresql) | Evaluate locks, dependencies and external SQL before choosing; add/backfill/drop is not universally required. [renaming](renaming.md) |
| <a id="comp-011"></a>COMP-011 | Stable identity can coexist with a human-readable identifier | Informative standards-body guidance, [COMP-cooluris](sources.md#comp-cooluris) | The note recommends mnemonic stable HTTP URIs; it does not require universal opaque keys. [API contracts](apis-schemas-and-configuration.md) |
| <a id="comp-012"></a>COMP-012 | HTTP DELETE describes removal of a resource association, with storage behavior defined by implementation | Protocol standard, [COMP-http-delete](sources.md#comp-http-delete) | Derive names such as `archived` from actual state transitions; an HTTP verb alone establishes no physical erasure or legal result. [README](../examples/README.md) |
| <a id="comp-013"></a>COMP-013 | Stripe authorization reserves funds for later capture | Provider documentation, [COMP-stripe-authorization](sources.md#comp-stripe-authorization) | A checkout click is an action in a user flow and does not establish authorization success. [README](../examples/README.md) |
| <a id="comp-014"></a>COMP-014 | Scope a rename by declaration identity and observable contracts, then check both changed and deliberately retained uses | Local verification policy informed by COMP-001 through COMP-010 | Compiler/test/search evidence is bounded by inspected paths, languages, and consumers. [Renaming](renaming.md) |
| <a id="comp-015"></a>COMP-015 | A changed predicate, default, unit, side effect or state transition is a behavior change even if introduced alongside a clearer name | Local classification policy, consistent with COMP-001/COMP-002 | Evaluate and authorize that behavior separately. [Renaming](renaming.md), [worked examples](../examples/README.md) |

## Local policy and engineering judgment

These adopted rules are naming-package policy, established by the project
instructions and naming workflow requirements accepted on 2026-09-06. Their
justification is the stated engineering objective and the linked maintained
resource. Empirical studies supply evidence for bounded findings separately.

| Claim | Adopted policy and rationale | Conditions and consuming references |
| --- | --- | --- |
| <a id="local-001"></a>LOCAL-001 | Use practitioner vocabulary. Read code, glossary and authoritative domain material; ask when meaning remains material and unresolved. Support: [local glossary adoption](sources.md#local-glossary), CON-002/003. | [Domain vocabulary](domain-vocabulary.md), [elicitation](elicitation.md); resolve the target context before equating neighboring terms. |
| <a id="local-002"></a>LOCAL-002 | Default to full words; permit established domain abbreviations appropriate to local scope. This is a project naming constraint. | [Language conventions](language-conventions.md), [selection](selection.md). Preserve contractual external spellings; EMP-002/003 establish the limited empirical support. |
| <a id="local-003"></a>LOCAL-003 | Scale the naming brief and questions to uncertainty. Read supplied evidence first and ask scenario questions whose answers change the decision. Support: [design adoption](sources.md#local-design). | [Elicitation](elicitation.md). A settled small choice can use a sentence; mandatory genus-differentia and three candidates are rejected as universal requirements. |
| <a id="local-004"></a>LOCAL-004 | Compare genuinely viable alternatives with task-specific criteria and grounded scores; show use sites and record rationale. A clear winner uses direct prose. Support: [matrix adoption](sources.md#local-matrix). | [Candidate generation](candidate-generation.md), [selection](selection.md). Candidate count follows uncertainty; missing facts remain assumptions or questions. |
| <a id="local-005"></a>LOCAL-005 | Review the selected or existing name separately against behavior, callers, neighboring concepts, documentation, and contracts. Revisit discovery or selection when the evidence contradicts it. | [Contextual validation](contextual-validation.md). Description-only input supports only description-level conclusions; an adequate existing name may be retained. |
| <a id="local-006"></a>LOCAL-006 | A rename preserves established truth conditions, units, defaults, cardinality, effects, and affected contracts; record authorized scope, binding identity, and deliberately retained spellings. Support: COMP-014/015. | [Renaming](renaming.md). A behavior change receives its own explicit scope and authorization. |
| <a id="local-007"></a>LOCAL-007 | Use fresh, proportionate checks and report commands, observed results, and coverage. Support: [verification adoption](sources.md#local-verification). | [Contextual validation](contextual-validation.md), [renaming](renaming.md). Test success supports exercised paths; source review and actual human judgment remain distinct evidence. |
| <a id="local-008"></a>LOCAL-008 | Write original examples with explicit software contracts, practitioner terms, and positive descriptions of present behavior. Keep code and output plain text. | [Foundations](foundations.md), [examples](../examples/README.md). Establish behavior before adding state modifiers; preserve licensing attribution through [sources](sources.md). |
| <a id="local-009"></a>LOCAL-009 | Keep published guidance and loaded dependencies in durable package or sibling resources. Human references own substance; entry points select and order it. Support: [documentation adoption](sources.md#local-documentation). | [Maintenance](maintenance.md). Repository-tree installation supplies documented siblings and their transitive loaded resources. |
| <a id="local-010"></a>LOCAL-010 | Retirement and rollback decisions examine support promises, instrumentation coverage, dormant consumers, and persisted data. | [Renaming](renaming.md), [API contracts](apis-schemas-and-configuration.md). Zero observed usage alone is insufficient; staged dual writes require reconciliation, backfill, and explicit removal evidence. |

## Disagreement resolutions

| Question and linked claims | Resolution for this guide |
| --- | --- |
| [Full words](#emp-002), [abbreviations](#emp-003), [length](#emp-004) | Hofmeister's generated abbreviations and Lawrie's mostly familiar ones support different comparisons. Preserve tasks and outcome measures. Apply LOCAL-002 as policy, without claiming universal empirical consensus. |
| [One-to-one terminology](#emp-005), [bounded context](#con-003), [SKOS labels](#con-007) | Use consistent terms inside the chosen context and explicit aliases across contracts. Global bijection and guaranteed exhaustive text search are excluded. |
| [Positive booleans](#emp-009), [Swift assertions](#lang-02), [Google API fields](#lang-09) | Assertion grammar, prefix rules, and predicate polarity are separate decisions. AIP-140 permits disabled and omits is; preserve the actual truth table, policy/capability meaning, and ecosystem scope. [B24](sources.md#b24) supports POS tagging only. |
| [Rust RFC](#lang-04), [current guidelines](#lang-05) | RFC 430 owns historical casing; API Guidelines own detailed conversion costs and ownership. Current crate casing remains unclear there. Preserve getter/iterator category exceptions. |
| [JavaScript](#lang-06), [TypeScript](#lang-07), [compiler contributors](#lang-08) | Each guide governs its project. Enum casing, private markers, and constant criteria differ. Verify language validity and the project's chosen convention separately. |
| [Unit suffixes](#emp-011), [quantities](#lang-10), [audio frames](#con-011) | Units can be carried by type, value, or field spelling. Verify actual dimensions before choosing a suffix. Buffer duration and end-to-end latency require different contracts. |
| [Minimal ontology commitment](#con-006), [subsumption](#con-004), [roles](#con-005) | Make precise, bounded conceptual commitments. Student/Human constraint direction is preserved. Software inheritance, opaque keys, and universal definition syntax require separate decisions. |
| [Persistent identity](#comp-011), [lexical labels](#con-007), [public renames](#comp-003) | Readable identifiers can be stable. Mandatory opacity and automatic new identity after any semantic edit are excluded. Determine actual identity and historical interpretation. |
| [Refactoring](#comp-001), [dynamic lookup](#comp-006), [stored pickle](#comp-007), [database rename](#comp-010) | A small internal rename can preserve behavior with bounded checks; public spellings and stored data expand scope. Direct database rename, retention, aliasing and staged migration are conditional options. |
| [HTTP deletion](#comp-012), [payment authorization](#comp-013), [clinical vocabulary](#con-012) | Software labels follow inspected transitions. Delete proves no physical erasure or legal compliance; checkout does not establish authorization; employment does not prove credentials. Clearing/settlement equations and legal conclusions are excluded. |
| [Generic names](#emp-008), [wrapper nouns](#emp-012), [intermediate variables](#emp-014) | Naming difficulty invites contextual inquiry. It cannot prove mixed responsibilities or justify adding invented active state. Named intermediate results have mixed empirical support. |
| [AIP custom methods](#lang-11), [Swift queries](#lang-02) | Artifact and language grammar differ. Custom resource-oriented operations can use verbs; Swift queries can use noun phrases. Universal verb-free URL and every-function-is-a-verb rules are rejected. |

## Verification and use

To assess a recommendation, locate its claim ID, read the cited source record
and precise section, compare the source's context with the current project, then
inspect actual behavior and representative uses. For example, a field named
`buffer_size_samples` fails if its parser consumes audio frames, even though its
spelling follows an otherwise useful unit convention (CON-011, LANG-10).

The register preserves 59 research claim IDs and 10 local policy IDs. Adopted
empirical findings preserve their task limits. Excluded claims have a disposition
and consuming review location so future authors can recognize and reassess them.
The abstract-only Avidan paper, 2006 journal full text, full ISO clauses, full
logistics BRS and unverified reproduction rights remain bounded access gaps;
adopted advice uses inspected material or explicit local policy. Source refresh
and source-dependent edits follow [maintenance](maintenance.md).
