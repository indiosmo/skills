# Documentation skill tasks

Build a skill that produces one document, or a related group of documents, from
verified evidence through document verification and maintenance. The finished skill replaces
`skills/documentation/` and covers the workflow in [GOAL.md](GOAL.md).

This is an implementation backlog. All tasks start unchecked. Each task has a
stable identifier, proposed deliverables, dependencies, and a completion condition
so it can be picked up separately. Paths below are relative to
`skills/documentation/` unless stated otherwise. Proposed filenames can change
during implementation; preserve task identifiers for tracking.

## Scope and working assumptions

- Keep `SKILL.md` focused on routing and workflow. Delegate established guidance
  to public references and mechanical checks to existing tools and rule packages.
  Local notes cover specific adaptations, workflow decisions, and editorial
  judgment that automation cannot supply.
- Treat the reference paths below as proposed homes for necessary local content,
  not a requirement to create a guide for every task. Consolidate short notes and
  link directly to upstream sections wherever those already meet the need.
- Keep templates and checklists concise. Add local prose or custom rules only when
  they address a demonstrated gap; assess that gap before creating each resource.
- Support creating, updating, reviewing, and checking drift in a selected document.
  Context review can identify related edits and navigation changes.
- Use Diataxis for tutorials, how-to guides, reference, and explanation. Give
  READMEs, ADRs, release notes, changelogs, and articles explicit treatment.
- Treat the consuming project's MkDocs site, Doxygen reference generation, and CI
  jobs as the existing documentation environment. Scope the skill to authoring,
  maintenance, and verification; generation pipeline design, hosting, deployment,
  and publication-job implementation are outside this backlog.
- Provide Vale with a Google-based house style, a Doxygen comment linter, and
  lychee checks. Invoke existing generation and build commands when needed for
  validation, using temporary output where appropriate. Make checks usable by CI.
- Start the Doxygen tooling investigation with C and C++. Confirm supported
  languages and dialects before implementing the parser.
- Manage custom Python tooling with uv. Prefer existing tools where they satisfy
  the requirement; build custom checks for the remaining gaps.
- Treat technical choices below as investigation tasks. Record a scored decision
  matrix when several viable approaches remain, using complexity, performance,
  reversibility, blast radius, maintenance, ergonomics, testability, and coupling
  where relevant.

## 1. Foundations and skill architecture

### DOC-01: Audit requirements, research, and existing guidance

- [ ] Map every requirement in the goal to a task and an acceptance scenario.
- [ ] Audit the research document's claims against its cited sources. Separate
  supported guidance, house preferences, disputed claims, and unsupported claims.
- [ ] Check especially its absolute rules and numerical prescriptions, such as
  sentence lengths, callout limits, quadrant boundaries, and ADR immutability.
- [ ] Inventory the current skill and its README, runbook, and ADR references.
  Record which rules to preserve, revise, consolidate, or retire.
- [ ] Reconcile drift-resistant prose with the exact commands and values needed
  in executable procedures and generated reference.

**Deliverables:** `references/sources.md`; requirement coverage and migration
notes alongside this backlog. The source register records links, relevant
sections, access dates, attribution or reuse requirements, and local adaptations.

**Depends on:** Nothing.

**Done when:** Every goal requirement has an owner task, and the research document
is usable as an input with its evidence limitations made explicit.

### DOC-02: Define the workflow and resource layout

- [ ] Define entry routes for create, update, review, drift analysis, source-comment
  documentation, and changelog work.
- [ ] Define stage inputs and outputs: contract, evidence, outline, draft,
  editorial review, context review, validation, and human review.
- [ ] Distinguish information required before drafting from uncertainties that can
  remain explicitly marked in a draft.
- [ ] Define how existing project conventions and explicit user instructions apply.
- [ ] Define where working records live, how a task resumes, and what belongs in
  the final delivery. Keep durable skill resources independent of temporary plans.
- [ ] Assign each concern to an upstream source, existing tool, or necessary local
  instruction. Define which source sections each route consults and how to report
  unavailable sources. Check interactions with writing, glossary, diagram, and
  language skills.

**Deliverables:** Skeleton `SKILL.md`; resource map and stage contracts.

**Depends on:** DOC-01.

**Done when:** Each supported entry route leads to a concrete output and its
required checks without loading every reference.

## 2. Document contract, evidence, and structure

