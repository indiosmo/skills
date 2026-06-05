# Structuring guidance for model adherence

The full principle set behind this skill. SKILL.md carries the workflow and
the short version; read this when you need the reasoning, the exact format a
retained bad example has to take, or the audit checklist -- especially when
restructuring a whole file rather than adding one rule.

A guidance document here means any file that tells an agent how to write code
(or prose) in a particular style: a set of rules, each usually illustrated by a
"good" example of the idiom you want and sometimes a "bad" example of the
anti-idiom you want avoided. The question this answers is: given that shape, how
do you arrange the parts so the model imitates the good and avoids the bad,
rather than the reverse?

The principles are grounded in the in-context-learning literature. Where the
evidence is strong, the principle is stated as a rule. Where it is suggestive
but not settled for this exact construct -- a labeled anti-idiom snippet sitting
in an agent's context while it edits code -- the principle is stated as the safe
default, and the uncertainty is flagged.

## The core asymmetry

The model imitates demonstrations. Every fluent, plausible snippet in the
context is something the model might pattern-match and emit -- regardless of the
label above it. A "Bad:" header is a weak signal compared to the strong signal
of a complete, idiomatic-looking code block. So a bad example is not free: it
teaches by contrast but it also primes by example, and the priming can win.

This gives a default stance: the good example is the asset, the bad example is a
cost that must earn its place. Lead with the good. Keep a bad example only when
it pays for the risk it carries, and when you keep one, format it the way the
evidence says negatives have to be formatted to help.

## What the evidence supports

The in-context-learning papers that study "negative examples" use the term for
constructs that are not quite a bare anti-idiom snippet (a wrong-but-corrected
answer with an explicit flag; a less-preferred-but-still-valid answer; a valid
example that merely lowers accuracy). So their pro-negative results do not
directly license keeping bare "Bad:" code blocks. What does transfer:

- Unlabeled bad content is indistinguishable from good content to the model. The
  one body of work built around negatives had to add an explicit flag before the
  negatives became usable at all. A bad example with no clear polarity marker is
  just another demonstration to imitate.
- There is an inverted-U on the proportion of negatives. A few flagged,
  corrected negatives can help; past some fraction they add noise and hurt. A
  file that trends toward half bad content sits on the falling side of that
  curve.
- The extra length of negatives is itself a degradation cost, named as such:
  longer context dilutes the signal you care about, independent of content.
- Deliberately low-quality demonstrations reliably underperform a neutral
  baseline, and fluent-but-flawed valid examples drag output toward the flaw.
- Demonstration content has a first-order effect on output -- the shape of
  guidance materially moves what the model produces; it is not noise.

What the evidence does not settle for this construct, and what you should
therefore treat conservatively rather than design around: whether a labeled bad
snippet primes the model to emit that idiom in a code diff; whether a bad-only
file is worse than no examples at all; whether good+bad beats good-only at equal
token budget for code idioms specifically; whether the bare label (no inline
fix) carries enough signal. When you have an eval, let it decide these. When you
do not, prefer the good-only form.

## Principle 1 -- Make the good example load-bearing

The thing you want emitted should be the longest, last, most detailed, and most
self-sufficient part of each rule. A reader who skips every bad block must still
get a complete, imitable specification of the idiom.

- For each rule, cover the good half alone. Does it fully specify the idiom
  without the bad half for contrast? If the rule only makes sense as "not that,"
  rewrite the good half so it stands on its own.
- The good snippet should look complete and runnable -- the exact thing you want
  pattern-matched. No ellipses or `...` in the part that carries the idiom.
- The rule prose should name the idiom positively (what to do), not only
  prohibit (what to avoid). Prohibitions are necessary but they are not
  demonstrations, and the model imitates demonstrations.

## Principle 2 -- If you keep a bad example, format it to help

The only negative formats the literature found beneficial were flagged AND
inline-corrected AND paired AND a minority. A bare labeled bad block is weaker
than any of those. Either upgrade a bad example to that format or drop it.

- Explicit, consistent polarity marker on the block. One exact, reserved token
  (`Bad:`), never a synonym, never ambiguous.
- Immediately adjacent correction. Follow the bad block right away with the good
  version of the same code, so the last thing in the pair is the correct form.
  Never end a rule on a bad block.
- Minimal and a minority. Keep the bad block short -- just enough to show the
  tell. Do not let bad code equal or exceed good code in volume within a rule,
  and do not let the file as a whole trend toward half bad.
- One tell per bad block. A bad block showing three anti-patterns at once
  triples the primable surface and muddies which mistake the rule is about.
  Split them.

Remove on sight: a bad block with no good counterpart in the same rule; a bad
block longer or more detailed than its good counterpart; a rule that ends on the
bad block.

## Principle 3 -- Bound the bad surface; never let it sprawl

Every line of fluent anti-pattern is a line the model might emit. Minimize both
the quantity and the fluency-without-warning of bad code.

