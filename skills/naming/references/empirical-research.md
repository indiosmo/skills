# What naming studies can tell you

Names can help readers understand a program, but the benefit depends on the
words, the task, and the context. The studies below help assess a recommendation's
strength. They complement inspection of the actual declaration, callers, and
contracts when choosing a particular name.

The source and claim identifiers connect this page to the
[source register](sources.md) and [evidence register](evidence.md). This is a
targeted review of identifier research and the claims used by this guide.
Publication selection followed those questions; it was not an exhaustive
systematic review. Original papers were inspected on 2026-09-06.

## Full words and familiar abbreviations

Two studies support giving readers meaningful words. Their abbreviation
conditions differ, which matters when applying the findings.

| Study | People and task | Comparison and finding | Decision limit |
| --- | --- | --- | --- |
| Hofmeister, Siegmund and Holt, 2017 | 72 retained experienced C# developers found semantic defects in short functions | Full words produced more defects found per minute than letters or mechanically shortened abbreviations | Artificial abbreviations, short snippets and a restricted viewport limit transfer to familiar domain terms and larger programs |
| Lawrie, Morrell, Feild and Binkley, 2007 | 128 people answered at least one function-description task; 80 completed twelve; participants included students and professionals | Full words and mostly familiar abbreviations both outperformed letters in initial description and recognition comparisons; words versus abbreviations was statistically indistinguishable | Small functions, participant attrition, subjective description grading, and task familiarity constrain generalization |

