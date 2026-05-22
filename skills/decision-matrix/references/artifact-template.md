# Decision Matrix HTML Artifact

The artifact is a single self-contained HTML file: one `<style>` block in the head, no
external CSS, no JavaScript, no CDN dependencies. A reader should be able to open it from
disk, email it, or drop it into a shared drive and have it render the same everywhere.

## Reference files

Two examples ship with the skill. They share the same palette and chrome -- the
difference is which optional knobs are turned on:

- **[../assets/example.html](../assets/example.html)** -- the full configuration: cards
  block above the table (level-3 approach presentation), per-cell score badges (1-5), a
  weight column, weighted-score footer, and a notes column on the right. Use as a
  starting point when one or more of those knobs is on. Demonstrates the
  **sparse-coloring** principle: not every cell is coloured.
- **[../assets/example-lean.html](../assets/example-lean.html)** -- the lean
  configuration: option headers carry a one-line subtitle (level-2 approach
  presentation), no scoring, no weight column, no notes column. Also demonstrates the
  **multi-decision** pattern (two stacked matrices for coupled sub-decisions) and the
  **"?" convention** for an unknown cell. Use as a starting point when none of the
  optional knobs apply.

Copy whichever is closer to the configuration you need and adapt content; do not redesign
the chrome unless the user asks. Visual consistency across decision matrices is more
valuable than per-artifact tailoring.

## Structure

The page reads top to bottom as:

1. **Title and lede** -- one `<h1>` with a short subtitle, followed by a one-paragraph
   `<p class="lede">` that names the decision and the context. Two or three sentences.
2. **Assumptions (optional)** -- an `.assumptions` block with `<h2>Assumptions</h2>` and a
   `<ul>` of premises the matrix takes as settled (scope decisions, environmental facts,
   tooling commitments). Omit when there are none.
3. **Open Questions (optional)** -- an `.open-questions` block with
   `<h2>Open Questions</h2>` and a `<ul>` of questions whose answers would change the
   decision. Omit when there are none.
4. **Approach presentation** -- inline in the table headers, optionally with a cards block
   (`.approaches`) above the matrix for options that need a paragraph of detail. See
   "Approach presentation knob" below.
5. **The matrix** -- a `<table>` with columns: Criterion, (optional) Weight, one column
   per option, (optional) Notes. An optional `<tfoot>` row carries the weighted score.
6. **Code samples (optional)** -- one small sample per option, below the matrix, when API
   shape, syntax, or call-site ergonomics are part of the comparison.
7. **Decision** -- a plain `<h2>Decision</h2>` (or `<h3>` inside a sub-decision section)
   followed by two to four short paragraphs. **No highlighted box, no coloured panel.**
   The emphasis is carried by a `<b>` on the chosen option in the lead sentence, not by
   chrome around the block.

The reader's eye flows: orient (lede), check the premises (Assumptions), see what is
still in flight (Open Questions), see the candidates (headers or cards), compare
(matrix), read the call (Decision). Assumptions and Open Questions sit above the matrix
because the matrix is read against them -- a reader who finds the call surprising should
be able to check the premises and the unresolved questions before re-reading the cells.

## Palette and chrome

A warm-paper palette with restrained colour. Reuse the CSS variables verbatim:

```css
--bg: #fafaf7;          /* page background */
--fg: #1a1a1a;          /* body text */
--muted: #6b6b6b;       /* lede, helper text, notes */
--rule: #d8d6cf;        /* table and card borders */
--accent: #6b5b3a;      /* section heading color */

--good-bg: #d8ebd2;     /* td.good background */
--good-fg: #1f4a26;     /* td.good text */
--ok-bg:   #f4ecc6;     /* td.ok background */
--ok-fg:   #5a4a10;     /* td.ok text */
--bad-bg:  #f0c8bc;     /* td.bad background */
--bad-fg:  #6a1d12;     /* td.bad text */
--na-bg:   #ececec;     /* td.na background */
--na-fg:   #555;        /* td.na text */
```

Do **not** tint option columns. The verdict colour on each cell is the only colour the
table should carry; tinting a whole column underneath muddies the contrast.

Typography: system sans-serif at ~15px. No web fonts. Uppercase section headings with
letter spacing distinguish structural heads from content.

Code-sample blocks use a local gruvbox dark medium palette. Keep the colours scoped to
the sample block; do not change the page palette.

## The matrix table

Columns, left to right:

