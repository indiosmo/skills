---
name: add-guidance
description: >-
  Fold a correction you just made into durable agent guidance, in the shape that
  maximizes how reliably the model follows it next time. Use this skill whenever
  you have corrected the agent and want it to get the thing right on the first
  try in a future session -- "add this to the guidelines", "capture this
  correction", "update the cpp guidelines so it stops doing X", "make a rule out
  of this", "/add-guidance". Also use it to restructure an existing
  rules-and-examples guidance file (a coding-standards doc, a style guide, a
  CLAUDE.md / AGENTS.md idioms section, a cpp-agent-examples-style file of
  good/bad pairs) into the adherence-optimized shape: the good example
  load-bearing and last, a bad example kept only where its tell is non-obvious
  and then flagged, paired, corrected, and held to a short minority. Reach for
  this any time you are editing a guidance document made of rules plus good/bad
  examples and you want the agent to actually imitate the good and avoid the bad.
---

# Add guidance

You corrected the agent; now make the correction stick. This skill turns a
one-off correction into a durable rule, written the way that makes a model
actually follow it -- and restructures existing guidance files into that same
shape.

## Why shape matters (read this first)

A guidance file teaches by demonstration. The model imitates the snippets it
sees, and it imitates them whether the label above says `Good:` or `Bad:` -- a
fluent, plausible code block is a strong signal; a one-word polarity header is a
weak one. So a bad example is never free: it teaches by contrast, but it also
primes the very pattern you are trying to suppress, and the priming can win.

That gives the whole skill its bias: **the good example is the asset; a bad
example is a cost that has to earn its place.** Lead with the good form, make it
complete and the last thing the reader sees, and add a `Bad:` block only where
the mistake is genuinely non-obvious from the good form alone. This is the shape
that won the adherence eval this skill is built from. The full reasoning and the
exact format a retained bad example must take live in
[`references/structuring-for-adherence.md`](references/structuring-for-adherence.md)
-- read it before restructuring a whole file, and any time you are unsure
whether a bad example is pulling its weight.

## Two modes

- **Add a correction** (the common case): something just happened in this
  session -- the agent wrote X, you said "no, do it like Y" -- and you want that
  captured. Start at "Add a correction" below.
