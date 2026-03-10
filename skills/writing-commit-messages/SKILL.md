---
name: writing-commit-messages
description: >-
  Write clear, consistent git commit messages following established conventions.
  Use when Claude needs to write a commit message, review commit messages, or
  when the user asks for help crafting commit messages. Triggers on: git commit,
  commit message, commit description, writing commits.
---

# Writing Commit Messages

Apply these rules every time a commit message is written.

## Subject Line Rules

1. **Imperative mood** -- write as a command: "Add feature", "Fix bug", "Remove deprecated method". Test with: "If applied, this commit will [your subject line]."
2. **50 characters or fewer** -- forces concise thinking. 72 is the hard limit. If the subject is too long, the commit may be doing too much.
3. **Capitalize the first word**
4. **No trailing period**

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

## Body Rules

5. **Separate subject from body with a blank line** -- required for `git log --oneline`, `format-patch`, and other tools to work correctly.
6. **Wrap at 72 characters** -- keeps text readable in terminals and `git log` output.
7. **Explain what and why, not how** -- the diff shows the how. The body provides context a future reader needs: why was this change necessary? What problem does it solve? What are the side effects or consequences?

## Body Template

Use a body when the subject alone does not convey enough context:

```
<Imperative subject, 50 chars or fewer>

<Why this change is needed. What problem it solves.
What side effects or consequences it has.
Wrap at 72 characters.>
```

When no body is needed (trivial or self-evident changes), a subject-only commit is fine.

## Example

```
Redirect user to login page after session timeout

Users were seeing a 403 error page when their session expired
during form submission. Redirect to login with a flash message
instead, preserving the return URL so they can resume after
re-authenticating.

Closes #1234
```