| Column     | Width | Required? | Content                                                          |
|------------|-------|-----------|------------------------------------------------------------------|
| Criterion  | ~14%  | yes       | Short criterion name, bold, warm background                      |
| Weight     | ~5%   | optional  | Criterion weight 1-5, centered, defaults to 1 (scoring mode only)|
| Option N   | flex  | yes       | Score badge (scoring mode only) + reasoning prose; bg = verdict  |
| Notes      | ~14%  | optional  | Cross-cutting commentary on the criterion                        |

Cells use this structure:

```html
<td class="good">
  Works on any machine, in CI, in containers, on a fresh clone.
</td>
```

With scoring on, the score badge sits at the front of the cell:

```html
<td class="good"><span class="score-badge">5</span>Works on any machine, in CI, in
containers, on a fresh clone.</td>
```

The cell's class (`good`, `ok`, `bad`, `na`, or no class for neutral) drives the
background colour. No verdict tag, no inner `.cell` div -- the reasoning is the whole
content. Cells can be very short ("Yes", "Ok", "Not supported") for binary criteria.

Verdict classes:

- `td.good` -- green; an appealing aspect, the option clearly handles the criterion well.
- `td.ok` -- yellow; a not-so-great aspect, the option works but with caveats worth
  knowing about.
- `td.bad` -- red; a blocker aspect, a serious concern.
- `td.na` -- italic grey; the criterion does not apply to this option.
- no class -- neutral aspect; the option neither shines nor stumbles. Leave the cell on
  the default white background. **Most cells should land here** -- coloured cells need
  the contrast of neutral ones around them to stand out.

For an unknown verdict, leave the cell uncoloured (no class) and prefix the prose with
"?":

```html
<td>? Not benchmarked yet -- likely similar to subtree but unconfirmed.</td>
```

The "?" signals the gap; the absence of colour signals "no verdict"; the question itself
moves into the Open Questions block.

The criterion column (`td.criterion`) uses the warm faint background `#faf8f1` to
separate row labels from data cells. If the weight or notes columns are present, they use
the same warm background.

### Approach presentation knob

Three levels; use the lowest one that does the job.

**Level 1: header only.** The option name in the `<th>` is self-evident.

```html
<th>Postgres</th>
```

**Level 2: header with subtitle.** A one-line description in an `opt-sub` span under the
option name.

```html
<th>Postgres <span class="opt-sub">Single relational store; structured queries via SQL.</span></th>
```

Style for `opt-sub`:

```css
th .opt-sub {
  display: block;
  font-weight: 400;
  color: var(--muted);
  font-size: 12px;
  margin-top: 3px;
  line-height: 1.4;
}
```

**Level 3: cards block above the table.** An `.approaches` grid before the matrix, with a
paragraph of detail per option. When the cards block is present, the `<th>` carries just
the option name -- do not duplicate the description as a subtitle.

```html
<div class="approaches">
  <div class="approach">
    <h3>A. Copy (current)</h3>
    <p>Plain files committed in <code>docs/cpp-guides/</code>. Periodic manual resync.</p>
  </div>
  ...
</div>
```

Style for `.approaches`:

```css
.approaches { display: grid; grid-template-columns: repeat(N, 1fr); gap: 12px; margin-bottom: 28px; }
.approach { padding: 12px 14px; border: 1px solid var(--rule); border-radius: 6px; background: white; }
.approach h3 { margin: 0 0 4px; font-size: 14px; letter-spacing: 0.02em; text-transform: uppercase; color: var(--accent); }
.approach p { margin: 0; font-size: 13px; color: var(--muted); }
```

### Score and weight columns (optional)

Off by default. **Include scoring only when the user explicitly asks for it.** When on,
two pieces of numeric information appear:

**Per-cell score badge (1-5).** A small bold badge at the start of each cell. 5 reads as
clearly green, 3 as yellow or no-colour, 1 as clearly red. Style:

```css
.score-badge {
  display: inline-block;
  min-width: 18px;
  padding: 1px 6px;
  margin-right: 8px;
  border-radius: 3px;
  background: rgba(0, 0, 0, 0.08);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  font-size: 12.5px;
  text-align: center;
  vertical-align: 1px;
}
```

Omit the badge entirely for unknown cells; "?" in the prose carries the signal.

**Weight column for criteria.** A "Wt" column at the left holds each criterion's
weight, **defaulting to 1**. The user edits individual weights to reflect what actually
matters. Use the same 1-5 range as the cell score.

**Weighted-score footer.** A `<tfoot>` row sums `sum(score * weight)` per option:

