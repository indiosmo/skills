#!/usr/bin/env python3
"""Render a review / writeup / code-understanding artifact from a JSON spec.

The spec is a JSON document that describes the artifact at a structural level
(metadata, files, annotations, suggestions, prose sections). The script glues
the spec into a self-contained HTML page. Visual choices (warm palette,
diff row template, bubble annotations, collapsible file panels) live in this
script so artifacts stay consistent across runs.

Usage:
    render_artifact.py --spec spec.json --output review.html
    render_artifact.py --spec - --output - < spec.json > review.html
    render_artifact.py --print-schema review   # print an example spec

Stdlib-only.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------- #
# CDN dependencies. Only Mermaid; diffs are rendered server-side.
# --------------------------------------------------------------------------- #

MERMAID_JS = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"

# --------------------------------------------------------------------------- #
# Severity / risk vocabulary. Fixed -- adding more dilutes the signal.
# --------------------------------------------------------------------------- #

SEVERITIES = {"blocking", "important", "nit", "praise"}
RISKS = {"safe", "worth-a-look", "needs-attention"}
OPEN_BY_DEFAULT_RISKS = {"worth-a-look", "needs-attention"}
OPEN_BY_DEFAULT_SEVERITIES = {"blocking", "important"}

RISK_LABELS = {
    "safe": "safe",
    "worth-a-look": "worth a look",
    "needs-attention": "needs attention",
}


def should_open(file_entry: dict[str, Any]) -> bool:
    """A file panel opens by default when the risk warrants it or any
    annotation is blocking/important. Safe panels stay collapsed."""
    if file_entry.get("risk") in OPEN_BY_DEFAULT_RISKS:
        return True
    for ann in file_entry.get("annotations", []):
        if ann.get("severity") in OPEN_BY_DEFAULT_SEVERITIES:
            return True
    return False


# --------------------------------------------------------------------------- #
# Markdown subset. Inline code, bold, italics, links, paragraph + bullet
# lists. Anything more elaborate belongs in a structured spec field.
# --------------------------------------------------------------------------- #

_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def render_inline_md(text: str) -> str:
    escaped = html.escape(text)
    escaped = _INLINE_CODE_RE.sub(r"<code>\1</code>", escaped)
    escaped = _BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = _ITALIC_RE.sub(r"<em>\1</em>", escaped)
    escaped = _LINK_RE.sub(r'<a href="\2">\1</a>', escaped)
    return escaped


def render_block_md(text: str) -> str:
    if not text:
        return ""
    out: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith(("- ", "* ")):
            items: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(("- ", "* ")):
                items.append(render_inline_md(lines[i].strip()[2:]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>")
            continue
        para: list[str] = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(("- ", "* ")):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{render_inline_md(' '.join(para))}</p>")
    return "".join(out)


# --------------------------------------------------------------------------- #
# Diff renderer. Server-side: parses unified diff, emits the .diff-row
# template adapted from the PR #247 reference artifact. The HTML shape:
#
#   <div class="diff">
#     <div class="diff-row hunk"><span class="ln"></span><span class="mark"></span>
#       <span class="code">@@ -A,B +C,D @@ optional context</span>
#     </div>
#     <div class="diff-row [add|del|ctx]">
#       <span class="ln">N</span><span class="mark">[+|-| ]</span><span class="code">...</span>
#     </div>
#     ...
#   </div>
#
# Line numbers reflect the post-change file for + and context rows; original
# file numbers for - rows. The hunk header's @@ counters drive both gutters.
# --------------------------------------------------------------------------- #


def parse_unified_diff(diff_text: str) -> list[dict[str, Any]]:
    """Return a list of {kind, old_ln, new_ln, mark, code} rows."""
    rows: list[dict[str, Any]] = []
    old_ln = 0
    new_ln = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff ") or raw.startswith("index ") or raw.startswith("similarity "):
            continue
        if raw.startswith("---") or raw.startswith("+++"):
            continue
        if raw.startswith("@@"):
            m = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@(.*)", raw)
            if m:
                old_ln = int(m.group(1))
                new_ln = int(m.group(2))
            rows.append({"kind": "hunk", "code": raw})
            continue
        if not raw:
            continue
        marker = raw[0]
        body = raw[1:] if len(raw) > 0 else ""
        if marker == "+":
            rows.append({"kind": "add", "new_ln": new_ln, "mark": "+", "code": body})
            new_ln += 1
        elif marker == "-":
            rows.append({"kind": "del", "old_ln": old_ln, "mark": "-", "code": body})
            old_ln += 1
        elif marker == " ":
            rows.append({"kind": "ctx", "old_ln": old_ln, "new_ln": new_ln, "mark": " ", "code": body})
            old_ln += 1
            new_ln += 1
        elif marker == "\\":
            # "\ No newline at end of file"
            rows.append({"kind": "hunk", "code": raw})
    return rows


def render_diff_rows(diff_text: str) -> str:
    if not diff_text.strip():
        return '<div class="diff empty">No diff content.</div>'
    rows = parse_unified_diff(diff_text)
    parts: list[str] = ['<div class="diff">']
    for row in rows:
        kind = row["kind"]
        if kind == "hunk":
            parts.append(
                '<div class="diff-row hunk">'
                '<span class="ln"></span><span class="mark"></span>'
                f'<span class="code">{html.escape(row["code"])}</span>'
                '</div>'
            )
        elif kind == "ctx":
            parts.append(
                '<div class="diff-row ctx">'
                f'<span class="ln">{row["new_ln"]}</span>'
                '<span class="mark"> </span>'
                f'<span class="code">{html.escape(row["code"])}</span>'
                '</div>'
            )
        elif kind == "add":
            parts.append(
                '<div class="diff-row add">'
                f'<span class="ln">{row["new_ln"]}</span>'
                '<span class="mark">+</span>'
                f'<span class="code">{html.escape(row["code"])}</span>'
                '</div>'
            )
        elif kind == "del":
            parts.append(
                '<div class="diff-row del">'
                f'<span class="ln">{row["old_ln"]}</span>'
                '<span class="mark">-</span>'
                f'<span class="code">{html.escape(row["code"])}</span>'
                '</div>'
            )
    parts.append("</div>")
    return "".join(parts)


# --------------------------------------------------------------------------- #
# Component renderers.
# --------------------------------------------------------------------------- #


def slugify(path: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-")


def render_header(spec: dict[str, Any]) -> str:
    title = html.escape(spec.get("title", "Review"))
    head = spec.get("head", {})
    base = spec.get("base", {})
    stats = spec.get("stats", {})
    repo_line = spec.get("repo_line", "")

    parts: list[str] = ['<header class="page-header">']
    if repo_line:
        parts.append(f'<div class="repo-line">{html.escape(repo_line)}</div>')
    parts.append(f'<h1>{title}</h1>')

    meta_bits: list[str] = []
    if base and head:
        meta_bits.append(
            f'<span class="branch">'
            f'{html.escape(head.get("ref", "?"))} '
            f'<span class="arrow">&rarr;</span> '
            f'{html.escape(base.get("ref", "?"))}'
            f'</span>'
        )
    if stats:
        meta_bits.append(
            '<span class="stat">'
            f'<span class="add">+{stats.get("insertions", 0)}</span> / '
            f'<span class="del">&minus;{stats.get("deletions", 0)}</span>'
            f' <span class="files">{stats.get("files", 0)} files changed</span>'
            '</span>'
        )
    if meta_bits:
        parts.append(f'<div class="meta-row">{" ".join(meta_bits)}</div>')

    commits = spec.get("commits") or []
    if commits:
        rows = []
        for c in commits:
            rows.append(
                '<tr>'
                f'<td class="mono">{html.escape(c.get("sha", "")[:7])}</td>'
                f'<td>{html.escape(c.get("author", ""))}</td>'
                f'<td>{html.escape(c.get("date", ""))}</td>'
                f'<td>{html.escape(c.get("subject", ""))}</td>'
                '</tr>'
            )
        parts.append(
            '<details class="commits">'
            '<summary>Commits</summary>'
            f'<table>{"".join(rows)}</table>'
            '</details>'
        )
    parts.append('</header>')
    return "".join(parts)


def render_risk_map(files: list[dict[str, Any]]) -> str:
    if not files:
        return ""
    chips = []
    for f in files:
        risk = f.get("risk", "safe")
        path = f.get("path", "")
        slug = slugify(path)
        label = path.rsplit("/", 1)[-1]
        chips.append(
            f'<a class="chip {risk}" href="#file-{slug}" title="{html.escape(path)}">'
            f'<span class="dot"></span>{html.escape(label)}</a>'
        )
    legend = (
        '<div class="legend">'
        '<span><span class="dot safe-dot"></span> safe</span>'
        '<span><span class="dot medium-dot"></span> worth a look</span>'
        '<span><span class="dot attention-dot"></span> needs attention</span>'
        '</div>'
    )
    return (
        '<section id="risk-map"><h2>Risk map</h2>'
        '<div class="risk-map">' + "".join(chips) + '</div>' + legend + '</section>'
    )


def render_summary(spec: dict[str, Any]) -> str:
    body = spec.get("summary_md", "")
    if not body:
        return ""
    return f'<section id="summary" class="prose"><h2>Summary</h2>{render_block_md(body)}</section>'


def render_file_card(file_entry: dict[str, Any]) -> str:
    """Every file is a collapsible <details>. Open by default when risk is
    worth-a-look/needs-attention or any annotation is blocking/important;
    closed by default otherwise. The body is the same regardless: an optional
    one-paragraph note, the diff if present, and any annotations."""
    path = file_entry.get("path", "")
    slug = slugify(path)
    risk = file_entry.get("risk", "safe")
    added = file_entry.get("added", 0)
    removed = file_entry.get("removed", 0)
    open_attr = " open" if should_open(file_entry) else ""

    summary = (
        '<summary>'
        f'<span class="file-path">{html.escape(path)}</span>'
        '<span class="file-summary-right">'
        f'<span class="risk-tag {risk}">{RISK_LABELS[risk]}</span>'
        f'<span class="file-delta"><span class="add">+{added}</span> '
        f'<span class="del">&minus;{removed}</span></span>'
        '<span class="chevron"></span>'
        '</span>'
        '</summary>'
    )

    body_parts: list[str] = []
    note = file_entry.get("note_md") or ""
    if note:
        body_parts.append(f'<div class="file-note">{render_block_md(note)}</div>')

    diff_text = file_entry.get("diff") or ""
    if diff_text.strip():
        body_parts.append(render_diff_rows(diff_text))

    annotations = file_entry.get("annotations") or []
    if annotations:
        bubbles = []
        for ann in annotations:
            sev = ann.get("severity", "nit")
            line = ann.get("line")
            line_label = f"line {line}" if line is not None else ""
            bubbles.append(
                f'<div class="bubble {sev}">'
                f'<div class="anchor">{html.escape(line_label)}</div>'
                f'<div class="bubble-body">'
                f'<span class="label">{sev.upper()}</span>'
                f'{render_block_md(ann.get("body_md", ""))}'
                '</div>'
                '</div>'
            )
        body_parts.append('<div class="comments">' + "".join(bubbles) + "</div>")

    if not body_parts:
        body_parts.append('<div class="file-note muted">No diff, annotations, or note for this file.</div>')

    return (
        f'<details class="file-card" id="file-{slug}"{open_attr}>'
        f'{summary}'
        f'<div class="file-body">{"".join(body_parts)}</div>'
        '</details>'
    )


def render_files(files: list[dict[str, Any]]) -> str:
    if not files:
        return ""
    # Order: open cards first (so reviewer's eye lands on them), then collapsed.
    open_files = [f for f in files if should_open(f)]
    collapsed_files = [f for f in files if not should_open(f)]
    ordered = open_files + collapsed_files
    panels = "".join(render_file_card(f) for f in ordered)
    return f'<section id="files"><h2>Files</h2>{panels}</section>'


def render_suggestions(spec: dict[str, Any]) -> str:
    items = spec.get("suggestions") or []
    if not items:
        return ""
    lis = "".join(
        f'<li>'
        f'<input type="checkbox" id="step-{i}">'
        f'<label for="step-{i}">{render_inline_md(item)}</label>'
        '</li>'
        for i, item in enumerate(items)
    )
    return (
        '<footer class="next-steps" id="suggestions">'
        '<h2>Suggested next steps</h2>'
        f'<ul class="checklist">{lis}</ul>'
        '</footer>'
    )


def render_section_md(spec: dict[str, Any], key: str, anchor: str, heading: str) -> str:
    body = spec.get(key)
    if not body:
        return ""
    return f'<section id="{anchor}" class="prose"><h2>{html.escape(heading)}</h2>{render_block_md(body)}</section>'


def render_mermaid_blocks(spec: dict[str, Any]) -> str:
    diagrams = spec.get("diagrams") or []
    if not diagrams:
        return ""
    blocks = []
    for d in diagrams:
        caption = d.get("caption", "")
        body = d.get("body", "")
        cap_html = f'<figcaption>{render_inline_md(caption)}</figcaption>' if caption else ""
        blocks.append(
            '<figure class="diagram">'
            f'<pre class="mermaid">{html.escape(body)}</pre>'
            f'{cap_html}</figure>'
        )
    return '<section id="diagrams"><h2>Diagrams</h2>' + "".join(blocks) + "</section>"


# --------------------------------------------------------------------------- #
# Kind dispatch.
# --------------------------------------------------------------------------- #


def render_review_body(spec: dict[str, Any]) -> str:
    parts = [
        render_header(spec),
        render_summary(spec),
        render_risk_map(spec.get("files", [])),
        render_files(spec.get("files", [])),
        render_suggestions(spec),
    ]
    return "".join(parts)


def render_writeup_body(spec: dict[str, Any]) -> str:
    parts = [render_header(spec)]
    parts.append(render_section_md(spec, "tldr_md", "tldr", "TL;DR"))
    parts.append(render_section_md(spec, "why_md", "why", "Why"))
    if spec.get("files"):
        items = []
        for f in spec["files"]:
            path = f.get("path", "")
            slug = slugify(path)
            note = f.get("note_md", "")
            open_attr = " open" if f.get("open") else ""
            items.append(
                f'<details class="file-note" id="file-{slug}"{open_attr}>'
                f'<summary><span class="file-path">{html.escape(path)}</span></summary>'
                f'<div class="body">{render_block_md(note)}</div>'
                '</details>'
            )
        parts.append(f'<section id="file-tour"><h2>File tour</h2>{"".join(items)}</section>')
    parts.append(render_section_md(spec, "focus_areas_md", "focus", "Focus areas"))
    parts.append(render_section_md(spec, "test_plan_md", "test-plan", "Test plan"))
    parts.append(render_section_md(spec, "rollout_md", "rollout", "Rollout / migration"))
    return "".join(parts)


def render_understanding_body(spec: dict[str, Any]) -> str:
    parts = [render_header(spec)]
    parts.append(render_section_md(spec, "intro_md", "intro", "Intro"))
    parts.append(render_mermaid_blocks(spec))
    parts.append(render_section_md(spec, "walkthrough_md", "walkthrough", "Walkthrough"))
    if spec.get("key_files"):
        items = "".join(
            f'<li><code>{html.escape(f.get("path", ""))}</code>'
            f' &mdash; {render_inline_md(f.get("role", ""))}</li>'
            for f in spec["key_files"]
        )
        parts.append(f'<section id="key-files" class="prose"><h2>Key files</h2><ul>{items}</ul></section>')
    parts.append(render_section_md(spec, "gotchas_md", "gotchas", "Gotchas"))
    return "".join(parts)


KIND_RENDERERS = {
    "review": render_review_body,
    "writeup": render_writeup_body,
    "understanding": render_understanding_body,
}


# --------------------------------------------------------------------------- #
# Page shell. CSS adapted from the PR #247 reference artifact: warm palette
# (ivory page, slate diff canvas, olive/rust accents), serif headings, mono
# diff, low-contrast transparent backgrounds for add/del rows.
# --------------------------------------------------------------------------- #


PAGE_CSS = """
:root {
  --ivory: #FAF9F5;
  --slate: #141413;
  --clay: #D97757;
  --oat: #E3DACC;
  --olive: #788C5D;
  --rust: #B04A3F;
  --gray-150: #F0EEE6;
  --gray-300: #D1CFC5;
  --gray-500: #87867F;
  --gray-700: #3D3D3A;
  --serif: ui-serif, Georgia, 'Times New Roman', serif;
  --sans: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --mono: ui-monospace, 'SF Mono', Menlo, Monaco, 'Liberation Mono', monospace;
  --max-w: 1100px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background: var(--ivory);
  color: var(--gray-700);
  font-family: var(--sans);
  font-size: 15px;
  line-height: 1.6;
  padding: 48px 24px 80px;
}
.page { max-width: var(--max-w); margin: 0 auto; }

