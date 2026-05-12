# PR Review HTML Template

Use this template when the user asks you to review someone else's pull request. The reader is a reviewer -- the PR author wearing a reviewer hat to triage the feedback, or a co-reviewer using the artifact to focus their own pass. The goal is to make blocking issues unmissable and to let the reader land on the right two or three files instead of scrolling 40 of them in a terminal.

This template is modelled on https://thariqs.github.io/html-effectiveness/03-code-review-pr.html. The structure progresses from cheap-to-read overview to expensive-to-read detail, so a reader can stop as soon as they have what they need.

## Required sections, in order

1. **Header strip** with the source branch, the base branch, the SHA range (`<base-short>..<head-short>`), the commit count, the contributor(s), and the additions / deletions / changed-files counts. All of these come from `git` (see SKILL.md step 2 for the exact commands). If the user gave you a PR number or title, include it in the header too -- but as a label, not a data source.

2. **Summary** -- three to five bullets, each one sentence, answering "what does this PR do and how?" Avoid restating the title. Mention the implementation approach (e.g. "introduces a `useOptimisticMutation` hook backed by react-query's `onMutate`/`onError` cycle").

3. **Risk map** -- a horizontal list of every changed file (or every group of files, for very large PRs), color-tagged by reviewer status:
   - `safe` -- read once, no concerns
   - `worth a look` -- non-trivial change but no issues found
   - `needs attention` -- has a blocking or important finding

   Render this as a row of small file-name chips colored by status (see `html-conventions.md`). Most files in a typical PR should land in `safe`; the map is most useful when it visibly concentrates the reader's attention on the two or three files that matter.

4. **File panels** -- one section per file that needs more than a chip. Each panel contains:
   - File path as a clickable header (anchor link).
   - A one-line role description ("Adds the optimistic-update hook used by the task list.")
   - A unified-diff block with original line numbers in the gutter. Show the hunks that matter; collapse long unchanged regions with a "show context" toggle if useful.
   - Inline annotations. Each annotation has a **severity tag**, a one-line summary, an explanation, and ideally a suggested fix or alternative.

5. **Recommendations** -- a short ordered list of what the author should do before merge. Repeat blocking findings here so they're impossible to miss. End with a sentence on whether the PR can be merged after the blocking items are addressed.

Optional sections, only when they earn space:

- **Mermaid diagram** of the post-change call path or data flow, if the change is structural enough that a diagram clarifies it.
- **Test coverage notes** if the diff is light on tests for risky logic.
- **Out-of-scope observations** for issues the reviewer noticed in surrounding code that the author may want to follow up on later (clearly tagged so they don't block the current PR).

## Severity vocabulary

Use exactly four severity tags. They map to colors in `html-conventions.md`.

| Tag           | Meaning                                                                 |
|---------------|-------------------------------------------------------------------------|
| **blocking**  | Will cause incorrect behavior, regression, security issue, or data loss. Must be fixed before merge. |
| **important** | Worth fixing in this PR -- missing edge case, unclear contract, sloppy error path. Won't break prod today but lowers the floor for tomorrow. |
| **nit**       | Style, naming, micro-readability. Author can take it or leave it.       |
| **praise**    | Genuinely good design or a careful fix. Use sparingly; it loses meaning at volume. |

Don't invent more tags. Reviewers triage by skimming the colored stripe down the left of each annotation; adding a fifth color dilutes that signal.

## Writing the annotations

- **Cite a file path and line number** for every annotation -- `src/hooks/useOptimisticMutation.ts:42`. Use the post-change line numbers, since that's what the author will be looking at.
- **Lead with the problem, not the fix.** "Missing `queryClient.cancelQueries` before applying optimistic data, so a slow in-flight refetch can overwrite the optimistic state when it returns." Then suggest the fix.
- **Quote the offending code inline** if a line or two clarifies it, especially when the surrounding diff is long.
- **Prefer one substantive annotation over three nibbling ones** on the same construct. Stacked nits on a function the author clearly thought hard about read as adversarial and rarely improve the code.
- **No emoji severity icons.** The colored tag is the signal; an emoji adds noise and breaks for screen readers and printouts.

## Example annotation block (semantic content)

```
[blocking]  src/hooks/useOptimisticMutation.ts:42
            Missing queryClient.cancelQueries before applying optimistic data.

            A slow in-flight refetch started before the mutation will resolve
            after onMutate and overwrite the optimistic value, snapping the UI
            back. Call queryClient.cancelQueries({ queryKey }) at the top of
            onMutate, before reading the previous snapshot.
```

In HTML this renders as a left-bordered block colored per severity, with the tag and file reference on the first line in monospace, the one-line summary in bold, and the explanation in normal weight.

## Diff rendering

The diff text is produced by `git`, not by you. Run `git diff <base>...<head> -- <file>` and embed the output verbatim. Wrap each line in a `<span>` with a class derived from its first character (`+` -> `line add`, `-` -> `line del`, anything else -> `line ctx`), strip the leading character if you want a cleaner column, and put the result inside `<pre class="diff">`. The wrapping is a 10-line text transform; see [html-conventions.md](html-conventions.md) for a Python template.

Two reasons to delegate, not retype:

1. **Correctness.** Hand-typed diffs drift -- a `+` becomes a `-`, a context line goes missing, a hunk header's line range disagrees with the body. `git diff` doesn't make those mistakes.
2. **Annotations can trust the line numbers.** If the hunk in the artifact is exactly what `git diff` produced, the hunk header `@@ -A,B +C,D @@` is real, and an annotation pointing at "the `+queryClient.cancelQueries` line in this hunk" is unambiguous.

Practical notes:

- Don't pull in a syntax-highlighter library; the diff is short and the cost-to-benefit is poor.
- Use the line-number gutter on the left. The post-change line numbers come from the `@@` hunk header (`+C,D` -> the first added or context line is line `C`); incrementing from there for each non-`-` line gives you the rest. A few lines of awk or Python is enough; do not eyeball it.
- If the hunk header has helpful context (function name from `@@ ... @@ <function>`), surface it as a small caption above the hunk -- that text is also straight from `git diff`.
- Show only the hunks that matter. Don't paste an entire 600-line file diff to flag a one-line issue; show a focused range, and `<details>` any expanded context the reader might want.

## What the reader does with the artifact

The reader opens the file, scans the risk map, jumps via anchor to the one or two `needs attention` files, reads the annotations top-down, and acts on them. The recommendations section is their checklist. Every design choice in this template serves that flow; if a section doesn't, omit it.
