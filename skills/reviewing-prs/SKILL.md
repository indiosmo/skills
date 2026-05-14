---
name: reviewing-prs
description: "Produce single-file HTML artifacts for reviewing a branch against a base (defaults to `main`): severity-tagged diff review, author-voice writeup, and code-understanding artifacts. Works on any local git repo; no GitHub auth required."
---

# Reviewing PRs

Produce single-file HTML artifacts for three closely related tasks. The audience for all three is **the reviewer** -- somebody trying to evaluate, understand, or sign off on code. The artifacts differ in what they put in front of that reader:

| Artifact            | What it puts in front of the reviewer                                              |
|---------------------|------------------------------------------------------------------------------------|
| **PR review**       | A diff rendered with margin notes, severity tags, and jump links -- easier to scan than scrolling a terminal. |
| **PR writeup**      | The author's side: motivation, before/after, a file-by-file tour with the *why*, and where to focus the review. |
| **Code understanding** | An unfamiliar piece of code made legible -- entry points, hot path, dependencies, gotchas -- so the reviewer can read it confidently. |

For a change-shaped request (review my branch, review this PR, summarise these commits), produce the review and the writeup by default; add one or more code-understanding artifacts when the change is wide enough or strange enough to need orientation (see step 1 of the workflow). For a "help me understand X" request with no branch comparison in sight, produce only the understanding artifact(s).

## Why HTML?

Diffs, call graphs and module maps are spatial. Markdown flattens them into linear text. HTML lets the reader scan a file-level risk map before any code, jump between sections with anchors, expand source on demand, and read a Mermaid call graph next to the prose that explains it. Token budgets are no longer the bottleneck they once were; readability is.

Keep that purpose in mind. The HTML is not a design showcase, it is a thinking aid. Restraint beats flourish.

## Workflow

### 1. Decide which artifacts to produce

