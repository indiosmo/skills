# Sources and adoption register

## Contents

- [Seed bibliography audit](#seed-bibliography-audit)
- [Empirical and formal naming sources](#empirical-and-formal-naming-sources)
- [Additional leads and access dispositions](#additional-leads-and-access-dispositions)
- [Concepts and domain terminology sources](#concepts-and-domain-terminology-sources)
- [Domain sources and example contracts](#domain-sources-and-example-contracts)
- [Language and artifact convention sources](#language-and-artifact-convention-sources)
- [Compatibility sources](#compatibility-sources)
- [Adopted local resources](#adopted-local-resources)

Use this register to identify the version, inspected material, authority and
reuse conditions behind a naming recommendation. [The evidence register](evidence.md)
owns claim dispositions and consuming references; [empirical research](empirical-research.md)
explains the experimental findings. Access date throughout: 2026-09-06.
Live documents are snapshots at that date; verify their applicability to the
language, protocol and library version in the project being named.

Original summaries and software examples are the reuse strategy. Each record
states its specific rights finding. Citation and public access establish
provenance; reproduction follows the applicable source license. Rejected or
unopened bibliography entries retain their identity for audit, with no adopted
content. Source titles retain their published spelling.

## Seed bibliography audit

All 27 starting entries have a disposition. Links in this table preserve their
original discovery locations; the sections below identify inspected primary
replacements, authors, versions, exact sections, access, and reuse decisions.
For unopened exclusions, author/date/license remain unverified and no content is
adopted. This is a relevance decision on the supplied title and claim context.

| Seed ID and original link | Identity and disposition | Access and reason |
| --- | --- | --- |
| <a id="b01"></a>[B01](https://martinfowler.com/bliki/TwoHardThings.html) | Fowler, Two Hard Things: excluded | Aphorism provenance adds no actionable naming evidence. Title/seed relevance assessment only. |
| <a id="b02"></a>[B02](https://webstore.ansi.org/preview-pages/ISO/preview_ISO+704-2022.pdf) | ISO 704:2022 ANSI preview: verified/qualified | Seven-page preview inspected, introduction 0.1, printed vi-vii. Adopt distinctions among objects, concepts, definitions, and designations only. |
| <a id="b03"></a>[B03](https://cdn.standards.iteh.ai/samples/79077/95f5c2196b2f4b31a88b216e6ee967c3/SIST-ISO-704-2023.pdf) | SIST ISO 704:2023 iTeh preview: replaced | National adoption preview duplicates B02 discovery purpose; use inspected ISO preview with narrower claims. Unopened. |
| <a id="b04"></a>[B04](https://www.scribd.com/document/665130432/ISO-704-2022) | Scribd ISO 704:2022: replaced | Use B02 publisher-authorized preview; unsupported full-standard rules remain excluded. Unopened. |
| <a id="b05"></a>[B05](https://www.researchgate.net/publication/2362508_A_Formal_Ontology_of_Properties) | ResearchGate A Formal Ontology of Properties: replaced | Same paper inspected at B16; repository listing is unnecessary intermediary. |
| <a id="b06"></a>[B06](https://www.researchgate.net/publication/220703743_Syntactic_Identifier_Conciseness_and_Consistency) | Lawrie, Feild and Binkley, SCAM 2006: replaced/qualified | Replace aggregator with author-hosted original below; syntax proxy evaluation and sampled concept judgments. |
| <a id="b07"></a>[B07](https://www.semanticscholar.org/paper/Concise-and-consistent-naming-Dei%C3%9Fenb%C3%B6ck-Pizka/ca221a1cc608f4c330e1b185b402cb616dd8429d) | Deissenboeck and Pizka: replaced/qualified | Inspect 2005 original; 2006 journal full text and exact seed indexed version remain unavailable. |
| <a id="b08"></a>[B08](https://se-radio.net/2016/12/se-radio-episode-278-peter-hilton-on-naming/) | Felienne interviewing Peter Hilton, 2016-12-20: excluded | Show notes/metadata read; audio uninspected. No interview finding adopted. |
| <a id="b09"></a>[B09](https://joostvdg.github.io/swe/naming/) | Joost van der Grinten naming resource collection: replaced | Use Fowler's specific Ubiquitous Language and Bounded Context essays for attributed practitioner guidance. On Naming and resource sections inspected in the compatibility audit; secondary resource collection supplies discovery context. |
| <a id="b10"></a>[B10](https://contextmapper.org/docs/anticorruption-layer/) | Context Mapper Anticorruption Layer: verified/qualified | Syntax and Semantic Rules inspected. Establishes tool-specific downstream pattern and validation, not a mandatory boundary translation rule. Exclude as general naming authority. |
| <a id="b11"></a>[B11](https://hilton.org.uk/blog/) | Peter Hilton blog index: replaced | Discovery index replaced by dated Naming smells essay below. |
| <a id="b12"></a>[B12](https://discourse.nixos.org/t/should-we-give-a-name-to-nix-on-non-nixos/21020) | Nix on non-NixOS discussion: excluded | A project naming discussion could illustrate disagreement; seed's causal claims about cognitive overload and growth require stronger evidence. Unopened. |
| <a id="b13"></a>[B13](https://forum.auxolotl.org/t/on-naming-things/81?page=2) | Aux naming discussion page 2: excluded | Anecdotal branding discussion is outside software identifier scope. Unopened. |
| <a id="b14"></a>[B14](https://discourse.nixos.org/t/nixpkgs-naming-vs-local-naming-of-installed-packages/18095) | Nixpkgs versus local package names: excluded | Ecosystem-specific installed-package discussion is unnecessary for initial package naming guidance. Unopened. |
| <a id="b15"></a>[B15](https://www.loa.istc.cnr.it/old/Papers/GuarinoWeltyOntoCleanv3.pdf) | Guarino/Welty, An Overview of OntoClean: verified/qualified | Original laboratory PDF, chapter 8, sections 8.1-8.2 and 8.3 metaproperty caveat inspected. Adopt bounded modeling distinctions below. |
| <a id="b16"></a>[B16](http://cui.unige.ch/isi/cours/aftsi/articles/01-guarino00formal.pdf) | Guarino/Welty, A Formal Ontology of Properties: verified/qualified | Eight-page original paper copy inspected at university URL; introduction and property taxonomy, PDF pages 5-6. Formal role/type distinctions only. |
| <a id="b17"></a>[B17](https://www.rd-alliance.org/sites/default/files/attachment/Ontology%20Engineering.pdf) | RDA Ontology Engineering slides: replaced | Gruber claims use author's original paper, section 3. Slides unopened. |
| <a id="b18"></a>[B18](https://semantic-web-journal.net/sites/default/files/58_54.pdf) | A Tour To Ontology Design and Development: excluded | Survey offers discovery breadth; inspected primary Gruber and OntoClean sources cover adopted concepts directly. Unopened. |
| <a id="b19"></a>[B19](https://contextmapper.org/docs/shared-kernel/) | Context Mapper Shared Kernel: verified/qualified | Syntax and Default Symmetric Relationship inspected; documentation demonstrates a symmetric context relationship in CML. Exclude tool syntax from naming guide. |
| <a id="b20"></a>[B20](https://steve-yegge.blogspot.com/2006/03/execution-in-kingdom-of-nouns.html) | Steve Yegge, March 2006: qualified | Practitioner satire, inspected opening and Kingdom of Nouns; design perspective only. |
| <a id="b21"></a>[B21](https://rust-lang.github.io/api-guidelines/naming.html) | Rust library team and contributors, live: qualified | Current API Guidelines naming sections inspected; historical RFC 430 remains a separate source. |
| <a id="b22"></a>[B22](https://www.scribd.com/document/754922698/Rust-API-Guidelines) | Scribd Rust guidelines copy, uploader/version unverified: replaced | Accessible HTML preview; primary Rust guidelines own adopted claims. |
| <a id="b23"></a>[B23](https://www.reddit.com/r/rust/comments/1j43h8g/rusts_functionmethod_naming_convention/) | Reddit community discussion, edition unverified: replaced | Accessible HTML; primary Rust sources own convention claims. |
| <a id="b24"></a>[B24](https://www.eecis.udel.edu/~pollock/879tainsef13/samir-postagging.pdf) | Gupta, Malik, Pollock and Vijay-Shanker, ICPC 2013: qualified | Original methods and evaluation inspected; POS tagging evidence. Boolean polarity attribution rejected. |
| <a id="b25"></a>[B25](https://nemo.inf.ufes.br/wp-content/papercite-data/pdf/incorporating_types_of_types_in_ontology_driven_conceptual_modeling_2022.pdf) | Incorporating Types of Types in Ontology-Driven Conceptual Modeling (2022): excluded | Higher-order conceptual modeling is beyond this software naming guide. Title/seed relevance assessment only; no formal claims adopted. |
| <a id="b26"></a>[B26](https://www.slideshare.net/slideshow/how-to-name-things-the-hardest-problem-in-programming/39383508) | SlideShare Hilton talk, edition/date unverified: excluded | HTML transcript accessible; images, narration, and presentation rights unverified. Dated author essay preferred. |
| <a id="b27"></a>[B27](https://speakerdeck.com/hilton/how-to-name-things-the-hardest-problem-in-programming) | Peter Hilton Speaker Deck account, edition/date unverified: excluded | Transcript opening inspected; presentation and third-party slide rights unverified. Dated author essay preferred. |

## Empirical and formal naming sources

<a id="emp-hofmeister-2017"></a>

### EMP-hofmeister-2017: Shorter Identifier Names Take Longer to Comprehend

Johannes Hofmeister, Janet Siegmund, Daniel V. Holt; 2017 conference manuscript. [Original paper](https://brains-on-code.github.io/shorter-identifier-names.pdf).
Inspected sections IV-VII, PDF pages 3-9; especially IV.A/C/E and V.A/B,
Table VII. Disposition: verified/qualified.

- Population: 72 retained experienced C# developers; 221 started, 135 finished,
  63 completed records excluded. German instructions, English identifiers.
- Task: semantic defect finding in short C# functions, followed by syntax-error
  controls; balanced within-participant naming conditions.
- Comparison: full words, single letters, mechanically shortened abbreviations
  using three consonants, with some familiar-prefix exceptions.
- Measurement/result: inverse viewing time, expressed as defects/minute;
  0.78 for words, 0.65 abbreviations, 0.66 letters. Word-versus-nonword contrast
  p=.004, dz=.32; authors report 19% higher speed. Abbreviations-versus-letters
  and syntax-error differences were nonsignificant.
- Limits: filtered online sample, restricted seven-line viewport, short tasks,
  and artificial abbreviations. Defect detection measures a comprehension task;
  production defect incidence and long-term maintenance cost were unmeasured.
- Reuse: author-hosted access; no permissive reuse grant identified in inspected
  material. Cite and paraphrase; create original examples.

<a id="emp-lawrie-2007"></a>

### EMP-lawrie-2007: Effective Identifier Names for Comprehension and Memory

Dawn Lawrie, Christopher Morrell, Henry Feild, David Binkley; Innovations in
Systems and Software Engineering 3(4), 303-318 (2007).
[Original manuscript](https://www.cs.loyola.edu/~binkley/papers/isse07-id-recall.pdf).
Inspected sections 2.1-2.6, 4.1-4.6 and conclusion, especially Table 1 and
section 4.4, PDF pages 7 and 11-12. Disposition: verified/qualified.

- Population: 128 answered at least one question; 80 completed twelve;
  approximately one-quarter students, others including experienced professionals.
- Task/artifacts: explain twelve C/C++/Java functions, report confidence, then
  recognize previously shown identifiers among six candidates.
- Comparison: full English words, abbreviations (mostly familiar; ten of 63
  supplied by an independent programmer), first-letter variants.
- Result: Table 1 description means 3.91/3.72/3.10 for words/abbreviations/letters;
  recognition proportions .81/.81/.72. Initial pairwise tests separated letters
  from both alternatives; words and abbreviations were statistically indistinguishable.
  The recall model associated more syllables with poorer recognition.
- Limits: small functions, attrition, subjective description grading,
  recognition rather than free recall, and interactions with task familiarity.
  Nonsignificance supplies uncertainty rather than proof of equivalence.
- Reuse: publicly readable manuscript; no open reuse license identified.
  Paraphrase with attribution; reproduce neither tasks nor figures.

### B06: Syntactic Identifier Conciseness and Consistency

Dawn Lawrie, Henry Feild, David Binkley; SCAM 2006,
DOI 10.1109/SCAM.2006.31.
[Author-hosted original](https://hank.feild.org/publications/scam06-conciseness.pdf).
Inspected sections 1-4.5, especially 3, 4.2-4.4 and Figures 1-2.
Disposition: replaced (primary link and corrected attribution), verified/qualified
for syntactic analysis.

- Artifacts: approximately 48.6 million lines across open and proprietary
  programs, mainly C/C++/Java, with Fortran examples.
- Task/comparison: detect name-pattern violations as a proxy for concept-based
  naming rules; compare selected findings with human concept judgments and
  inspect program versions. Humans supply an oracle, rather than a comprehension
  experiment population.
- Result: about three-quarters of case-study detections matched concept-based
  violations. Seven projects with at least four versions supplied essentially
  no evidence of increasing synonym violations with evolution.
- Limits: syntactic approximation, false positives, sampled judgments, and scope
  context. Section 4.3 explicitly illustrates qualification supplied by a type
  or local scope. Violation counts measure naming-pattern prevalence.
- Reuse: author-hosted conference manuscript; no permissive reuse grant found.
  Cite the original and paraphrase.

<a id="emp-deissenboeck-2005"></a>

### B07 / EMP-deissenboeck-2005: Concise and Consistent Naming

Florian Deissenboeck, Markus Pizka; IWPC 2005.
[TUM original](https://wwwbroy.in.tum.de/publ/papers/deissenboeck_pizka_identifier_naming.pdf).
Inspected sections 1.1, 3.1-3.2, 4, 5 and 6, PDF pages 1, 4-10.
Disposition: B07 aggregator replaced with this explicitly identified version;
formal model verified/qualified.

- Evidence: conceptual model, development observations, lexical corpus counts,
  and identifier-dictionary tool design.
- Population/task: CloneDetective development by two graduate and ten
  undergraduate students; observations concerning ambiguous position concepts.
  Eclipse, JDK, and Tomcat provide Java identifier counts.
- Comparison/result: formal correctness, conciseness, and consistency definitions
  relate names to a scoped concept set. The project account describes maintenance
  difficulty; it supplies neither controlled rename treatment nor defect-rate
  correlation. Conciseness denotes semantic specificity, not few characters.
- Limits: proposed benefits and observational explanation require their own
  evidence class. Universal causal or quantitative productivity claims are excluded.
- Reuse: IEEE proceedings copyright appears in the PDF. Paraphrase with
  citation; use original diagrams and scenarios.

The [2006 journal edition](https://link.springer.com/article/10.1007/s11219-006-9219-1)
is Software Quality Journal 14, 261-282, September 2006, DOI
10.1007/s11219-006-9219-1. Its publisher abstract identifies the formal model
and dictionary. Only metadata, abstract, references, and rights section were
accessible. The Semantic Scholar seed URL returned an internal fetch error;
its exact indexed version remains unresolved. Attribute adopted detailed claims
to the inspected 2005 edition. The journal edition's additional methods and
results remain unverified. Its rights page offers reprint permission requests;
no open license was established.

### B24: Part-of-Speech Tagging of Program Identifiers for Improved Text-based Software Engineering Tools

Samir Gupta, Sana Malik, Lori Pollock, K. Vijay-Shanker; ICPC 2013.
[Original paper](https://www.eecis.udel.edu/~pollock/879tainsef13/samir-postagging.pdf);
[author publication metadata](https://www.eecis.udel.edu/~sgupta/publication.html).
Inspected introductory claim, identifier grammar sections, evaluation IV.A-C,
Tables II-III, and threats IV.D, PDF pages 1, 3-9.
Disposition: verified/qualified for grammar/tool evidence; excluded as empirical
support for positive boolean polarity.

- Artifacts/task: POSSE versus TemplateTagger and TreeTagger on 210 Java and
  100 C++ method/class/attribute names; two independent-of-authorship annotators
  jointly established the gold tags using signature and language context.
- Measures/result: complete identifier tagging accuracy; POSSE 91.4% Java and
  85% C++, against TreeTagger 77.1%/74% and TemplateTagger 75.7%/65%.
- Limits: small held-out identifier sets, annotation judgments, and grammar
  coverage. Grammar recognition accuracy supplies tool evidence, while boolean
  truth-condition comprehension requires a different experiment.
- Reuse: institutional manuscript; no open reuse permission identified.
  Cite/paraphrase; exclude copied identifier datasets and grammar tables.

<a id="emp-cates-2021"></a>

### EMP-cates-2021: Does Code Structure Affect Comprehension? On Using and Naming Intermediate Variables

Roee Cates, Nadav Yunik, Dror G. Feitelson; arXiv:2103.11008v1, March 19, 2021.
[Original manuscript](https://arxiv.org/pdf/2103.11008).
Inspected design and population IV, results V, discussion VI, threats VII,
PDF pages 2-8. Disposition: verified/qualified; identify the inspected preprint.

- Population: 113 Python-experienced participants answered at least one task;
  93 completed six; 58% reported at least three years of programming work.
- Task: give meaningful function names to six mathematical Python functions.
- Comparison: compound expressions, intermediate variables with meaningless
  names, intermediate variables with meaningful names.
- Measures/result: correct understanding and time to correct answer. Against
  compound expressions, meaningful intermediate variables improved correctness significantly for only one
  individual function, the hardest; pooled evidence favored that version,
  largely driven by this case. Several other comparisons were inconclusive.
- Limits: structural and naming changes combine in the extreme comparison;
  mathematical familiarity, attrition, and few functions constrain transfer.
  More named temporaries cannot be promised to improve every use site.
- Reuse: arXiv access establishes readability; this inspection established no
  permissive redistribution license. Paraphrase, link, and create original examples.

<a id="emp-sharif-2010"></a>

### EMP-sharif-2010: An Eye Tracking Study on camelCase and under_score Identifier Styles

Bonita Sharif, Jonathan I. Maletic; ICPC 2010, 196-205,
DOI 10.1109/ICPC.2010.41.
[Author-hosted manuscript](https://www.cs.kent.edu/~jmaletic/papers/ICPC2010-CamelCaseUnderScoreClouds.pdf).
Inspected sections III-IV, V-VI, PDF pages 2-9.
Disposition: verified/qualified as identifier-recognition evidence.

- Population: analysis describes 15 programmers, mostly trained in underscores.
  III.F's subgroup counts sum to 17, an internal reporting inconsistency; avoid
  publishing the subgroup breakdown.
- Task: eight phrase-to-identifier recognition tasks, selecting among four
  similar names; within-participant camelCase/underscore comparison.
- Measures/result: correctness, response time, and gaze effort. The simple model
  reports camelCase taking 932 ms (20%) longer, p=.037. Only one answer was
  wrong, limiting accuracy comparisons. Stated style preferences were mixed.
- Limits: tiny sample, different paired phrases, fixed task order, isolated
  recognition rather than program maintenance. Transfer to ecosystem policy
  requires judgment about actual readers and conventions.
- Reuse: [laboratory publication notice](https://sdml.info/publications.html)
  identifies prepress copies and directs copyright questions to publishers.
  Cite/paraphrase; create original stimuli.

## Additional leads and access dispositions

<a id="emp-avidan-2017"></a>EMP-avidan-2017: Eran Avidan and Dror G. Feitelson, *Effects of Variable Names
on Comprehension: An Empirical Study*, ICPC 2017, 55-65,
DOI 10.1109/ICPC.2017.27. The
[author institution record](https://cris.huji.ac.il/en/publications/effects-of-variable-names-on-comprehension-an-empirical-study/)
supplies an abstract: nine professional developers, six production utility
methods, original versus single-letter names; three methods lacked significant
differences, interpreted as poor or misleading original names. Metadata records
IEEE copyright. ResearchGate offered a full-text request rather than a paper;
the author's guessed publications URL was unavailable. Disposition: unresolved
full-text access, excluded from adopted detailed empirical recommendations.
Its abstract remains optional context with these access limits. The core validation workflow is justified as local engineering
judgment and executable contextual checks without needing this study.

Other surfaced candidates: neural identifier repair and model-adversarial
renaming studies concern machine performance and are excluded from human
comprehension claims. The single-letter-variable survey is a discovery lead
about associations, rather than inspected causal comprehension evidence;
exclude pending primary-method inspection. Takang et al. and Binkley et al.
appear in inspected papers' related work; their results remain secondary reports
in this audit. Do not present those as independently read replications.

## Concepts and domain terminology sources

<a id="con-iso704-preview"></a>

### CON-iso704-preview / CON-001

Source: ISO, [ISO 704:2022 preview](https://webstore.ansi.org/preview-pages/ISO/preview_ISO%2B704-2022.pdf),
introduction 0.1, printed vi-vii (PDF pages 6-7), 2022. Standard within its
terminology-work scope; full normative clauses were unavailable.

Verified/qualified claim: objects are conceptualized; definitions and designations
represent concepts. Software application is local adaptation: distinguish a
shipment record, its modeled concept, its variable name, and its displayed label.
Use a behavior description and examples to establish the distinction needed for
the naming decision. Mandatory genus-differentia for every name is unsupported by
the inspected preview and is excluded. Reuse: ISO copyright/all-rights-reserved
notice inspected; paraphrase with attribution, retain no diagrams or copied tables.

<a id="con-fowler-language"></a>

### CON-fowler-language / CON-002

Source: Martin Fowler, [Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html),
October 31, 2006, main article paragraphs 1-2. Practitioner guidance explaining
Eric Evans, with Evans attributed in the article; Evans's book was not inspected.

Verified/adopted: develop and test model vocabulary through conversations with
domain experts, revising language as understanding improves. Example application:
ask a dispatcher what makes a consignment distinct while reading its contract and
existing model. A glossary entry is evidence to check against behavior, rather
than an automatic replacement for expert discussion. Reuse: Fowler copyright
notice present, broad reuse permission unverified; original paraphrase, no copied
Evans quotation.

<a id="con-fowler-context"></a>

### CON-fowler-context / CON-003

Source: Martin Fowler, [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html),
January 15, 2014, opening through discussion of multiple canonical models.

Verified/adopted practitioner guidance: maintain internally consistent models
within explicit boundaries and describe relationships between them. Different
contexts can assign different meanings to a shared word. Example application:
`booking.shipment` and `transport.consignment` require explicit mapping evidence
before being equated. This does not require a service per context or an
anticorruption layer for every integration. Reuse: copyright notice present;
paraphrase with attribution, no copied diagram.

### B15 / CON-004

Source: Nicola Guarino and Christopher A. Welty,
[An Overview of OntoClean](https://www.loa.istc.cnr.it/old/Papers/GuarinoWeltyOntoCleanv3.pdf),
laboratory-hosted chapter 8, file version v3; publication year unconfirmed from
inspected title. Exact sections: 8.1 Properties, classes, and subsumption; 8.2
Essence and Rigidity, Identity and Unity, Constraints and Assumptions; 8.3
Assigning Metaproperties, PDF pages 2-6 and 8.

Verified/qualified formal claim: if parent Q subsumes child P, every P is Q in
every modeled possible world. An anti-rigid Q requires anti-rigid P; consequently
an anti-rigid Student parent cannot contain rigid Human as a child. Reversing
those roles is not forbidden by this constraint. Identity concerns recognizing
the same individual; unity concerns its parts and boundaries. These are ontology
commitments, not programming-language inheritance laws. Practical adaptation:
record whether `EncounterParticipant` represents a time-bounded participation
record or an enduring person before choosing its name. Class implementation is a
separate design judgment. Reuse permission unverified; paraphrase only.

### B16 / CON-005

Source: Nicola Guarino and Christopher Welty,
[A Formal Ontology of Properties](https://cui.unige.ch/isi/cours/aftsi/articles/01-guarino00formal.pdf),
2000 paper, university-hosted copy. Inspected introduction and property taxonomy
subsections Types, Quasi-Types, Material Roles, Formal Roles (PDF pages 1, 5-6).

Verified/qualified: formal roles combine anti-rigidity and dependence; type
properties supply identity. Membership conditions and identity conditions answer
different questions. Software use is analogy: `SpecimenReceived` records an event
in an invented application, while `Specimen` models the referenced material.
Whether an entity satisfies a predicate differs from which entity it is.
Exclusion: the paper supplies no opaque-URI recommendation; remove that seed
attribution. Reuse permission unverified; paraphrase with authors and URL.

<a id="con-gruber"></a>

### CON-gruber / CON-006

Source: Thomas R. Gruber,
[Toward Principles for the Design of Ontologies Used for Knowledge Sharing](https://tomgruber.org/writing/onto-design.pdf),
author-hosted manuscript, revision August 23, 1993, title identifies publication
in IJHCS 43, pages 907-928. Section 3, PDF pages 3-5 inspected.

Verified/qualified: proposed ontology design criteria include clarity, coherence,
extendibility, minimal encoding bias, and minimal ontological commitment. Minimal
commitment concerns assertions about the modeled world; it coexists with precise
definitions of distinctions worth making. Treating it as advice for short or
vague names is unsupported. Adaptation: define the actual effect of
`record_specimen_receipt` precisely and avoid inventing laboratory workflow rules
to fill gaps. Evidence is conceptual design argument and case studies, not a
controlled identifier-comprehension experiment. Reuse permission unverified;
paraphrase only, preserve manuscript revision metadata.

<a id="con-skos"></a>

### CON-skos / CON-007

Source: Alistair Miles and Sean Bechhofer, editors,
[SKOS Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/),
W3C Recommendation, August 18, 2009. Inspected synopsis, sections 3, 5.3-5.4,
5.6.4-5.6.5, and 6 table of contents/notes boundaries.

Verified/qualified standard: resources can have preferred and alternative lexical
labels; S14 permits at most one preferred label per language tag, not one global
name per concept. URI identity and lexical labeling are different roles. This
supports distinguishing `specimen_identifier` from `display_label`; it does not
mandate opaque database keys or guarantee URI persistence. A canonical internal
term plus explicit aliases is local policy, conditional on scope and contracts.
Reuse: W3C document-use rules linked on the specification; current
[document license](https://www.w3.org/copyright/document-license-2023/) inspected.
Use original paraphrase and citation; copied/adapted material would require its
applicable notices and conditions to be preserved.

### Context Mapper source limits

[Anticorruption Layer](https://contextmapper.org/docs/anticorruption-layer/),
Syntax/Semantic Rules, and [Shared Kernel](https://contextmapper.org/docs/shared-kernel/),
Syntax/Default Symmetric Relationship, are Context Mapper project documentation,
undated inspected versions with 2025 footer. They describe CML. B10's validation
even distinguishes the tool authors' interpretation from the original pattern.
Both are primary for tool behavior, qualified corroboration of multiple context
relationships, and excluded as universal naming rules. No code copied. Copyright
notice inspected; documentation reuse license unverified.

## Domain sources and example contracts

These are terminology checks for software examples. Each invented behavior below
is an example contract; domain sources establish vocabulary, not that behavior.

<a id="con-cme-glossary"></a>

### CON-cme-glossary / CON-008

Source: CME Group, [Glossary](https://www.cmegroup.com/education/glossary),
undated live reference, headings Bid Price, Ask Price, Offer (Ask Or Sell),
Bid/Ask Spread and Resting Order inspected. Practitioner reference.

Verified/adopted: bid concerns buying; ask/offer concerns selling; bid/ask spread
compares their prices. Original example contract: `spread = ask - bid`, with
both values explicitly prices in one instrument and unit. These terms are more
informative than `first_value` and `second_value`. Real feeds may have missing
sides or venue-specific conventions; the example must state its valid inputs.
Reuse permission unverified, original paraphrase only; no strategy or fee claims.

<a id="con-cme-orders"></a>

### CON-cme-orders / CON-009

Source: CME Group, [Order Functionalities](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457414497),
Order Aggressor Indicator section, live documentation, exact revision date
unconfirmed. Practitioner/protocol documentation inspected.

Verified/qualified: aggressor describes an incoming order matching resting book
orders and removing liquidity in the specified continuous-trading setting.
The documentation scopes aggressor reporting by trading state and instrument
structure. Invented example: `resting_price` is the price of the matched resting
order; `aggressor_limit_price` is the incoming order limit. Preserve both even
when one trade makes them equal. Fee/rebate claims and a universal identity
between aggressor, buyer and maker/taker are excluded. Reuse permission
unverified; original paraphrase only.

<a id="con-uncefact-vocabulary"></a>

### CON-uncefact-vocabulary / CON-010

Source: UN/CEFACT, [Web Vocabulary](https://test.uncefact.org/vocabulary/),
Classes table, Consignment, Shipment and Booking entries; accessible test-site
version, unversioned and unsuitable as a claim about a finalized universal
standard. Practitioner project vocabulary.

Verified/qualified: this vocabulary separates a transport-contract consignment
from trade items shipped seller-to-buyer; booking records reserved transport
services. Invented example: a sales-side shipment can map to two transport-side
consignments, according to the example's explicit split rule. Use
`consignments_by_shipment_identifier` for that mapping and show cardinality.
Terminology varies by logistics context; verify the target project glossary.
Reuse/license unspecified in inspected page; original paraphrases and citation.

Supplementary access record: UN/CEFACT's September 2022
[Integrated Track and Trace BRS](https://unece.org/sites/default/files/2023-07/BRS-IntegratedTrackandTraceforMulti-ModalTransportationv0.1-Final.pdf)
returned internal errors on direct opens. Indexed original excerpts for section
1.1, Figure 2 discussion (printed page 9) and Appendix 1 were readable through
search; they distinguish trade and transport and discuss splitting/consolidation.
Use them only as access-limited corroboration. A UNECE announcement uses a looser
same-meaning phrasing for shipment/consignment, reinforcing the need to preserve
the chosen document and context rather than claim a universal distinction.

<a id="con-portaudio"></a>

### CON-portaudio / CON-011

Source: PortAudio project,
[V19 portaudio.h API reference](https://portaudio.com/docs/v19-doxydocs/portaudio_8h.html),
Pa_OpenStream parameters and declarations, inspected live V19 documentation.
Supplement: Phil Burk, [Audio Latency](https://portaudio.com/docs/latency.html),
2002, V18, What is Latency and PortAudio and Latency sections.

Verified/qualified: distinguish sample rate, channels, frames per buffer and
latency. A frame groups simultaneous channel samples; buffer duration is only
one part of latency. Invented example: at 48,000 frames/second, 480 frames occupy
0.010 seconds; stereo contains 960 scalar samples. Prefer `buffer_frames`,
`sample_rate_hz`, `buffer_duration_seconds` where untyped context needs units.
Typed quantities can supply units themselves. `latency` requires an explicit
measurement boundary. V18 operational tuning advice is excluded; V19 owns API
behavior. Reuse: V18 copyright notice inspected; no source code copied, separate
documentation license unverified.

<a id="con-fhir-encounter"></a>

### CON-fhir-encounter / CON-012

Source: HL7 FHIR [Encounter R5](https://hl7.org/fhir/R5/encounter.html),
v5.0.0, resource definition and section 8.11.1 Scope and Usage inspected.
Standard vocabulary within this release.

Verified/qualified: Encounter models healthcare interactions with an encounter
lifecycle and setting, including movement between practitioners and locations.
Invented example: `EncounterClosed` records an application transition with
explicit timestamp and encounter identifier; its contract states exactly which
stored status changed. A naming example can demonstrate event versus entity
without making clinical discharge, treatment, or retention claims.

<a id="con-fhir-observation"></a>

### CON-fhir-observation / CON-013

Source: HL7 FHIR [Observation R5](https://hl7.org/fhir/R5/observation.html),
v5.0.0, definition and 10.1.1 Scope and Usage inspected. Verified/qualified:
Observation carries measurements/assertions, including laboratory data;
DiagnosticReport can organize observations with clinical/workflow context.
Invented application: `lab_result` holds one laboratory observation, while
`diagnostic_report` groups results. State actual representation and cardinality
before renaming `result` to either term. This source establishes data-model
vocabulary, not diagnostic criteria or medical recommendations.

<a id="con-fhir-specimen"></a>

### CON-fhir-specimen / CON-014

Source: HL7 FHIR [Specimen R5](https://hl7.org/fhir/R5/specimen.html),
v5.0.0, definition and 10.8.1 Scope and Usage inspected. Verified/qualified:
Specimen represents material sampled from biological entities, objects, or the
environment. Invented software example: `record_specimen_receipt` writes a
receipt record; `SpecimenReceived` names its emitted event only if that emission
is established by the example contract. Receipt alone establishes no medical
conclusion.

FHIR reuse for CON-012 through CON-014: the release's
[license page](https://hl7.org/fhir/R5/license.html) was inspected; FHIR uses
CC0, with separately identified terminology and external material exceptions.
Use original examples and release citations; these records import no external
clinical code system content.

## Language and artifact convention sources

| Identifier | Primary source, author/version, inspected sections | Evidence and disposition | Reuse finding |
| --- | --- | --- | --- |
| <a id="lang-google-cpp"></a>LANG-google-cpp | Google, [C++ Style Guide](https://google.github.io/styleguide/cppguide.html#Naming), live; Choosing Names, File Names, Type Names, Variable Names, Function Names, Namespace Names; Namespaces | Verified/qualified organizational convention; LANG-01 | [Repository license](https://github.com/google/styleguide/blob/gh-pages/LICENSE): CC BY 3.0; attribute Google and link source/license for adapted text. |
| <a id="lang-swift"></a>LANG-swift | Swift project, [API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/), live; Fundamentals; Promote Clear Usage; Strive for Fluent Usage; Use Terminology Well; General Conventions | Verified/qualified language/API guidance; LANG-02 | [Website license](https://github.com/swiftlang/swift-org-website/blob/main/LICENSE.txt): Apache 2.0 with runtime exception; use original examples and attribution. |
| <a id="lang-python"></a>LANG-python | Guido van Rossum, Barry Warsaw, Nick Coghlan, [PEP 8](https://peps.python.org/pep-0008/#naming-conventions), created 2001-07-05; inspected page modification 2025-04-04; Naming Conventions and Programming Recommendations | Verified/qualified Python guidance; LANG-03 | Copyright section places the PEP in the public domain; retain attribution for provenance. |
| <a id="lang-rfc430"></a>LANG-rfc430 | Rust project, [RFC 430](https://rust-lang.github.io/rfcs/0430-finalizing-naming-conventions.html#general-naming-conventions), start 2014-11-02; General naming conventions and unwrap/into_foo/into_inner | Verified/qualified historical conventions proposal; LANG-04 | RFC-specific license not inspected; paraphrase and link. |
| B21 | Rust library team and contributors, [Rust API Guidelines: Naming](https://rust-lang.github.io/api-guidelines/naming.html), live; C-CASE, C-CONV, C-GETTER, C-ITER | Verified/qualified current ecosystem recommendations; LANG-05 | [Repository License](https://github.com/rust-lang/api-guidelines#license): MIT or Apache 2.0; preserve applicable notices for copied material. |
| <a id="lang-javascript"></a>LANG-javascript | Google, [JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html#naming), live; 6.1, 6.2.1-6.2.10, 6.3 | Verified/qualified Google JavaScript/Closure conventions; LANG-06 | Google style guide CC BY 3.0, as above. |
| <a id="lang-typescript"></a>LANG-typescript | Google, [TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#naming), live; Naming, Imports, Use modules not namespaces | Verified/qualified Google convention; LANG-07 | Google style guide CC BY 3.0, as above. |
| <a id="lang-typescript-contributors"></a>LANG-typescript-contributors | Microsoft TypeScript contributors, [Coding guidelines](https://github.com/microsoft/TypeScript/wiki/Coding-guidelines#names), page edited 2021-05-24; opening scope statement, Names | Verified/qualified compiler-project guidance; LANG-08 | Wiki-specific reuse terms not inspected; cite and paraphrase. |
| <a id="lang-aip140"></a>LANG-aip140 | Google, [AIP-140 Field names](https://google.aip.dev/140), live approved AIP; Guidance, Case, Uniformity, Repeated fields, Abbreviations, Verbs, Booleans, Reserved words, Conflicts | Verified/qualified Google resource-oriented API guidance; LANG-09 | Footer: CC BY 4.0 prose; Apache 2.0 code. |
| <a id="lang-aip141"></a>LANG-aip141 | Google, [AIP-141 Quantities](https://google.aip.dev/141#guidance), created 2019-07-18; changelog includes 2025-07-09; Guidance, Inverse units, Specialized messages | Verified/qualified quantity field guidance; LANG-10 | Footer: CC BY 4.0 prose; Apache 2.0 code. |
| <a id="lang-aip136"></a>LANG-aip136 | Google, [AIP-136 Custom methods](https://google.aip.dev/136#guidance), created 2019-01-25, live; Guidance, Stateless methods, Declarative-friendly resources | Verified/qualified API convention; LANG-11 | Footer: CC BY 4.0 prose; Apache 2.0 code. |
| <a id="lang-protobuf"></a>LANG-protobuf | Protocol Buffers project, [Style Guide](https://protobuf.dev/programming-guides/style/), live; File Structure, Identifier naming styles, Packages, Message Names, Field Names | Verified/qualified schema convention and generator collision rationale; LANG-12 | Page reuse license not separately inspected; original summaries and examples only. |
| <a id="lang-domain-events"></a>LANG-domain-events | Microsoft, [Domain events: Design and implementation](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation#implement-domain-events), live; Implement domain events | Verified/qualified DDD/.NET practitioner guidance; LANG-13 | Page-specific reuse terms not inspected; paraphrase with attribution. |
| <a id="lang-cqrs-commands"></a>LANG-cqrs-commands | Peter Vogel, Microsoft MSDN Magazine, [Leverage CQRS to Create Highly Responsive Systems](https://learn.microsoft.com/en-us/archive/msdn-magazine/2016/july/cqrs-leverage-cqrs-to-create-highly-responsive-systems#handling-commands-and-events), July 2016; Handling Commands and Events | Verified/qualified practitioner guidance; full relevant section accessible despite page authorization notice; LANG-13. | Reuse terms unverified; no text or examples copied. |
| B08 | Felienne interviewing Peter Hilton, [SE Radio 278](https://se-radio.net/2016/12/se-radio-episode-278-peter-hilton-on-naming/), 2016-12-20; description and Show Notes | Excluded as direct claim support: inspected metadata establishes topics, not interview findings; specific author essay is preferable. | Audio reuse terms unverified; no reproduction. |
| B11 | Peter Hilton, [blog index](https://hilton.org.uk/blog/), live | Replaced by LANG-hilton-smells; index is discovery only. | Index footer links author's site license. |
| <a id="lang-hilton-smells"></a>LANG-hilton-smells | Peter Hilton, [Naming smells](https://hilton.org.uk/blog/naming-smells), 2016-10-31; Abstract names, Numeric suffixes, Abbreviated names, Vague words, Vestigial Hungarian notation, Wrong names | Verified/qualified practitioner essay; LANG-14 | Footer: CC BY-NC-SA 4.0, excluding images/presentations; required credit identifies Peter Hilton and hilton.org.uk. Use brief attributed summary, original examples; reproduce no essay assets. |
| B20 | Steve Yegge, [Execution in the Kingdom of Nouns](https://steve-yegge.blogspot.com/2006/03/execution-in-kingdom-of-nouns.html), March 2006; opening and Kingdom of Nouns | Verified/qualified practitioner satire; LANG-15 | Reuse permission unverified; link and summarize briefly. |
| B22 | [Scribd Rust API Guidelines copy](https://www.scribd.com/document/754922698/Rust-API-Guidelines), uploader/version unverified; HTML preview accessible | Replaced by B21, which has authoritative ownership and version context. | Third-party upload grants no assumed rights. |
| B23 | [Reddit Rust naming discussion](https://www.reddit.com/r/rust/comments/1j43h8g/rusts_functionmethod_naming_convention/), community discussion, HTML accessible | Replaced by B21 and LANG-rfc430; discussion is unnecessary for current convention claims. | No excerpts copied. |
| B26 | [SlideShare naming talk](https://www.slideshare.net/slideshow/how-to-name-things-the-hardest-problem-in-programming/39383508), title matches Peter Hilton talk, edition/date unverified; HTML transcript accessible | Excluded: unnecessary duplicate presentation channel; claims use author's dated essay. | Presentation-specific rights unverified; reproduce no slides. |
| B27 | Peter Hilton account, [Speaker Deck naming talk](https://speakerdeck.com/hilton/how-to-name-things-the-hardest-problem-in-programming), edition/date unverified; transcript opening inspected | Excluded: talk transcript mixes quotations and images; essay provides precise self-contained support. | Site's blog license explicitly excludes presentations; individual slides credit third parties. Reproduce no slides. |

## Compatibility sources

All sources were accessed through the web tool on 2026-09-06. Sections listed
below were opened and inspected, rather than inferred from search snippets.
Documentation versions are those displayed by the accessed page; a rolling URL
needs refreshing against the implementation's actual version. No empirical
performance or defect-rate claim is adopted in this report.

| Identifier | Author, version, and exact inspected source | Evidence and limits | Reuse and disposition |
| --- | --- | --- | --- |
| <a id="comp-refactoring"></a>COMP-refactoring | Martin Fowler, [Refactoring](https://refactoring.com/), opening definition, Definition, Automated tools are helpful; [Change Function Declaration](https://refactoring.com/catalog/changeFunctionDeclaration.html), catalog entry; live pages, no revision date displayed | Practitioner definition and public catalog summary; full book mechanics require book access | Copyright Martin Fowler displayed; original paraphrase and link only. Verified/adopted definition; qualified tool guidance |
| <a id="comp-aip180"></a>COMP-aip180 | Google, approved AIP-180, live version accessed 2026-09-06; header created/updated 2019-07-23, latest changelog 2025-10-21; [Backwards compatibility](https://google.aip.dev/180), Guidance, Adding components, Removing or renaming components, Moving components between files, Changing resource names, Semantic changes, Default values, Serializing defaults, Changelog and footer | Official policy for Google-style multi-consumer APIs, especially protobuf/JSON; expressly indicative rather than exhaustive. Changelog establishes revisions later than the header date | Footer: CC BY 4.0 prose and Apache 2.0 code samples, except where noted. Preserve attribution and identify changes for reused prose; this report uses paraphrase and links. Verified/qualified |
| <a id="comp-protojson"></a>COMP-protojson | Protocol Buffers project, [ProtoJSON Format](https://protobuf.dev/programming-guides/json/), Field names as JSON keys, Presence and default-values, Duplicate keys, Enum Aliasing/Safe Renaming Strategy, Any, ProtoJSON Wire Safety; rolling specification | Format rules and a concrete distributed enum migration; binary, generated source, JSON and stored data have different compatibility surfaces | Terms URL returned internal error; license unresolved for reproduction. Paraphrase/link only; no copied examples. Verified/qualified |
| <a id="comp-proto3"></a>COMP-proto3 | Protocol Buffers project, [Language Guide (proto 3)](https://protobuf.dev/programming-guides/proto3/), Assigning Field Numbers, Reserved Field Numbers, Reserved Field Names, Updating A Message Type, Defining Services, Generating Your Classes; rolling guide | Documents field-number identity, reservation, schema evolution and generated bindings; protobuf-specific | Same license limit as COMP-protojson. Paraphrase/link only. Verified/qualified |
| <a id="comp-python-runtime"></a>COMP-python-runtime | Python Software Foundation, Python 3.14.7, [getattr](https://docs.python.org/3/library/functions.html#getattr) and [hasattr](https://docs.python.org/3/library/functions.html#hasattr) | Official runtime semantics for string attribute lookup; language-aware reference tools need separate dynamic-use inspection | [Python license](https://docs.python.org/3/license.html) inspected; PSF License Version 2, examples additionally zero-clause BSD. Original examples preferred. Verified/adopted |
| <a id="comp-python-pickle"></a>COMP-python-pickle | Python Software Foundation, Python 3.14.7, [What can be pickled and unpickled?](https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled), Pickling Class Instances | Functions/classes use qualified names and importable definitions; instance state also matters. These rules apply to pickle, not every serializer | Same Python license. Paraphrase/link only. Verified/adopted |
| <a id="comp-python-cli"></a>COMP-python-cli | Python Software Foundation, Python 3.14.7, [argparse dest](https://docs.python.org/3/library/argparse.html#dest), deprecated | Public option spelling can map to a separate attribute. Shared destinations have parser-specific precedence; deprecated keyword added in 3.13 | Same Python license. Paraphrase/link and original examples. Verified/qualified |
| <a id="comp-kubernetes"></a>COMP-kubernetes | Kubernetes contributors, [Deprecation Policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/), REST resources, Component config structures, Deprecating a flag or CLI, Deprecating a feature or behavior; live policy | Project-specific version, stability, warning, and support rules. CLI/configuration are contractual surfaces | Inspected policy and [Documentation Content Guide](https://kubernetes.io/docs/contribute/style/content-guide/) did not expose licensing in retrieved text. License unresolved; paraphrase/link only. Verified/qualified |
| <a id="comp-postgresql"></a>COMP-postgresql | PostgreSQL Global Development Group, PostgreSQL 18, [ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html), Synopsis, Description, RENAME, Notes, Examples | Direct column rename exists; operations have locking and dependency effects. Database feature support alone cannot verify external consumers | [PostgreSQL License](https://www.postgresql.org/about/licence/) inspected: permissive notice-retaining license. Original examples preferred. Verified/qualified |
| <a id="comp-cooluris"></a>COMP-cooluris | Leo Sauermann and Richard Cyganiak, editors, W3C Interest Group Note 2008-12-03, [Cool URIs for the Semantic Web](https://www.w3.org/TR/2008/NOTE-cooluris-20081203/), Status, Scope, section 4.5 | Informative HTTP/RDF guidance, not a Recommendation; supports persistence and mnemonic identifiers under its scope | Copyright and W3C document-use link displayed; terms not fully inspected. Paraphrase/link only. Verified/qualified |
| <a id="comp-http-delete"></a>COMP-http-delete | Roy Fielding, Mark Nottingham and Julian Reschke, RFC 9110, June 2022, [section 9.3.5 DELETE](https://www.rfc-editor.org/rfc/rfc9110.html#name-delete) | HTTP semantics permit underlying information/storage to remain; says nothing about a particular application's legal obligations | RFC copyright/IETF Trust notice applies; reproduce no prose or code. Verified/adopted for HTTP scope |
| <a id="comp-stripe-authorization"></a>COMP-stripe-authorization | Stripe, [Place a hold on a payment method](https://docs.stripe.com/payments/place-a-hold-on-a-payment-method), introduction and authorization/capture explanation; rolling documentation | Provider-specific distinction between authorization, capture and expiration; insufficient for a universal clearing/settlement glossary | No documentation reuse license established; paraphrase/link only. Verified/qualified |

License uncertainty restricts reproduction, not linking to inspected evidence.
The guide preserves source-level attribution and uses original scenarios.

## Adopted local resources

The repository skill authors and maintainers own these living resources; the
inspected edition is the repository tree on 2026-09-06. Their authority here is
local workflow policy. Preserve repository notices when distributing the tree;
external rights remain attached to their respective sources. Naming paraphrases
workflow decisions and links directly to maintained resources.

| ID and resource | Inspected sections and adoption boundary | Consuming reference |
| --- | --- | --- |
| <a id="local-documentation"></a>LOCAL-documentation: [Documentation](../../documentation/SKILL.md), [maintenance](../../documentation/references/maintenance.md), [evidence](../../documentation/references/evidence.md) | Human references own guidance; a concise entry point routes readers. Claim kinds and source refresh govern this register. | This register and maintenance |
| <a id="local-design"></a>LOCAL-design: [Design](../../design/SKILL.md#the-interview-resolves-what-discovery-surfaces) | Read available code and language first; ask concrete scenario questions about material uncertainty. Naming uses a proportionate brief. The complete discovery/interview/HTML design workflow applies to a requested design task. | [Elicitation](elicitation.md) |
| <a id="local-matrix"></a>LOCAL-matrix: [Decision matrix](../../decision-matrix/SKILL.md#workflow), [artifact template](../../decision-matrix/references/artifact-template.md), [HTML asset](../../decision-matrix/assets/example-lean.html) | Adopt task-specific criteria, cell reasoning before decision, use sites, assumptions, and HTML structure. Candidate count follows semantic uncertainty; a clear winner uses concise prose. Scores aid judgment. Record a recommendation as a recommendation and an accepted decision as a decision. | [Selection](selection.md) |
| <a id="local-glossary"></a>LOCAL-glossary: [Glossary](../../glossary/SKILL.md#how-meaning-is-derived) | Establish terms using code, domain authorities and explicit divergence handling; consult the glossary without automatically launching a whole-codebase glossary project. | [Domain vocabulary](domain-vocabulary.md) |
| <a id="local-creating-skills"></a>LOCAL-creating-skills: [Creating skills](../../creating-skills/SKILL.md) | Entry-point routing, independent evaluation, objective grading and actual human review govern package development and revision. | [Maintenance](maintenance.md) |
| <a id="local-verification"></a>LOCAL-verification: [Verification before completion](../../verification-before-completion/SKILL.md) | Fresh command evidence supports completion claims within the checks' actual scope. | [Contextual validation](contextual-validation.md), [Renaming](renaming.md) |

Repository-tree installation supplies these siblings and their loaded resources.
See [maintenance](maintenance.md) for refresh and installation checks.