- **Restructure a file**: take an existing guidance file and re-shape it into
  the adherence-optimized form (the "apply the same refactoring to our
  guidelines" task). Start at "Restructure a file" below.

---

## Add a correction

### 1. Recover the correction, and generalize it

Reconstruct three things from the recent conversation -- ask the user only for
what you genuinely cannot infer:

- **The idiom** -- the form you were corrected *toward*. This becomes the good
  example. State it as a positive: "derive the expected value from the domain,"
  not "stop deriving it from the implementation."
- **The tell** -- the specific, recognizable mistake you made. This is what a
  bad example, if any, would show, and what the rule is meant to catch.
- **The rule it generalizes to.** This is the load-bearing step. The correction
  happened on one file with one set of names, but the guidance will be read a
  thousand times across code you have never seen. Lift the principle out of the
  specifics: a fix to one `OrderId` accessor is really "give each domain field a
  strong type and access it through its named method." If you cannot name a
  general principle, the correction is a one-off preference -- say so and stop
  rather than minting a brittle rule (see "When not to add a rule").

### 2. Find where it belongs

Locate the guidance the project already ships. Look, in order, for: an existing
good/bad-example file (a `*-examples.md`, a coding-standards or style doc), a
rules/idioms section in `CLAUDE.md` / `AGENTS.md`, a `guidelines/` or `docs/`
directory, editor rule files (`.cursor/rules`, `.github/`). Many projects split
**rules prose** (a "context" file) from **examples** (a paired-snippet file); if
so, you will touch both. Confirm the target file with the user when more than one
plausibly fits, or when none exists and you would be creating one.

Then check whether the rule is already there. If an existing rule covers this,
**sharpen that rule** instead of adding a second one -- two rules teaching the
same tell multiply the primable surface without teaching more. Adding is the last
resort, not the first.

### 3. Write the good example and the rule prose

Match the file's existing conventions exactly -- section heading style, the
reserved markers it already uses (`Good:` / `Bad:`), and its placeholder
vocabulary (e.g. `lib::` stand-ins for project types). Do not introduce a synonym
marker like `Avoid:` or `Anti-pattern:` if the file uses `Bad:`.

- Write the **rule prose** as a positive instruction that names the idiom and
  says briefly *why* it holds. The model has good theory of mind; a reason it
  understands beats a bare prohibition it must obey on faith.
- Write the **good example** as the complete, imitable thing you want emitted --
  it should look like real, runnable code in the project's idiom, with no `...`
  in the part that carries the idiom. A reader who sees only this block should be
  able to reproduce the pattern.
- The good example comes first and the rule ends on it.

### 4. Decide whether a bad example earns its place

Default to **no bad example.** Add one only when the tell is not self-evident
from the good form -- when a reader could see the good example and still not
realize the specific trap you fell into. (East vs west const is non-obvious;
"don't leave a TODO" is obvious -- skip it.)

If you do add one, format it the way the evidence says negatives have to be
formatted to help, or it is pure liability:

- **Flagged** with the file's exact `Bad:` marker.
- **Reduced to the tell.** Strip every line of correct scaffolding around the one
  bad line -- a `Bad:` block full of good imports and good signatures is
  mostly-good code under a bad header, maximal contamination for minimal
  teaching. A single `BAD: T const&  ->  GOOD: const T&` contrast often beats a
  whole bad function.
- **One tell only.** If you are tempted to show three mistakes, that is three
  bad examples (or, better, one rule each).
- **Immediately corrected.** Follow the `Bad:` block right away with the `Good:`
  form of the same code, so the pair -- and the rule -- ends on what to write.
- **A short minority.** The bad block must be shorter than its good counterpart,
  and the file as a whole must stay well under half bad.

If the project keeps a tells / lint / "things we keep correcting" list, add this
tell to it in the same change and keep the mapping one-to-one (see Principle 4 in
the reference).

### 5. Verify before you finish

Re-read your edit cold against this checklist:

- The good half stands alone and fully specifies the idiom.
- The rule ends on the good form, not a bad block.
- If a bad block is present: it is shorter than the good block, shows exactly one
  tell, uses the exact reserved marker, and is immediately followed by the
  corrected good form.
- Deleting every bad block from the file would still leave valid, complete
  guidance.
- The rule prose reads coherently whether or not the examples are there.

Then tell the user what you changed and where, and -- briefly -- why you did or
did not add a bad example, so the judgment call is theirs to override.

---

## Restructure a file

Use this when an existing guidance file is in the wrong shape -- typically a
file that is roughly half `Bad:` blocks, ends rules on the bad form, or wraps its
anti-patterns in fluent scaffolding. The goal is to move it to the
adherence-optimized shape without changing what it teaches.

Read [`references/structuring-for-adherence.md`](references/structuring-for-adherence.md)
in full first -- the restructure leans on the whole principle set, not just the
summary. Then, rule by rule:

1. **Lead with the good form** and make it the complete, load-bearing element.
   If the good half only makes sense as "not the bad thing," rewrite it to stand
   on its own.
2. **Re-shape the rule prose** to name the idiom positively, not only to
   prohibit.
3. **Triage each bad block.** Drop it if its tell is self-evident from the good
   form. Keep it only where the tell is non-obvious -- and then reduce it to the
   fragment that carries the tell, ensure it is flagged, immediately corrected,
   and a short minority, and split any block showing more than one tell.
4. **End every rule on the good form.**
5. **Normalize the markers** to one exact reserved token per polarity so the
   file is cleanly machine-separable (a good-only variant should be derivable by
   deleting `Bad:` blocks, with no hand-editing).

Preserve the file's domain vocabulary and the rules' meaning; you are changing
arrangement and proportion, not the standard. When done, run the file-level
checks from the reference: bad code is a clear minority of example volume, every
tell has one canonical demonstration, and removing all bad blocks leaves valid
guidance. Summarize for the user what you dropped, what you kept and why, and the
rough before/after good-vs-bad balance.

---

## When not to add a rule

Push back instead of writing guidance when:

- **It is a one-off, not a principle.** A correction that only makes sense for
  this one file, with no general idiom behind it, will read as noise to a future
  agent and dilute the rules that matter. Name the missing general principle, or
  decline.
- **A rule already covers it.** Sharpen the existing rule; do not add a near
  duplicate. Duplicated demonstrations -- good or bad -- multiply primable
  surface without teaching more.
- **It contradicts an existing rule.** Surface the conflict to the user and
  resolve which wins before editing; do not silently leave two rules pulling in
  opposite directions.

A guidance file is read on every session it loads. Restraint about what goes in
is part of making the things that *are* in it land.

## Worked shape

What a single rule looks like in the target form -- good example first and last,
a bad block only because east-vs-west const is a non-obvious tell, reduced to the
fragment that carries it, immediately corrected:

> ## Const placement
>
> Place `const` to the left of the type (west const) so every declaration reads
> the same way and the qualifier is where readers scan for it.
>
> Good:
> ```cpp
> const order_book& book = session.book();
> ```
>
> East const reads backwards from the rest of the codebase and is easy to miss on
> a pointer.
>
> Bad:
> ```cpp
> order_book const& book = session.book();
> ```
>
> Good:
> ```cpp
> const order_book& book = session.book();
> ```