The inputs to this skill are always two git refs: a **base** (defaults to `main`, or `master` if `main` doesn't exist, or whatever the user names) and a **head** (defaults to `HEAD`, i.e. the current branch). The skill is repo-local: it uses `git`, not `gh` or any GitHub API, so authentication is not required. If the user mentions a PR number, treat it as a hint at the head branch name; still drive the work from `git`.

The default for any change-shaped request (`review my branch`, `review this PR`, `look at the diff against main`, etc.) is to produce **both** the review *and* the writeup. A review without a writeup leaves the reviewer guessing about intent; a writeup without a review is incomplete. Producing both forces you to articulate the *why* before nitpicking the *what*, which surfaces better findings.

- The **review** carries your findings (severity-tagged, file:line cited).
- The **writeup** carries the change's intent, ordered by conceptual importance -- written in the author's voice as a best-faith reconstruction of why the change exists. If the user *is* the author, lean on what they tell you and ask if anything is unclear.

Then decide whether to also produce **one or more code-understanding artifacts**. Spend an understanding artifact when the reviewer needs orientation before the diff makes sense. Strong signals:

- The change touches more than a handful of files, or files in more than one module / directory.
- The diff crosses a trust boundary, an integration point (DB, queue, external API), or an async / lifecycle boundary you have to think about.
- A new public surface is introduced (new exported function, class, schema, route).
- The change is a refactor, rename, or move -- the reviewer needs the pre-change shape to evaluate the post-change shape.
- The code uses domain terminology a fresh reviewer wouldn't know.
- Three or more files only make sense when read together.

If any of those apply, produce an understanding artifact for the relevant slice (often the subsystem the change touches; sometimes pre-change vs post-change as two separate artifacts if the diff fundamentally changes how the area works). For a small, single-file, self-contained change, skip it; the diff and the writeup are enough.

If the request is *not* about a branch comparison -- "explain how X works", "I need to understand the auth flow" with no branch in sight -- then produce only the code-understanding artifact(s). The review and writeup don't apply.

Always produce separate HTML files for each artifact. Don't cram everything into one page; the audiences and reading flows differ enough that the artifacts shouldn't be stapled together.

### 2. Gather the raw material

Don't write a single line of HTML before you understand the change. Read the per-artifact templates as needed: [references/pr-review.md](references/pr-review.md), [references/pr-writeup.md](references/pr-writeup.md), [references/code-understanding.md](references/code-understanding.md). For the visual conventions the renderer enforces (palette, severity colors, diff chrome), see [references/html-conventions.md](references/html-conventions.md) -- the templates cross-link into it where relevant.

**Resolve the base and head refs first.** If the user named them, use those. Otherwise:

- Head: the current branch -- `git rev-parse --abbrev-ref HEAD`. If that returns `HEAD` (detached), ask the user.
- Base: try `git symbolic-ref refs/remotes/origin/HEAD --short` (gives e.g. `origin/main`); fall back to `main`, then `master`. Verify with `git rev-parse --verify <name>` before using.

If `head == base`, you have nothing to diff -- ask the user what change they want reviewed. If the head branch hasn't been pushed, that's fine; everything below works against local refs.

**Delegate every mechanical operation to `git`. Don't reproduce diff hunks, line counts, or file lists from memory** -- the LLM is a poor stand-in for `git`. Use it to interpret the change, not to retype it. The triple-dot range (`<base>...<head>`) is the right form: it diffs from the merge base, so commits already on `main` don't appear in the output.

- Branch metadata for the header strip: `git rev-parse --abbrev-ref HEAD` (head), `git rev-parse --short <base> <head>` (SHAs), `git log <base>..<head> --pretty=format:'%h %an %ad %s' --date=short` (commits, authors, dates), `git shortlog -sn <base>..<head>` (contributor counts).
- Aggregate counts: `git diff --shortstat <base>...<head>` gives `N files changed, A insertions(+), D deletions(-)`.
- File list with per-file counts (drives the stats grid / risk map / per-file table): `git diff --numstat <base>...<head>` produces `<added>\t<removed>\t<path>` lines that parse trivially.
- Unified diff for the whole change: `git diff <base>...<head>`.
- Per-file diff for a single panel: `git diff <base>...<head> -- path/to/file`.
- Post-change file contents (so annotations cite real line numbers): `git show <head>:<path>` or the `Read` tool. The diff hunk header's `+N` line counter is correct only inside that hunk; don't extrapolate.

The raw `git diff` text is what the renderer's per-file `diff` field expects. **Never retype hunk content**: capture `git diff <base>...<head> -- <path>` into a variable and drop it straight into the spec.

`gh` is not required, even when available. If the user explicitly asks you to use it (e.g. to fetch a PR description for the writeup intro) and they confirm authentication, use it; otherwise ignore it.

For code-understanding work, read the entry-point files first, then follow the callstack. Note actual `file_path:line_number` references; the reader uses them to navigate. Don't paraphrase line numbers from memory -- read the file and copy them.

If anything is ambiguous (which base branch, which subsystem, what level of detail), make a reasonable call and note the assumption in the artifact's intro so the user can correct it.

### 3. Plan the artifact before writing it

Write an outline in the conversation (or as a scratch list) before generating HTML. A good outline names the sections, the diagrams, and the severity-tagged findings (for reviews). This is cheap to revise; HTML is not.

For each Mermaid diagram you plan, decide why it earns its place. Call graphs, request paths, state machines and module dependencies are good candidates. A diagram that just restates a bulleted list is not. See [skills/mermaid](../mermaid/SKILL.md) for diagram-type selection and syntax.

### 4. Build a JSON spec; let the script render the HTML

**Don't hand-write HTML.** The skill ships a renderer that takes a JSON spec and produces a self-contained HTML artifact with a warm light page chrome, a slate diff canvas with cream code text and transparent rgba add/del tints, collapsible file panels, bubble-style annotations, a risk map, and a suggestions checklist. Your job is the spec; the script's job is to keep the visual output identical across runs.

The renderer lives at `scripts/render_artifact.py`, and full example specs for each artifact kind live alongside it in `scripts/examples/` (`review-spec.json`, `writeup-spec.json`, `understanding-spec.json`). Print the example spec to learn the shape:

```bash
python3 skills/reviewing-prs/scripts/render_artifact.py --print-schema review
python3 skills/reviewing-prs/scripts/render_artifact.py --print-schema writeup
python3 skills/reviewing-prs/scripts/render_artifact.py --print-schema understanding
```

A review spec carries: header metadata (refs, SHAs, stats, commits), a `summary_md` (small markdown subset), a list of `files` each with `path`, `risk`, `added`/`removed`, the raw `diff` text from `git diff`, and per-line `annotations` (each with `severity` and `body_md`), plus a `suggestions` list rendered as a checklist at the bottom. **Pipe `git diff <base>...<head> -- <path>` straight into each file's `diff` field; don't paraphrase.**

Render:

```bash
python3 skills/reviewing-prs/scripts/render_artifact.py \
  --spec /tmp/spec.json \
  --output ./review-artifacts/review-<slug>.html
```

The script validates the spec first (severity vocabulary, risk vocabulary, required fields) and refuses to render if anything is malformed. Use `--validate-only` to check a spec without writing output.

What the script handles, so you don't have to:

- Server-side diff rendering. The script parses unified diff text and emits structured rows with line numbers, mark, and code text -- no client-side library, no syntax highlighter, no fight with someone else's dark theme.
- Open vs collapsed file panels. Files at risk `worth-a-look` / `needs-attention`, or with any `blocking` / `important` annotation, render as full open cards with the diff and bubble-style annotations. All others render as one-line collapsed `<details>` rows with an optional `note_md` for a one-paragraph summary.
- The warm palette, the serif headings, the risk-map chips with anchor highlighting, the suggestions checklist.
- Mermaid is the only CDN dependency, loaded only when the spec carries `diagrams`.

### 5. Validate every Mermaid diagram before saving

A Mermaid diagram with a syntax error degrades silently: the reader sees an empty area or a literal code block where the diagram should be, and that's a worse outcome than no diagram at all. Validate every `<pre class="mermaid">` block before you consider the artifact done. Don't trust visual inspection of the source -- corner cases like `:=`, unquoted labels with parentheses, and `<br/>` in node labels parse in some diagram types and not others.

For each diagram, extract the body and run it through `mmdc`:

```python
import re, subprocess, tempfile
from pathlib import Path

def validate_mermaid_in(html_path: Path) -> list[tuple[int, str]]:
    text = html_path.read_text()
    failures = []
    for idx, m in enumerate(re.finditer(r'<pre class="mermaid">(.*?)</pre>', text, re.S)):
        body = m.group(1).strip()
        with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False) as f:
            f.write(body)
            tmp = f.name
        proc = subprocess.run(["mmdc", "-i", tmp, "-o", tmp + ".svg"], capture_output=True, text=True)
        if proc.returncode != 0:
            failures.append((idx, proc.stderr.splitlines()[-1] if proc.stderr else "unknown error"))
    return failures
```

Alternatively, use the [mermaid skill](../mermaid/SKILL.md) (`skills/mermaid/scripts/validate_mermaid.py`) which wraps the same call with nicer error reporting and supports the `beautiful-mermaid` renderer when available.

If a diagram fails, fix it (see the mermaid skill for syntax fixes) and revalidate. If a diagram cannot be made to validate, fall back to plain text or remove it entirely. Shipping a broken diagram is not an option.

For diagrams that should also be eyeballed (call graphs, request paths -- anything where layout matters), render to SVG with `mmdc -i tmp.mmd -o tmp.svg` and open the SVG. Mermaid's auto-layout sometimes produces overlapping edges or cramped nodes; fix the layout via direction hints (`flowchart LR` vs `TB`) or by simplifying the node labels.

### 6. Save and surface the output

Save to `./review-artifacts/<artifact-kind>-<slug>-<timestamp>.html` (create the directory if missing). Use a slug that names the head branch, a PR number if the user supplied one, or the module being explained -- `auth-refactor-review.html`, `pr-1247-writeup.html`, `auth-flow-understanding.html`. Print the absolute path so the user can open it with `open <path>` or `xdg-open <path>`.

If you produced more than one artifact, list each path and what it contains in a short final summary (two or three lines is plenty).

## Pitfalls to avoid

- **Fabricated line numbers.** Always cite line numbers from the actual file you read, not from the diff hunk header (which counts post-change file lines but only for that hunk). If you didn't read the file, don't cite the line.
- **Hand-rendered diffs.** Don't retype hunks from memory or from a paraphrase of the diff, and don't try to reproduce the visual chrome (severity pills, risk chips, collapsible panels) by hand. Capture `git diff <base>...<head> -- <path>` straight into each file's `diff` field in the spec, and let `render_artifact.py` produce the HTML. Hand-built HTML is how this skill regresses on consistency between runs.
- **Reading without filtering.** A 40-file PR doesn't need 40 file panels of equal weight. The risk map exists so most files get one line ("safe, formatting only") and the interesting two or three get full treatment.
- **Dressing up the page.** Animations, custom cursors, gradient meshes, decorative fonts -- these belong in the `frontend-design` skill's marketing-page output, not here. The reader is doing work; don't get in the way.
- **One mega-artifact.** A writeup is not a review is not an understanding doc. Their audiences and purposes differ. Producing separate files keeps each one focused and shareable.
- **Diagrams that restate prose.** A Mermaid graph that lists "Step 1 → Step 2 → Step 3" next to a numbered list duplicates information. Use diagrams for branching, joining, cycles, or anything genuinely two-dimensional.
- **Unvalidated Mermaid.** Don't ship a diagram you haven't run through `mmdc`. The diagram source can look fine and still fail to parse for non-obvious reasons (a `:` in a state-diagram transition label, an unquoted parenthesis in a flowchart node, a `<br/>` in a context that doesn't allow it). The reader gets a blank slot, not an error message; you'll never know it broke unless you validated.
- **Linking out where the reader can't follow.** Internal company URLs, JIRA tickets, and private GitHub links should be clearly labelled as such; don't pretend the reader has access.

## Quick reference: what each artifact contains

The full templates live in `references/`; this table is just orientation. The renderer's visual conventions (palette, severity colors, diff chrome) are documented separately in [references/html-conventions.md](references/html-conventions.md).

| [PR review](references/pr-review.md) | [PR writeup](references/pr-writeup.md) | [Code understanding](references/code-understanding.md) |
|-------------------------------|-----------------------------|---------------------------------|
| PR metadata header            | TL;DR (2-3 sentences)       | Title: "How X flows through Y"  |
| Summary of what the PR does   | Why (problem + impact)      | Short intro + trust boundaries  |
| File-level risk map           | Change stats grid + per-file table | Request path / call graph (Mermaid) |
| File panels with annotated diffs | File-by-file conceptual tour | Numbered callstack walkthrough  |
| Severity-tagged inline comments | Focus areas with line refs | Key files list                  |
| Recommendations / blocking items | Test plan, rollout / migration notes | Gotchas / non-obvious invariants |
