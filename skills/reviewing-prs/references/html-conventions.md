# HTML conventions for review artifacts

These conventions describe what **`scripts/render_artifact.py`** produces. They are *not* a checklist for the agent to reimplement -- the renderer owns the visual layer so artifacts stay consistent across runs. If a convention here ever drifts from the script, the script is the source of truth; update the script first.

The agent's job stops at producing the JSON spec. Don't hand-write CSS or diff HTML.

## What the renderer produces

- **Self-contained single HTML file**, no build step.
- **Warm light palette** for page chrome: ivory background, slate text, gray-300 borders, serif headings. Designed to read like a document, not a marketing page.
- **Dark slate diff canvas** (`#141413`) with cream code text (`#E8E6DC`) and **transparent rgba add/del row backgrounds** (olive 18% on add, rust 18% on del). The low-contrast tint reads cleanly without the harsh red/green of typical dark-mode diffs.
- **Server-side diff rendering** -- the script parses unified diff text and emits structured `<div class="diff-row [add|del|ctx|hunk]">` rows with line-number / mark / code spans. No `diff2html`, no `highlight.js`, no client-side parsing. The diff comes out the same on every run.
- **Wide page** (1100px max content width, comfortable on big monitors; collapses gracefully below 720px).
- **Collapsible file panels.** Files at risk `worth-a-look` / `needs-attention`, or with any `blocking` / `important` annotation, render as full open cards (diff + comments). All other files render as one-line `<details>` summaries with an optional `note_md` body when expanded.
- **Bubble-style annotations** anchored to the diff: white card on a tinted gray-150 strip, with a CSS triangle pointing at the diff and a 4px left border in the severity accent color.
- **Risk-map chips** at the top of a review, each linking to its file panel. Anchor clicks briefly highlight the destination card.
- **"Suggested next steps" checklist** in a card at the bottom of a review, as `<ul>` of `<input type="checkbox">` items (visual only -- not persisted).
- **Mermaid diagrams** loaded only when the spec carries `diagrams`. CDN: `mermaid@10` ESM bundle, neutral theme.

## Palette

| Token | Value | Use |
|-------|-------|-----|
| `--ivory` | `#FAF9F5` | page background |
| `--slate` | `#141413` | h1/h2/h3, diff canvas |
| `--clay` | `#D97757` | blocking accent, risk `needs-attention` |
| `--oat` | `#E3DACC` | risk `worth-a-look` background |
| `--olive` | `#788C5D` | additions, praise, safe |
| `--rust` | `#B04A3F` | deletions |
| `--gray-150` | `#F0EEE6` | comments strip, inline code background |
| `--gray-300` | `#D1CFC5` | borders |
| `--gray-500` | `#87867F` | muted text, line numbers |
| `--gray-700` | `#3D3D3A` | body text |

Don't introduce other colors. Don't gradient, glow, or animate (the only motion is a 1.4s highlight ring on anchor click).

## Severity / risk vocabulary

Fixed. The validator rejects anything else.

- **Severities**: `blocking`, `important`, `nit`, `praise`.
- **File risks**: `safe`, `worth-a-look`, `needs-attention`.

Each severity drives the bubble's left border, triangle, and label color. Each risk drives the file-card pill color and whether the panel renders open or collapsed.

## CDN dependencies

Just Mermaid, and only when the spec carries diagrams:

| Asset | URL |
|-------|-----|
| Mermaid (ESM) | `https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs` |

Everything else is inline -- CSS, the diff rows, the scroll-highlight JS. The artifact survives a network outage as long as it didn't use Mermaid.

## Spec input

Print the example for the shape you need:

```bash
python3 scripts/render_artifact.py --print-schema review
python3 scripts/render_artifact.py --print-schema writeup
python3 scripts/render_artifact.py --print-schema understanding
```

Key invariants:

- Every spec has `kind` and `title`.
- For `review`: each file under `files[]` carries `path`, `risk`, `added`, `removed`. If the file is open (risk worth-a-look or higher, or any blocking/important annotation), it also carries `diff` (the raw `git diff` text) and optional `annotations[]`. If collapsed, it carries an optional `note_md` rendered when the user expands the row.
- Every annotation carries `severity` and `body_md`; line numbers go in `line`.
- Markdown fields (`*_md`) accept: paragraphs, `- ` / `* ` lists, inline `` `code` ``, `**bold**`, `*italic*`, `[link](url)`. Anything more elaborate (headings, tables) belongs in a structured field.

## Mermaid

Validate every diagram with `mmdc` before saving the spec. The renderer embeds whatever you put in `diagrams[].body`; a broken diagram still renders as a blank slot. Use the [mermaid skill](../../mermaid/SKILL.md) for syntax + validation helpers.

## Printability

- `@media print` flips the diff canvas to white-on-black-text with very light add/del tints, so a PDF print stays legible.
- All cards have `page-break-inside: avoid`.
- Sticky behavior: none. Nothing overlaps in print.

## Extending the renderer

If a real eval surfaces a missing visual capability (a new section type, an additional risk level, a different diff layout), modify `scripts/render_artifact.py`. Don't ship workaround HTML inside specs. Workarounds are how this skill regresses on the "one source of truth" property.
