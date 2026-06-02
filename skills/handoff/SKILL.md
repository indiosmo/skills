---
name: handoff
description: Write a handoff document so a fresh agent or teammate can pick up the current work cold. Also use when wrapping up, running low on context, or asked to checkpoint state.
argument-hint: "what the next session/agent will use this handoff for"
---

# Handoff

A handoff is the document a fresh agent reads to continue work it has zero memory of. The next reader has no scrollback: not the dead ends you already ruled out, not the command that finally passed, not the decision you made at 2pm and forgot to write down. The handoff is the only thing that crosses the session boundary, so it has to carry everything that mattered and nothing that didn't.

The governing instinct is **map, not territory**. A handoff points at the plan, the spec, the commits, and the files -- it does not re-typeset them. A reader with the handoff plus repo access should be able to reconstruct the full state; a reader without repo access was never the audience. Duplicating a diff or a design rationale into the handoff just creates a second copy that goes stale the moment someone touches the code.

These are not "compact summaries" -- the real ones run anywhere from forty lines to three hundred. Length follows the work. A handoff that elides the failing-test list to stay short has failed at its one job.

## The decisive question: is this work anchored to a plan file?

Everything downstream -- where the handoff lives, whether it has a resume section -- turns on this.

**Plan-backed work** (there is a `<topic>-plan.md`, a migration doc, a phased checklist the session was executing against): the handoff is a dated `## Handoff - <YYYY-MM-DD>` section at the end of that plan, not a separate file. Keeping it in the plan means the next agent opens one file and sees both the design and the current cut-over point. If a prior `## Handoff` section exists, update it in place rather than stacking a second one -- the handoff reflects current state, and git history holds the previous state.

**Standalone work** (an ad-hoc session not anchored to any plan -- "go fix this flaky test", "investigate why the build is slow"): write a `work-in-progress/<topic>-handoff.md` at the repo root. There is no plan to fold it into, so it stands on its own.

Save location is always under the repo's `work-in-progress/` -- both the plan and the standalone handoff live there. Do not write handoffs to the OS temp dir; they are working artifacts the user revisits across sessions and expects to find in the tree.

## Use the argument

If the user passed an argument, it tells you how the handoff will be consumed -- "the next session will do the documentation phase", "another person is taking this over", "I'm going to feed this to a parallel-agent dispatch". Tailor accordingly: a handoff for a teammate leans harder on context and decisions; a handoff feeding a `/dispatching-parallel-agents` run leans harder on a crisp, parallelizable task list; a handoff for the next phase of a plan leans hard on the resume section. When no argument is given, infer the purpose from the conversation and state your assumption in the opening line.

## Resume section: only when there is something to resume

A multi-phase plan where this session finished a phase has a genuine resume: the next phase, with whatever the current phase changed about it. Write a **How to resume** section -- the concrete first moves for the next agent (files to read, commands to confirm state).

Self-contained work that is *done* has nothing to resume -- the handoff is a record of what happened and why, not a launch pad. Self-contained work that is *unfinished* (you ran out of context mid-task) does have a resume: the rest of the task. Write the resume section when there is a clear next move for a fresh agent; skip it when the work is closed.

## What the handoff contains

Sections in this order. Include a section only when it has real content -- an empty "Open questions" is worse than none, because it tells the reader you checked and there were none when you simply padded.

| Section | What goes in it |
|---|---|
| Opening line | State at the cut-over point in one sentence, plus the companion pointer: "Companion to [`<topic>-plan.md`](...); read that first for the design and rationale." For a plan-embedded handoff the pointer is implicit. |
| Goal | What this session/phase was trying to achieve. One short paragraph. Skip if the plan already states it and nothing changed. |
| What landed | What actually changed, grouped by phase/theme/workstream. `file:line` refs, not pasted code. Name the commits if they exist. This is the heart of the document. |
| Decisions taken | Calls made during execution that the plan did not pre-decide -- naming, scope cuts, a chosen approach among alternatives. One line each, with the why. |
| Verification | The exact commands run and their results: `./build.sh asan` clean, `mil_strong_type_test` 74 assertions in 14 cases passing. Real output, not "tests pass". |
| What's pending / Next steps | What remains, numbered and actionable. For a phased plan, this is the next phase with any adjustments the current phase forced. |
| Open questions | Things whose answer changes what the next agent does. Phrase as questions; when you have a recommendation, state it ("Recommend option 1: skip entirely, note the deviation in the commit message."). |
| How to resume | The first concrete moves: which files to read (this doc + the plan), which commands confirm current state. A bash block when the moves are mechanical. |
| Cautions | Things that will bite a fresh agent: uncommitted worktree state, environment quirks, a file mid-edit, something that must not be reverted. |

