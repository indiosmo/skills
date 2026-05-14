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
2. **Approach presentation** -- inline in the table headers, optionally with a cards block
   (`.approaches`) above the matrix for options that need a paragraph of detail. See
   "Approach presentation knob" below.
3. **The matrix** -- a `<table>` with columns: Criterion, (optional) Weight, one column
   per option, (optional) Notes. An optional `<tfoot>` row carries the weighted score.
4. **Interpretation** -- a `.recommendation` block with `<h2>Interpretation</h2>` and
   two to four short paragraphs in the user's voice. Highlighted background so it stands
   out.
5. **Open Questions** -- an `.open-questions` block with `<h2>Open Questions</h2>` and a
   `<ul>` of questions whose answers would change the interpretation.

The reader's eye flows: orient (lede), see the candidates (headers or cards), compare
(matrix), read the take (Interpretation), see what would change it (Open Questions).

## Palette and chrome

A warm-paper palette with restrained colour. Reuse the CSS variables verbatim:

```css
--bg: #fafaf7;          /* page background */
--fg: #1a1a1a;          /* body text */
--muted: #6b6b6b;       /* lede, helper text, notes */
--rule: #d8d6cf;        /* table and card borders */
--accent: #6b5b3a;      /* section heading color */
--highlight: #fff6d6;   /* recommendation block background */

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

### Number of option columns

Three or four is the sweet spot for most decisions. Two collapses into pros-and-cons; six
or more dilutes attention and the later columns get sloppy. If you have many candidates,
consider whether some are variants of the same approach and can be merged with a
footnote.

Keep cell prose to one or two sentences. If a cell needs three sentences, it is either
mixing two criteria (split the row) or burying a caveat (state the trade-off directly).

## The Interpretation block

Two to four short paragraphs in a highlighted box, written in the user's voice. Use
`<b>` tags to anchor the eye on the key claims:

```html
<div class="recommendation">
  <h2>Interpretation</h2>
  <p>
    <b>Option B is the weakest</b> despite winning on [criterion]. The two killers are
    [criterion 1] and [criterion 2].
  </p>
  <p>
    <b>Options A and D are the strong options.</b> [Why A is fine for now; what D buys
    if conditions change.]
  </p>
  <p>
    <b>Option C is overkill</b> unless [specific condition]. [Why the matrix rejects it.]
  </p>
  <p style="margin-bottom: 0;">
    <b>Leaning toward:</b> [option] for now; revisit [other option] when [trigger
    condition].
  </p>
</div>
```

Use **bold leads** to make the block scannable. The reader who only reads the bold text
should still come away with the position.

The final paragraph names the leaning option with a trigger condition for revisiting.
Decision matrices are most useful when they include the "when to revisit" clause -- that
is what makes them durable artifacts rather than one-time analyses.

The block reads as the user's own synthesis of their own matrix. Use "the matrix points
toward...", "the killer for B is...", "leaning toward..." -- not "I recommend...", "you
should pick...".

## The Open Questions block

An `.open-questions` block with a bullet list of questions. Each question should be a
thing whose answer would change the interpretation. Bold the question lead so it scans:

```html
<div class="open-questions">
  <h2>Open Questions</h2>
  <ul>
    <li><b>Question?</b> Why it matters / what answer would flip the call.</li>
    ...
  </ul>
</div>
```

Three to five questions is typical. Fewer suggests overconfidence; more suggests the
matrix ran ahead of the research. Phrase as questions the user is still working through,
not as questions Claude is asking the user.

## Content rules

- **No marketing language.** "Robust", "scalable", "elegant" are not specifications.
  Replace with the concrete property.
- **Specific over generic.** "Breaks on any host that does not have `/home/msi/...`"
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
2. `<h2 class="subdecision">` for sub-decision 1, optionally followed by its cards block,
   then its matrix table.
3. `<h2 class="subdecision">` for sub-decision 2, optionally followed by its cards block,
   then its matrix table.
4. (Repeat as needed; cap at three sub-decisions per artifact.)
5. One Interpretation block that addresses all sub-decisions and the order in which to
   commit.
6. One Open Questions block.

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
- Scan each column for all-green. A column with no yellow and no red means you are
  rationalizing or missing a criterion the approach fails on. Real options have trade-offs;
  if you cannot find one, ask what someone who dislikes the option would say.
- Scan each row for all-green. A row with no discrimination is a wasted row; cut it or
  sharpen the criterion.
- Scan the whole matrix for over-colouring. If more than ~60% of cells are coloured, you
  are over-grading -- look for cells whose verdict is mild and pull them back to neutral.
- If scoring is on, check the weighted score against your intuition. Mismatch means the
  cells or weights are off, not that the score is wrong.
- Ask: would a reasonable reader pick a different option from this matrix? If yes, the
  Interpretation needs a stronger argument or the matrix needs another criterion.

When the user pushes back on the interpretation, do not re-tune weights to match. Either
add a criterion the user is implicitly weighting, or update a cell whose verdict was too
generous. The matrix should reflect the conversation, not paper over it.
