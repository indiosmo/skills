---
name: make-project-skill
description: Creates a comprehensive skill for using a library or framework by exploring its documentation. Use when asked to create a skill from documentation, generate a "using-X" skill, explore library docs and compile best practices, or when the user wants to build expertise for a specific project/library. Takes a documentation URL (e.g., https://docs.streamlit.io/) and optional skill name as arguments. Produces a complete skill with idioms, patterns, caveats, and best practices extracted by parallel exploration agents.
---

# Make Project Skill

Creates a skill for a library/framework by exploring its documentation with parallel agents, then synthesizing findings into a cohesive skill.

## Workflow Overview

1. Parse arguments (docs URL, optional skill name)
2. Discover documentation structure
3. Spawn parallel exploration agents for each section
4. Collect findings into markdown files
5. Synthesize into final skill

## Step 1: Parse Arguments

From `$ARGUMENTS`, extract:
- **docs-url** (required): Documentation root URL
- **skill-name** (optional): Output skill name. Default: infer from URL (e.g., `https://docs.streamlit.io/` → `using-streamlit`)

```
Arguments: $ARGUMENTS
```

If no URL provided, ask the user.

## Step 2: Discover Documentation Structure

Fetch the main docs page with WebFetch. Identify 4-8 major sections from:
- Navigation menus/sidebars
- Table of contents
- Section headers ("Getting Started", "API Reference", "Guides", etc.)

Create a list of `{section-name, section-url}` pairs.

## Step 3: Spawn Exploration Agents

Create scratchpad directory, then spawn parallel agents:

```bash
mkdir -p {scratchpad}/findings
```

For each section, use Task tool with:
- `subagent_type: general-purpose`
- `run_in_background: true`
- Prompt: See [references/agent-prompts.md](references/agent-prompts.md) for detailed template

**Abbreviated agent prompt:**
```
Explore "{section-name}" docs at {section-url} for {library-name}.
Use WebFetch to navigate. Extract: concepts, best practices, pitfalls, code patterns, key APIs.
Write to: {scratchpad}/findings/{section-name}.md
```

**Launch all agents in parallel** - multiple Task calls in one message.

## Step 4: Collect Findings

Wait for all agents to complete. Read findings from `{scratchpad}/findings/*.md`.

Verify all expected files exist before proceeding.

## Step 5: Synthesize Skill

Spawn a synthesis agent (`subagent_type: general-purpose`) to:

1. Read all files in `{scratchpad}/findings/`
2. Initialize skill: `python3 {skill-creator}/scripts/init_skill.py {skill-name} --path {output-path}`
3. Write SKILL.md with sections: Overview, Quick Start, Core Concepts, Common Patterns, Pitfalls, Best Practices, API Reference
4. Split into `references/` if content exceeds 400 lines
5. Delete unused example files

See [references/agent-prompts.md](references/agent-prompts.md) for detailed synthesis prompt template.

## Paths Reference

- Scratchpad: Use the session scratchpad directory for findings
- Skill output: `/home/msi/workspace/skills/.claude/skills/{skill-name}/`
- Skill creator: `/home/msi/workspace/skills/.claude/skills/skill-creator/`

## Example

Input: `/make-project-skill https://docs.streamlit.io/`

Output: `/home/msi/workspace/skills/.claude/skills/using-streamlit/` with:
- `SKILL.md` - Comprehensive Streamlit usage guide
- `references/` - Detailed patterns and API docs (if needed)
