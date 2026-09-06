# Maintaining the documentation skill

A maintainer updates the skill when upstream guidance, tool behavior, project
conventions or acceptance findings change. Start with the affected route and its
human reference, then inspect the templates, examples and tests that depend on
it. Preserve a concise entry point and load detailed material by task.

## Sources and editorial guidance

Use [the source register](sources.md) to find adopted sections, access dates,
local adaptations and attribution requirements. Recheck primary guidance before
changing a rule. Record source changes and access failures, separate upstream
requirements from house preferences, and preserve necessary notices when
redistributing licensed material. Remove duplicated guidance when an upstream
reference or native tool adequately owns it.

When changing a human reference, check its purpose, audience, context, structure,
examples and source links independently of SKILL.md. Then verify the entry
point's read condition and section links, its corresponding templates and
completed examples. A routing layer should add selection and instructions while
the base reference remains independently useful. References over 300 lines need
a contents list; split only when the resulting references have distinct useful
purposes.

## Tool and rule changes

Review the locked Python dependency changes and release notes before updating
parsers or verification tools. Re-run each linter rule's valid and invalid cases,
source-position and malformed-input tests, supported-language fixtures, and the
representative runtime measurement. Update the enforcement map when grammar
support or native Doxygen diagnostics change. Each custom rule retains a stable
identifier, upstream link, documented scope and regression cases.

Update the Vale binary and Google package reproducibly, then run prose and source
fixtures, vocabulary, scoped exceptions and code-token false-positive cases.
Recheck the installed tool's configuration syntax. Link-checker upgrades require
valid, broken, redirect, fragment and transport-failure checks; review exclusions
for a current reason. Keep native diagnostics visible in validation reports.

## Environment and acceptance

Exercise the existing Doxygen/MkDocs fixture with temporary output and preserved
relative paths. Inspect reference signatures, examples and cross-references,
site navigation/assets/anchors, and combined generated links. Run examples with
their pinned setup and expected outputs, including planted semantic defects.
Use the [acceptance rubric](../tests/acceptance/README.md) for all supported routes,
missing evidence, unavailable tools and reader-oriented quality assessment.

After a routing or workflow change, run representative independent authoring
scenarios and compare the results with the previous skill where useful. Retain
prompts, input revisions, outputs, grading and known limits in the development
review record. Run package format and local-link checks on the assembled skill,
then audit the actual task requirements before claiming completion. Report human
review status separately from passing automated checks.
