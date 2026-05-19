---
name: decision-matrix
description: Compare options across criteria and produce a single-file HTML decision-matrix artifact.
---

# Decision Matrix

A decision matrix is a small table -- options across the top, criteria down the side, a short
verdict in each cell -- whose purpose is **not** to compute the right answer. Its purpose is to
make a design conversation possible. Once the alternatives are named and the criteria are
named, disagreement has somewhere to land: on a specific cell, on a missing option, on a
weight, on a criterion the matrix forgot. Without the matrix, "I think we should use X" and "I
think we should use Y" pass each other in the dark.

This skill covers two things: the **concepts** -- what goes where and why -- and the
**artifact** -- a single self-contained HTML page that renders the matrix and the
decision in a form you can share and revisit.

## When to reach for this

Use a decision matrix when:

- Two or more options plausibly work and the right one is not obvious.
- The choice is reversible only at meaningful cost -- worth thinking about before committing.
- You are in the research, design, or planning phase, before any code is written.
- The user is weighing libraries, storage strategies, schemas, sync mechanisms, architectures,
  deployment targets, protocols, repo layouts, or anything where "it depends" is the honest
  first answer.

Skip the matrix when:

- One option clearly dominates after a minute of thought. Say so and move on.
- The decision is binary and uncontroversial (yes/no toggles, single-bit flags).
- The decision is so cheap to reverse that prototyping beats analyzing.

When in doubt, draft the matrix anyway. If a dominant option emerges three rows in, stop and
say so -- the time spent is small and the audit trail is worth keeping.

## The Hickey framing

Rich Hickey's argument in "Design in Practice" is that programmers reach for implementation too
early and treat the choice of approach as a tactical detail rather than the design itself. The
matrix is a forcing function against that habit. It compels you to:

- **Name more than one option.** A single-option "design" is a decision dressed as a fact.
- **Name the criteria you care about.** Vague preferences ("simpler", "better") get reduced to
  specific properties the cell can speak to.
- **Score each option against each criterion explicitly.** No option gets a free pass on its
  weakness; no option gets dismissed without a stated reason.
- **Record the rationale.** Six months later, "we picked X because of Y" survives staff
  turnover, your own forgetting, and the temptation to re-litigate the call from scratch.

The matrix is a thinking tool, then an artifact. The artifact only earns its keep if the
thinking was honest.

## Anatomy

Every matrix has the same parts. Get each one right and the artifact mostly writes itself.

### Options (columns)

Three or four options is the sweet spot. Two is too binary -- it collapses into a
pros-and-cons list and loses the comparative power. Six or more dilutes attention and the
later columns get sloppy.

**Include the status quo.** If the user is currently doing X, "keep doing X" is an option.
Skipping it hides the cost of change. In the bundled example, `assets/example.html`, "A. Copy
(current)" is the first column for exactly this reason.

**Include at least one option you suspect will lose.** A matrix where every option is a
contender is suspicious -- you have likely pre-filtered. An option that fails badly in the
matrix is still useful: it documents *why* the obvious-sounding alternative does not work.

Name options short and specific (`Postgres`, `Git submodule`, `WebSocket`), not vague
(`a database`, `version control`, `a messaging layer`).

### Criteria (rows)

Criteria are the properties of an option that matter for this decision. Pick them by asking
"what would make me regret a choice?" -- regret modes are criteria.

Good criteria are:

- **Project-specific.** Generic criteria like "simplicity" or "quality" do not differentiate.
  Replace with the actual concern: "clone / CI experience", "blast radius of an edit",
  "reproducibility on a fresh laptop".
- **Discriminating.** A criterion every option scores equally on is wasted real estate. Cut it
  or replace it with a sharper version.
- **Phrased as a property of the option.** "Path portability" works; "Is it portable?" works
  less well -- cells read more cleanly when the criterion names an attribute.
- **A mix of axes.** Correctness, ergonomics, performance, reversibility, blast radius,
  maintenance cost, coupling, testability, security, repo size, setup cost. Lean toward axes
  the team has been burned on before.

Five to ten criteria is typical. Fewer than four and the matrix looks unconvincing; more than
twelve and the reader stops reading.

### Approach presentation (three levels)

Each option needs enough description that a reader can tell what it is without scrolling
back. There are three levels of presentation; use the lowest one that does the job.

1. **Header only.** The option name in the `<th>` is self-evident -- `Postgres`,
   `WebSocket`, `git submodule`. No subtitle, no card.
