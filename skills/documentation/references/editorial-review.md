# Reviewing a draft for its reader

An editorial review asks whether a reader can use the document accurately and
confidently. Read the contract, draft and evidence register together. Record
findings with [the review template](../templates/review-findings.md), then apply
corrections and recheck the affected claims and examples.

## Check claims and actions

For each material claim, locate its source at the target version. Check that
wording preserves conditions, scope and certainty. Quote unsupported sentences
exactly and identify missing evidence. Confirm that prerequisites give the reader
a usable starting state: tools, permissions, environment, inputs and necessary
prior knowledge. Walk each procedure from that state. Replace ambiguous actions
such as "configure it appropriately" with evidenced settings or a specific
decision rule and observable result.

For example, if a draft says "Count any file with this command" but the source
opens UTF-8 text, narrow the claim to supported text input and document relevant
errors. If a command contains a placeholder, explain how the reader obtains its
value. An unavailable environment leaves execution unverified; record that limit
instead of inventing expected output.

## Review language and presentation

Apply [house style](house-style.md) and relevant upstream guidance. Match domain
terms to their definitions and actual interface labels. Check titles, headings,
voice, word choice and scanability. Assess whether paragraphs and lists group
related ideas in the order the reader needs them. Place warning conditions before
the consequential action and verify that the response is actionable.

Inspect rendered tables, diagrams, images, labels and link text. A text alternative
should communicate the information needed for the task. Syntax validity alone
cannot establish that a diagram explains its relationships or an image has a
useful description. Preserve meaningful technical constraints while removing
empty qualifications and slogans.

## Preserve examples and use reader feedback

Compare edited code samples with their runnable source. Recheck quoting,
indentation, flags, identifiers, output assertions and side effects using
[example verification](examples.md). A grammatical edit that changes a parameter
name is a code change and needs behavior verification.

When available, inspect support issues, reader feedback and friction logs. Trace
a report such as "I could not find the sample file" to its version and starting
state before adding a prerequisite. Treat repeated confusion as evidence to
investigate, with links and dates in the findings record. Complete the
[contextual review](contextual-review.md) after the local pass.
