---
name: reviewing-plans
description: Review and red-team implementation plans before finalization. Triggers on phrases like "review my plan", "check this plan for issues", "red-team this implementation plan", "is this plan complete", "find flaws in my plan". Dispatches a review agent to find logic errors, missed edge cases, regressions, incomplete steps, and specification gaps, then consolidates findings into a revised plan.
---

# Reviewing Plans

Review draft implementation plans before finalization by dispatching parallel review agents that check for completeness and actively try to find correctness flaws.

## Workflow

### 1. Locate the draft plan

Find the plan to review using these checks in order:

1. Check if the user provided or pasted a plan in their current message.
2. Check if plan mode was used earlier in the conversation and a draft plan exists in context.
3. Check if the user referenced a file path containing the plan -- if so, read that file.
4. If none of the above, ask the user to provide the plan (paste it, point to a file, or run plan mode first).

Once the plan is located, also gather:

- The user's goal -- what they are trying to achieve
- Relevant codebase context (file structure, key modules, existing patterns)

### 2. Dispatch review agents

Read [references/review-prompt.md](references/review-prompt.md) for the review prompt template. Substitute `[PLAN_CONTENT]` with the full draft plan text and `[USER_GOAL]` with a description of the user's goal.

**Claude review agent** (always dispatch):

Use the Agent tool with `subagent_type: "general-purpose"`. Pass the fully substituted review prompt. Instruct the agent to read relevant source files to verify the plan's assumptions against actual code.

**Codex review agent** (if available):

If `mcp__codex__codex` exists in the available tool set (including deferred tools), also dispatch it in the same parallel tool call alongside the Claude review agent. Call `mcp__codex__codex` with the fully substituted review prompt as `prompt`, the current working directory as `cwd`, `approval-policy` set to `"never"`, and `sandbox` set to `"read-only"`.

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