The [2017 experiment](https://brains-on-code.github.io/shorter-identifier-names.pdf),
sections IV-VII and Table VII, reports a 19% increase in defect-finding speed for
words compared with the two shorter conditions. That is a task-specific measure
of finding seeded defects. It cannot establish a reduction in defects introduced
into production software. Its abbreviations generally retained three consonants,
with some familiar-prefix exceptions. An accepted term such as `http` needs its
own audience and context assessment. Claims EMP-001 through EMP-004 preserve
these boundaries.

The [2007 experiment](https://www.cs.loyola.edu/~binkley/papers/isse07-id-recall.pdf),
sections 2 and 4, used C, C++ and Java functions and mostly familiar abbreviations.
Table 1's mean description ratings were 3.91 for words, 3.72 for abbreviations and
3.10 for letters. The corresponding identifier-recognition proportions were
0.81, 0.81 and 0.72. These numbers describe the study's tasks and grading scale.
The paper separately analyzes confidence and memory. A statistically
indistinguishable result leaves uncertainty about the difference; it does not
prove equivalence.

For this guide, full words are the default, with accepted domain abbreviations
appropriate in local scope. That is an explicit project policy, informed by
research and the intended readers. Apply it by asking whether a reader knows
the term and whether expanding it would clarify the role. Preserve externally
specified spellings as contracts. See [domain vocabulary](domain-vocabulary.md)
and [language conventions](language-conventions.md).

## Comprehension and memory answer different questions

Explaining a function, finding a defect, recognizing an identifier, and recalling
a name without choices are different tasks. The Lawrie study's memory task
asked participants to recognize previously displayed identifiers among choices.
Its model associated additional syllables with poorer recognition. This finding
does not establish a preferred maximum identifier length for a codebase.

Consider these original use-site sketches:

```python
retry_policy.should_retry(attempt_count=attempt_count)
should_retry_delivery_after_transient_failure(attempt_count)
```

The first call can obtain policy and domain context from its receiver and nearby
code. A free function can include relevant context in its name; its module and
surrounding code also contribute meaning. Which is clearer depends on their
actual contracts and readers. Counting characters
cannot establish whether the extra words communicate a needed distinction.
See [foundations](foundations.md) for the role of scope and
[contextual validation](contextual-validation.md) for the evidence to inspect.

## A naming model is a different kind of evidence

Deissenboeck and Pizka's
[Concise and Consistent Naming](https://wwwbroy.in.tum.de/publ/papers/deissenboeck_pizka_identifier_naming.pdf)
(IWPC 2005, sections 3-6) proposes a model relating identifiers to scoped concepts
and an identifier dictionary. Its project observations illustrate ambiguity;
its corpus counts describe identifier use. In that model, conciseness concerns
semantic specificity rather than character count.

The model gives a useful review question: do two similar names denote the same
concept, or does their difference preserve something a reader needs? Its
observational examples do not measure a causal reduction in maintenance cost or
a correlation between naming violations and production defect rates. The 2006
journal edition's metadata and abstract were accessible; detailed claims here
refer to the inspected 2005 manuscript. See EMP-001, EMP-005 and EMP-006.

Lawrie, Feild and Binkley's
[Syntactic Identifier Conciseness and Consistency](https://hank.feild.org/publications/scam06-conciseness.pdf)
(SCAM 2006, sections 3-4) is a separate paper by different authors. It detects
syntactic patterns across about 48.6 million lines of code and compares selected
findings with human concept judgments. Roughly three-quarters of case-study
detections agreed with concept-based violations. These are detector and corpus
results. Its version study supplied essentially no evidence of increasing
synonym violations across the seven examined evolving projects.

A search or detector can flag a candidate inconsistency. Resolving it requires
the referent and scope: two independent `status` fields can accurately describe
different state machines. The practical review procedure is local engineering
judgment informed by the model, with its outcome checked against actual code.

## Grammar recognition and boolean meaning

Gupta, Malik, Pollock and Vijay-Shanker's
[Part-of-Speech Tagging of Program Identifiers](https://www.eecis.udel.edu/~pollock/879tainsef13/samir-postagging.pdf)
(ICPC 2013, evaluation IV.A-C and threats IV.D) compares tagging tools against human
annotations for 210 Java and 100 C++ identifiers. POSSE's complete-identifier
accuracy was 91.4% and 85%, respectively. The experiment evaluates a grammar
recognizer.

Boolean naming in this guide relies on accurate truth conditions, call-site
grammar, and the relevant ecosystem convention. For example,
`retry_enabled` may describe policy while `connection_available` describes
current state. Both can be clear, and neither alone establishes whether an
operation should retry. The tagging study supplies no comparison of positive
and negative predicates that would justify changing those truth conditions.
See EMP-009 and [variables and state](variables-and-state.md).

## Additional evidence with narrow transfer

Cates, Yunik and Feitelson's
[intermediate-variable study](https://arxiv.org/pdf/2103.11008)
(inspected preprint v1, 2021, sections IV-VII) asked Python-experienced
participants to name six mathematical functions. Of 113 participants who
answered a task, 93 completed all six. It compared compound expressions with
intermediate variables carrying meaningful or meaningless names. Comparing
meaningful intermediate variables with compound expressions produced a significant
correctness improvement for only one individual function, the hardest; pooled
results were largely driven by that case. Naming a useful sub-result can
help, but introducing more named temporaries needs use-site justification.
The comparison of extremes also changes structure. See EMP-014.

Sharif and Maletic's
[identifier-style eye-tracking study](https://www.cs.kent.edu/~jmaletic/papers/ICPC2010-CamelCaseUnderScoreClouds.pdf)
(ICPC 2010, sections III-VI) describes 15 programmers selecting identifiers that
matched phrases. It reports faster underscore recognition in its simple model.
The participants' training, tiny sample, paired phrases, and fixed task order
limit transfer to normal maintenance work. Subgroup counts in its demographic
description are internally inconsistent, so this guide retains the overall
reported analysis size and flags that limitation. Familiarity and ecosystem
convention remain part of a real casing decision. See EMP-010.

Avidan and Feitelson's 2017 study was located through its
[author-institution record](https://cris.huji.ac.il/en/publications/effects-of-variable-names-on-comprehension-an-empirical-study/).
Only the abstract and metadata were available. Its detailed methods and results
remain outside the adopted empirical foundation. The
[evidence register](evidence.md) records this access limit for future review.

## Apply findings to a naming decision

Start from the behavior and the reader's available context. Use meaningful,
recognized terms; keep the distinctions the program actually implements. Show
the proposed name in representative calls and declarations, then review its fit
against independent contextual evidence. A published aggregate result can
support a heuristic; the actual naming decision still needs that local evidence.

Report what was checked and what remains uncertain. This guide's workflow,
decision matrices, and rename checks are engineering procedures whose utility
requires their own evaluation. The studies above establish their stated tasks,
not a measured improvement from using this complete skill.