### DOC-03: Define the document contract and elicitation procedure

- [ ] Capture audience, prior knowledge, reader task, intent, Diataxis category
  where applicable, success condition, scope, product version, source material,
  destination within the existing documentation, and output structure.
- [ ] Capture relevant constraints: prerequisites, access, environment, publication
  conventions, domain terminology, and review ownership.
- [ ] Define how to infer answers from existing material and ask only for gaps.
- [ ] Include a worked contract for a single page and one for a multipart tutorial.

**Deliverables:** `references/document-contract.md`;
`templates/document-contract.md`.

**Depends on:** DOC-02.

**Done when:** Another author can use a completed contract to determine what to
write, who it serves, and how success will be assessed.

### DOC-04: Define evidence collection and claim traceability

- [ ] Define how to verify claims against code, specifications, issues, API
  schemas, UI text, tests, subject-matter expert notes, and existing documents.
- [ ] Define how to resolve conflicting sources for the target version and how to
  record inaccessible sources, uncertainty, and assumptions.
- [ ] Distinguish observed behavior, intended behavior, historical rationale, and
  inference. Specify evidence needed for each.
- [ ] Define useful citations and links: source location, revision or version,
  retrieval date where relevant, and reader-facing versus review-only evidence.
- [ ] Define how to preserve provenance when an editorial change alters a claim.

**Deliverables:** `references/evidence.md`; `templates/evidence-register.md`.

**Depends on:** DOC-03.

**Done when:** A reviewer can locate support for a claim and identify unresolved
claims without reconstructing the author's investigation.

### DOC-05: Define document selection and outlining

