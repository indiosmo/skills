# Applying the Google-based house style

Authors use the [Google developer documentation style guide](https://developers.google.com/style)
for editorial guidance and its [Vale package](https://vale.sh/explorer/google)
for automated checks. Start with Google's [highlights](https://developers.google.com/style/highlights),
then consult the relevant topic while writing. Installation, pinned versions and
invocation belong in the validation resources.

## Necessary local adaptations

Use the consuming project's established terminology and explicit user
instructions. Establish unfamiliar domain terms from the project's glossary,
public domain references and subject-matter experts; record unresolved conflicts.
Add accepted terms and prohibited alternatives to Vale vocabulary only after
confirming their intended meaning. A local abbreviation is appropriate when
practitioners use it and the audience understands it.

Write positive descriptions of current behavior. Explain non-obvious reasons
where the relevant code or decision lives. Link shared rationale and definitions
instead of duplicating them across neighboring pages. Use plain text in code,
comments and command output. Keep exact commands, values and required inputs in
procedures and versioned reference when readers need them; verify them against
their source. Narrative summaries should describe stable patterns when an
inventory adds no reader value.

These are house adaptations for consistency and maintenance. Sentence length,
paragraph length and number of callouts are editorial signals, with no fixed
local numerical limit. Google describes
[active voice](https://developers.google.com/style/voice) as a preference with
valid exceptions. Explain an exception by reader need rather than weakening
all diagnostics for a document.

## Editorial judgment

Vale identifies patterns in wording. Authors and reviewers still assess whether
a reader has enough prior knowledge, whether steps have useful expected results,
and whether examples retain their meaning. Check heading hierarchy, scanability,
link purpose, image descriptions and warning placement in the rendered document.
Use Google's [procedures](https://developers.google.com/style/procedures),
[headings](https://developers.google.com/style/headings),
[code samples](https://developers.google.com/style/code-samples) and
[notices](https://developers.google.com/style/notices) for their specific topics.

Write the Docs' [beginner's guide](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/)
and [documentation principles](https://www.writethedocs.org/guide/writing/docs-principles/)
help reviewers assess audience fit, usefulness and maintenance. Apply those
questions to the contract and outline rather than expanding this page into a
second style manual. Custom lint rules require an observed gap, rationale,
positive and negative fixtures, and an owner; the upstream Google package owns
its existing rules.
