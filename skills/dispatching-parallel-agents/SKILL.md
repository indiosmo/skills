---
name: dispatching-parallel-agents
description: Dispatch concurrent subagents for independent subtasks in Claude Code or Codex CLI.
---

# Dispatching Parallel Agents

Dispatch one subagent per independent task. Let them work concurrently, then consolidate results in the current branch and working tree. Use this skill when a request decomposes into 2 or more separable subtasks.

The orchestrating agent owns the split, the prompts, and the final integration. Subagents own only the files, modules, or questions assigned to them.

## When to Dispatch

Use parallel agents when tasks are **independent**: no sequential dependency, no shared decision point, and no overlapping file ownership.

Common patterns:

| Pattern | Example |
|---------|---------|
| Independent failures | 3 test files failing with different root causes |
| Subsystem exploration | Explore auth, billing, and notification subsystems separately |
| Competing hypotheses | Simultaneously test two theories about a bug by writing and running code for each |
| Research | Look up docs for 3 libraries concurrently |
| Code changes | Fix bug in backend API while updating frontend component |

Do not dispatch subagents when:
- One task's result determines another task's scope
- Two agents would edit the same file or tightly coupled files
- You need full system context before splitting the work
- The runtime cannot safely support concurrent writes in the current checkout

## The Pattern

### 1. Identify independent units of work

Split by problem domain, subsystem, file set, or question. Each unit must be self-contained: an agent should be able to complete its task without knowing what the other agents are doing.

For code changes, assign a disjoint write scope to each subagent:
- Specific files: `src/auth/session.ts` and `src/auth/session.test.ts`
- A module or package: `packages/billing/`
- A read-only topic: "map the routing flow and return file references"

If the write scopes overlap, do the shared part yourself in the orchestrating thread or serialize that part after the parallel work returns.

### 2. Write focused agent prompts

Each prompt needs:
- **Scope** -- exactly what to investigate, fix, or produce
- **Context** -- error messages, file paths, relevant background
- **Ownership** -- the files, directories, or subsystem the agent may edit
- **Constraints** -- boundaries, commands to avoid, and files not to touch
- **Expected output** -- what to return (summary, code, answer)

Why focused prompts matter: a narrow, context-rich prompt gives the subagent a clear objective and avoids wasted work. Broad prompts ("fix all the tests") cause the agent to spend tokens discovering scope instead of solving the problem, and increase the chance it drifts into another agent's territory.

### 3. Dispatch all agents in a single message

Dispatch all subagents in one turn so they run concurrently. If you dispatch agents across separate turns, many runtimes will run them sequentially and lose the concurrency benefit.

Platform notes:
- **If Claude Code:** use the Agent or Task tool available in that environment. Send one tool call per independent task in the same response. Keep agents in the current checkout unless the user explicitly asks for a separate checkout.
- **If Codex CLI:** Codex spawns subagents only when explicitly asked. Use direct wording such as "spawn one subagent per point" or use the available subagent tool. Pick `explorer` for read-heavy work and `worker` for implementation work when those agent types are available.

Keep the work in the current branch and working tree. Avoid prompts that tell subagents to create separate checkouts, make commits, merge branches, or run broad git operations. If the user's environment forbids commits, tell subagents not to commit and to leave file edits unstaged.

Example subagent prompt structure:

```
Investigate and fix the 3 failing tests in src/auth/session.test.ts.
Ownership: src/auth/session.ts and src/auth/session.test.ts only.
Context: [paste failures].
Constraints: do not edit billing, routing, or database files. Do not commit.
Return: root cause, files changed, tests run, and any remaining risk.
```

```
Investigate and fix the 2 failing tests in src/billing/invoice.test.ts.
Ownership: src/billing/ only.
Context: [paste failures].
Constraints: do not edit auth files. Do not commit.
Return: root cause, files changed, tests run, and any remaining risk.
```

Both agents are dispatched in the same turn, so they execute concurrently.

### 4. Consolidate results

When agents return:
- Read each summary
- Inspect the changed files
- Check for overlapping edits or inconsistent assumptions
- Synthesize findings into a coherent answer or integrated changeset
- Verify the combined result (run tests, review, etc.)

### 5. Handle failures

If an agent fails or times out:
- Read whatever partial output it returned to understand how far it got.
- Retry the failed task with a narrower scope or more context, not the entire batch.
- If two agents return contradictory conclusions, dispatch a third agent with both results and ask it to resolve the conflict, or investigate the discrepancy yourself.

## Practical Concurrency Limits

Keep parallel dispatches to roughly 3 to 5 concurrent agents. Beyond that, resource contention and consolidation overhead usually outweigh the speed gains. If you have more than 5 independent subtasks, batch them into rounds.

## Agent Prompt Examples

### Exploring a subsystem

```
Explore the authentication subsystem in src/auth/.
Answer: What auth strategies are supported? How are sessions managed?
What middleware is used? Return a brief summary of the architecture.
```

### Fixing an independent failure

```
Fix the 3 failing tests in src/agents/agent-tool-abort.test.ts:
1. "should abort tool with partial output" - expects 'interrupted at' in message
2. "should handle mixed completed and aborted tools" - fast tool aborted instead of completed
3. "should properly track pendingToolCount" - expects 3 results but gets 0

Read the test file, identify root causes, fix them.
Ownership: src/agents/agent-tool-abort.test.ts and the smallest required production file only.
Do not edit unrelated tests. Do not commit.
Return: summary of root cause and fix for each test, files changed, and tests run.
```

### Testing competing hypotheses simultaneously

Dispatch two agents at once, one per hypothesis:

Agent 1:
```
We suspect the request timeout is caused by a slow database query in
src/api/users.ts. Profile the getUsersByOrg query against the test
database, measure execution time, and check for missing indexes.
Return: query time, explain plan output, and whether this explains
the 5-second timeout.
```

Agent 2:
```
We suspect the request timeout is caused by an unbounded retry loop
in src/api/client.ts. Read the retry logic, trace what happens when
the upstream service returns 503, and determine whether retries could
compound to exceed 5 seconds. Return: analysis of retry behavior and
whether this explains the 5-second timeout.
```

Both run concurrently. When results return, compare them to determine which hypothesis (or both) explains the timeout.

## Writing Good Prompts

**Focused, not broad.** "Fix agent-tool-abort.test.ts" not "Fix all the tests."

**Context-rich, not vague.** Paste error messages, file paths, relevant details.

**Owned, not overlapping.** "Modify only src/auth/ and its tests" not "fix anything related to login."

**Constrained.** "Do not commit" or "do not edit database migrations."

**Output-specific.** "Return a summary of findings" or "Return the fixed code."

## Consolidation Strategies

The consolidation approach depends on what the agents produced.

**Combining local code edits.** Each code-writing agent edits only its assigned files in the current branch and working tree. After all agents finish, review `git diff`, inspect touched files, and run the relevant tests. Resolve any integration issue in the orchestrating thread.

**Synthesizing research.** When agents explored different subsystems or documentation sources, read all summaries, extract the key facts from each, and combine them into a single structured answer. Call out any gaps where no agent covered a topic.

**Reconciling contradictions.** When agents reach different conclusions about the same question, present both findings side by side, identify the specific evidence each agent relied on, and either resolve the conflict yourself or dispatch a targeted follow-up agent with both sets of evidence to arbitrate.

**Combining test fixes.** If agents fixed tests in separate files, review the combined changes and run the full test suite to confirm no cross-test regressions.
