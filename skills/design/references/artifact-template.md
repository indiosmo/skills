# Design Brief HTML Artifact

The artifact is a single self-contained HTML file: one `<style>` block in the head, no external CSS, no JavaScript, no CDN dependencies. A reader should be able to open it from disk, email it, or drop it into a shared drive and have it render the same everywhere.

The brief **reuses the [decision-matrix](../../decision-matrix/SKILL.md) skill's palette and chrome**. Read [../../decision-matrix/references/artifact-template.md](../../decision-matrix/references/artifact-template.md) first -- the warm-paper palette, the Assumptions and Open Questions blocks, the matrix table, the cells, the Decision block, and the code-sample block all transfer verbatim. This document covers only what is specific to the design brief.

## Structure

The page reads top to bottom as:

1. **Title and lede** -- one `<h1>` naming the change, followed by a one-paragraph `<p class="lede">`. Two or three sentences: what the change is, why it exists, where it lands. The reader who only reads the lede should know what brief they are holding.
2. **Goal** -- a short `<section class="goal">` with `<h2>Goal</h2>` and either one paragraph or three bullets. The outcome the change must produce, stated as an outcome (not as a list of tasks).
3. **Terminology** (optional) -- a `<section class="terminology">` establishing the shared language the rest of the brief is written in. See "Terminology" below. Omit when the change introduces no term worth pinning down.
4. **Assumptions** (optional) -- the same `.assumptions` block decision-matrix uses. Premises the brief takes as settled. Omit when there are none.
5. **Open Questions** (optional) -- the same `.open-questions` block decision-matrix uses. Questions whose answer would change the design. Omit when there are none.
6. **Requirements** -- a `<section class="requirements">` with `<h2>Requirements</h2>` and a `<ul>` of verifiable requirements.
7. **Impact map** -- a `<section class="impact">` with `<h2>Impact map</h2>` and one sub-section per module touched. See "Impact map" below.
8. **Decision points** -- a `<section class="decisions">` with `<h2>Decision points</h2>` and one `<h3 class="subdecision">` per decision. Each decision either embeds a full matrix (see "Embedded matrices") or carries a one-line trade-off note plus a Decision block when resolved.
9. **Code samples** (optional) -- one or more code-sample blocks (decision-matrix's `.code-samples` chrome) placed under the decision point they support, *not* in a separate section at the end.
10. **Risks and edge cases** (optional) -- a `<section class="risks">` with `<h2>Risks and edge cases</h2>` and a `<ul>` of risks, each citing the `file:line` where the risk lives.

The reader's eye flows: orient (lede, goal), learn the language (Terminology), check premises (Assumptions), see what is in flight (Open Questions), see what the change must do (Requirements), see where it lands (Impact map), see the calls being made (Decision points with embedded matrices), then risks. The order matches a reader's thinking order: outcome -> vocabulary -> shape -> blast radius -> trade-offs -> watch-outs.

Omit any optional section that would be empty. A header with "TBD" underneath is worse than no header.

## The lede

One paragraph, two or three sentences. Names the change in plain language, the user-visible reason it exists, and the part of the codebase it touches. Avoid hedging ("we are considering possibly"), avoid restating the prompt, avoid promising what the artifact contains ("this brief covers...").

Good: "Add OAuth login alongside the existing username/password flow. The change extends `web/auth/` and introduces a new `oauth/` module; existing sessions keep working unchanged."

Bad: "This document explores the OAuth login feature. We will look at requirements, impact, and open questions in turn."

## Goal

The outcome, not the task list. One paragraph or three bullets. If it reads as "implement X, then Y, then Z" it is a plan stub, not a goal -- rewrite as the user-visible outcome.

Good: "Users can sign in with Google or GitHub. Existing username/password users see no change. Admin tooling can audit which identity provider issued a session."

Bad: "Add OAuth provider config, write the callback handler, store provider IDs in the user table."

## Terminology

The shared-language block. It establishes what the domain words in the rest of the brief mean, so requirements and decisions written on top of them inherit one reading, not several. It is the working surface for the language: settled terms that are genuine domain vocabulary promote to `GLOSSARY.md` (the durable home); terms that are only a local clarification for this change stay here.

A `<dl>` of terms. Each `<dt>` is the headword; each `<dd>` is either a one-sentence definition (what the term *is*) or, while still in flight, the ambiguity plus an `.unresolved` flag. Two entry shapes:

- **Settled** -- a one-sentence definition. If the term is already in `GLOSSARY.md`, quote that definition and mark it so the reader knows the durable home holds it.
- **Unresolved** -- the term the change hinges on whose meaning is not yet pinned down, with a one-line note on what is ambiguous (overloaded between two concepts, conflicts with the glossary, undefined). These are the terminology items the interview walks down; as each resolves, replace the flag with a definition.

```html
<section class="terminology">
  <h2>Terminology</h2>
  <dl>
    <dt>Identity provider</dt>
    <dd>The external service (Google, GitHub) that authenticates the user and issues the token the callback exchanges. <span class="glossary-ref">in GLOSSARY.md</span></dd>

    <dt>Session</dt>
    <dd class="unresolved">Unresolved: the glossary defines a session as a server-side auth record, but the OAuth flow also calls the provider's token grant a "session" -- the brief needs one word per concept.</dd>
  </dl>
</section>
```

Style (small additions on top of decision-matrix's base):

```css
.terminology dl { margin: 0; }
.terminology dt { font-weight: 600; font-size: 14px; margin: 12px 0 2px; }
.terminology dd { margin: 0 0 4px; padding-left: 16px; font-size: 14px; }
.terminology dd.unresolved { color: var(--accent); font-style: italic; }
.terminology .glossary-ref { font-size: 12px; color: var(--muted); font-style: italic; }
```

Reuse decision-matrix's `--accent` and `--muted` custom properties; do not introduce new colours. Define a term only when a newcomer to the domain would have to look it up -- a word used in its ordinary English sense does not earn an entry.

## Requirements

A `<ul>` of verifiable statements. Each entry stands alone -- a reader should be able to read one bullet and know what it asserts. Test for verifiability: can someone tell whether the implementation meets this entry by running something or reading something? If no, rewrite.

Group implicitly by topic via order; do not introduce sub-headings unless the list runs past about ten entries. If it does, you may be conflating multiple changes -- consider whether the brief should be split.

## Impact map

The blast-radius view. One `<h3>` per module, followed by a `<ul>` of `<li>` entries. Each entry is either:

- `<code>path/to/file.ts:142</code> -- one-line note on what changes there.
- `<code>path/to/new-file.ts</code> -- new file -- one-line note on what it contains.
- `<code>path/to/module/</code> -- new module -- one-line note on what it contains.

Then a separate `<h3>External dependencies</h3>` sub-section for libraries, frameworks, or services the change introduces or upgrades. Each entry names the dependency and the reason in one line.

Markup:

```html
<section class="impact">
  <h2>Impact map</h2>
  <h3>web/auth</h3>
  <ul>
    <li><code>web/auth/session.ts:142</code> -- add provider-id field to session record</li>
    <li><code>web/auth/middleware.ts:88</code> -- branch on provider when resolving the user</li>
  </ul>
  <h3>oauth (new)</h3>
  <ul>
    <li><code>oauth/google.ts</code> -- new file -- Google OAuth callback handler</li>
    <li><code>oauth/github.ts</code> -- new file -- GitHub OAuth callback handler</li>
  </ul>
  <h3>External dependencies</h3>
  <ul>
    <li><code>oauth-client@2.x</code> -- token exchange and refresh</li>
  </ul>
</section>
```

Style (small additions on top of decision-matrix's base):

```css
.impact h3 { font-size: 13px; text-transform: uppercase; letter-spacing: 0.02em; color: var(--accent); margin: 18px 0 6px; }
.impact ul { margin: 0 0 12px; padding-left: 20px; }
.impact li { margin: 3px 0; font-size: 14px; }
.impact code { font: 12.5px/1.45 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; background: #f3f1ea; padding: 1px 5px; border-radius: 3px; }
```

If the change touches only one module, the impact map can be a single `<ul>` without sub-headings.

## Decision points

Each decision is its own `<h3 class="subdecision">` block. The decision-matrix skill's `h2.subdecision` styling applies; reuse it for `h3.subdecision` with proportional sizing (this section nests one level deeper).

Two shapes per decision, depending on whether the call needs a matrix:

### Shape A: with embedded matrix

Use when two or more options have real trade-offs and the call is non-obvious. The matrix and its Decision block follow the decision-matrix skill's conventions verbatim -- header-only / header-with-subtitle / cards block per "approach presentation knob", neutral cells where the criterion does not discriminate, palette unchanged.

```html
<h3 class="subdecision">Where does the OAuth callback handler live?</h3>
<table>
  <thead><tr><th>Criterion</th><th>web/auth/</th><th>oauth/ (new module)</th></tr></thead>
  <tbody>
    <!-- rows -->
  </tbody>
</table>
<h4 class="decision">Decision</h4>
<p class="decision-body"><b>oauth/.</b> ...</p>
```

Until the user resolves the decision, omit the Decision block. The matrix stands alone with the trade-offs visible; the call gets added during iteration (see SKILL.md "Iterate").

### Shape B: one-line trade-off note

Use when the call is small or obvious enough that a matrix would be theater. One paragraph stating the options and the trade-off; one Decision block when resolved.

```html
<h3 class="subdecision">Token storage encoding</h3>
<p>JSON vs. msgpack for the persisted refresh-token blob. JSON is consistent with the rest of the session schema; msgpack saves ~30% on row size but adds a dependency.</p>
<h4 class="decision">Decision</h4>
<p class="decision-body"><b>JSON.</b> The size saving does not pay back the dependency cost for a column that holds at most a few hundred bytes per user.</p>
```

Use `<h4 class="decision">` (one level smaller than decision-matrix uses for sub-decisions inside a multi-matrix artifact). Reuse decision-matrix's `.decision-body` styling.

### Code samples for a decision point

When a decision turns on call-site ergonomics or API shape, place the code-samples block (decision-matrix's `.code-samples`) immediately under the matrix or under the trade-off note, *before* any Decision block. One snippet per option; keep them small and comparable. See decision-matrix's "Code samples" section for the markup and palette.

## Risks and edge cases

A `<ul>` of risks, each one line, each citing the `file:line` where the risk actually lives (or naming the cross-cutting condition if it has no single home). Order by severity loosely; do not introduce severity tags.

```html
<section class="risks">
  <h2>Risks and edge cases</h2>
  <ul>
    <li>Session reuse across providers: <code>web/auth/session.ts:204</code> conflates provider sessions if the same email is used by both.</li>
    <li>Refresh-token rotation: nothing in the existing flow handles refresh failures; needs an explicit error path.</li>
  </ul>
</section>
```

If risks cluster around a specific decision, consider whether they belong inside that decision's section instead.

## Filename and location

`<topic>-design.html` in the working directory by default. Examples:

- `oauth-login-design.html`
- `cache-migration-design.html`
- `tenant-isolation-design.html`

If the brief lives alongside a ticket or ADR, place it next to that document. If the user names a directory, use that. Print the absolute path after writing so the user can open it with `xdg-open <path>` or equivalent.

## Iterating

A brief is not write-once. See SKILL.md "Interview to resolution" for the mechanics: replace each unresolved Terminology flag with a definition (and promote durable terms to `GLOSSARY.md`), promote answered Open Questions into Assumptions, add the Decision block under each resolved decision-point matrix (and an ADR under `docs/adr/` for a hard-to-reverse call), re-read the impact map and requirements against the new premise, fix anything that drifted. The Assumptions block and the glossary are the audit log; do not silently delete entries.

When every Terminology entry is defined, every Open Question is gone, and every decision point carries a Decision block, the brief is done.
