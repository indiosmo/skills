---
name: design
description: Produce an HTML design brief for a proposed change through parallel discovery and an interview that resolves every open item.
---

# Design

A design brief is what sits between "we should do X" and "here is the implementation plan for X". It records what the change actually has to do, the language the change is described in, where in the codebase it lands, what is still uncertain, what calls need to be made, and the trade-offs behind each call. The plan comes later; once the brief is settled the plan is rote.

The skill has two engines. The first is a **discovery pass** run in parallel: multiple agents look at the change from different angles and ground their findings in real source files, the project's README tree, its `INDEX.md` navigation maps, and its `GLOSSARY.md`. The second is an **interview** that walks every open item the discovery surfaced -- undefined terms, open questions, and decision points -- down to resolution, one question at a time. Discovery fills the brief; the interview empties its open items.

The brief is the artifact; resolutions have durable homes beyond it. A term, once defined, belongs in `GLOSSARY.md` so the next agent and the next teammate share the same word without re-deriving it from the code. A hard-to-reverse call, once made, belongs in an ADR so a future reader learns why. A trade-off call belongs in an embedded decision matrix. The brief points at these; it does not duplicate them.

The brief is not the plan. When the user is ready to plan, they ask normally -- "produce an implementation plan from <design>.html" -- and Claude reads the brief the same way it reads any other input.

## When to reach for this

Use when the user is at the start of a non-trivial change and the design space is still open:

- "Help me think through how to add OAuth login."
- "I want to migrate the cache layer; what are we deciding?"
- "Scope adding tenant isolation across the API."
- "Before I plan this out, what are the open questions?"

Skip when:

- The change is small enough that one Claude pass produces a sensible plan directly.
- The user already knows the design and wants the plan.
- The decision is binary, uncontroversial, or already made.

When in doubt, ask "is the *shape* of the change settled, or are we still figuring out what we're building?" The brief is for the second case.

## What the brief contains

Sections appear in this order. Skip any section that would be empty rather than padding it.

| Section | What goes in it |
|---|---|
| Lede | One paragraph: what change, why it exists, where it lands. |
| Goal | The outcome the change must produce. One short paragraph or three bullets. |
| Terminology | The domain terms the change hinges on, each with a settled definition or a flag that it is still unresolved. The working surface for the shared language; settled terms promote to `GLOSSARY.md`. |
| Requirements | What the change must do, in concrete terms. Each entry is verifiable. |
| Assumptions | Premises the brief takes as settled -- scope, environmental facts, tooling. |
| Impact map | Files, modules, and external dependencies the change touches. Real paths and `file:line` refs. |
| Decision points | The calls the user has to make. Embed a decision matrix when there are real trade-offs; record a one-line decision when the call is obvious. A resolved call that is hard to reverse also gets an ADR. |
| Code samples | Side-by-side snippets when caller-side ergonomics or API shape matter. |
| Open questions | Things whose answer would change the design. Phrased as questions. |
| Risks / edge cases | Failure modes, regressions, and conditions the design has to account for. |

Terminology, Assumptions, and Open Questions live in the same head-of-document block they live in for a decision matrix; they are read against the rest of the brief. As terms get defined, give them a definition in the Terminology block and promote the durable ones to `GLOSSARY.md`. As questions get answered, promote them into Assumptions.

The brief is a thinking artifact, not a status doc. A section that says "TBD" or "to be determined" is not earning its place -- either capture the open question explicitly or remove the section.

## The shared language comes first

A design conversation that has not pinned down its terms argues past itself: one person's "account" is the Customer, the other's is the User, and the requirements written on top of that ambiguity inherit it. Before the brief is settled, the words it uses have to mean one thing each.

The glossary is where that one meaning lives. The [glossary](../glossary/SKILL.md) skill owns `GLOSSARY.md` -- the ubiquitous-language layer that gives the team and its agents one shared vocabulary, so meaning is stated once instead of re-derived from the code on every read (and re-derived differently each time). The design skill is a heavy consumer and a contributor to it:

