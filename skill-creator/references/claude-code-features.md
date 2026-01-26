# Claude Code-Specific Features

This reference documents features available when creating skills specifically for Claude Code.

## Extended Frontmatter Fields

Beyond the required `name` and `description` fields, Claude Code supports these additional frontmatter options:

### Invocation Control

```yaml
---
name: my-skill
description: Skill description here
argument-hint: <filename>           # Hint shown in autocomplete (e.g., "/my-skill <filename>")
user-invocable: false               # Hide from / menu (default: true)
disable-model-invocation: true      # Prevent Claude from auto-loading (default: false)
---
```

- `argument-hint`: Displays hint text after skill name in autocomplete
- `user-invocable`: Set to `false` to hide from the slash command menu
- `disable-model-invocation`: Set to `true` to prevent Claude from automatically loading this skill

### Tool Permissions

```yaml
---
name: deploy-skill
description: Deployment automation skill
allowed-tools:
  - Bash(npm run build)
  - Bash(npm run deploy)
  - Bash(git push*)
---
```

Tools listed in `allowed-tools` can be used without prompting for user permission. Use glob patterns for flexibility.

### Model Selection

```yaml
---
name: quick-analysis
description: Fast analysis tasks
model: haiku
---
```

Options: `haiku` (fast, cheap), `sonnet` (balanced), `opus` (highest quality). When not specified, uses the session's default model.

### Subagent Execution

```yaml
---
name: background-task
description: Runs as a subagent
context: fork
agent: general-purpose
---
```

- `context: fork`: Skill runs as a subagent in a separate context
- `agent`: Subagent type to use (`general-purpose`, `Bash`, `Explore`, etc.)

Use subagent execution for tasks that should run independently without cluttering the main conversation.

### Skill-Scoped Hooks

```yaml
---
name: commit-skill
description: Git commit workflow
hooks:
  - event: post_tool_call
    tool: Bash
    script: scripts/verify_commit.sh
---
```

Hooks can run scripts in response to events when the skill is active.

## Dynamic Context Injection

Use shell command substitution to inject dynamic content when the skill loads:

```markdown
---
name: project-aware
description: Skill with dynamic context
---

# Project-Aware Skill

Current git branch: `!git branch --show-current`

Recent commits:
`!git log --oneline -5`

Available scripts:
`!ls scripts/`
```

The `!`command`` syntax runs shell commands and injects their output before sending content to Claude. Useful for:

- Including current project state
- Listing available files or options
- Injecting environment-specific configuration

## String Substitution Variables

These variables are replaced when the skill is loaded:

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | Arguments passed after skill name (e.g., `/skill arg1 arg2` → `arg1 arg2`) |
| `${CLAUDE_SESSION_ID}` | Current session identifier |

Example usage:

```markdown
---
name: file-processor
description: Process the specified file
argument-hint: <filename>
---

# File Processor

Processing file: $ARGUMENTS

Use the session ID ${CLAUDE_SESSION_ID} for temporary file naming.
```

## Subagent Patterns

### When to Use Subagents

Use `context: fork` when:

- The task should run in the background
- You want to isolate the task from the main conversation
- The skill performs a single focused operation

### Subagent Example

```yaml
---
name: run-tests
description: Run test suite in background
context: fork
agent: Bash
allowed-tools:
  - Bash(npm test*)
  - Bash(pytest*)
---

Run the test suite and report results.
```

### Available Agent Types

| Agent | Use For |
|-------|---------|
| `general-purpose` | Multi-step tasks requiring various tools |
| `Bash` | Command execution focused tasks |
| `Explore` | Codebase exploration and searching |
| `Plan` | Architecture and implementation planning |

## Best Practices for Claude Code Skills

1. **Use `allowed-tools` sparingly** - Only pre-approve tools that are safe and essential
2. **Consider subagents for isolation** - Keep the main conversation clean
3. **Use dynamic injection wisely** - Don't inject large amounts of data
4. **Test with different models** - Ensure skill works with haiku, sonnet, and opus
5. **Document arguments clearly** - Use `argument-hint` to guide users