```html
<tfoot>
  <tr>
    <td colspan="2">Weighted score (sum of score &times; weight; tune weights to taste)</td>
    <td class="score">39</td>
    <td class="score">22</td>
    ...
  </tr>
</tfoot>
```

The "tune weights to taste" parenthetical is important. It tells the reader the number is
structured commentary, not an oracle. If the score and the cell colours tell the same
story, the score is redundant -- pull it back off.

### Notes column (optional)

Off by default. Turn on when most rows have genuinely cross-cutting commentary to carry --
caveats about the criterion itself, constraints that apply across all options, context the
column readings would otherwise miss. If most rows would be empty, drop the column.

### Code samples (optional)

Use code samples when comparing API shapes, syntax, or caller-side ergonomics and the
side-by-side snippets reveal something the prose matrix cannot. Typical triggers:
call-site clarity, error-handling shape, generic type noise, migration edits, or whether
the domain concept is named at the caller.

Skip the block when the code would be toy scaffolding, when the decision is mostly
operational or architectural, or when the relevant syntax already fits cleanly inside a
cell. Code samples are supporting evidence, not another required section.

Place the block immediately below the matrix it supports and before that matrix's
Decision block. In multi-decision artifacts, each sub-decision may include or omit its
own block.

Markup:

```html
<div class="samples">
  <div class="sample">
    <h3>A. Free function</h3>
<pre><code><span class="kw">auto</span> order =
  <span class="fn">make_order</span>(symbol, side, quantity);</code></pre>
  </div>
  <div class="sample">
    <h3>B. Builder</h3>
<pre><code><span class="kw">auto</span> order =
  <span class="type">OrderBuilder</span>(symbol).<span class="fn">side</span>(side).<span class="fn">quantity</span>(quantity).<span class="fn">build</span>();</code></pre>
  </div>
</div>
```

Two arrangements show up in practice:

- **Multi-card grid (option-by-option comparison).** One `<div class="sample">` per option,
  inside one `<div class="samples">`. The auto-fit grid wraps the cards into two columns
  on a wide screen and stacks them on narrow ones. This is the most common use of the
  block -- placed under a decision-point matrix, before its Decision block, when seeing
  the call sites side by side would change the read.
- **Single card ("this is the chosen shape").** One `<div class="sample">` alone inside a
  `<div class="samples">`. Useful after a decision is settled and the artifact wants to
  show the canonical call-site shape the chosen option produces -- typically placed under
  the Decision block, not above it. Distinct from the comparison block: this one's job is
  reference, not comparison.

Keep snippets small enough to scan without horizontal scrolling. Prefer the caller's view
over implementation sketches. The auto-fit grid handles two, three, or four columns
without per-count overrides -- pick the snippet count from the decision, not from a
layout constraint.

The card header (`<h3>`) carries the option name (in a multi-card block) or a short label
(in a single-card block). The body uses inline `<span>` classes for syntax highlighting:

- `kw` -- keywords and language built-ins (`auto`, `const`, `template`, `typename`, `return`)
- `type` -- type names (`Order`, `OrderBuilder`)
- `fn` -- function and method names (`make_order`, `build`)
- `ns` -- namespaces and module prefixes (`std`, `aor`)
- `str` -- string literals
- `com` -- comments

Highlight only what the comparison turns on. Over-highlighting (every identifier coloured)
reads like a rainbow and adds no information. Under-highlighting (one keyword in the
whole snippet) wastes the chrome. Highlight the names the matrix cells reference and the
syntax shape (keywords, types) that distinguishes one option from another.

Style (paste into the page `<style>` block):

```css
:root {
  --code-bg:   #282828;
  --code-fg:   #d4be98;
  --code-rule: #504945;
  --code-head: #1d2021;
}
.samples {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 14px;
  margin: 14px 0 18px;
}
.sample {
  background: var(--code-bg);
  border: 1px solid var(--code-rule);
  border-radius: 6px;
  color: var(--code-fg);
  min-width: 0;
  overflow: hidden;
}
.sample h3 {
  background: var(--code-head);
  color: #fabd2f;
  font-size: 12px;
  letter-spacing: 0.04em;
  margin: 0;
  padding: 8px 12px;
  text-transform: uppercase;
}
.sample pre {
  font: 12.5px/1.5 "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  margin: 0;
  overflow-x: auto;
  padding: 12px 14px 14px;
}
.sample pre code { background: transparent; border-radius: 0; color: inherit; font-size: inherit; padding: 0; }
.sample .kw   { color: #fb4934; }
.sample .type { color: #fabd2f; }
.sample .fn   { color: #b8bb26; }
.sample .ns   { color: #83a598; }
.sample .str  { color: #b8bb26; }
.sample .com  { color: #928374; font-style: italic; }
```