a { color: var(--gray-700); text-decoration: underline; text-decoration-color: var(--gray-300); }
a:hover { color: var(--slate); text-decoration-color: var(--gray-500); }

/* ---------- Header ---------- */
header.page-header {
  border: 1.5px solid var(--gray-300);
  border-radius: 12px;
  padding: 28px 32px;
  background: #fff;
  margin-bottom: 36px;
}
.repo-line {
  font-family: var(--mono);
  font-size: 12.5px;
  color: var(--gray-500);
  letter-spacing: 0.01em;
  margin-bottom: 10px;
}
h1 {
  font-family: var(--serif);
  font-weight: 500;
  font-size: 30px;
  line-height: 1.25;
  color: var(--slate);
  margin-bottom: 18px;
}
.meta-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}
.branch {
  font-family: var(--mono);
  font-size: 12.5px;
  color: var(--gray-700);
  background: var(--gray-150);
  border: 1.5px solid var(--gray-300);
  border-radius: 8px;
  padding: 6px 10px;
}
.branch .arrow { color: var(--gray-500); margin: 0 6px; }
.stat { font-family: var(--mono); font-size: 13px; }
.stat .add { color: var(--olive); font-weight: 600; }
.stat .del { color: var(--rust); font-weight: 600; }
.stat .files { color: var(--gray-500); margin-left: 10px; }

