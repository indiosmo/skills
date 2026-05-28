# Codex CLI sandbox

This is a reference for working inside the Codex CLI sandbox without burning cycles on rejected commands or unnecessary approval prompts. Read it the first time a refusal or approval request surprises you; do not iterate workarounds blindly.

## Mental model

Codex CLI wraps every tool call in an OS-level sandbox and runs a managed approval policy on top of it. The two layers are independent:

- **Sandbox mode** sets the boundary: what filesystem and network access is permitted at all.
- **Approval policy** decides what happens when the agent wants to cross that boundary.

The current deployment is configured by `codex/requirements.toml` (relative to this repo root):

- `allowed_sandbox_modes = ["read-only", "workspace-write"]` -- `danger-full-access` is not available. There is no way to disable the sandbox.
- `allowed_approval_policies = ["on-request"]` -- the agent runs under `on-request`. Commands inside the boundary execute without prompting; commands that cross the boundary fall back to an approval prompt.
- `allowed_approvals_reviewers = ["user"]` -- approvals go to the user, not to an auto-reviewer. There is no `auto_review` agent silently approving things on your behalf.
- A managed `PreToolUse` hook (`/etc/codex/hooks/codex-block-git-write.sh`) intercepts every `Bash` call and blocks git operations that mutate remote state or unsafely rewrite history.

## Sandbox modes

### read-only

Files can be read. Edits and command execution require approval. Use this when the task is purely investigative.

### workspace-write (default)

- Read and edit any file in the current workspace.
- Run routine local commands (build, test, lint, format) without prompting.
- Editing files **outside** the workspace requires approval.
- Network access requires approval.
- Three paths are read-only **regardless of mode**: `.git`, `.agents`, and `.codex`. The hook layer also blocks remote-changing git operations even when a write to `.git` would be allowed.

The "workspace" is the directory Codex was launched in. Treat anything outside that subtree as out-of-bounds without an approval round trip.

## Approval policy

Under `on-request`:

- **No prompt:** reads in `read-only` mode; reads, edits inside the workspace, and routine local commands in `workspace-write` mode.
- **Prompt the user:** edits outside the workspace, network access, commands flagged as "destructive" by an MCP tool, and any operation that crosses the sandbox boundary.
- **Denied outright by the hook:** the git write operations enumerated below; these never produce an approval prompt -- they fail.

The user is the reviewer. Plan for the cost of a round trip when you need to step outside the sandbox; batch boundary-crossing work where possible and tell the user up front what you intend to ask for.

## Filesystem

Things that work without an approval prompt:

- Reads anywhere the underlying OS permits.
- Edits to any file under the workspace root, except `.git`, `.agents`, `.codex`.
- Writes to the system temp directory (`$TMPDIR`) and to in-workspace scratch directories.

Things that prompt for approval:

- Writes outside the workspace, including the user's home directory and other repositories.
- Reads or writes of files the user has explicitly marked read-only via configuration.

Practical guidance:

- **Use `$TMPDIR` for scratch files.** It is sandbox-writable and ephemeral. Hard-coded `/tmp/foo.json` may also work but is less portable.
- **Keep durable outputs inside the workspace.** Anything you want to live past the session goes under the project root.
- **Do not write to `.git`, `.agents`, or `.codex`.** They are read-only by policy. Use `git` (without remote-mutating verbs) to interact with the repository.
- **Avoid blanket reads of `~`.** If a task seems to require reading credentials, configuration, or another repository, surface the question to the user instead of probing.

## Network

Network access prompts for approval in `workspace-write` mode. Practical implications:

- A single multi-step task that needs the network (fetch docs, install deps, hit an API) should describe up front what it will do, so the user can approve once and you can proceed.
- For documentation lookups, prefer MCP-provided tools (e.g. context7, Ref) where they exist, because they go through the tool layer rather than asking the user per request.
- For GitHub interactions, prefer `gh` over raw HTTPS. `gh` is the standard interface and the hook layer is calibrated for it.

When the user denies a network request, do not retry with a different URL or a different tool. Ask them what they would like instead.

## Git

The `codex-block-git-write.sh` hook blocks commits, remote-mutating operations, and history-rewriting operations. Expect rejection for, at minimum:

- `git commit`
- `git push`, `git push --force`, `git push --force-with-lease`
- `git reset --hard` against shared refs
- `git rebase` and `git commit --amend` of published commits
- Anything passed with `--no-verify` or `--no-gpg-sign`

Reads (`git status`, `git log`, `git diff`, `git show`, `git fetch`) and staging (`git add`) are unaffected. The hook fails the call rather than queueing it for approval; if you need a blocked operation, ask the user to run it directly.

## Multi-statement bash and shell expansion

A common source of confusion: a long compound command fails, the output mentions strange syntax errors or empty paths, and it looks like sandbox enforcement -- when in fact the command was mangled by quoting. The Codex sandbox isolates filesystem and network access; it does not intercept bash or change how variables expand. Reasoning like "I'm sandboxed and `$!` isn't expanding" is wrong -- the two are independent layers.

Telltale signs that the failure is shell-side and not sandbox-side:

- Variables appear literally in the output (`$BGPID`, `$!`) instead of expanding.
- `ps` rejects an argument with `process ID list syntax error` (the variable expanded to empty).
- `cat: '/proc/$!/wchan': No such file or directory` (path is literal).
- No approval prompt and no "Operation not permitted" anywhere in the output.
- The same command works when broken into separate `Bash` calls.

When the diagnostic logic is non-trivial, write the script to a file under `$TMPDIR` (or under the workspace) and run it with `bash "$TMPDIR/diag.sh"`. That keeps quoting predictable and makes the script reusable.

**Use the file-writing tool, not `cat <<'EOF'` inside a `Bash` call.** Writing a script via a heredoc inside `Bash` re-introduces the same quoting and indentation problems you are trying to escape: leading whitespace from the surrounding prompt can shift the shebang off column 0 and cause the kernel to fall back to `/bin/sh` or fail to recognise the script entirely. A direct write puts exact bytes on disk -- no quoting layer, no indentation leakage, no shebang offset. If you must do it inline, prefer `bash -c '...'` with single quotes around the body so the outer wrapping cannot touch `$!` or other special variables.

## When a command is refused or prompts unexpectedly

1. Read the message. Codex distinguishes between "needs approval" (boundary crossing) and "blocked" (hook or sandbox refusal).
2. Match it to the rules above. Most events fall into: write outside workspace, network access, git write blocked by hook, or write to `.git` / `.agents` / `.codex`.
3. Pick the response:
   - Write outside workspace -> reroute the write inside the workspace or to `$TMPDIR`. If it must be outside, ask the user once with full context.
   - Network -> ask the user with a clear statement of which host and why.
   - Git write blocked -> ask the user to run it.
   - `.git` / `.agents` / `.codex` -> stop. Use the proper tool (`git`, the agent config UI, etc.) instead of direct file edits.
4. Do not iterate variations to slip past the boundary. Within a session the policy is stable; the next attempt will be refused the same way.
5. **Three-strikes rule.** If after three attempts you still cannot get the command through (refused, blocked, or wedged), stop. Ask the user to run it themselves, or describe what you were trying to do and ask how they would like to proceed. Continued retries do not help, and the wasted approval round trips burn the user's attention along with your context.