- **Read it during discovery.** If `GLOSSARY.md` exists, the discovery agents read it and ground the brief's language in it. A term the change depends on that is already defined needs no further work -- cite the definition and move on.
- **Challenge usage against it.** When the user (or the code) uses a term in a way that conflicts with its glossary definition, surface the conflict rather than silently picking one reading. "The glossary defines cancellation as the buyer withdrawing before dispatch, but you seem to mean the carrier returning the parcel -- which is it?"
- **Surface what is missing or fuzzy.** A term the change hinges on that the glossary does not define, or defines too loosely to decide a requirement, becomes an unresolved entry in the brief's Terminology block and a question for the interview.
- **Write resolutions back.** When the interview pins down a term that is genuine domain vocabulary, add it to `GLOSSARY.md` following the glossary skill's entry schema (a headword on its own line, then one essential sentence saying what the term *is*). If the codebase has no glossary yet and the change surfaces several terms worth defining, suggest running the glossary skill for a full pass rather than hand-rolling a partial one mid-design.

Terms that are only a local clarification for this one change -- not vocabulary the wider domain shares -- can stay in the brief's Terminology block and never reach `GLOSSARY.md`. The test is the glossary skill's inclusion filter: would a competent newcomer to the domain have to look this up across the codebase, or only for this change? Domain vocabulary promotes; change-local shorthand stays in the brief.

## The interview resolves what discovery surfaces

Discovery produces a brief with open items: unresolved terms, open questions, and decision points without decisions. The interview is how those get closed. It is the same technique a relentless design review uses -- walk every branch of the design tree until each leaf is resolved, explicitly declared out of scope, or moved to a separate follow-up brief.

How to run it:

- **One question at a time.** Ask, wait for the answer, fold it into the brief, then ask the next. A wall of ten questions gets one skimmed answer; one question gets a real one.
- **For each question, give your recommended answer.** The interview is not a blank survey. State the call you would make and why, then let the user confirm, correct, or override. A recommendation the user rejects is still progress -- it surfaces the constraint you were missing.
- **Explore the codebase instead of asking, when the codebase can answer.** If a question is "does the rate limiter already scope per-tenant?", read the rate limiter -- do not ask the user to be your grep. Reserve questions for what the code cannot tell you: intent, priorities, constraints that live outside the repo.
- **Walk dependencies in order.** Some decisions only make sense once an earlier one is made (where the OAuth callback lives depends on whether `oauth/` exists as a module). Resolve the upstream decision first; the downstream one may dissolve or reshape.
- **Stress-test with concrete scenarios.** When a domain relationship or a boundary is fuzzy, invent a specific scenario that forces precision. "A customer cancels after the carrier has scanned the parcel but before it leaves the depot -- is that a cancellation or a return?" The edge case is where the vague term breaks.
- **Every item lands in one of three states.** Resolved (its answer is now an Assumption, a Decision, or a glossary entry), explicitly out of scope (recorded as such so a later reader knows it was considered and excluded), or deferred to a follow-up brief (linked, so the thread is not lost). "We will figure that out later" without one of these three is not a resolution.

The interview ends when every open item has reached one of those three states. At that point the brief has no open questions, every decision point carries a decision, and every term it uses is defined.

## Recording decisions: matrix, ADR, or a line

A decision point resolves into one of three weights of record. Pick the lightest one that captures the call.

- **A one-line decision.** The call was obvious once stated; there were not really competing options. Record it in a sentence inside the decision-point block. Most calls are this.
- **An embedded decision matrix.** Two or more options had real trade-offs and the call was non-obvious. Use the [decision-matrix](../decision-matrix/SKILL.md) skill: name the options (including the status quo and at least one likely-loser), score them against project-specific criteria, and write the Decision block. The matrix embeds in the brief under its decision point. Its "When to reach for this" criteria decide whether a call earns a matrix.
- **An ADR, in addition.** When a resolved call is *hard to reverse*, *surprising without context*, and *the result of a real trade-off* -- all three -- it also earns an architectural decision record. The decision matrix is the front matter of that ADR: the matrix shows the alternatives and the scoring, the ADR records the context, the decision, and the consequences in durable form under `docs/adr/`. Use the [documentation](../documentation/SKILL.md) skill's ADR reference for the format and numbering. Offer the ADR; do not write it unsolicited for every call. If any of the three conditions is missing, skip it -- an easily-reversed or unsurprising decision does not need a record beyond the brief.