details.commits { margin-top: 16px; }
details.commits summary {
  cursor: pointer;
  color: var(--gray-500);
  font-size: 12.5px;
  font-family: var(--mono);
}
details.commits table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  font-size: 13px;
  font-family: var(--mono);
}
details.commits td {
  padding: 4px 12px 4px 0;
  border-bottom: 1px solid var(--gray-150);
  color: var(--gray-700);
}
details.commits td:first-child { color: var(--gray-500); }

/* ---------- Sections ---------- */
section { margin-bottom: 40px; scroll-margin-top: 20px; }
h2 {
  font-family: var(--serif);
  font-weight: 500;
  font-size: 21px;
  color: var(--slate);
  margin-bottom: 14px;
}
h3 {
  font-family: var(--sans);
  font-weight: 600;
  font-size: 15px;
  color: var(--slate);
  margin: 18px 0 8px;
}
.prose p { margin-bottom: 10px; }
.prose ul { list-style: none; padding: 0; }
.prose li {
  position: relative;
  padding-left: 22px;
  margin-bottom: 10px;
}
.prose li::before {
  content: "";
  position: absolute;
  left: 4px;
  top: 9px;
  width: 6px;
  height: 6px;
  background: var(--gray-500);
  border-radius: 2px;
}
.prose code, .bubble code, .checklist code, .body code, .file-path code, details.commits code {
  font-family: var(--mono);
  font-size: 12.5px;
  background: var(--gray-150);
  padding: 1px 5px;
  border-radius: 4px;
}

