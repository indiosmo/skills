---
name: writing-commit-messages
description: >-
  Claude must use this skill whenever it writes, reviews, edits, or suggests a
  git commit message. This includes: composing a commit message during "commit
  this" or "save my changes" requests, reviewing or rewriting existing commit
  messages, preparing commits for a pull request, squashing or rewording commits
  during interactive rebase, amending commit descriptions, and generating
  changelogs or release notes from commit history. Triggers on: git commit,
  commit message, commit description, writing commits, save my changes, commit
  this, squash commits, amend commit, reword commit, changelog from commits,
  prepare PR commits, review commit messages.
---

# Writing Commit Messages

Apply these rules every time a commit message is written, reviewed, or amended.

## Subject Line Rules

- **Imperative mood** -- write as a command: "Add feature", "Fix bug", "Remove deprecated method". This matches git's own convention for auto-generated merge and revert commits ("Merge branch...", "Revert ..."). Test with: "If applied, this commit will [your subject line]."
- **50 characters or fewer** -- this is the target because `git log --oneline` and GitHub's commit list truncate long subjects (GitHub cuts around 72 characters). If the subject exceeds 50 characters, the commit may be doing too much. 72 is the hard limit.
- **Capitalize the first word**
- **No trailing period**
- **Name the affected component** -- when the repository contains multiple independent components (modules, packages, skills, services), name the one this commit touches in the subject. See [Scope](#scope).

Good subjects:
```
Refactor user authentication flow
Fix null pointer in payment processing
Add rate limiting to API endpoints
Remove unused database migration scripts
```

Bad subjects:
```
fixed a bug                          # past tense, vague
updates.                             # lowercase, period, vague
Refactoring the user auth flow to be cleaner and better organized   # too long, not imperative
```

## Scope

In a repository with multiple independent components (modules, packages, skills, services), **every commit subject must name the affected component**. A reader scanning `git log --oneline` should be able to tell whether a commit is relevant without opening the diff. Match the form the project's existing commits already use -- a `scope:` prefix (git, the Linux kernel, Conventional Commits) or prose ("... in the X skill", "... to the X module"). Name one component at a sensible level of granularity, not a file path.

Scope follows the substantive change, not the file count. A commit whose real edit lives in one component must name that component even when auxiliary files (CLAUDE.md, README, top-level config) are touched as reinforcement. Commits that change these rules themselves are not exempt -- scope them to the skill, module, or package being edited. Omit the scope only when the change genuinely spans the whole repository.

Good -- a reader knows which component changed:
```
Add convergence-path guidance to ansible skill
writing-commit-messages: Require scope in subject
```

Bad -- reader must open the diff to find out which of many skills was touched:
```
Remove Co-Authored-By and Signed-off-by trailers
Forbid variable lists in README files
```

## Body Rules

- **Separate subject from body with a blank line** -- required for `git log --oneline`, `format-patch`, and other tools to work correctly.
- **Wrap at 72 characters** -- git does not auto-wrap commit message bodies. Unwrapped lines cause horizontal scrolling in terminals, `git log`, and code review tools that render fixed-width text. 72 characters keeps text readable everywhere.
- **Explain what and why, not how** -- the diff shows the how. The body provides context a future reader needs: why was this change necessary? What problem does it solve? What are the side effects or consequences? For bug fixes, state the faulty behavior, what you changed, and how the change corrects it. For behavioral changes, state what happened before and what happens now. A reader should understand the motivation without opening the diff.
- **Be direct** -- lead each paragraph with an imperative verb ("Add ...", "Fix ...", "Remove ..."). Cut filler words and throat-clearing ("Also", "Additionally", "In order to"). Apply the **writing-clearly-and-concisely** skill to all commit prose.

## When a Body Is Needed

A subject-only commit is fine for trivial, self-evident changes (typo fixes, dependency bumps, renaming a variable). Add a body when:

- The reasoning behind the change is not obvious from the diff
- The commit introduces a breaking change
- Migration steps or manual actions are required after applying the commit
- There are non-trivial side effects, performance implications, or tradeoffs
- The change reverts or supersedes a previous commit and the context matters

When in doubt, add a body. A few sentences of context now saves minutes of archaeology later.

## Conventional Commits

If the project uses Conventional Commits, follow its existing convention. Common prefixes:

- `feat:` -- a new feature
- `fix:` -- a bug fix
- `chore:` -- maintenance tasks (dependency updates, CI config, tooling)
- `docs:` -- documentation-only changes

When a Conventional Commits prefix is used, it replaces the first word of the subject: `feat: Add dark mode toggle` rather than `feat: add dark mode toggle` (capitalize after the prefix the same way you would without it). If the project does not already use Conventional Commits, do not introduce the convention unilaterally.

## Trailers

Place trailers at the end of the body, each on its own line with no blank lines between them.

- **Issue references** -- `Closes #1234` or `Fixes #1234`. Use when the commit fully resolves an issue. Use `Refs #1234` when the commit is related but does not close the issue.

## Template

```
<Imperative subject, 50 chars or fewer>

<Why this change is needed. What problem it solves.
What side effects or consequences it has.
Wrap at 72 characters.>

<Trailers, if applicable>
```

## Examples

Single-concern commit with what/why:
```
Redirect user to login page after session timeout

Users were seeing a 403 error page when their session expired
during form submission. Redirect to login with a flash message
instead, preserving the return URL so they can resume after
re-authenticating.

Closes #1234
```

Multi-concern commit -- each paragraph leads with an imperative
verb and states what was done plus why:
```
Add gateway console certification helper

Implement the BOE gateway console tool for manual certification
of the inbound-error-disconnect scenario. The helper accepts a
local BOE session and lets the operator inject unknown
ExecutionReportNew messages to trigger the error threshold
disconnect.

Fix session lifecycle: remove unschedule from stop() as the
fsm_async_close path already handles it. The duplicated call
would throw with "is not scheduled" before calling into
disconnect().

Improve scheduler logging with session IDs.
```

Bad body style -- "Also" glues unrelated items and buries the
motivation:
```
Also add auction-order and client-does-not-resend certification
scenarios, and remove a stray break-after-return in ospec
normalization.
```
Each of those deserves its own paragraph with an imperative lead
and a brief reason.
