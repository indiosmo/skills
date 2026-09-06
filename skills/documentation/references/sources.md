# Sources and adoption decisions

This register helps documentation authors locate the guidance behind the workflow
and distinguish upstream advice from local editorial choices. Consult the relevant
section when writing or reviewing that kind of material. Product claims still
need evidence from the product and version being documented.

The sources below were accessed on **2026-09-06**. Access confirms the cited
guidance, rather than pinning the source for all future work. Record the version
of each installed tool and rule package when running validation.

## Document purpose and reader needs

| Source and relevant sections | Adoption and local adaptation | Attribution and reuse |
| --- | --- | --- |
| Daniele Procida, [Diataxis compass](https://diataxis.fr/compass/#using-the-compass), [tutorials](https://diataxis.fr/tutorials/), [how-to guides](https://diataxis.fr/how-to-guides/), [reference](https://diataxis.fr/reference/#provide-examples), and [explanation](https://diataxis.fr/explanation/#keep-explanation-closely-bounded) | Route by reader need and keep each page focused. A useful illustrative example can belong in reference. Give ADRs, changelogs, release notes, and orientation pages their own contracts. | Attribute the framework to Procida and link to diataxis.fr, as requested in the [colophon](https://diataxis.fr/colophon/#citation-and-contribution). Local templates are original adaptations; consult repository licensing before copying text or diagrams. |
| Write the Docs, [How to write software documentation](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/#what-to-include-in-software-documentation), including audience, installation, examples, and README | Establish who needs the page, provide a usable starting point, and route readers to deeper material. Select sections by the document contract. | Credit Write the Docs when referring to its guidance. Link rather than reproduce its template; verify applicable licensing before redistribution. |
| Write the Docs, [Documentation principles](https://www.writethedocs.org/guide/writing/docs-principles/#principles-for-great-content), especially ARID, Skimmable, Exemplary, Consistent, and Current | Keep information maintainable while allowing repetition needed for a usable procedure. Use descriptive headings and links, project terms, and current examples. | Original local synthesis with source links; verify licensing before copying substantial material. |

## Language and presentation

| Source and relevant sections | Adoption and local adaptation | Attribution and reuse |
| --- | --- | --- |
| Google, [developer documentation style guide](https://developers.google.com/style), [global audience](https://developers.google.com/style/translation), [active voice and exceptions](https://developers.google.com/style/voice#exceptions), and [notices](https://developers.google.com/style/notices#when-not-to-use-a-note-notice-type) | Google supplies the baseline. Favor clear actors and accessible wording; retain appropriate passive constructions. Place prerequisites before actions. Review notice placement and density in context. | Google pages state CC BY 4.0 for prose and Apache 2.0 for samples unless otherwise noted. Preserve attribution and identify modifications when adapting licensed content. |
| Google, [Markdown style guide](https://google.github.io/styleguide/docguide/style.html), lists, code, and links | Use the consuming project's Markdown dialect and renderer. Verify fences, nesting, and rendered links in that environment. | Link to guidance; check the repository license before copying its examples or text. |
| Vale, [Google package](https://vale.sh/explorer/google) and [code-aware linting](https://vale.sh/features/code) | Adopt the published Google rule package. Configure source-comment scopes and inspect coverage against actual language fixtures. Editorial and factual review complement lint results. | Preserve the package's license and notices if vendoring it. Installation through the package manager keeps upstream ownership explicit. Tool documentation links are references, not copied rules. |

## Source comments and build verification

| Source and relevant sections | Adoption and local adaptation | Attribution and reuse |
| --- | --- | --- |
| Liviu Ionescu, [micro-os-plus Doxygen style guide](https://micro-os-plus.github.io/develop/doxygen-style-guide/), comment blocks, command conventions, groups, and samples | Adopt the source-comment style with explicit language scope and rule-by-rule enforcement coverage. Record exceptions and adaptations beside the coverage record. | The page credits Liviu Ionescu. Link diagnostics to upstream sections. Verify applicable repository licensing before copying guide text or samples; custom fixtures should be original. |
| Doxygen, [documentation blocks](https://www.doxygen.nl/manual/docblocks.html) and [configuration](https://www.doxygen.nl/manual/config.html) | Consult command semantics and the project's effective configuration when checking generated reference and diagnostics. | Official manual links; consult upstream licensing for redistribution. Recheck applicable settings for the installed version. |
| MkDocs, [validation configuration](https://www.mkdocs.org/user-guide/configuration/#validation) | Inspect configured warning levels and covered links, then run the existing build with strict checking where applicable. | Link to official documentation; check the repository license for copied material. |
| lychee, [command-line flags](https://lychee.cli.rs/guides/cli/) | Record input scope, exclusions, authentication requirements, and fragment-checking behavior. Inspect rendered anchors when source checks cannot establish them. | Link to official documentation; preserve upstream license if distributing the tool. |

## Decision records and API semantics

| Source and relevant sections | Adoption and local adaptation | Attribution and reuse |
| --- | --- | --- |
| Michael Nygard, [Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions), Decision: title, context, decision, status, consequences | Preserve rationale and accepted decisions; mark supersession with a replacement link. Use the project's status vocabulary. Document real adverse consequences; choose prose or lists that communicate them clearly. | Attribute the ADR pattern to Nygard. Local templates express the pattern in original wording. Consult the publisher before reproducing substantial prose. |
| IETF, [RFC 9110, status codes](https://www.rfc-editor.org/rfc/rfc9110.html#name-status-codes) | Verify HTTP semantics against the standard and endpoint behavior against product evidence. Redirects alone do not establish deprecation. | Cite RFC number and section. Consult the RFC copyright and IETF Trust notices before copying normative text or code. |
| GraphQL working group, [GraphQL over HTTP draft, status codes](https://graphql.github.io/graphql-over-http/draft/#sec-Status-Codes) | Check response media type and implementation behavior. Distinguish transport failures, request errors, and partial execution results. | Cite this as a draft with access date, and check the repository license for copied material. |

## Empirical evidence and its limits

| Study and relevant sections | Supported use and limitation | Attribution and reuse |
| --- | --- | --- |
| Gorski, Moller, Wiefling, and Lo Iacono, [I just looked for the solution!](https://www.stephanwiefling.de/papers/csp-eyetracking-tse2021.pdf), abstract, sections 4-7; DOI 10.1109/TSE.2021.3094171 | A study of 49 junior developers supports placing security information near functional examples in its CSP task. Broader editorial application is an inference; it establishes no universal scanning pattern or fixed paragraph layout. | Author-hosted IEEE postprint. Its notice permits personal use and requires permission for specified republication and reuse. Cite findings; use original local examples. |
| Uddin and Robillard, [How API Documentation Fails](https://www.cs.mcgill.ca/~martin/papers/ieeesw2015.pdf), survey results and limitations | Supports checking incompleteness, ambiguity, and incorrectness. The author-hosted manuscript contains editorial marks; use it for the qualitative result and consult the published article for exact publication quotations. Survey responses establish reported problems in that sample. | Cite the authors and article; check publisher permissions before reproducing tables or figures. |
| Liu and colleagues, [Improving API Caveats Accessibility by Mining API Caveats Knowledge Graph](https://mingwei-liu.github.io/assets/pdf/icsme2018_apicaveatskg.pdf), abstract and evaluation | Supports investigating discoverability of API caveats. A documentation author's choice of warning placement is a local adaptation. | Author-hosted research paper; cite findings and check the publication notice before reproducing components. |

## Local editorial decisions

The workflow requires a reader contract, claim evidence, example verification,
context review, and recorded validation results. Human review covers factual
claims, security guidance, migrations, destructive operations, compatibility,
and release-sensitive information. These are house requirements adopted for
this workflow; empirical studies establish neither their exact sequence nor
their sufficiency.

Write concise prose that preserves needed detail. Use exact commands, values,
versions, expected outputs, and error conditions where the reader needs them to
perform or verify a task. Associate those details with a maintained source and
verification record. Explain mechanisms and rationale at a stable level in
conceptual material. This is the local reconciliation of maintainability with
executable documentation.

When a source is unavailable, record its URL, attempted access, and the unresolved
claim. Continue with verified material and mark remaining uncertainty for review.
Recheck upstream sources when a rule package, renderer, or project convention
changes. Confirm applicable licensing when copying upstream material and retain
the required attribution and notices.

## Reproducible tooling evidence

On 2026-09-06, the implementation retrieved the official
[Vale 3.20.0 release](https://github.com/vale-cli/vale/releases/tag/v3.20.0) and
[checksum manifest](https://github.com/vale-cli/vale/releases/download/v3.20.0/vale_3.20.0_checksums.txt),
then verified the Linux x86_64 archive before installation. The Google
[v0.7.1 archive](https://github.com/errata-ai/Google/releases/download/v0.7.1/Google.zip)
is pinned by its observed SHA-256 digest in the setup script. Its
[repository](https://github.com/vale-cli/Google) identifies the package as an
MIT-licensed implementation of Google's CC BY 4.0 guidance. These pins own rule
behavior; test results own the demonstrated coverage of comments and markup.

The [Vale code-aware guide](https://vale.sh/features/code) describes original
position mapping and Markdown associations. Local fixtures verify those features
for the extensions listed in [the invocation guide](vale.md). The configured
exclusions use official [TokenIgnores](https://docs.vale.sh/keys/tokenignores)
and [BlockIgnores](https://docs.vale.sh/keys/blockignores) settings. Re-run fixtures
when extending their regular expressions or updating the upstream packages.

Link fixtures use `lychee-bin==0.24.2` through uv and verify the resulting
`lychee 0.24.2` version. The upstream [CLI guide](https://lychee.cli.rs/guides/cli/)
owns option semantics. Local adaptations enable full fragment checks and retain
access failures, temporary network errors, and exclusions as distinct reported
limits. The [link-validation guide](link-validation.md) records the operating
defaults and coverage; controlled HTTP and HTML fixtures provide execution
evidence independently of external-site availability.
