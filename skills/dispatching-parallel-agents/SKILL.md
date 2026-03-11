---
name: dispatching-parallel-agents
description: Use the Agent tool to dispatch concurrent subagents whenever a request naturally decomposes into 2 or more separable subtasks. Always consider this skill when a user's request naturally decomposes into 2 or more separable subtasks, even if the user doesn't explicitly ask for parallelism. Examples include exploring separate subsystems then consolidating findings, fixing independent failures in parallel, testing competing hypotheses simultaneously, researching multiple topics concurrently, or any work that can be split into concurrent subagent calls.
---

# Dispatching Parallel Agents

Dispatch one subagent per independent task using the Agent tool. Let them work concurrently, then consolidate results. Always consider parallel dispatch when a request decomposes into 2+ separable subtasks, even if the user did not explicitly ask for parallelism.

## When to Dispatch

Use parallel agents when tasks are **independent** -- no shared state, no sequential dependencies, no file conflicts.

Common patterns:

| Pattern | Example |
|---------|---------|
| Independent failures | 3 test files failing with different root causes |
| Subsystem exploration | Explore auth, billing, and notification subsystems separately |
| Competing hypotheses | Simultaneously test two theories about a bug by writing and running code for each |
| Research | Look up docs for 3 libraries concurrently |
| Code changes | Fix bug in backend API while updating frontend component |

Do NOT use when:
- Tasks are related (one result informs another)
- Agents would edit the same files
- You need full system context before acting

## The Pattern

### 1. Identify independent units of work

Split by problem domain, subsystem, or question. Each unit must be self-contained -- an agent should be able to complete its task without knowing what other agents are doing.

### 2. Write focused agent prompts

Each prompt needs:
- **Scope** -- exactly what to investigate, fix, or produce
- **Context** -- error messages, file paths, relevant background
- **Constraints** -- what NOT to touch, boundaries
- **Expected output** -- what to return (summary, code, answer)

Why focused prompts matter: a narrow, context-rich prompt gives the subagent a clear objective and avoids wasted work. Broad prompts ("fix all the tests") cause the agent to spend tokens discovering scope instead of solving the problem, and increase the chance it drifts into another agent's territory.

### 3. Dispatch all agents in a single message

Call the Agent tool multiple times in one response so they run concurrently. This is critical: if you dispatch agents across separate messages they run sequentially, losing the entire concurrency benefit.

Use `isolation: "worktree"` when agents make code changes. Worktree isolation gives each agent its own git working tree so concurrent file writes do not collide. Without it, two agents editing files in the same working tree will produce git conflicts or silently overwrite each other's work. Skip worktree isolation for read-only tasks (exploration, research, running existing tests) where agents do not modify files.

Example Agent tool call structure:

```
Tool: Agent
prompt: "Investigate and fix the 3 failing tests in src/auth/session.test.ts. The failures are: [paste errors]. Read the test file, identify root causes, fix them. Do NOT change production code unless it has a bug. Return a summary of root cause and fix for each test."
isolation: "worktree"
```

```
Tool: Agent
prompt: "Investigate and fix the 2 failing tests in src/billing/invoice.test.ts. The failures are: [paste errors]. Read the test file, identify root causes, fix them. Do NOT change production code unless it has a bug. Return a summary of root cause and fix for each test."
isolation: "worktree"
```

Both calls appear in the same response, so they execute concurrently.

### 4. Consolidate results

When agents return:
- Read each summary
- Check for conflicts (especially if agents edited code)
- Synthesize findings into a coherent answer or integrated changeset
- Verify the combined result (run tests, review, etc.)

### 5. Handle failures

If an agent fails or times out:
- Read whatever partial output it returned to understand how far it got.
- Retry the failed task with a narrower scope or more context, not the entire batch.
- If two agents return contradictory conclusions, dispatch a third agent with both results and ask it to resolve the conflict, or investigate the discrepancy yourself.

## Practical Concurrency Limits

Keep parallel dispatches to roughly 3-5 concurrent agents. Beyond that, resource contention and context-switching overhead outweigh the speed gains, and consolidation becomes significantly harder. If you have more than 5 independent subtasks, batch them into rounds.

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
Do NOT change production code unless it has a bug.
Return: summary of root cause and fix for each test.
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

**Constrained.** "Only modify files in src/auth/" or "Do NOT change production code."

**Output-specific.** "Return a summary of findings" or "Return the fixed code."

## Consolidation Strategies

The consolidation approach depends on what the agents produced.

**Merging code from worktrees.** Each worktree agent produces commits on an isolated branch. After all agents finish, merge each branch into the main working tree one at a time. Run the test suite after each merge to catch integration issues early rather than after all merges.

**Synthesizing research.** When agents explored different subsystems or documentation sources, read all summaries, extract the key facts from each, and combine them into a single structured answer. Call out any gaps where no agent covered a topic.

**Reconciling contradictions.** When agents reach different conclusions about the same question, present both findings side by side, identify the specific evidence each agent relied on, and either resolve the conflict yourself or dispatch a targeted follow-up agent with both sets of evidence to arbitrate.

**Combining test fixes.** If agents fixed tests in separate files, merge all changes and run the full test suite to confirm no cross-test regressions.
