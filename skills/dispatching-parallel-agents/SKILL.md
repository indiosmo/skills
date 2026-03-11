---
name: dispatching-parallel-agents
description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies. Examples include exploring separate subsystems then consolidating findings, fixing independent failures in parallel, running quick one-off checks (write/build/run code to confirm a hypothesis), researching multiple topics simultaneously, or any work that can be split into concurrent agents.
---

# Dispatching Parallel Agents

Dispatch one agent per independent task. Let them work concurrently, then consolidate results.

## When to Dispatch

Use parallel agents when tasks are **independent** -- no shared state, no sequential dependencies, no file conflicts.

Common patterns:

| Pattern | Example |
|---------|---------|
| Independent failures | 3 test files failing with different root causes |
| Subsystem exploration | Explore auth, billing, and notification subsystems separately |
| Hypothesis testing | Write and run 2 code snippets to confirm competing theories |
| Research | Look up docs for 3 libraries simultaneously |
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

### 3. Dispatch all agents in a single message

Use the Agent tool with multiple tool calls in one message so they run concurrently. Use `isolation: "worktree"` when agents make code changes to avoid file conflicts.

### 4. Consolidate results

When agents return:
- Read each summary
- Check for conflicts (especially if agents edited code)
- Synthesize findings into a coherent answer or integrated changeset
- Verify the combined result (run tests, review, etc.)

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

### Quick hypothesis check

```
Write a short Python script that tests whether the `csv` module
handles embedded newlines in quoted fields correctly when using
`quoting=csv.QUOTE_ALL`. Run it and return the output.
```

## Writing Good Prompts

**Focused, not broad.** "Fix agent-tool-abort.test.ts" not "Fix all the tests."

**Context-rich, not vague.** Paste error messages, file paths, relevant details.

**Constrained.** "Only modify files in src/auth/" or "Do NOT change production code."

**Output-specific.** "Return a summary of findings" or "Return the fixed code."

## Consolidation

The main agent's job after dispatch:
1. **Review** -- understand what each agent found or changed
2. **Detect conflicts** -- did agents touch overlapping code or reach contradictory conclusions?
3. **Synthesize** -- merge findings into a single coherent result
4. **Verify** -- run the full test suite, check consistency, spot-check agent work