- [ ] Build a routing guide using the [Diataxis compass](https://diataxis.fr/compass/).
- [ ] Explain how to split mixed-purpose material and connect related pages.
- [ ] Define when a README provides orientation and routes readers onward, and how
  ADRs, release notes, changelogs, and articles express their own intent.
- [ ] Define single-page versus multipart criteria, page ordering, navigation,
  prerequisites, outcomes, limitations, errors, examples, and related links.
- [ ] Include contrasting outlines that expose common classification mistakes.

**Deliverables:** `references/document-types.md`; `references/structure.md`;
`templates/outline.md`.

**Depends on:** DOC-03, DOC-04.

**Done when:** Each supported document intent has a structure appropriate to its
reader task, with conditional sections clearly marked.

## 3. Writing references and templates

### DOC-06: Adopt Google style and identify editorial guidance gaps

- [ ] Adopt the [Google Vale package](https://vale.sh/explorer/google) as the
  baseline for automated style checks; DOC-12 owns installation and configuration.
- [ ] Link authors to relevant sections of the
  [Google style guide](https://developers.google.com/style), with the upstream
  package owning its lint rules and the upstream guide owning its full guidance.
- [ ] Identify guidance requiring editorial judgment, such as audience-appropriate
  terminology, adequate prerequisites, useful expected outcomes, scanability,
  accessible descriptions, and placement of warnings. Place each item in its
  owning structure, example, or review reference.
- [ ] Use Write the Docs' [writing guide](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/)
  and [principles](https://www.writethedocs.org/guide/writing/docs-principles/)
  to inform those editorial checks.
- [ ] Preserve useful existing guidance on information ownership, duplication,
  rationale, and positive descriptions of current behavior.
- [ ] Define how to establish idiomatic domain vocabulary and manage project terms.
- [ ] Record only necessary project or house adaptations, with rationale. Propose
  custom Vale rules only for demonstrated gaps in the adopted package.

**Deliverables:** A short `references/house-style.md` describing adoption, source
links, and necessary adaptations; editorial checks in their owning references.

**Depends on:** DOC-01, DOC-05.

**Done when:** The skill uses the upstream Google baseline, editorial checks cover
the relevant gaps, and any custom rules or overrides have an explicit justification.

### DOC-07: Connect Diataxis guidance to concise document templates

- [ ] Route to the upstream Diataxis guidance for each type. Keep local notes
  focused on applying it within the contract, evidence, and verification workflow.

- [ ] Tutorial: learning outcome, prepared environment, tested path, observable
  progress, cleanup where needed, and next learning step.
- [ ] How-to: operational goal, prerequisites, ordered actions, applicable branches,
  verification, and failure recovery.
- [ ] Reference: consistent structure, source ownership, constraints and errors,
  generated content boundaries, and links to relevant tasks and explanations.
- [ ] Explanation: concepts, relationships, rationale, tradeoffs, and useful diagrams.
- [ ] Provide a completed example for each type and a short review checklist.
- [ ] Make template instructions removable and sections conditional on reader need.

**Deliverables:** Upstream links in the document-type router; concise templates
named `tutorial.md`, `how-to.md`, `reference.md`, and `explanation.md`; completed
examples under `examples/`. Add local reference notes only for specific gaps.

**Depends on:** DOC-05, DOC-06.

**Done when:** Each template produces a coherent page and its example demonstrates
the distinction from adjacent document types.

### DOC-08: Preserve and extend the other document types

- [ ] Retain concise, specific README guidance for root, module, and component orientation.
- [ ] Adapt runbook guidance for operational preconditions, risk, verification,
  recovery, and escalation paths grounded in project evidence.
- [ ] Adapt ADR guidance for context, alternatives, decision, consequences, status,
  supersession, and project-specific numbering conventions.
- [ ] Add release-note, code-changelog, and documentation-changelog structures.
- [ ] Define article intent, attribution, argument structure, and fact checking.
- [ ] Add a worked example for each type; reuse the common style and evidence rules.

**Deliverables:** Concise routing and specific adaptations for these document
types, linked to suitable public guidance; corresponding templates and examples.
Consolidate or shorten the existing references as appropriate.

**Depends on:** DOC-01, DOC-05, DOC-06.

**Done when:** Every additional intent named in the goal has a usable route,
template, and review criteria, and the existing skill's useful guidance is covered.

## 4. Doxygen documentation and custom linter

### DOC-09: Adopt the upstream Doxygen style and map enforcement gaps

- [ ] Inventory every rule in the
  [micro-os-plus Doxygen style guide](https://micro-os-plus.github.io/develop/doxygen-style-guide/).
- [ ] Keep the upstream guide as the human and agent reference. Record a compact
  enforcement map using source-section links and classifications: Vale, Doxygen,
  custom linter, or human review.
- [ ] Give implemented checks stable identifiers and test cases. Keep detailed
  mechanical rule definitions with their implementation and tests.
- [ ] Record house adaptations and decide the supported languages, declarations,
  comment forms, tags, and file types.
- [ ] Add short review prompts for meaningful API contracts where needed, including
  preconditions, lifetime, ownership, errors, and concurrency guarantees.

**Deliverables:** Short Doxygen adoption notes with upstream links, adaptations,
and enforcement coverage; a machine-readable check catalog if needed by DOC-11.

**Depends on:** DOC-01, DOC-06.

**Done when:** Upstream guidance is directly accessible from the workflow, coverage
gaps are explicit, and custom checks have a justified scope.

### DOC-10: Design the Doxygen linter

- [ ] Compare available Doxygen diagnostics, parser-backed checks, and existing
  linters against the rule inventory. Evaluate tree-sitter and compiler-backed
  parsing where declaration semantics matter.
- [ ] Use representative source fixtures to choose the minimum sufficient approach.
- [ ] Define the CLI: input directory or files, recursive discovery, language and
  extension selection, exclusions, configuration, severities, and exit statuses.
- [ ] Define diagnostics with rule identifier, path, line, column, explanation,
  and suggested correction; provide plain text and structured output.
- [ ] Define behavior for generated and vendored files, symlinks, encodings,
  malformed source, unsupported syntax, and suppressions with reasons.
- [ ] Define which rules can be checked mechanically and how skipped or unsupported
  checks appear in results. Scope any automatic fixes separately.

**Deliverables:** `references/doxygen-linter.md`; CLI contract; parser decision
matrix; fixture inventory.

**Depends on:** DOC-09.

**Done when:** The design has demonstrated source-location accuracy and adequate
syntax coverage, and every rule has a planned implementation or review path.

### DOC-11: Implement and package the Doxygen linter

- [ ] Create a uv-managed Python tool with dependency metadata, a lockfile, CLI
  entry point, and documented invocation from a consuming project.
- [ ] Implement discovery, parsing, comment association, rule checks, diagnostic
  formatting, configuration, and exit behavior from DOC-10.
- [ ] Test valid and invalid examples for each implemented rule, including comment
  delimiters inside strings, multiline comments, templates, overloads, macros,
  and declaration/comment association where supported.
- [ ] Test exclusions, suppressions, malformed inputs, and diagnostic locations.
- [ ] Check runtime on a representative directory and document measured limits.

**Deliverables:** `tools/doxygen_linter/` with `pyproject.toml`, `uv.lock`, source,
tests, and fixtures; usage in `references/doxygen-linter.md`.

**Depends on:** DOC-10.

**Done when:** A directory-level invocation reports the expected findings and exit
status, valid fixtures pass, and coverage matches the published rule catalog.

## 5. Verification tools and documentation environment

### DOC-12: Configure Vale for documents and source comments

- [ ] Use the [Google Vale package](https://vale.sh/explorer/google) directly and
  configure only necessary overrides, project vocabulary, and justified gap checks.
- [ ] Verify [code-aware linting](https://vale.sh/features/code) for the selected
  languages and Doxygen comment forms using the chosen Vale version.
- [ ] Configure markup handling so identifiers, commands, tags, URLs, and executable
  examples receive the intended treatment.
- [ ] Add accepted and rejected terminology, severity policy, and scoped exceptions.
- [ ] Pin or otherwise make reproducible the Vale binary and style-package setup.
- [ ] Test prose and source-comment fixtures, including original source positions
  and false-positive cases. Record which house rules remain manual checks.

**Deliverables:** `assets/vale/` containing `.vale.ini`, necessary vocabulary,
fixtures, and any justified custom rules; concise invocation notes with upstream
configuration links.

**Depends on:** DOC-06, DOC-09.

**Done when:** The same house style runs on Markdown and supported source comments
with useful diagnostics and without treating code tokens as ordinary prose.

### DOC-13: Validate source comments in generated reference

- [ ] Discover the project's Doxygen configuration, source scope, generation
  command, warning policy, and existing reference integration.
- [ ] Define when comment linting is sufficient and when a generation run is
  needed to inspect rendering, symbol resolution, or Doxygen diagnostics.
- [ ] Run generation with temporary output where appropriate, preserving the
  project's relevant settings and resolving relative input paths correctly.
- [ ] Inspect signatures, overloads, parameter documentation, examples, and
  cross-references produced from changed source comments.
- [ ] Map generation findings back to editable source comments. Report missing
  configuration or dependencies and the resulting verification limits.

**Deliverables:** `references/generated-reference-validation.md`; a small test
fixture with Doxygen configuration and expected rendering or diagnostic results.

**Depends on:** DOC-09.

**Done when:** The workflow catches planted comment and cross-reference defects
using the existing generation setup and produces source-level corrections.

### DOC-14: Write and verify documents in an existing MkDocs site

- [ ] Inspect the site's existing navigation, Markdown extensions, theme features,
  version conventions, and build command before choosing document syntax.
- [ ] Cover page placement, relative links, anchors, images, diagrams, code fences,
  admonitions, and multipart navigation using the project's conventions.
- [ ] Define document-related navigation edits and links needed to make a new or
  moved page discoverable in the existing site.
- [ ] Run the existing strict build, optionally into a temporary directory, and
  inspect rendered documents. Test the diagnostics available in that configuration
  and identify the additional checks needed.
- [ ] Report unavailable configuration, tools, or build prerequisites as validation
  limits with enough detail for the project maintainer to act.

**Deliverables:** `references/mkdocs-authoring.md`; a minimal site under test
fixtures for authoring and validation scenarios.

**Depends on:** DOC-05. Combined reference-link checks also depend on DOC-13.

**Done when:** A document change fits the existing site and its rendering,
navigation, and build diagnostics have been checked without redesigning the site.

### DOC-15: Configure link validation

- [ ] Configure [lychee](https://github.com/lycheeverse/lychee) for external links.
- [ ] Define which checks own local files, anchors, generated symbol links, and
  links in the built site. Prove coverage with deliberately broken examples.
- [ ] Define handling of redirects, fragments, authenticated sites, network
  failures, rate limits, retries, caching, and justified exclusions.
- [ ] Distinguish broken, unchecked, and temporarily unreachable links in reports.

**Deliverables:** `assets/lychee/lychee.toml`; `references/link-validation.md`;
link-validation fixtures.

**Depends on:** DOC-13, DOC-14.

**Done when:** Broken-link fixtures fail predictably, valid fixtures pass, and
network limitations remain visible in the reported result.

### DOC-16: Make examples verifiable artifacts

- [ ] Define how to keep runnable examples in source files and include them in pages,
  or extract explicitly marked examples when that fits the project.
- [ ] Define language, setup, dependencies, placeholders, expected results, timeout,
  cleanup, and target-version metadata needed to reproduce an example.
- [ ] Prefer project build and test commands. Decide whether extraction or an
  execution adapter needs a small custom tool after testing existing mechanisms.
- [ ] Define explicit treatment of pseudocode, partial fragments, interactive steps,
  and examples needing external services or human execution.
- [ ] Verify example meaning after editorial changes, including quoting, indentation,
  flags, identifiers, and output assertions.

**Deliverables:** `references/examples.md`; example manifest template; runnable
fixtures; an example-checking tool only if the investigation establishes a gap.

**Depends on:** DOC-04, DOC-06, DOC-14.

**Done when:** Each example has an execution result or an explicit validation limit,
and a deliberately broken runnable example is caught.

### DOC-17: Assemble the validation workflow

- [ ] Provide repeatable commands for Vale, Doxygen style checks, Doxygen generation,
  MkDocs strict build, links, and example verification in dependency order.
- [ ] Define checks for changed documents and when generated dependencies require
  broader validation.
- [ ] Report pass, fail, skipped, and blocked outcomes with commands, versions,
  scope, and diagnostic locations.
- [ ] Document check invocation, dependencies, exit statuses, and diagnostics for
  local use and integration into the project's existing CI verification jobs.
  Explain failure troubleshooting and preserve project settings when using assets.
- [ ] Use a thin runner only where it improves invocation or reporting. Keep native
  tool diagnostics available.

**Deliverables:** `references/validation.md`; validation command entry point;
`templates/validation-report.md`; CI invocation examples and integration fixtures.

**Depends on:** DOC-11 through DOC-16.

**Done when:** One documented workflow passes on the valid fixture and fails for
each planted validation defect, with skipped checks visible.

## 6. Editorial review, context, and maintenance

### DOC-18: Define editorial and contextual review

- [ ] Review factual support, domain terminology, clarity, scanability, style,
  prerequisites, expected outcomes, and semantic preservation in examples.
- [ ] Inspect parent, sibling, child, and relevant reference documents for
  contradictions, duplication, naming, organization, and missing connections.
- [ ] Define useful links, backlinks, related explanations, analogies, and
  "see also" material according to reader need.
- [ ] Record related edits and their evidence; keep the selected document's scope
  explicit when broader changes emerge.
- [ ] Define how feedback, support issues, and friction logs supply evidence of
  missing steps or explanations when available.

**Deliverables:** `references/editorial-review.md`;
`references/contextual-review.md`; `templates/review-findings.md`.

**Depends on:** DOC-04, DOC-06, DOC-07, DOC-08.

**Done when:** Review fixtures expose an unsupported claim, ambiguous instruction,
terminology mismatch, duplicated explanation, and contradictory neighboring page.

### DOC-19: Define code and documentation changelog workflows

- [ ] Define the revision or release range and inspect relevant diffs alongside
  commit messages, issues, release metadata, and existing changelog conventions.
- [ ] Classify user-visible code changes separately from documentation changes.
- [ ] Group and deduplicate entries, check reverted changes, and link supporting
  history. Verify compatibility and migration statements against evidence.
- [ ] Define release notes as a reader-focused account derived from verified changes.
- [ ] Evaluate whether a read-only history collector materially helps; specify one
  only if native git commands leave a demonstrated gap.

**Deliverables:** `references/changelog-workflow.md`; worked history fixture and
expected code changelog, documentation changelog, and release notes.

**Depends on:** DOC-04, DOC-08.

**Done when:** The same history produces distinct, supported outputs for code and
documentation, with unresolved release claims flagged for review.

### DOC-20: Define document drift analysis

- [ ] Start from a selected document and identify relevant source files, symbols,
  schemas, tests, linked pages, examples, and versions.
- [ ] Compare current claims against current evidence and available history.
- [ ] Classify factual mismatch, broken link, stale example, terminology change,
  contradiction, and unverifiable claim.
- [ ] Record exact affected text, evidence, impact, and proposed correction.
- [ ] Reuse link and example checks. Investigate dependency tracking or a small
  collector only if manual source mapping proves insufficient.

**Deliverables:** `references/drift-analysis.md`; `templates/drift-report.md`;
before-and-after drift fixtures.

**Depends on:** DOC-04, DOC-15, DOC-16, DOC-18.

**Done when:** Planted source changes produce specific findings, while unchanged
claims and unavailable evidence receive accurate classifications.

### DOC-21: Define final verification and human review

- [ ] Implement the skeptical developer and technical editor pass with exactly the
  eight finding categories requested in the goal:
  1. Unsupported claims, with the exact sentence and missing evidence.
  2. Missing prerequisites.
  3. Ambiguous actions.
  4. Steps unverifiable from the supplied source material.
  5. Inconsistent product terminology.
  6. Content belonging in another Diataxis quadrant.
  7. Google-style issues in titles, headings, voice, and word choice.
  8. Risks of changing meaning in code samples.
- [ ] Define an unambiguous empty result when the pass finds no issues. Keep tool
  execution reports and delivery summaries separate from this findings-only output.
- [ ] Define the human review record for factual claims, security guidance,
  migrations, destructive operations, compatibility, and release-sensitive content.
- [ ] Identify the relevant reviewer, evidence, unresolved findings, review status,
  and changes that require renewed review.

**Deliverables:** `references/final-verification.md`;
`templates/final-findings.md`; `templates/human-review.md`.

**Depends on:** DOC-17, DOC-18, DOC-19, DOC-20.

**Done when:** The final pass produces only the specified findings, and the delivery
record distinguishes validation results from completed or pending human review.

## 7. Integration and completion

### DOC-22: Build acceptance scenarios for the whole skill

- [ ] Create scenarios for a tutorial, multipart tutorial, how-to or runbook,
  explanation, generated reference, README update, ADR, article, release notes,
  both changelogs, and drift review.
- [ ] Include incomplete evidence, conflicting versions, missing tools, unavailable
  links, an existing site, and source comments with style violations.
- [ ] Define expected routing, artifacts, findings, and validation outcomes. Add
  expert review criteria where quality requires judgment.
- [ ] Run representative end-to-end scenarios and record defects for the owning
  tasks. Verify that the workflow stays focused on the selected document or group.

**Deliverables:** `tests/` and `examples/` fixtures; acceptance rubric and results.

**Depends on:** Draft the rubric after DOC-02; run full acceptance after DOC-21.

**Done when:** Each goal requirement is exercised, automated checks catch their
target defects, and reviewed examples demonstrate usable documentation.

### DOC-23: Finish the skill and replace the existing version

- [ ] Complete `SKILL.md` routing, progressive loading, stage transitions, tool
  invocation, failure handling, and final output instructions.
- [ ] Finish the migration checklist from DOC-01 and reconcile duplicated rules.
- [ ] Verify reference and template links, tool paths, dependency setup, and example
  commands from a consuming project.
- [ ] Check that durable resources use durable references, that upstream links
  resolve to the relevant guidance, and that local instructions cover specific
  needs. Remove duplicated upstream explanations and rules already owned by tools.
- [ ] Document maintenance of source references, rule catalogs, tool versions,
  style packages, integrations, and regression fixtures.
- [ ] Run the applicable skill-format checks and DOC-22 acceptance scenarios on
  the assembled package.

**Deliverables:** Completed replacement `skills/documentation/`;
`references/maintenance.md`; final acceptance record.

**Depends on:** DOC-01 through DOC-22.

**Done when:** The replacement supports every promised route, all required assets
are present, applicable checks pass, and unresolved review items are explicitly
accounted for before declaring the skill complete.

## Suggested execution order

1. Complete DOC-01 and DOC-02 to establish scope and ownership.
2. Complete DOC-03 through DOC-06 to stabilize the document contract and rules.
3. Work separately on the document types (DOC-07 and DOC-08), Doxygen reference
   and linter (DOC-09 through DOC-11), and environment-aware verification (DOC-12 through
   DOC-16), respecting their listed dependencies.
4. Develop editorial, changelog, and drift workflows as their references and
   fixtures become available. Draft acceptance scenarios early.
5. Integrate validation and final review, exercise the assembled skill, and finish
   replacement through DOC-17, DOC-21, DOC-22, and DOC-23.

The custom Doxygen linter is an explicit deliverable. Example extraction,
validation orchestration, history collection, and drift collection are candidate
automation work: each owning task first establishes whether a custom tool is
needed. This keeps those decisions independently reviewable.