The brief, the decision matrix, and the ADR form a gradient of durability: the brief is the working artifact for this change, the matrix preserves the comparison, the ADR is the long-lived record a future engineer finds when they ask "why is it built this way?". A call that is hard to reverse appears in all three; a trivial call appears only in the brief.

## Workflow

### 1. Confirm scope and locate the language and doc layer

Find the seed for the discovery pass:

1. If the user pasted a task description in their current message, use it.
2. If the user pointed at an issue, ticket, or doc, read that file.
3. If the conversation already established the change, summarise it in two or three sentences and confirm before dispatching.
4. Otherwise ask the user for: what they are trying to achieve, any constraints they already know, and any starting file paths.

Pin down the working directory and the parts of the codebase the change is likely to touch. Discovery agents need a real entry point; "look at the whole repo" wastes their context.

Locate the project's existing language and orientation layer so discovery can build on it instead of re-deriving it:

- **`GLOSSARY.md`** at the repo root (and any per-subdomain `GLOSSARY.md`) -- the shared vocabulary. Note whether one exists; its absence is itself a finding (the change may be the moment to start one).
- **The README tree** -- the orientation prose. The root README plus any subdirectory READMEs covering the modules the change touches.
- **`INDEX.md`** navigation maps, where the project keeps them -- the map of where things live, which gives discovery agents real entry points instead of a blind search.

Pick a `<topic>` slug for the change (e.g. `oauth-login`, `cache-migration`, `mil-preprocessor-consolidation`) and create a working folder for the artifacts this skill produces:

- Default: `work-in-progress/<topic>/` under the repo root, if that directory already exists or matches project convention.
- Otherwise: `<topic>/` in the working directory.
- If the user names a folder, use that.

Every artifact this skill produces -- raw agent findings, the discovery comparison, the HTML brief, any follow-up notes -- lands in that folder. A reader who opens the folder later should be able to reconstruct the design pass without rereading chat scrollback. Durable resolutions (glossary entries, ADRs) land in their real homes (`GLOSSARY.md`, `docs/adr/`), not the working folder.

### 2. Dispatch discovery agents in parallel

Read [references/discovery-prompt.md](references/discovery-prompt.md) for the discovery prompt template. Substitute `[TASK]` with the user's task description (or the summary you confirmed), and `[STARTING_CONTEXT]` with the files, modules, or entry points to start from -- including the `GLOSSARY.md`, READMEs, and `INDEX.md` files located in step 1.

See [../dispatching-parallel-agents/SKILL.md](../dispatching-parallel-agents/SKILL.md) for the broader pattern. The dispatch here is simpler than the general case: every discovery agent gets the same prompt; the diversity comes from different models and different exploration paths.

**Claude discovery agent** (always dispatch):

Use the Agent tool with `subagent_type: "general-purpose"`. Pass the fully substituted discovery prompt. Instruct the agent to read relevant source files to ground every finding in actual code, and to consult the README tree, `INDEX.md`, and `GLOSSARY.md` for orientation and language.

**Codex discovery agent** (if available):

If `mcp__codex__codex` exists in the available tool set (including deferred tools), dispatch it in the same parallel tool call alongside the Claude agent. Call it with the fully substituted prompt as `prompt`, the current working directory as `cwd`, `approval-policy` set to `"never"`, and `sandbox` set to `"read-only"`.

Dispatch both in one message so they run concurrently.

Both agents return structured findings: requirements, terminology (with glossary cross-references and conflicts), impact map (with `file:line` refs), decision points (with options and trade-offs), open questions, risks. They do *not* produce HTML and they do *not* propose an implementation plan.

### 3. Persist agent findings and compare