The `.sample pre code` override is necessary because the page's default `code` styling
gives inline `<code>` a warm-paper background; the dark sample card has its own
background and the inline rule has to be cleared inside it.

These inline classes are enough for short illustrative samples. Do not pull in
highlight.js, Prism, web fonts, or a CDN for a decision-matrix artifact. See
`assets/example-lean.html` for a worked code-samples block under sub-decision 2.

### Number of option columns

Three or four is the sweet spot for most decisions. Two collapses into pros-and-cons; six
or more dilutes attention and the later columns get sloppy. If you have many candidates,
consider whether some are variants of the same approach and can be merged with a
footnote.

Keep cell prose to one or two sentences. If a cell needs three sentences, it is either
mixing two criteria (split the row) or burying a caveat (state the trade-off directly).

## The Decision block

A plain heading followed by two to four short paragraphs of class `decision-body`.
**No wrapping div, no coloured panel, no highlighted box.** The chosen option is
emphasised inline with a `<b>` tag in the lead sentence; chrome around the block is
unnecessary.

For a single-matrix artifact, use a top-level `<h2>` heading (the existing accented
uppercase style applies):

```html
<h2>Decision</h2>
<p class="decision-body">
  <b>Subtree.</b> The two criteria that decided it are blast radius and reproducibility:
  every other option either leaks edits across consumers or fails on a fresh clone.
</p>
<p class="decision-body">
  Copy is the runner-up and would have stayed the call if the guides had not started
  drifting; subtree buys an explicit "last pulled" history without losing the
  local-files ergonomics.
</p>
<p class="decision-body">Revisit when guides ship independently of this repo.</p>
```

For a multi-decision artifact, use `<h3 class="decision">` immediately after each
sub-decision's matrix, or after its optional code-sample block, with the same
`decision-body` paragraphs underneath:

```html
<h3 class="decision">Decision</h3>
<p class="decision-body">
  <b>Apply the multiplier inside the gateway.</b> Centralising the multiplication is
  the only option that prevents silent PnL drift across forgotten call sites.
</p>
<p class="decision-body">
  Passing the multiplier in the request is the clearest at the call site, but the
  schema bump and per-caller consistency burden aren't worth it for a transformation
  that is fundamentally a property of the venue, not the order.
</p>
```

Styles:

```css
h3.decision {
  font-size: 15px;
  margin: 18px 0 8px;
  color: var(--accent);
  letter-spacing: 0.02em;
  text-transform: uppercase;
}
.decision-body { margin: 8px 0; max-width: 78ch; }
```

Content rules for the Decision block:

- **First sentence states the choice and emphasises it.** `<b>` on the option name (or a
  leading `<b>Decision: option-name.</b>`). The reader who only reads the bold lead
  should come away with the call.
- **One or two sentences of reasoning.** Point at the criteria that decided it; do not
  restate the cell prose.
- **Discarded options only when not obvious.** If an alternative genuinely tempted, add a
  sentence on what would have flipped it. Skip this for options the matrix already ruled
  out clearly.
- **Optional revisit clause.** A single short sentence on the trigger that would re-open
  the decision. This is what makes decision matrices durable rather than one-time
  analyses; include it when there is a concrete trigger to name.

The block records the decision and its grounds. Do not phrase it as a reading of the
matrix ("the matrix points toward...") or as advice from outside ("I recommend...",
"you should pick..."). State the call.

## The Assumptions block

See SKILL.md "Assumptions" for what goes in this block and how to phrase entries.
Markup:

```html
<div class="assumptions">
  <h2>Assumptions</h2>
  <ul>
    <li><b>Premise topic:</b> settled statement of fact, on its own terms.</li>
    ...
  </ul>
</div>
```

Style (mirrors the Open Questions block; both render as warm-paper cards above the
matrix):

```css
.assumptions {
  margin: 0 0 18px;
  padding: 16px 20px;
  background: white;
  border: 1px solid var(--rule);
  border-radius: 6px;
}
.assumptions h2 { margin-top: 0; }
.assumptions ul { margin: 0; padding-left: 20px; }
.assumptions li { margin: 4px 0; }
.assumptions li b { color: var(--accent); }
```