/* ---------- Risk map ---------- */
.risk-map { display: flex; flex-wrap: wrap; gap: 10px; }
.chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1.5px solid var(--gray-300);
  font-family: var(--mono);
  font-size: 12.5px;
  color: var(--slate);
  text-decoration: none;
  background: #fff;
  transition: transform 0.12s ease;
}
.chip:hover { transform: translateY(-1px); text-decoration: none; }
.chip .dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }
.chip.safe { background: rgba(120,140,93,0.10); border-color: rgba(120,140,93,0.45); }
.chip.safe .dot { background: var(--olive); }
.chip.worth-a-look { background: var(--oat); }
.chip.worth-a-look .dot { background: #B89B6E; }
.chip.needs-attention { background: rgba(217,119,87,0.12); border-color: rgba(217,119,87,0.55); }
.chip.needs-attention .dot { background: var(--clay); }

.legend {
  margin-top: 12px;
  font-size: 12px;
  color: var(--gray-500);
  display: flex;
  gap: 18px;
  flex-wrap: wrap;
}
.legend span { display: inline-flex; align-items: center; gap: 6px; }
.legend .dot { width: 8px; height: 8px; border-radius: 50%; }
.legend .safe-dot { background: var(--olive); }
.legend .medium-dot { background: #B89B6E; }
.legend .attention-dot { background: var(--clay); }

/* ---------- File cards (collapsible) ---------- */
details.file-card {
  border: 1.5px solid var(--gray-300);
  border-radius: 12px;
  background: #fff;
  margin-bottom: 16px;
  overflow: hidden;
  scroll-margin-top: 20px;
}
details.file-card > summary {
  list-style: none;
  cursor: pointer;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border-bottom: 1.5px solid transparent;
}
details.file-card[open] > summary {
  border-bottom-color: var(--gray-150);
}
details.file-card > summary::-webkit-details-marker { display: none; }
.file-path {
  font-family: var(--mono);
  font-size: 13.5px;
  color: var(--slate);
}
.file-summary-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.file-delta { font-family: var(--mono); font-size: 12px; color: var(--gray-500); }
.file-delta .add { color: var(--olive); }
.file-delta .del { color: var(--rust); }
.chevron {
  width: 14px;
  height: 14px;
  display: inline-block;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><path d='M3.5 6l4.5 4.5L12.5 6' stroke='%2387867F' stroke-width='1.6' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg>");
  background-repeat: no-repeat;
  background-position: center;
  transition: transform 0.15s ease;
  flex-shrink: 0;
}
details.file-card[open] .chevron { transform: rotate(180deg); }
.file-body { display: flex; flex-direction: column; }
.file-note {
  padding: 14px 20px;
  font-size: 13.5px;
  color: var(--gray-700);
}
.file-note.muted { color: var(--gray-500); font-style: italic; }
.file-note p { margin-bottom: 8px; }
.file-note p:last-child { margin-bottom: 0; }

.risk-tag {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 600;
}
.risk-tag.safe { background: rgba(120,140,93,0.15); color: var(--olive); }
.risk-tag.worth-a-look { background: var(--oat); color: #7A6A4F; }
.risk-tag.needs-attention { background: rgba(217,119,87,0.15); color: var(--clay); }

/* ---------- Diff block ---------- */
.diff {
  background: var(--slate);
  font-family: var(--mono);
  font-size: 12.5px;
  line-height: 1.7;
  overflow-x: auto;
}
.diff.empty {
  color: var(--gray-500);
  padding: 16px 20px;
  font-style: italic;
}
.diff-row {
  display: grid;
  grid-template-columns: 56px 22px 1fr;
  align-items: baseline;
  padding: 0 14px 0 0;
  white-space: pre;
}
.diff-row .ln {
  text-align: right;
  padding-right: 14px;
  color: var(--gray-500);
  user-select: none;
}
.diff-row .mark {
  text-align: center;
  color: var(--gray-500);
}
.diff-row .code { color: #E8E6DC; }
.diff-row.ctx .code { color: #B8B6AC; }
.diff-row.add { background: rgba(120,140,93,0.18); }
.diff-row.add .mark { color: var(--olive); }
.diff-row.del { background: rgba(176,74,63,0.18); }
.diff-row.del .mark { color: var(--rust); }
.diff-row.hunk {
  background: rgba(255,255,255,0.04);
  color: var(--gray-500);
  padding: 4px 14px 4px 0;
}
.diff-row.hunk .code { color: var(--gray-500); }

/* ---------- Review comments ---------- */
.comments {
  padding: 18px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  background: var(--gray-150);
}
.bubble {
  position: relative;
  background: #fff;
  border: 1.5px solid var(--gray-300);
  border-left-width: 4px;
  border-radius: 8px;
  padding: 12px 14px 12px 16px;
  max-width: 760px;
}
.bubble.blocking { border-left-color: var(--clay); }
.bubble.important { border-left-color: #B89B6E; }
.bubble.nit { border-left-color: var(--gray-300); }
.bubble.praise { border-left-color: var(--olive); }
.bubble::before {
  content: "";
  position: absolute;
  left: -9px;
  top: 16px;
  width: 12px;
  height: 12px;
  background: #fff;
  border-left: 1.5px solid var(--gray-300);
  border-bottom: 1.5px solid var(--gray-300);
  transform: rotate(45deg);
}
.bubble.blocking::before { border-left-color: var(--clay); border-bottom-color: var(--clay); }
.bubble.important::before { border-left-color: #B89B6E; border-bottom-color: #B89B6E; }
.bubble.praise::before { border-left-color: var(--olive); border-bottom-color: var(--olive); }
.bubble .anchor {
  font-family: var(--mono);
  font-size: 11.5px;
  color: var(--gray-500);
  margin-bottom: 4px;
}
.bubble .label {
  display: inline-block;
  font-size: 10.5px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 700;
  margin-right: 8px;
}
.bubble.blocking .label { color: var(--clay); }
.bubble.important .label { color: #B89B6E; }
.bubble.nit .label { color: var(--gray-500); }
.bubble.praise .label { color: var(--olive); }
.bubble-body p { font-size: 13.5px; color: var(--gray-700); margin: 0; display: inline; }
.bubble-body p + p { display: block; margin-top: 8px; }
.bubble-body ul { margin-top: 8px; }

/* ---------- Writeup file-tour ---------- */
details.file-note {
  border: 1.5px solid var(--gray-300);
  border-radius: 12px;
  background: #fff;
  margin-bottom: 14px;
}
details.file-note summary {
  list-style: none;
  cursor: pointer;
  padding: 14px 20px;
  font-family: var(--mono);
  font-size: 13.5px;
  color: var(--slate);
}
details.file-note summary::-webkit-details-marker { display: none; }
details.file-note summary::after {
  content: "+";
  font-family: var(--mono);
  color: var(--gray-500);
  font-size: 16px;
  margin-left: 6px;
  float: right;
}
details.file-note[open] summary::after { content: "−"; }
details.file-note .body { padding: 0 20px 16px; }

/* ---------- Footer / next steps ---------- */
footer.next-steps {
  border: 1.5px solid var(--gray-300);
  border-radius: 12px;
  background: #fff;
  padding: 24px 28px;
}
.checklist { list-style: none; padding: 0; }
.checklist li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 8px 0;
}
.checklist input[type="checkbox"] {
  width: 17px;
  height: 17px;
  margin-top: 2px;
  accent-color: var(--olive);
  cursor: pointer;
  flex-shrink: 0;
}
.checklist label { cursor: pointer; flex: 1; }

/* ---------- Diagrams ---------- */
figure.diagram {
  margin: 16px 0;
  padding: 20px;
  background: #fff;
  border: 1.5px solid var(--gray-300);
  border-radius: 12px;
}
figure.diagram figcaption {
  color: var(--gray-500);
  font-size: 12.5px;
  margin-top: 10px;
  text-align: center;
  font-family: var(--sans);
}
.mermaid { text-align: center; }

/* ---------- Responsive ---------- */
@media (max-width: 720px) {
  body { padding: 24px 12px 60px; }
  header.page-header { padding: 20px; }
  details.file-card > summary, .comments, .file-note { padding: 14px; }
  .diff-row { grid-template-columns: 42px 18px 1fr; font-size: 12px; }
}

/* ---------- Print ---------- */
@media print {
  body { background: #fff; }
  details { page-break-inside: avoid; }
  .diff { background: #fff; color: #000; }
  .diff-row .code { color: #000; }
  .diff-row.ctx .code { color: #444; }
  .diff-row.add { background: #eaf3df; }
  .diff-row.del { background: #f7d7d3; }
  .diff-row.add .mark, .diff-row.del .mark { color: #000; }
}
"""


SCROLL_HIGHLIGHT_JS = r"""
document.querySelectorAll('.risk-map a, .chip').forEach(function (a) {
  a.addEventListener('click', function () {
    var target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    target.style.transition = 'box-shadow 180ms ease';
    target.style.boxShadow = '0 0 0 3px rgba(217,119,87,0.35)';
    setTimeout(function () { target.style.boxShadow = 'none'; }, 1400);
    if (target.tagName === 'DETAILS') target.open = true;
  });
});
"""


MERMAID_INIT = """
<script type="module">
  import mermaid from '%MERMAID_JS%';
  mermaid.initialize({ startOnLoad: true, theme: 'neutral', securityLevel: 'loose' });
</script>
""".replace("%MERMAID_JS%", MERMAID_JS)


def render_page(spec: dict[str, Any]) -> str:
    kind = spec.get("kind")
    if kind not in KIND_RENDERERS:
        raise ValueError(f"unknown kind: {kind!r}. expected one of {sorted(KIND_RENDERERS)}")
    body_html = KIND_RENDERERS[kind](spec)
    has_mermaid = bool(spec.get("diagrams"))

    head_parts = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<title>{html.escape(spec.get("title", "Review"))}</title>',
        f'<style>{PAGE_CSS}</style>',
    ]

    foot_parts = [f'<script>{SCROLL_HIGHLIGHT_JS}</script>']
    if has_mermaid:
        foot_parts.append(MERMAID_INIT)

    return (
        '<!doctype html><html lang="en"><head>'
        + "".join(head_parts)
        + '</head><body><main class="page">'
        + body_html
        + '</main>'
        + "".join(foot_parts)
        + '</body></html>'
    )


# --------------------------------------------------------------------------- #
# Spec validation.
# --------------------------------------------------------------------------- #


def validate_spec(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    kind = spec.get("kind")
    if kind not in KIND_RENDERERS:
        errors.append(f"kind must be one of {sorted(KIND_RENDERERS)}; got {kind!r}")
        return errors
    if not spec.get("title"):
        errors.append("title is required")
    if kind == "review":
        for i, f in enumerate(spec.get("files", [])):
            where = f"files[{i}] ({f.get('path', '?')})"
            if not f.get("path"):
                errors.append(f"{where}: path is required")
            if f.get("risk") and f["risk"] not in RISKS:
                errors.append(f"{where}: risk must be one of {sorted(RISKS)}; got {f['risk']!r}")
            for j, ann in enumerate(f.get("annotations", [])):
                if ann.get("severity") not in SEVERITIES:
                    errors.append(
                        f"{where}.annotations[{j}]: severity must be one of "
                        f"{sorted(SEVERITIES)}; got {ann.get('severity')!r}"
                    )
    return errors


# --------------------------------------------------------------------------- #
# Example specs.
# --------------------------------------------------------------------------- #


EXAMPLE_REVIEW_SPEC = {
    "kind": "review",
    "title": "Add optimistic updates to task list mutations",
    "repo_line": "example-app/web · Pull Request #247",
    "head": {"ref": "feature/optimistic-tasks", "sha": "a1b2c3d4"},
    "base": {"ref": "main", "sha": "e5f6a7b8"},
    "stats": {"files": 6, "insertions": 142, "deletions": 38},
    "commits": [
        {"sha": "a1b2c3d", "author": "Alex Example", "date": "2026-05-10",
         "subject": "Add optimistic updates to task list"}
    ],
    "summary_md": (
        "- Replaces the await-then-refetch pattern in `TaskList` with optimistic cache writes, "
        "so toggling or reordering a task feels instant instead of waiting ~300ms for the round-trip.\n"
        "- Introduces a small `useOptimisticTasks` hook that wraps the mutation, snapshots the "
        "previous list, and rolls back on error.\n"
        "- Extends the API client to accept an idempotency key per mutation and adds a toast when "
        "a rollback fires."
    ),
    "files": [
        {
            "path": "src/hooks/useOptimisticTasks.ts",
            "risk": "needs-attention",
            "added": 58,
            "removed": 0,
            "diff": "@@ -0,0 +1,20 @@\n"
                    "+import { useMutation, useQueryClient } from '@tanstack/react-query';\n"
                    "+import { updateTask, TaskPatch } from '../api/tasks';\n"
                    "+import type { Task } from '../types/task';\n"
                    "+\n"
                    "+export function useOptimisticTasks(boardId: string) {\n"
                    "+  const qc = useQueryClient();\n"
                    "+  const key = ['tasks', boardId];\n"
                    "+\n"
                    "+  return useMutation({\n"
                    "+    mutationFn: (patch: TaskPatch) => updateTask(patch),\n"
                    "+    onMutate: async (patch) => {\n"
                    "+      const prev = qc.getQueryData<Task[]>(key);\n"
                    "+      qc.setQueryData<Task[]>(key, (old = []) =>\n"
                    "+        old.map(t => t.id === patch.id ? { ...t, ...patch } : t)\n"
                    "+      );\n"
                    "+      return { prev };\n"
                    "+    },\n"
                    "+    onError: (_e, _p, ctx) => qc.setQueryData(key, ctx?.prev),\n"
                    "+  });\n"
                    "+}\n",
            "annotations": [
                {"line": 11, "severity": "blocking",
                 "body_md": "`onMutate` doesn't call `qc.cancelQueries(key)` first. If a background "
                            "refetch lands between the optimistic write and the server response, it "
                            "will clobber the optimistic state and the UI will flicker back to the old value."},
                {"line": 18, "severity": "nit",
                 "body_md": "Rollback restores the list but never surfaces the error. Consider wiring "
                            "the existing `pushToast` here so users know the toggle didn't stick."}
            ]
        },
        {
            "path": "src/components/Toast.tsx",
            "risk": "safe",
            "added": 14,
            "removed": 2,
            "diff": "",
            "note_md": "Adds a `variant=\"warning\"` style and exports `pushToast`. Purely additive, "
                       "no behaviour change for existing call sites."
        },
        {
            "path": "src/types/task.ts",
            "risk": "safe",
            "added": 6,
            "removed": 2,
            "diff": "",
            "note_md": "Widens `Task.status` to include `\"archived\"` and adds an optional "
                       "`updatedAt` timestamp. Type-only change."
        }
    ],
    "suggestions": [
        "Add `await qc.cancelQueries(key)` at the top of `onMutate` in `useOptimisticTasks.ts`.",
        "Move idempotency-key generation into the mutation context so retries reuse the same key.",
        "Either consume `isPending` in `TaskRow` or remove it from the destructure to keep lint clean."
    ]
}


EXAMPLE_WRITEUP_SPEC = {
    "kind": "writeup",
    "title": "Writeup: feat/optimistic-tasks",
    "head": {"ref": "feat/optimistic-tasks", "sha": "a1b2c3d4"},
    "base": {"ref": "main", "sha": "e5f6a7b8"},
    "stats": {"files": 5, "insertions": 91, "deletions": 12},
    "tldr_md": "Task toggles now feel instant. The list updates before the server confirms; "
               "if the request fails we roll back.",
    "why_md": "Users on slow networks were tapping a task and watching it sit in 'pending' for "
              "a second or more. Optimistic updates remove that latency.",
    "files": [
        {"path": "src/hooks/useOptimisticTasks.ts",
         "note_md": "New mutation hook. Wraps `updateTask` with optimistic cache writes and "
                    "automatic rollback on error.",
         "open": True}
    ],
    "focus_areas_md": "- The cache-key contract -- if you rename the query key, both the mutation "
                      "and the components reading the list must agree.\n"
                      "- Error path: failing the request rolls back but doesn't toast.",
    "test_plan_md": "- Toggle a task offline -- it should snap back when the request errors.\n"
                    "- Toggle rapidly twice -- both should settle to the latest server value.",
    "rollout_md": "Ship behind the `optimistic_tasks` flag, on for staff for one day, then 10% rollout."
}


EXAMPLE_UNDERSTANDING_SPEC = {
    "kind": "understanding",
    "title": "How a task toggle flows through the app",
    "intro_md": "A click on a task row travels through three layers: the React component, "
                "the mutation hook, and the API client. This artifact walks each step.",
    "diagrams": [
        {"caption": "Request path on success",
         "body": "flowchart LR\n  Click[TaskRow click] --> Hook[useOptimisticTasks]\n"
                 "  Hook --> Cache[(React Query cache)]\n  Hook --> API[updateTask]\n"
                 "  API --> Server[(REST endpoint)]\n  Server --> Hook"}
    ],
    "walkthrough_md": "1. Component fires -- `TaskRow` calls `toggle(id)`.\n"
                      "2. Hook writes -- `useOptimisticTasks.onMutate` snapshots the cache and "
                      "applies the optimistic patch.\n"
                      "3. API call -- `updateTask` sends a PATCH with the new state.\n"
                      "4. Settle -- on success, the server response replaces the optimistic "
                      "value; on error, the snapshot is restored.",
    "key_files": [
        {"path": "src/hooks/useOptimisticTasks.ts", "role": "mutation hook"},
        {"path": "src/api/tasks.ts", "role": "REST client"},
        {"path": "src/components/TaskList.tsx", "role": "consumer"}
    ],
    "gotchas_md": "- The cache key is `['tasks', boardId]` -- changing it anywhere requires "
                  "changing it everywhere.\n"
                  "- `onMutate` must call `cancelQueries` first or a background refetch will "
                  "clobber the optimistic write."
}


EXAMPLES = {
    "review": EXAMPLE_REVIEW_SPEC,
    "writeup": EXAMPLE_WRITEUP_SPEC,
    "understanding": EXAMPLE_UNDERSTANDING_SPEC,
}


# --------------------------------------------------------------------------- #
# CLI.
# --------------------------------------------------------------------------- #


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a review artifact from a JSON spec.")
    parser.add_argument("--spec", help="Path to JSON spec, or '-' for stdin.")
    parser.add_argument("--output", help="Path to output HTML, or '-' for stdout.")
    parser.add_argument("--print-schema", choices=sorted(EXAMPLES),
                        help="Print an example spec for the given kind and exit.")
    parser.add_argument("--validate-only", action="store_true",
                        help="Validate the spec and print errors; do not render.")
    args = parser.parse_args(argv)

    if args.print_schema:
        print(json.dumps(EXAMPLES[args.print_schema], indent=2))
        return 0

    if not args.spec:
        parser.error("--spec is required (or use --print-schema)")

    spec_text = sys.stdin.read() if args.spec == "-" else Path(args.spec).read_text()

    try:
        spec = json.loads(spec_text)
    except json.JSONDecodeError as exc:
        print(f"spec is not valid JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate_spec(spec)
    if errors:
        print("spec validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 2

    if args.validate_only:
        print("spec is valid.")
        return 0

    html_out = render_page(spec)
    if not args.output or args.output == "-":
        sys.stdout.write(html_out)
    else:
        Path(args.output).write_text(html_out)
        print(f"wrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
