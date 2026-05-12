# PR Writeup HTML Template

Use this template either when the user is the PR author drafting a richer description than the GitHub "Description" box, or when you are reviewing someone else's PR and producing the writeup alongside the review as a best-faith reconstruction of the author's intent (the default behaviour of this skill on PR-shaped requests).

The reader is a reviewer context-switching from unrelated work, with limited time. Lead with why, then what, then how.

**A note on voice when you are not the author.** The writeup is written in the author's voice -- first person -- even when *you* (the LLM) are the one producing it. The point is to put the reviewer inside the author's reasoning: "we chose X because Y, the alternative we rejected was Z." When you are reconstructing intent rather than reporting it, do two things: (1) keep the prose grounded in what the diff actually shows, not what you imagine the author might have wanted; (2) add a small italic note at the top of the writeup -- one sentence -- saying that the writeup is a reviewer-side reconstruction, so the actual author can correct anything you got wrong. Don't sprinkle "I think" or "presumably" through the prose; the disclaimer carries the uncertainty in one place.

This template is modelled on https://thariqs.github.io/html-effectiveness/17-pr-writeup.html. The writing should be technical but conversational. Parenthetical asides are good; over-formal prose is bad.

## Required sections, in order

1. **Header strip** -- PR title, number (if it exists), author, target branch. Add an anchor-link bar near the top so the reader can jump straight to the section that matters to them.

2. **TL;DR** -- two or three sentences. State the problem and the fix, with a concrete number if you have one. "Comment notifications were dropping under load (p99 latency 1.4s, ~3% silent failures). This PR moves email/push delivery onto a retrying worker with a dead-letter queue, taking p99 to 180ms with no observable drops in a 4h soak."

3. **Why** -- a paragraph or two, plus metrics or screenshots if applicable. Make the business or user-facing case. Reviewers who agree with the *why* approve faster and review the *how* more charitably.

4. **Change stats** -- a compact orientation block answering "how big and what shape is this PR?" before any prose. It has two parts:

   - A **stats grid** of large numerical callouts: file count, `+lines`, `−lines`, and optionally one more dimension that fits the change (e.g. "tests touched", "code files vs docs files", "configs changed"). Three to five tiles is the right size. The numbers come from `git diff --shortstat <base>...<head>`; don't recount by hand.
   - A **per-file table** with one row per touched file: path in monospace, a small change-type pill (`add` / `expand` / `trim` / `rename` / `delete` / `docs` -- pick from a small fixed vocabulary), per-file `+N / −N` in the added/removed colors, and a one-line description of the file's role in the change. Source the per-file numbers from `git diff --numstat <base>...HEAD`, which prints `<added>\t<removed>\t<path>` and is trivially parseable.

   This table doubles as a table of contents for the file-by-file tour that follows, so anchor each path to its panel below.

5. **File-by-file tour** -- ordered by *conceptual importance*, not alphabetical or by file count. Each file gets:
   - Path in monospace.
   - One or two sentences on its role.
   - An inline diff or code snippet of the noteworthy hunk (not the whole file). For diff snippets, lift the bytes from `git diff <base>...<head> -- <path>` and run them through the transform in [html-conventions.md](html-conventions.md); don't retype the `+`/`-` lines. For non-diff code samples (e.g. quoting the post-change function to explain its shape), `git show <head>:<path>` or a `Read` of the file is the source of truth.
   - Optional caption explaining a subtle choice (e.g. "we don't throw on a muted-channel error -- ack and park, so retry doesn't loop").

6. **Focus areas** -- three to five bulleted items, each with a file and line range, naming what the reviewer should look at hardest. This is the writeup equivalent of "here are the parts I'm least sure about" or "here are the parts most likely to break things." It is invaluable; reviewers love being pointed.

7. **Test plan** -- what was tested, how, and what was deliberately not tested. Use subheads for unit / integration / load / manual as appropriate. Include the actual command(s) you ran if a reviewer might want to reproduce.

8. **Rollout** -- if the change is risky enough to need staged deployment, feature flags, dual-writes, or a migration, describe the plan and the rollback path. Skip this section for low-risk PRs; padding it dilutes its meaning when it matters.

Optional sections:

- **Architecture diagram** (Mermaid) showing post-change topology if the change touches more than one service or process. See `skills/mermaid` for diagram-type selection.
- **What's out of scope** -- name two or three nearby things you deliberately didn't change, so reviewers don't ask. "No per-user digest batching yet -- bundling would make this unreviewable; tracked in issue #842."
- **Open questions** -- where you specifically want a reviewer's opinion. Frame these as questions, not as undecided code.

## Writing style

- Speak as the author, in plain prose. First-person plural ("we") or singular ("I") both work; pick one and stick to it.
- Parenthetical asides are good. They carry the "I considered this but..." reasoning that doesn't merit a full paragraph.
- Bold the numbers. `p99 on comments.create: **180 ms**` lets the reader scan the page and absorb the magnitudes without reading every word.
- Inline code snippets are short. If a snippet is more than ~15 lines, ask whether you really need it, or whether a description plus a file:line reference would do.
- Don't restate the diff. The reviewer can read the diff. The writeup explains the parts the diff *doesn't* show: why this approach over the alternatives, what was almost done differently, what the failure modes are.

## What success looks like

A reviewer who opens this artifact, reads the TL;DR, glances at Focus Areas, jumps to one file panel, and approves with a one-line comment. That's the goal. Every section is in service of compressing the reviewer's time without dropping signal.