Place the block immediately under the lede, before any sub-decision heading. In a
multi-decision artifact, there is exactly one Assumptions block for the whole document
-- premises apply across the matrices, not per-matrix.

## The Open Questions block

See SKILL.md "Open Questions" for what goes here and how to phrase entries. Markup:

```html
<div class="open-questions">
  <h2>Open Questions</h2>
  <ul>
    <li><b>Question?</b> Why it matters / what answer would flip the call.</li>
    ...
  </ul>
</div>
```

Place the block immediately under the lede (and under the Assumptions block when both
are present), before any sub-decision heading. There is exactly one Open Questions
block for the whole document.

Style:

```css
.open-questions {
  margin: 0 0 24px;
  padding: 16px 20px;
  background: white;
  border: 1px solid var(--rule);
  border-radius: 6px;
}
.open-questions h2 { margin-top: 0; }
.open-questions ul { margin: 0; padding-left: 20px; }
.open-questions li { margin: 4px 0; }
.open-questions li b { color: var(--accent); }
```

## Content rules

- **No marketing language.** "Robust", "scalable", "elegant" are not specifications.
  Replace with the concrete property.
- **Specific over generic.** "Breaks on any host that does not have `/home/alice/...`"
  beats "not portable".
- **The verdict is the cell's background colour.** No inline uppercase tags, no bare
  adjectives standing in for a verdict. Cells that genuinely have no verdict get no class
  and stay on the default background.
- **No icons or emoji.** The verdict colour is the only chrome.
- **No screenshots or images.** A decision matrix is text-and-table; embedded images
  bloat the file and rarely add value.
- **No external dependencies.** No `<link rel="stylesheet">` to a CDN, no `<script>`
  tags, no font imports. Self-contained or it does not ship.

## Multi-decision artifacts

When the research question contains two or three coupled sub-decisions, build one HTML
document with stacked matrices. Structure:

1. Title and lede (whole document).
2. (Optional) Assumptions block -- one for the whole document; premises apply across
   the matrices.
3. (Optional) Open Questions block -- one for the whole document; questions span the
   matrices.
4. `<h2 class="subdecision">` for sub-decision 1, optionally followed by its cards block,
   then its matrix table, optional code samples, then an `<h3 class="decision">Decision</h3>`
   block.
5. `<h2 class="subdecision">` for sub-decision 2, optionally followed by its cards block,
   then its matrix table, optional code samples, then an `<h3 class="decision">Decision</h3>`
   block.
6. (Repeat as needed; cap at three sub-decisions per artifact.)

Place each Decision block immediately under the matrix it decides, with only that matrix's
optional code-sample block between them. Do not collect the calls into a single combined
block at the end of the document -- that forces the reader to scroll between matrix and
verdict. If the sub-decisions have an ordering dependency (commit A before A's choice
constrains B), state that inside the relevant Decision block, not in a separate block.

Assumptions and Open Questions go above the first sub-decision -- never at the bottom
or interleaved between sub-decisions. A premise that applies to only one sub-decision
is still recorded once, at the top.

Style for the sub-decision heading:

```css
h2.subdecision {
  font-size: 18px;
  margin-top: 44px;
  color: var(--fg);
  text-transform: none;
  letter-spacing: 0;
  border-top: 2px solid var(--rule);
  padding-top: 20px;
}
```

Each sub-decision picks its own approach-presentation level and its own optional columns
independently -- one might warrant a cards block and a weight column, the next might fit
header-only options with neither. The palette and chrome stay constant; the knobs do not
have to.

See `assets/example-lean.html` for the worked pattern.

## Filename and location

`<topic>-decision.html` in the working directory by default. Examples:

- `cache-storage-decision.html`
- `auth-strategy-decision.html`
- `sync-mechanism-decision.html`

If the matrix lives alongside an ADR or design doc, place it next to that document. If
the user names a directory, use that. Print the absolute path after writing so the user
can open it with `xdg-open <path>` or equivalent.

## Iterating

A decision matrix is not write-once. After the first draft:

- Read each row aloud. Cells that mumble need rewriting.
- Ask: would a reasonable reader pick a different option from this matrix? If yes,
  the Decision needs a stronger argument or the matrix needs another criterion.
- Run the draft against SKILL.md "Common failure modes" -- the all-green row/column,
  over-colouring, weighting-until-favourite-wins, and reverse-engineered-score
  checks all live there.
- When the user resolves an Open Question, work through SKILL.md "Resolving open
  questions".
