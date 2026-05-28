# Cursor sandbox

This is a reference for working inside Cursor Agent with this repository's project-level sandbox and hooks.

## Mental model

Cursor has three separate control layers:

- **Sandbox** sets the process boundary for terminal commands. In this repository, `.cursor/sandbox.json` gives sandboxed commands read/write access to the workspace and no extra read/write paths.
- **Hooks** enforce command policy before tools run. `.cursor/hooks.json` registers `.cursor/hooks/block-git-write.sh` for shell commands.
- **Rules** guide the model. `.cursor/rules/sandbox-policy.mdc` tells Cursor about the same policy, but rules are not enforcement.

Use all three layers together. The sandbox handles filesystem boundaries, the hook blocks git writes, and the rule helps the agent avoid predictable refusals.

## Recommended Cursor settings

Use these editor settings for the policy this repository expects:

- Auto-Run Mode: `Run in Sandbox`
- Auto-run network access: `sandbox.json Only`
- External-File Protection: enabled
- File-Deletion Protection: enabled
- Dotfile Protection: enabled
- Command Allowlist: keep empty unless you deliberately want a command to run outside the sandbox without approval
- Run Everything: disabled

Cursor's command allowlist is an approval convenience, not the primary security boundary. Keep commands in the sandbox by default.

## Filesystem

The project sandbox is configured as `workspace_readwrite` with:

- no `additionalReadwritePaths`
- no `additionalReadonlyPaths`
- `disableTmpWrite: true`
- no network domains in `networkPolicy.allow`

Practical guidance:

- Open the repository root as the Cursor workspace. The sandbox boundary follows the opened workspace.
- Keep generated files, diagnostics, and scratch outputs inside the workspace.
- Do not write to `/tmp`, `$TMPDIR`, the home directory, or another checkout from Cursor Agent. This differs from the Claude and Codex guidance because this Cursor profile disables temp writes to match the "no writes outside the workspace" policy.
- If a task needs external files, ask the user to copy them into the workspace or approve a different workflow.

## Git

The Cursor hook blocks shell commands that contain:

- `git commit`
- `git push`
- `git reset`
- `git rebase`
- `--no-verify`
- `--no-gpg-sign`

Read-only git commands such as `git status`, `git diff`, `git log`, and `git show` remain available. `git add` is not blocked by the hook, but the project rule tells agents to leave changes unstaged unless the user asks for staging.

If the hook blocks a command, do not retry the same operation through an alias, another working directory, or a wrapper. Ask the user to run the git operation.

## Network

The project sandbox file denies network access by default. To make that effective in Cursor's editor UI, set Auto-run network access to `sandbox.json Only`. Other Cursor network modes can add built-in defaults or allow all sandboxed network access.

If a task needs network access, tell the user which host is needed and why. Do not add domains to the project sandbox file as a side effect of a feature task.

## Troubleshooting

If a command behaves unexpectedly:

1. Check Cursor Settings > Hooks and the Hooks output channel to confirm the project hook loaded.
2. Restart Cursor after changing hook files.
3. Confirm the workspace is trusted. Cursor only runs project hooks in trusted workspaces.
4. Confirm the repository root, not a parent directory such as the home directory or filesystem root, is the opened workspace.
5. On Linux or WSL, confirm the sandbox is available. Cursor's terminal documentation requires Linux kernel 6.2 or later with Landlock v3 support and unprivileged user namespaces.
6. Stop after three failed attempts with the same refusal. The policy is stable within a session.
