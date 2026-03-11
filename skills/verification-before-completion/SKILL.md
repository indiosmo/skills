---
name: verification-before-completion
description: Ensures all completion claims are backed by fresh verification evidence. Triggers whenever about to claim work is complete, tests pass, builds succeed, bugs are fixed, or any positive status; also applies before committing, creating PRs, closing issues, or reporting status.
---

# Verification Before Completion

## Overview

Claiming work is complete without verification leads to false claims that erode trust and cause rework. Skipping verification does not save time -- it shifts the cost onto your collaborator, who must then discover the real state and redo work.

**Core principle:** Evidence before claims, always.

## The Gate Function

```
BEFORE claiming completion or reporting success:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skipping any step means making an unverified claim.
```

## Verification Requirements

| Claim | What You Must Run | What Is Not Sufficient |
|-------|-------------------|------------------------|
| Tests pass | Test command output showing 0 failures | A previous run, or "should pass" |
| Linter clean | Linter output showing 0 errors | Partial check, extrapolation |
| Build succeeds | Build command with exit 0 | Linter passing, "logs look good" |
| Bug fixed | Reproduce original symptom, confirm it no longer occurs | Code changed, assumed fixed |
| Regression test works | Red-green cycle: test fails without fix, passes with fix | Test passes once without verifying it can fail |
| Agent completed task | VCS diff shows correct changes | Agent self-reporting "success" |
| Requirements met | Line-by-line checklist against the plan | Tests passing alone |

## Warning Signs to Watch For

Stop and verify if you notice yourself:

- Using hedging language: "should", "probably", "seems to"
- Expressing satisfaction before running commands ("Done!", "That should do it")
- About to commit, push, or open a PR without fresh verification output
- Trusting an agent's success report without independent confirmation
- Relying on partial verification (linter passed, so build must be fine)
- Rationalizing why this case is an exception ("just this once", "I'm confident")
- Treating a previous passing run as proof of the current state

The underlying problem in each case is the same: making a claim without current evidence to support it.

## Key Patterns

**Tests:**
```
CORRECT: [Run test command] -> [See: 34/34 pass] -> "All tests pass"
INCORRECT: "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
CORRECT: Write test -> Run (pass) -> Revert fix -> Run (MUST FAIL) -> Restore fix -> Run (pass)
INCORRECT: "I've written a regression test" (without red-green verification)
```

**Build:**
```
CORRECT: [Run build] -> [See: exit 0] -> "Build passes"
INCORRECT: "Linter passed" (linter does not check compilation)
```

**Requirements:**
```
CORRECT: Re-read plan -> Create checklist -> Verify each item -> Report gaps or completion
INCORRECT: "Tests pass, phase complete"
```

**Agent delegation:**
```
CORRECT: Agent reports success -> Check VCS diff -> Verify changes -> Report actual state
INCORRECT: Trust agent report without checking
```

## Finding the Right Command

If you are unsure what command to run for verification, check these sources in the project:

- **CI config**: `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` -- shows what the CI pipeline actually runs
- **package.json**: `scripts` section (npm test, npm run build, npm run lint)
- **Makefile**: common targets like `make test`, `make build`, `make check`
- **pyproject.toml / setup.cfg**: `[tool.pytest]`, `[tool.mypy]`, `[tool.ruff]` sections; also check `scripts` in `[project.scripts]`
- **Cargo.toml**: `cargo test`, `cargo build`, `cargo clippy`
- **Project README or CONTRIBUTING docs**: often list the exact verification steps

When in doubt, look at what CI runs -- that is the authoritative set of checks.

## Why This Matters

Unverified claims cause real problems:

- Collaborators lose trust when claims turn out to be wrong
- Undefined functions or missing imports ship and crash at runtime
- Requirements get marked complete when they are not, leading to incomplete features
- Time is wasted on false completion followed by rediscovery and rework

Verification takes seconds. Recovering from false claims takes much longer.

## When To Apply

**Before these actions:**
- Claiming work is complete, tests pass, builds succeed, or bugs are fixed
- Summarizing status to a collaborator
- Committing code or creating a PR
- Closing an issue or marking a task done
- Moving on to the next task after finishing one

This does not apply to every interim statement during active work -- it applies at the boundaries where you are reporting a result or taking an action based on that result.

## The Bottom Line

Run the command. Read the output. Then claim the result.