- Strip ornamental bad code. If a bad block wraps its one bad line in correct,
  idiomatic scaffolding (good imports, good signatures, good naming), the model
  sees mostly-good code under a bad header -- maximal contamination for minimal
  teaching. Reduce it to the smallest fragment that carries the tell.
- Prefer a diff or a one-line contrast over a full plausible function. A single
  `BAD: X  ->  GOOD: Y` line teaches the tell with almost no primable surface.
- Keep a bad example only where the tell is non-obvious from the good example
  alone. If the good form makes the bad form self-evidently wrong, the bad block
  is pure cost -- drop it.

## Principle 4 -- Map each bad example one-to-one to a named mistake

Maintain a ground-truth list of the specific mistakes the guidance is meant to
prevent (a tells list, a lint catalogue, a "things we keep correcting" log).
Every bad example should map to exactly one item on that list, and every item
the guidance claims to teach should have at most one canonical bad
demonstration.

- Audit both directions: each bad block names a mistake that exists on the list,
  and no single mistake is demonstrated by bad code in three different rules.
  Duplicated anti-pattern demos multiply primable surface without teaching more.
- This mapping is what lets a regression trace back to the example that caused
  it. Keep it explicit -- a stable id or a comment tying the rule to the mistake.
- When you add a rule, add its mistake to the list in the same change, or do not
  add the bad example.

If the project keeps no such list, the tells live implicitly in the rules
themselves; still avoid demonstrating the same mistake with bad code in more
than one rule.

## Principle 5 -- Keep the structure consistent and mechanically separable

Use one fixed shape for every rule so the document can be parsed, split, and
re-derived without hand-editing -- by a tool, by the next agent, or by you six
months later. This is what makes it cheap to produce a good-only variant, to
audit proportions, or to regenerate the file.

- One exact reserved marker per polarity (`Good:` / `Bad:`), never varied -- no
  `Avoid:`, `Anti-pattern:`, `Don't:` synonyms.
- One block per marker, cleanly delimited (a fenced code block immediately under
  the marker). No two polarities sharing a fence. No prose-embedded bad
  one-liners that a split would miss.
- The good half must survive deletion of every bad block intact. After removing
  all bad blocks, the file must still read as complete guidance. Test this: do
  the removal and read the result cold.
- Keep the rule prose independent of which examples are present. If a rule's
  prose leans on a specific example for sense, move that dependency into the
  prose itself or into the good example -- never leave the rule incoherent once a
  bad block is stripped.

## Principle 6 -- Treat ordering and proportion as deliberate levers

- Within a pair, put the good example last by default. Recency favors the last
  demonstration; ending on the good form is the safe choice.
- Hold the bad proportion low and roughly constant across rules. Aim for bad
  blocks to be the short minority within each rule, not half the file.
- Make proportion visible. If you track anything about the file, track
  good-vs-bad volume per rule, so a quality regression can be correlated with bad
  proportion rather than guessed at.

## Principle 7 -- Default to good-only; let evidence override

The structure above is hygiene -- ship it regardless. What it does not do is
pre-decide whether a given bad example should exist at all.

- With no eval to consult, default to good-only. Keep a bad example only where
  its tell is genuinely non-obvious from the good form and you have upgraded it
  to the Principle 2 format. The literature does not measure whether a labeled
  anti-idiom primes emission in a code diff, so do not assume bad examples are
  safe.
- With an eval, wire the decision to measured adherence, not to intuition. If
  good-only matches or beats good+bad at lower token cost, drop the bad halves
  into a separate review doc and ship good-only. If good+bad genuinely wins at
  equal token budget, keep bad examples -- but only in the upgraded format, and
  re-test that the upgraded format is what wins. If the prose alone recovers the
  examples' effect, trim examples hard and invest in the prose.

## Review checklist

For each rule:
1. The good half stands alone and fully specifies the idiom.
2. The rule ends on the good form, not the bad form.
3. The bad block, if present, is shorter than the good block and shows exactly
   one tell.
4. The bad block is immediately corrected by the adjacent good form.
5. The bad block's tell exists on the mistakes list and is not duplicated across
   rules.
6. Markers are the exact reserved tokens; blocks are cleanly fenced and
   machine-separable.
7. Removing all bad blocks leaves valid, complete guidance.
8. The rule prose is coherent independent of which examples are present.

For the file as a whole:
9. Bad code is a minority of total example volume.
10. Good/bad volume is recorded per rule if anything about the file is tracked.
11. Every mistake the file claims to teach has one canonical good (and at most
    one bad) demonstration.

## One-paragraph summary

Make the good example the complete, last, load-bearing element of every rule.
Name the idiom positively in the prose, not just the prohibition. Keep a bad
example only when its tell is non-obvious, and when you keep one, flag it, pair
it, correct it inline, and keep it the short minority -- the only negative format
the evidence found helpful. Bound and de-ornament the bad surface so there is
little fluent anti-pattern to imitate, and map every bad block one-to-one to a
named mistake. Keep one consistent, machine-separable structure so a good-only
variant is derivable without hand-edits. Default to good-only; let an eval, not
intuition, decide whether the bad halves stay.
