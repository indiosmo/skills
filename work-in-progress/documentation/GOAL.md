# Goal

Create a documentation skill for producing documentation following the diataxis framework, publishing with mkdocs, using doxygen to generate documentation from code (to serve as the reference part of diataxis).

https://vale.sh/ for linting both docs and comments in code (https://vale.sh/features/code), starting from google's style guide (https://vale.sh/explorer/google).

The skill focuses on writing a single document (or related group of documents if multi-part for organization reasons, like a multi step tutorial).

The skill should follow best practices and standards of technical writing ( see work-in-progress/documentation/Tech Writing AI Skill Research.md )

Before writing a document we should establish the audience, the task, the source of truth, output structure.

Draft from verified sources. State uncertainty instead of guessing. Keep each page faithful to its Diátaxis purpose (although we have other categories like ADRs and Release Notes that don't necessarily fit diataxis, so take those into consideration as well). Follow the Google-based house style. Treat examples as executable artifacts. Require human review for factual claims, security guidance, migrations, destructive operations, compatibility claims, and release-sensitive information.

--

The skill should cover different aspects of the process of producing documentation (not in order, not exhaustive)

Define the document contract
    Reader: developer, administrator, end user, support engineer, or maintainer.
    Diataxis category: (https://diataxis.fr/compass/)
    Intent: related to diataxis category but covers other things that don't fit like: changelog, release notes, articles, ADR, ...
    Success condition: what the reader can accomplish after following it.
    Evidence: spec, issue, API schema, code, UI copy, test results, SME notes, and existing style guide. This one is very important, the documentation should be grounded in facts, have proper links/citations, etc.

Define the structure
  Produce an outline with prerequisites, task steps, expected outcomes, limitations, errors, links, examples.
  Decide on single or multi file.

Production
  Writing the actual document given the elicited contract and the defined structure.
  Following proper practices/style (see https://developers.google.com/style and the writethedocs references).

Editorial pass
  Validate/check claims, check for idiomatic terminology in context of the domain, improve clarity, scanability/skimmability (see the writethedocs references).


Contextual pass
  Review the document in context of the rest of the documentation;
  Contradictions, unecessary duplication, organizational issues.
  Potential links, explanations in terms of or in connection with something else, analogies, "see also" sections, etc. Potential updates to other existing docs in light of the one being worked on (e.g. a backlink, etc.)

Validation
  Validate like code, lint with vale, build with mkdocs --strict (validating links, etc), use lychee (https://github.com/lycheeverse/lychee) for external link validation.
  Validate doxygen comments according to the style guide (both vale and the doxygen style guide below.)

Changelogs
  Reviewing git history for changes to keep changelogs, for the code, and another for docs themselves (e.g. added a page, changed something on a page, ...)

Drift analysis
  Given the current state of a given document, check the links and code relevant to it to detect mismatches/drift.

Final verification checklist
  Review the draft as a skeptical developer and technical editor.

  Return only:
  1. Unsupported claims, with the exact sentence and missing evidence
  2. Missing prerequisites
  3. Ambiguous actions
  4. Steps that cannot be verified from the provided source material
  5. Inconsistent product terminology
  6. Content that belongs in another Diátaxis quadrant
  7. Google-style issues in titles, headings, voice, and word choice
  8. Risks of accidentally changing meaning in code samples


# References

Our own existing `skills/documentation/` which is more specific, its about inlined READMEs, and ADRs and guides.
This new skill is intended to subsume and replace that one.

work-in-progress/documentation/Tech Writing AI Skill Research.md

https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/
https://www.writethedocs.org/guide/writing/docs-principles/

https://micro-os-plus.github.io/develop/doxygen-style-guide/ (this specifically should become one of the skill documents, with all the rules, so that both agents and humans can refer to, and ideally a linter script that we can point to a directory and lints docstrings in every file there. can be a python tool (use uv for dependency mangement), can use tree-siter if it helps, etc.).

https://developers.google.com/style