Before consolidating, write each agent's raw markdown to the working folder so the user can review the inputs to the brief, and so a later agent (a consolidator, an implementation planner) can read them from disk instead of relying on orchestrator context.

Write:

- `<topic>/agent-claude.md` -- the Claude discovery agent's findings verbatim.
- `<topic>/agent-codex.md` -- the Codex agent's findings verbatim, if it ran.
- `<topic>/discovery-comparison.md` -- a short side-by-side covering:
  - **Agreement**: convergent conclusions both agents reached independently. Strong signal for the brief.
  - **Disagreement**: items where the agents contradict each other. These become decision points in the brief, not silently-resolved details.
  - **Only Claude surfaced** / **Only Codex surfaced**: items one agent found and the other missed. Often coverage gaps (different headers walked, different starting context interpreted) rather than real disagreements -- but worth listing so the brief can carry the union with confidence levels visible.
  - One short closing paragraph on what the comparison implies for the brief (scope changes, additional decisions, removed redundancy).

Skip the comparison file when only one agent ran -- there is nothing to compare. The single agent's findings file is enough.

The comparison is the bridge between raw findings and the consolidated brief. Producing it forces the orchestrator to actually read both agents' outputs against each other, not just deduplicate by string match.

### 4. Consolidate

Working from the on-disk findings (not orchestrator memory):

1. Read each agent's findings file and the comparison.
2. Deduplicate overlapping items. Two agents naming the same requirement is a signal; record it once.
3. Reconcile terminology against `GLOSSARY.md`. A term both agents flag as undefined or used inconsistently becomes an unresolved entry in the Terminology block; a term the glossary already defines cleanly gets cited, not redefined.
4. Surface disagreements explicitly -- if one agent says the auth module is fine to extend and the other says it needs replacing, that disagreement is a decision point in the brief, not an item to silently resolve.
5. Group impact-map entries by module so the reader sees the shape of the blast radius.
6. For each decision point, decide whether it warrants a full decision matrix or just a one-line trade-off note. Use the [decision-matrix](../decision-matrix/SKILL.md) skill's "When to reach for this" criteria.
7. For each code sample candidate, decide whether a side-by-side snippet would change the read. Skip the rest.

### 5. Produce the HTML artifact

Generate a single self-contained HTML file. See [references/artifact-template.md](references/artifact-template.md) for structure, palette, and content conventions. The brief reuses the [decision-matrix](../decision-matrix/SKILL.md) skill's warm-paper palette and chrome so embedded matrices read consistently and so a project's design briefs and decision matrices look like one family of documents.

Save as `<topic>/<topic>-design.html` in the working folder picked in step 1. Print the absolute path so the user can open it with `xdg-open <path>` or equivalent.

### 6. Surface in chat

After writing the file, give the user a short summary in chat:

- One line on the chosen framing of the change.
- Two or three lines naming the most consequential open questions, undefined terms, or decision points.
- The artifact path.

Do not restate the impact map or the full requirements list in chat -- the HTML carries that. The chat summary is the bridge to the artifact and the opening of the interview, not a duplicate of the brief.

### 7. Interview to resolution

The brief at the end of step 6 has open items: unresolved terms, open questions, and decision points without decisions. Walk them down one at a time using the technique in [references/interview.md](references/interview.md) and summarised under "The interview resolves what discovery surfaces" above.

As each item resolves, write the resolution to every place it belongs:

1. **Define terms inline and promote the durable ones.** Give the term a definition in the Terminology block. If it is genuine domain vocabulary, add it to `GLOSSARY.md` following the glossary skill's entry schema; if it is change-local shorthand, leave it in the brief.
2. **Promote answered questions into Assumptions.** Remove them from Open Questions and add the answer to Assumptions, phrased as a settled premise.
3. **Record decisions at the right weight.** A one-line decision goes inside its decision-point block. A non-obvious trade-off gets an embedded decision matrix. A hard-to-reverse, surprising, real-trade-off call also gets an ADR under `docs/adr/`, with the matrix as its front matter. See "Recording decisions" above.
4. **Re-read the rest of the brief against the new premise.** If the answer narrows the design space, some requirements or impact entries may be wrong now; fix them. If it opens new questions or surfaces a new term, add them.
5. **Record out-of-scope and deferred items.** An item the user rules out is recorded as out of scope (so a later reader knows it was considered). An item deferred to later becomes a linked follow-up brief, not a dropped thread.
6. **Leave a trail.** The Assumptions block and the glossary are the audit log -- a reader who comes back later should be able to tell which premises and which definitions shaped the design.