2. **Header with subtitle.** A one-line `opt-sub` underneath the option name inside the
   `<th>`. Use when the name alone is ambiguous and one line of context resolves it. For
   "Throttle Próprio com reserva de Cancel" the subtitle "Separa X% do throttle para
   cancelamentos." is enough. This is the `assets/example-lean.html` shape.
3. **Header plus a cards block above the matrix.** A `.approaches` grid (one card per
   option) before the table, with a paragraph of detail per option. Use only when a
   one-line subtitle does not fit and the option needs a real description. When the cards
   block is present, the headers carry just the option name -- do not duplicate the
   description as a subtitle. This is the `assets/example.html` shape.

Mixing levels within a single matrix is rare and usually a sign you have not picked the
right level. Mixing levels across sub-decisions in a multi-decision artifact is fine --
each sub-decision picks the level its options actually need.

### Cells

Each cell carries a **verdict** and a **short reasoning** of one or two sentences. The
background colour carries the verdict; the cell body carries the reasoning. There is no
inline verdict tag -- the colour does that work alone.

The palette (from Rich Hickey's "Design in Practice" talk):

- **Green** (`td.good`): an *appealing aspect* -- the option clearly handles the criterion
  well. A scanning eye reads green as "this is a reason to pick this option".
- **Yellow** (`td.ok`): a *not-so-great aspect* -- the option handles the criterion, but
  with caveats or with effort worth knowing about. Yellow means "requires consideration",
  not "fine".
- **Red** (`td.bad`): a *blocker aspect* -- a serious concern, a real cost against this
  option. A reader scanning the column should see red as a stop signal.
- **No colour** (no class): a *neutral aspect* -- the option neither shines nor stumbles
  on this criterion; the cell is informational only. **Most cells should land here.**
- **Italic grey** (`td.na`): the criterion does not apply to this option. Distinct from
  neutral -- na is "this question is meaningless here", neutral is "the answer doesn't
  swing the decision either way".

**Default to no colour.** A useful matrix typically colours only 30-50% of its cells --
the ones that genuinely discriminate. When every cell is green, yellow, or red, the
colour stops carrying signal: the eye has nowhere to land and the verdicts blur into
wallpaper. Neutral cells exist precisely to give the coloured cells contrast. A row where
three options all "handle it fine" and one fails is read more clearly with one red cell
and three neutral cells than with three green cells and one red one.

The criterion column itself uses a distinct warm background (`td.criterion`) to separate
the row label from the data cells.

Cells should be specific, not generic. "Breaks on any host that does not have
`/home/msi/...`. CI, sandboxes, fresh laptop -- all see a dangling link." beats "not
portable". A cell can be very short ("Yes", "Ok", "Not supported") when the criterion is
binary -- but make sure the colour still carries the verdict.

**Unknowns.** For an aspect you cannot grade concretely yet, leave the cell uncoloured
and put a literal "?" at the start of the cell prose -- for example, "? Not measured;
likely similar to subtree but never benchmarked." Do not introduce a new colour for
unknown; the "?" signals the gap, the absence of colour signals "no verdict", and the
question goes into the Open Questions block. A cell with no concrete content at all is a
signal you do not yet understand the option well enough to compare it -- research the gap
or mark it "?", but do not paper over it with a generic adjective.

Avoid burying caveats in adjectives ("mostly works", "somewhat painful"). If something is
mixed, say what the mix is.

### Notes column (optional)

A right-hand `notes` column carries cross-cutting commentary on a criterion -- observations
that apply to all options or to none of them, caveats about the criterion itself, related
constraints. Off by default. Turn it on only when you have something genuinely
cross-cutting to say on most rows; if the column would be mostly empty, drop it. If every
row has a notes entry, the column is probably restating things that belong in the
criterion's label.

### Score and weight columns (optional)

**Off by default. Omit both unless the user explicitly asks for scoring.** The cell
colours and the Decision prose already carry the answer; adding numbers without a
reason makes the matrix look more authoritative than it is.

Turn scoring on only when:

- The user explicitly asks for a score, weighted score, or numeric ranking.
- The decision is contentious enough that a summary statistic helps anchor against
  intuition. Use the gap between the score and your gut as a diagnostic: if they agree,
  you have a clean call; if they disagree, either the cells, the weights, or your
  intuition is wrong -- figure out which.

When scoring is on, **two pieces of numeric information** appear on the matrix:

- **Score (1-5) per cell.** Each cell carries a small badge with its score: 5 = clearly
  appealing, 3 = neutral or mixed, 1 = a real blocker. The score should match the cell's
  colour band -- 4-5 reads as green territory, 3 as yellow or no-colour, 1-2 as red. For
  unknown cells, leave the score off and put "?" in the prose.
- **Weight column for criteria.** A "Wt" column at the left holds each criterion's
  weight. **Defaults to 1 across all rows** -- the user can edit individual weights to
  reflect what actually matters. Use the same 1-5 range as the cell score, where 5 means
  "this criterion could dominate the decision" and 1 means "nice to have, would not flip
  the call alone".

A `<tfoot>` row sums `sum(score * weight)` per option. Label the footer "tune weights to
taste" so the reader knows the number is commentary rather than a verdict.

Scoring is a *thinking* aid more than a *computing* aid; two people who agree on the
matrix can still disagree on weights, and that disagreement is itself a useful signal. If
the score and the colours tell the same story, the score is redundant -- pull it back
off. If they disagree, that disagreement is the artifact's most interesting output.

### Decision

A short prose section -- two to four short paragraphs -- that records the call. Title the
block **"Decision"** (not "Interpretation", not "Recommendation", not "My read").

Structure each Decision block as:

1. **State the decision.** First sentence names the chosen option and emphasises it
   visually (`<b>` on the option name or a leading "Decision: " bold). The reader who
   only reads one line should come away with the choice.
2. **State the reasoning.** One or two sentences naming the criteria that made the call.
   Point at specific rows of the matrix; do not restate the cell prose.
3. **Considerations for discarding the other options** -- only when not obvious from the
   matrix. A sentence per option that genuinely tempted: what it would have bought, what
   would have to change for it to flip the call. Skip this for options the matrix already
   ruled out clearly.

Phrase the prose as a direct statement of the decision and its grounds. Do not write
"the matrix points me toward X", "the killer for B is...", or other user-voice framings
-- the reader knows the matrix is right above; the Decision block records the call, not
a reading of the table. Equally, do not write "I recommend X" or "you should pick X" --
the artifact records a decision the user has made, not advice being handed to them.

Render the block as a plain heading followed by paragraphs. Do **not** wrap it in a
highlighted box or coloured panel. The emphasis is carried by the bold lead on the
chosen option, not by chrome around the block.

### Assumptions

A short list of premises the matrix takes as settled -- scope decisions, environmental
facts, committed tooling choices -- that constrain the design space the matrix explores.
Examples: "The graded build copies only `submission/`", "Catch2 is the committed test
framework", "There is no second C/C++ consumer outside this directory."

The block exists to make the matrix's inputs visible. A reader who disputes the call
can check whether they actually disagree with the matrix or with one of its premises.
It is also where resolved open questions go to live (see "Resolving open questions"
below): when the user pins down an answer the matrix was treating as uncertain, the
answer belongs here, not buried inside cell prose.

Title this block **"Assumptions"**. Phrase each entry as a settled premise on its own
terms -- e.g. "Library count: at least four (a utils library plus order routing,
market data, and matching engine) and one application." Do not phrase the entry as a
question with the answer tacked on, and do not append a matrix-level consequence: the
matrix is evaluated against the assumptions, never the reverse. When an assumption
bears on a specific verdict, reference it from the cell or the Decision block where
it actually decides something ("B's faithfulness to the grader holds because the
pipeline copies only `submission/`"); the assumption itself stays neutral.

Omit the block entirely when there are no significant premises to surface. Three to
five entries is typical when present; more than seven suggests the matrix is doing too
much.

### Open Questions

A short list of things that would change the decision if answered differently. These
are the assumptions the matrix smuggled in -- surface them so they stay live while the
decision is in flight. Examples: "How often does this actually change?", "Is there
another consumer to account for?", "Are we optimizing for cold-start or steady-state?"

Title this block **"Open Questions"** (not "Open questions for you"). Phrase as questions
the user is still working through, not as questions Claude is putting to the user.

Both Assumptions and Open Questions render **above** the matrix tables, immediately under
the lede. A reader should see what the matrix takes as given and what is still in flight
before reading the comparison that depends on them. As questions get resolved in
conversation, promote them into Assumptions -- see "Resolving open questions" below.

## Multi-decision artifacts

A single research question often contains two or three smaller decisions that are coupled
but distinct. Rather than build separate artifacts for each, stack them in one HTML
document: one `<h2>` heading per sub-decision, with its own option cards (optional) and its
own matrix table, in the order the reader will think about them.

For example, "How should we represent contract sizes on aggregates?" can resolve into two
matrices stacked in one artifact:

1. *How do we model the size?* -- options: add a ratio column to group members vs. use a
   contract multiplier.
2. *Where do we apply the multiplier?* -- options: pass the adjusted quantity in the
   request vs. apply inside the gateway vs. pass the multiplier in the request.

The second decision only makes sense once the first is chosen. Stacking makes that
sequencing explicit. Each sub-decision carries its own Decision block immediately under
its matrix -- the reader reads the matrix, sees the call, and moves on to the next
sub-decision. Avoid a single combined "decisions" block at the end of the artifact; it
forces the reader to scroll back to match calls to matrices. See
`assets/example-lean.html` for the pattern.

Each sub-decision picks its own approach-presentation level and its own optional columns
independently -- one sub-decision might need the cards block while another fits header-only
options, and one might warrant a weight column while another does not. Visual consistency
(same palette, same chrome) matters; matching every knob across sub-decisions does not.

Limit a single artifact to two or three coupled sub-decisions. More than that, the document
loses focus -- split into separate artifacts and link between them.

## Workflow

### 1. Confirm the decision is worth a matrix

Ask: are there really multiple viable options here, or is the user looking for permission to
pick the obvious one? A two-line answer is better than a forced four-column matrix.

If only one option is plausible, say so directly. The skill is opt-in; not every design
question is a decision-matrix question.

### 2. Brainstorm options, including the status quo and a likely-loser

Draft three or four options in plain text in the conversation first. Sanity-check coverage
before committing to a layout:

- Is the current approach represented?
- Is there an option a reader might assume but that this decision rules out?
- Are the options at the same level of abstraction? (Comparing "Postgres" to "key-value
  storage" is a category error; pick "Postgres" vs "DynamoDB" vs "Redis" or "relational" vs
  "key-value" vs "document" -- not a mix.)

### 3. Draft criteria from the regret modes

For each option, ask: "If we picked this, what would we regret in six months?" Each distinct
regret becomes a candidate criterion. Then prune: drop any criterion that every option scores
the same on, and any criterion whose distinction the user does not actually care about for
this project.

### 4. Score the cells before writing the decision

Fill in verdicts and short reasoning for every cell before writing the Decision prose.
This order matters. Writing the Decision first invites the matrix to be
reverse-engineered to support it; filling in cells first lets the matrix surprise you.

If filling in a cell forces you to add a criterion you had not thought of, add it. If it
forces you to drop or merge an option, do that too. The first pass is exploratory; the matrix
is allowed to change shape.

### 5. Write the decision

Once cells are stable, write the Decision block in plain prose. State the chosen option
in the first sentence and emphasise it. Follow with one or two sentences of reasoning
that point at the criteria that decided the call. If an alternative genuinely tempted,
add one sentence on what would have flipped it. Do not phrase the block as a reading of
the matrix ("the matrix points me toward...") or as outside advice ("I recommend...") --
state the decision directly.

If scoring is on (see "Score and weight columns"), sum each column and note where the
score and your intuition disagree -- that gap is information. Either the weights are
wrong, the verdicts are wrong, or your intuition is wrong; figure out which. If neither
the agreement nor the disagreement is informative, the score is doing no work -- pull
it back off.

### 6. List assumptions and open questions

Skim the cells for premises: "the team is one person", "the grader copies only X", "we
already have a CI cluster", "this rarely changes". Settled premises go in the
**Assumptions** block; unverified premises whose answer would flip the call go in the
**Open Questions** block. See the "Assumptions" and "Open Questions" sections under
Anatomy for the phrasing rules.

### 7. Produce the HTML artifact

Generate a single self-contained HTML file from the matrix. See
[references/artifact-template.md](references/artifact-template.md) for structure, styling
conventions, and content rules. Two reference files ship with the skill:

- [assets/example.html](assets/example.html) -- a worked example with the optional knobs
  turned on: cards block above the table, score (1-5) per cell, weight column, weighted
  score footer, notes column on the right.
- [assets/example-lean.html](assets/example-lean.html) -- a worked example with the
  optional knobs turned off: option headers with subtitles, no scoring, no weights, no
  notes column, two stacked matrices for a multi-decision artifact. Also demonstrates
  the "?" convention for an unknown cell.

Copy whichever is closer to the knob configuration you need, then adapt the title,
options, criteria, cells, Decision, Assumptions, and Open Questions to the current
decision. The two files share the same palette and chrome -- the difference is which
knobs are on.

Save the file as `<topic>-decision.html` (e.g. `cache-storage-decision.html`,
`sync-mechanism-decision.html`) in the working directory, or wherever the user asks.
Print the absolute path so the user can open it.

### 8. Surface the decision in chat

After writing the file, give the user a two- or three-line summary in chat: the chosen
option, the main reason, and the most important open question. The HTML is for reviewing
and keeping; the chat summary is for the immediate response.

## Resolving open questions

A decision matrix is rarely settled on the first pass. The Open Questions block names
the premises the matrix could not pin down: assumptions about scope, environmental
facts, or tooling commitments whose answers would change the call. When the user
resolves one in conversation, update the artifact rather than letting the answer live
only in chat.

The mechanics:

1. **Promote the answer into the Assumptions block** (using the phrasing rules in
   the Assumptions section above). Remove it from Open Questions.
2. **Re-read the matrix against the new assumption.** If the answer narrows the
   design space, some cells may be wrong, some criteria may become irrelevant, an
   option may even drop out. Adjust the cells, not the decision -- the matrix still
   has to support the call honestly.
3. **Update the Decision block if the resolution actually changed something.** If a
   sub-decision's call would have flipped under the previous uncertainty, say so:
   "with X resolved as Y, the call stands but by a narrower margin; Z is now the
   clean fallback." The Decision block is where you name the assumption that did the
   deciding. If the resolution confirmed the existing call cleanly, leave the block
   alone.
4. **Leave a trail.** The Assumptions entry is the audit log -- a reader who comes
   back six months later should be able to tell which premises shaped the matrix.
   Do not silently delete criteria or options that became irrelevant; the cells or
   the Decision block should make the consequence visible where it actually applies.

Avoid these mistakes:

- **Stuffing the answer into the matrix without surfacing it.** A reader who only
  sees the matrix should still be able to tell which premises it depends on. Hidden
  assumptions are why decisions get re-litigated.
- **Re-tuning weights or cells to preserve the original call.** If a resolution
  would flip the decision, let it flip. The matrix lies if it papers over the
  change.
- **Leaving the open question on the list once answered.** Promotion is mandatory --
  an entry in Open Questions is, by definition, still open.

## Common failure modes

- **Two-column matrices.** Almost always a sign the third option was prematurely filtered.
  Force yourself to name at least one more before committing to a two-option comparison. If
  there really are only two, a pros-and-cons list may serve better than a matrix.
- **Generic criteria.** "Simplicity", "performance", "quality" without further specification.
  Replace with the project-specific property the criterion is gesturing at.
- **An all-green row.** The criterion does not discriminate between options. Cut it or
  replace it with a sharper version.
- **An all-green column.** You are almost certainly rationalizing, or you have not
  considered a criterion where this approach genuinely falters. Every real option has
  trade-offs; a column with no yellow and no red is a column that has not been
  cross-examined. Ask: "what would someone who hates this approach say?" -- their answer
  is the missing criterion.
- **Colouring every cell.** When every cell is green, yellow, or red, the colour stops
  carrying signal -- the eye has nowhere to land. Leave neutral cells uncoloured so the
  verdict cells stand out. If you cannot find a single neutral cell across the whole
  matrix, you are over-grading.
- **Reverse-engineered scores.** If you wrote the Decision first and then filled in
  cells to match, the artifact lies. Fill in cells first.
- **Weighting until your favorite wins.** Weights are tunable, but tuning them after seeing
  the score is intellectual sleight of hand. Set weights from the criteria themselves --
  "this matters more because [concrete reason]" -- not from the desired outcome.
- **Premature matrix.** If the user is brainstorming options and you produce a polished HTML
  before the option set is stable, you will throw it away. Draft in plain text first; commit
  to HTML once the shape is settled.
- **Treating the score as the answer.** The score is a summary statistic of a structured
  conversation. The structured conversation is the artifact.

## Tone and style

Apply the [writing-clearly-and-concisely](../writing-clearly-and-concisely/SKILL.md) skill
to cell prose and the Decision block. Cells are read fast; needless words hurt more
here than elsewhere. The Decision block states the call directly -- not as a reading of
the matrix ("the matrix points toward...") and not as advice from outside ("I
recommend..."). It is a record of what was decided and why.

Avoid glyphs and icons (no checkmarks, no traffic lights as Unicode). The verdict is
carried by the cell's background colour alone -- no inline tag, no emoji, no Unicode
shapes. Plain text survives copy-paste and screen readers.

## Related skills

- [documentation](../documentation/SKILL.md) -- for the broader principles of writing
  durable artifacts that survive drift. A decision matrix is closely related to an ADR
  (architecture decision record) and can be the front matter of one.
- [writing-clearly-and-concisely](../writing-clearly-and-concisely/SKILL.md) -- for cell
  prose and the Decision block.
- [reviewing-plans](../reviewing-plans/SKILL.md) -- if the matrix is going into a draft
  implementation plan, run the plan through review before committing to it.
