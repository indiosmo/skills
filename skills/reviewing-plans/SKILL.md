---
name: reviewing-plans
description: Review and red-team implementation plans for completeness, correctness, and potential flaws before finalization. Use when Claude has drafted an implementation plan (from plan mode or otherwise) and needs to verify it before producing the final version. Dispatches parallel review agents -- always a Claude agent, and always a Codex agent when the mcp__codex__codex tool is available -- to find logic errors, missed edge cases, potential regressions, incomplete steps, and specification gaps, then consolidates reviews into a refined final plan.
---

# Reviewing Plans

Review draft implementation plans before finalization by dispatching parallel review agents that check for completeness and actively try to find correctness flaws.

## Workflow

### 1. Capture the draft plan and context

Before dispatching reviewers, gather:

- The full draft plan text (from plan mode context, a file, or arguments)
- The user's goal -- what they are trying to achieve
- Relevant codebase context (file structure, key modules, existing patterns)

### 2. Dispatch review agents in parallel

Read [references/review-prompt.md](references/review-prompt.md) for the review prompt template. Substitute `[PLAN_CONTENT]` with the full draft plan text and `[USER_GOAL]` with a description of the user's goal.

Send a single message with multiple tool calls to run reviews concurrently.

**Claude review agent** (always dispatch):

Use the Agent tool with `subagent_type: "general-purpose"`. Pass the fully substituted review prompt. Instruct the agent to read relevant source files to verify the plan's assumptions against actual code.

**Codex review agent** (MUST dispatch when available):

Before dispatching, check whether `mcp__codex__codex` exists in the available tool set (including deferred tools). If it is available, you MUST dispatch it alongside the Claude review agent in the same parallel tool call. Do NOT skip it or wait for the user to ask. The whole point of this skill is to get independent parallel reviews.

Call `mcp__codex__codex` with:

- `prompt`: The fully substituted review prompt (include all plan text inline)
- `cwd`: The current working directory so Codex can read the codebase
- `approval-policy`: `"never"`
- `sandbox`: `"read-only"`

Only if `mcp__codex__codex` is confirmed to not exist in the tool set (not listed in available tools or deferred tools), proceed with the Claude review agent alone.

### 3. Consolidate reviews

When all agents return:

1. Read each review's findings
2. Deduplicate overlapping issues
3. Categorize by severity:
   - **Blocking** -- logic errors, missing steps, incorrect assumptions, potential regressions
   - **Important** -- missing edge cases, unclear steps, incomplete specifications
   - **Advisory** -- style suggestions, minor improvements
4. Present the consolidated review summary to the user with blocking and important issues highlighted

### 4. Revise the plan

Incorporate all blocking and important issues into a revised final plan. Advisory items may be incorporated at discretion. If the review status was "Approved" from all reviewers with no blocking or important issues, the draft plan can be finalized as-is.