Drop, merge, or rename these to fit the work -- a small handoff might be just Opening line, What landed, Verification, Next steps. The table is the menu, not a form to fill.

## Writing principles

**Reference, do not duplicate.** Link the plan, the ADR, the spec by markdown path. Cite code as `file:line`. Point at git (`git show <sha>`, `git diff <base>...HEAD`) and build/test commands instead of pasting their output wholesale. The handoff names where the truth lives; it is not a second copy of the truth. This is the single most load-bearing habit -- a handoff that inlines a diff is obsolete the next commit.

**Verification is specific or it is noise.** "I tested it" tells the next agent nothing they can trust. The command you ran and the count it produced -- `74 assertions in 14 test cases`, `asan clean`, `3 approval snapshots accepted` -- is a fact they can re-derive. Give them the command so they can.

**Open questions carry your best answer.** You spent the session in this problem; the next agent has not. When you flag an open question, attach the answer you'd give if forced to choose, and why. A bare question makes them redo the thinking you already did.

**Write for a reader with no context, in the present tense.** Describe the state the code is in now and what to do next -- not the journey. The reader does not need the three approaches you abandoned unless one of them is a trap they might re-enter; if so, that is a Caution, phrased as "do not X because Y", not a travelogue.

**Redact secrets.** API keys, tokens, passwords, PII do not belong in a working doc that lives in the tree. Reference the secret's location ("token in `.env`, key `FOO_API_KEY`"), never its value.

## Workflow

1. **Determine plan-backed vs standalone.** Look for a `<topic>-plan.md` or equivalent the session was executing against. If present and the work is plan-backed, the handoff is a `## Handoff - <date>` section in that plan. If the session was ad-hoc, it is a standalone `work-in-progress/<topic>-handoff.md`. When genuinely ambiguous, ask the user.

2. **Read the argument and the conversation.** Establish what landed, what was decided, what was verified, and what is left -- from the actual session, not assumption. Run `git status` / `git log --oneline` / `git diff --stat` to ground "what landed" in real changes rather than memory.

3. **Decide whether there is a resume.** Multi-phase plan with a finished phase, or unfinished standalone work: write How to resume. Closed self-contained work: skip it.

4. **Draft the sections that have content.** Follow the table order; drop empty sections. Keep every claim referenced -- `file:line`, command, commit, or plan link.

5. **Write it to the right place.** Append/update the plan's handoff section, or write the standalone file. Print the absolute path.

6. **Surface in chat.** Two or three lines: where it landed, the one decision or open question that most shapes what comes next, and the path. Do not restate the document in chat.

## Pitfalls to avoid

- **Pasting the diff.** The git tree is the diff. A handoff that inlines code is a stale copy waiting to mislead. Reference `file:line` and `git show`.
- **"Tests pass" with no command.** Unverifiable and untrustworthy. Name the command and the count.
- **A resume section on finished work.** If there is nothing to pick up, the handoff is a record, not a launch pad. Forcing a "next steps" onto closed work invents work.
- **Writing to the temp dir.** These are revisited across sessions; they live in `work-in-progress/` in the tree.
- **A standalone handoff file when a plan exists.** Two files the reader must reconcile, that drift apart. If the work is plan-backed, the handoff goes in the plan.
- **Padding empty sections.** "Open questions: none", "Cautions: N/A" -- drop the section. Its absence says the same thing without the noise.
- **Travelogue.** "First I tried X, then Y failed, then I realized Z." The next agent needs the current state and the next move, not the history. The exception is a dead end they might re-enter -- record that as a Caution.
- **Bare open questions.** You did the investigation; hand over your answer, not just the question.

## Related skills

- [design](../design/SKILL.md) -- produces the design brief that often becomes the plan a handoff later checkpoints. The handoff is the running-state counterpart to the design's up-front shape.
- [dispatching-parallel-agents](../dispatching-parallel-agents/SKILL.md) -- a handoff written to feed a parallel dispatch should front-load a crisp, independent task list.
- `writing-clearly-and-concisely` -- separately installed; apply to the opening line, the decisions, and the open-question recommendations. A handoff is read fast under time pressure; needless words cost more here.
