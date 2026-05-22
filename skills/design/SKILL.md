---
name: design
description: Produce an HTML design brief for a proposed change. A parallel-agent discovery pass surfaces requirements, codebase impact, open questions, decision points (with embedded decision matrices), and illustrative code samples. The brief is the input to a later implementation plan; it is not the plan itself.
---

# Design

A design brief is what sits between "we should do X" and "here is the implementation plan for X". It records what the change actually has to do, where in the codebase it lands, what is still uncertain, what calls need to be made, and the trade-offs behind each call. The plan comes later; once the brief is settled the plan is rote.

This skill runs the discovery pass in parallel (multiple agents look at the change from different angles, ground their findings in real source files), consolidates their findings into a single HTML brief, and then iterates the brief with the user as questions get answered and decisions get pinned down.

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
| Requirements | What the change must do, in concrete terms. Each entry is verifiable. |
| Assumptions | Premises the brief takes as settled -- scope, environmental facts, tooling. |
| Impact map | Files, modules, and external dependencies the change touches. Real paths and `file:line` refs. |
| Decision points | The calls the user has to make. Embed a decision matrix when there are real trade-offs; record a one-line decision when the call is obvious. |
| Code samples | Side-by-side snippets when caller-side ergonomics or API shape matter. |
| Open questions | Things whose answer would change the design. Phrased as questions. |
| Risks / edge cases | Failure modes, regressions, and conditions the design has to account for. |

Assumptions and Open Questions live in the same head-of-document block they live in for a decision matrix; they are read against the rest of the brief. As questions get answered, promote them into Assumptions.

The brief is a thinking artifact, not a status doc. A section that says "TBD" or "to be determined" is not earning its place -- either capture the open question explicitly or remove the section.

## Workflow

### 1. Confirm scope and gather the seed

Find the seed for the discovery pass:

1. If the user pasted a task description in their current message, use it.
2. If the user pointed at an issue, ticket, or doc, read that file.
3. If the conversation already established the change, summarise it in two or three sentences and confirm before dispatching.
4. Otherwise ask the user for: what they are trying to achieve, any constraints they already know, and any starting file paths.

Pin down the working directory and the parts of the codebase the change is likely to touch. Discovery agents need a real entry point; "look at the whole repo" wastes their context.

### 2. Dispatch discovery agents in parallel

Read [references/discovery-prompt.md](references/discovery-prompt.md) for the discovery prompt template. Substitute `[TASK]` with the user's task description (or the summary you confirmed), and `[STARTING_CONTEXT]` with the files, modules, or entry points to start from.

See [../dispatching-parallel-agents/SKILL.md](../dispatching-parallel-agents/SKILL.md) for the broader pattern. The dispatch here is simpler than the general case: every discovery agent gets the same prompt; the diversity comes from different models and different exploration paths.

**Claude discovery agent** (always dispatch):

Use the Agent tool with `subagent_type: "general-purpose"`. Pass the fully substituted discovery prompt. Instruct the agent to read relevant source files to ground every finding in actual code.

**Codex discovery agent** (if available):

If `mcp__codex__codex` exists in the available tool set (including deferred tools), dispatch it in the same parallel tool call alongside the Claude agent. Call it with the fully substituted prompt as `prompt`, the current working directory as `cwd`, `approval-policy` set to `"never"`, and `sandbox` set to `"read-only"`.

Dispatch both in one message so they run concurrently.

Both agents return structured findings: requirements, impact map (with `file:line` refs), decision points (with options and trade-offs), open questions, risks. They do *not* produce HTML and they do *not* propose an implementation plan.

### 3. Consolidate

When all agents return:

1. Read each agent's findings.
2. Deduplicate overlapping items. Two agents naming the same requirement is a signal; record it once.
3. Surface disagreements explicitly -- if one agent says the auth module is fine to extend and the other says it needs replacing, that disagreement is a decision point, not an item to silently resolve.
4. Group impact-map entries by module so the reader sees the shape of the blast radius.
5. For each decision point, decide whether it warrants a full decision matrix or just a one-line trade-off note. Use the [decision-matrix](../decision-matrix/SKILL.md) skill's "When to reach for this" criteria.
6. For each code sample candidate, decide whether a side-by-side snippet would change the read. Skip the rest.

### 4. Produce the HTML artifact

Generate a single self-contained HTML file. See [references/artifact-template.md](references/artifact-template.md) for structure, palette, and content conventions. The brief reuses the [decision-matrix](../decision-matrix/SKILL.md) skill's warm-paper palette and chrome so embedded matrices read consistently and so a project's design briefs and decision matrices look like one family of documents.

Save as `<topic>-design.html` in the working directory (or wherever the user asks). Print the absolute path so the user can open it with `xdg-open <path>` or equivalent.

### 5. Surface in chat

After writing the file, give the user a short summary in chat:

- One line on the chosen framing of the change.
- Two or three lines naming the most consequential open questions or decision points.
- The artifact path.

Do not restate the impact map or the full requirements list in chat -- the HTML carries that. The chat summary is the bridge to the artifact, not a duplicate of it.

### 6. Iterate

The brief is not done on the first pass. As the user answers open questions and makes decisions:

1. **Promote answered questions into Assumptions.** Remove them from Open Questions and add the answer to Assumptions, phrased as a settled premise.
2. **Record decisions inside their decision-point block.** For matrix-backed decisions, add the Decision block immediately under the matrix (see decision-matrix's "Decision" section for phrasing). For one-line decisions, replace the trade-off note with the call.
3. **Re-read the rest of the brief against the new premise.** If the answer narrows the design space, some requirements or impact entries may be wrong now; fix them. If it opens new questions, add them.
4. **Leave a trail.** The Assumptions block is the audit log -- a reader who comes back later should be able to tell which premises shaped the design.

When every open question is resolved and every decision is recorded, the brief is done. The user can then ask Claude to produce the implementation plan from it.

## Pitfalls to avoid

- **Discovery agents that propose solutions.** The agents surface the design space; they do not pick from it. A return value that reads "we should do X" is the agent overstepping -- the user picks, not the agent. Re-prompt or strip the proposal.
- **Impact maps from memory.** Every `file:line` reference comes from a file the agent actually read. Made-up line numbers in a design brief poison every downstream decision that hangs off them.
- **Requirements that are not verifiable.** "Should be performant" is not a requirement; "p99 latency stays under 50ms for the existing benchmark suite" is. If a requirement cannot be checked, it cannot be planned against.
- **Premature decision matrices.** A matrix on a one-option "decision" is theater. Embed a matrix only when two or more options are real and the call is non-obvious.
- **Filling sections to fill them.** No Open Questions block beats one with three made-up questions. Same for Assumptions, Risks, and Code Samples.
- **Letting the brief drift into a plan.** "Implement the auth middleware" is a plan step; "decide whether auth middleware lives in `web/` or in a shared `auth/` module" is a decision point. The brief is the input to the plan, not the plan itself.
- **One mega-document for unrelated changes.** A design brief covers one change. If the user is scoping three changes, produce three briefs and link between them.

## Related skills

- [decision-matrix](../decision-matrix/SKILL.md) -- for embedded decision matrices and for the visual palette the brief reuses.
- [dispatching-parallel-agents](../dispatching-parallel-agents/SKILL.md) -- for the broader pattern this skill instantiates.
- [reviewing-prs](../reviewing-prs/SKILL.md) -- the sibling artifact pattern for *reviewing* code; this skill is the sibling for *designing* it.
- `writing-clearly-and-concisely` -- separately installed; apply to the lede, the goal, and the decision-point trade-off notes. Brief prose is read fast and needless words hurt more here than elsewhere.
