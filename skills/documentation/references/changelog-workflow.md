# Deriving changelogs and release notes

A changelog records changes within a verified revision range. Release notes
explain their consequences for a particular reader. Begin with the target
release, audience, version range and existing project conventions. Use the
[code changelog](../templates/code-changelog.md),
[documentation changelog](../templates/documentation-changelog.md) or
[release-note template](../templates/release-notes.md) for the requested output.

## Inspect the range

Resolve the base and target revisions before collecting changes. Read the
existing changelog to learn grouping, version headings and link conventions.
Native git commands provide the relevant evidence without a custom collector:

```sh
git rev-parse --verify BASE_COMMIT
git rev-parse --verify TARGET_COMMIT
git log --reverse --format=fuller BASE_COMMIT..TARGET_COMMIT
git diff --stat BASE_COMMIT TARGET_COMMIT
git diff BASE_COMMIT TARGET_COMMIT -- src docs
git show COMMIT -- relevant/path
```

Replace uppercase placeholders with the verified revisions and actual project
paths. Compare the final tree diff with individual commits: a reverted feature
may appear in history while producing no shipped change. Inspect relevant
issues, accepted decisions, release metadata and tests alongside commit messages.
A message such as "support binary input" does not prove that behavior shipped.
Native commands expose both sequence and net effect, so a custom history
collector has no demonstrated benefit for this workflow.

## Classify and verify

Classify user-visible code behavior separately from documentation changes,
including mixed commits. Group related changes into one meaningful entry, link
supporting history and exclude fully reverted changes from shipped additions.
Explain a partial revert's surviving effect. Check whether internal refactoring
has an actual reader impact before adding a release-note entry.

Verify compatibility, migration steps, availability dates and deprecations
against the target version and approved release evidence. Record unresolved
claims explicitly for the release reviewer. Keep human review and evidence
records separate from the reader-facing changelog.

The [worked history fixture](../tests/editorial/history/README.md) includes code,
documentation, a revert and an unverified release promise. Its expected outputs
show distinct supported entries from the same bounded history. The fixture uses
original synthetic patches so reviewers can inspect every claim independently.

## Write for the output's reader

Code changelogs describe observable product changes and necessary upgrade action.
Documentation changelogs describe added or corrected reader guidance and where
it can be found. Release notes lead with the impact readers need to assess and
link detail; they are not a transcription of commit subjects. Use the project's
release conventions and the public
[Keep a Changelog guidance](https://keepachangelog.com/en/1.1.0/) where useful.
Recheck the final entries against the net diff and evidence register before
requesting release review.