When every open question is resolved, every term is defined, and every decision is recorded, the brief is done. The user can then ask Claude to produce the implementation plan from it.

## Pitfalls to avoid

- **Discovery agents that propose solutions.** The agents surface the design space; they do not pick from it. A return value that reads "we should do X" is the agent overstepping -- the user picks, not the agent. Re-prompt or strip the proposal. (The interview is the exception: there you *do* recommend an answer per question -- but the user still makes the call.)
- **Skipping the persistence step.** The orchestrator's working memory is opaque to the user and is lost when the session ends. The on-disk findings and the discovery comparison are what gets reviewed, what a later planner agent reads, and what survives a `/compact` or a fresh session. "I already have the findings in context" is not a substitute -- write them out.
- **Comparison file that is just two bullet lists side by side.** The point is the synthesis: where the agents converged (strong signal), where they contradicted (decision point), what each found alone (coverage gap or unique catch). A reader should be able to skim the comparison and know whether the brief leans on consensus or on a single agent's catch.
- **Impact maps from memory.** Every `file:line` reference comes from a file the agent actually read. Made-up line numbers in a design brief poison every downstream decision that hangs off them.
- **Requirements that are not verifiable.** "Should be performant" is not a requirement; "p99 latency stays under 50ms for the existing benchmark suite" is. If a requirement cannot be checked, it cannot be planned against.
- **Premature decision matrices.** A matrix on a one-option "decision" is theater. Embed a matrix only when two or more options are real and the call is non-obvious.
- **An ADR for every decision.** ADRs are for calls that are hard to reverse, surprising, and a real trade-off -- all three. Writing one for an easily-reversed or obvious call is bureaucracy that buries the ADRs that matter.
- **Defining every term.** The Terminology block and the glossary are for words whose domain meaning a newcomer would have to look up. A term used in its plain-English sense is not a glossary entry; do not pad the language layer with words that carry their ordinary meaning.
- **Filling sections to fill them.** No Open Questions block beats one with three made-up questions. Same for Terminology, Assumptions, Risks, and Code Samples.
- **Batching the interview.** Ten questions in one message gets one skimmed answer. Ask one, fold in the answer, ask the next.
- **Asking what the codebase can answer.** If a question is settled by reading a file, read the file. Reserve questions for intent, priorities, and constraints outside the repo.
- **Letting the brief drift into a plan.** "Implement the auth middleware" is a plan step; "decide whether auth middleware lives in `web/` or in a shared `auth/` module" is a decision point. The brief is the input to the plan, not the plan itself.
- **One mega-document for unrelated changes.** A design brief covers one change. If the user is scoping three changes, produce three briefs and link between them.

## Related skills

- [glossary](../glossary/SKILL.md) -- owns `GLOSSARY.md`, the shared vocabulary the brief grounds its language in and writes resolved terms back to. Run it for a full glossary pass when a codebase has none.
- [decision-matrix](../decision-matrix/SKILL.md) -- for embedded decision matrices and for the visual palette the brief reuses.
- [documentation](../documentation/SKILL.md) -- for the ADR format a hard-to-reverse decision is recorded in, and for the README conventions discovery reads.
- [dispatching-parallel-agents](../dispatching-parallel-agents/SKILL.md) -- for the broader pattern the discovery pass instantiates.
- [reviewing-prs](../reviewing-prs/SKILL.md) -- the sibling artifact pattern for *reviewing* code; this skill is the sibling for *designing* it.
- `writing-clearly-and-concisely` -- separately installed; apply to the lede, the goal, and the decision-point trade-off notes. Brief prose is read fast and needless words hurt more here than elsewhere.
