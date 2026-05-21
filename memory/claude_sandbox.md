# Claude Code sandbox

This is a reference for working inside the Claude Code sandbox without burning cycles on rejected commands. Read it the first time a sandbox refusal surprises you; do not try a sequence of variations hoping something sticks.

## Mental model

Claude Code runs every `Bash` invocation inside an OS-level sandbox: bubblewrap on Linux and WSL2, Seatbelt on macOS. The sandbox enforces filesystem and network boundaries on the bash subprocess and on every child process it spawns, including tools like `npm`, `pytest`, `kubectl`, `terraform`, and `git`. `Read`, `Edit`, and `Write` are governed by the permission system rather than the sandbox, but they share the same configured filesystem deny rules.

The current deployment uses managed settings (`claude/managed-settings.json`, relative to this repo root) that the local agent cannot loosen:

- `sandbox.enabled: true`
- `sandbox.failIfUnavailable: true` -- if the OS sandbox cannot start, commands fail rather than silently falling back to unsandboxed execution.
- `sandbox.autoAllowBashIfSandboxed: true` -- sandboxed bash runs without per-command approval prompts.
- `sandbox.allowUnsandboxedCommands: false` -- the `dangerouslyDisableSandbox` escape hatch is disabled. There is no way to "step outside" the sandbox; retrying with that flag does nothing.
- `allowManagedHooksOnly: true` plus a `PreToolUse` hook that blocks git write operations.
- `allowManagedPermissionRulesOnly: true` and `disableBypassPermissionsMode: "disable"`.

Skim the `Bash` tool description in the system prompt to see the exact allow and deny lists for the current session. The lists below describe the steady state at the time this document was written; the runtime values are authoritative.

## Filesystem

### Writable paths

Bash can write only inside these roots:

- `.` -- the current working directory and everything beneath it. This is the project root.
- `$TMPDIR` -- per-session scratch space. Always prefer this over hard-coded paths.
- `/tmp` and `/tmp/claude` (and `/private/tmp/claude` on macOS) -- system temp, available but not preferred.
- Specific dev nodes: `/dev/stdout`, `/dev/stderr`, `/dev/null`, `/dev/tty`, `/dev/dtracehelper`, `/dev/autofs_nowait`.
- Tool log directories: `~/.npm/_logs`, `~/.claude/debug`.

Within the allowed roots, these specific paths are denied:

- `~/.claude/settings.json`, `<project>/.claude/settings.json`, `<project>/.claude/settings.local.json`
- `/etc/claude-code/managed-settings.json` and `/etc/claude-code/managed-settings.d/**`
- `/mnt/c/Program Files/ClaudeCode/managed-settings.json` and `.../managed-settings.d/**` (Windows policy paths via WSL)
- `<project>/.claude/skills/**`
- `<project>/config/**`

Reading is broader than writing: the entire filesystem is readable except for these denied roots:

- `~/.ssh/**`
- `~/.aws/**`
- `~/.config/gh/**`

### Practical guidance

- **Scratch files: use `$TMPDIR`.** The base `Bash` tool description says so explicitly, and `$TMPDIR` is guaranteed to be a sandbox-writable path on every platform. Do not hard-code `/tmp/foo.json` or `~/scratch.txt`.
- **Outputs that belong with the work: write under the project root.** Anything tracked in git, anything the user will want to inspect later, anything that survives the session.
- **Do not try to edit your own configuration.** `~/.claude/settings.json`, `.claude/settings.json`, the managed-settings files, and the project's `config/` directory are intentionally blocked. If a change there is genuinely required, ask the user to make it.
- **Do not try to read credentials.** `~/.ssh`, `~/.aws`, and `~/.config/gh` are denied at the OS level. If a task seems to require reading these, you are probably solving the wrong problem -- ask the user instead.
- **Symlinks check both ends.** A symlink inside the workspace that points to `~/.ssh/id_rsa` is still blocked. Do not chase the denial by trying to read through links.

## Network

The sandbox enforces a per-session network allowlist. The current allowed hosts are visible in the `Bash` tool description (`Network: {"allowedHosts":[...]}`); they are mostly documentation hosts plus `github.com` and `raw.githubusercontent.com`. There is no general internet access from inside `bash`.

- **For arbitrary documentation, use `WebFetch` rather than `curl` or `wget`.** `WebFetch` goes through the tool layer, not the sandbox, and is governed by `WebFetch(...)` permission rules.
- **For GitHub interactions, prefer `gh` over `git`-over-HTTPS-to-an-unallowed-mirror.** `github.com` is on the allowlist, so `gh api`, `gh pr`, `gh issue`, and `git fetch origin` against a GitHub remote will work.
- **Do not retry with a different protocol or a redirect chain.** The proxy decides based on the requested hostname, not the redirected hostname; a `bit.ly` URL that ultimately resolves to an allowed host is still rejected because the request goes to `bit.ly` first.

When a network call is refused, do not iterate -- the allowlist will not change mid-session. Tell the user the host that is missing.

## Git

A managed `PreToolUse` hook runs `claude-block-git-write.sh` on every `Bash` call and blocks git operations that mutate remote state or rewrite local history in unsafe ways. Expect rejection for, at minimum:

- `git push`, `git push --force`, `git push --force-with-lease`
- `git reset --hard` against shared refs
- `git rebase` / `git commit --amend` of published commits
- Anything passed with `--no-verify` or `--no-gpg-sign`

Read commands (`git status`, `git log`, `git diff`, `git show`, `git fetch`) are unaffected. Local commits and `git add` are unaffected. If you genuinely need a blocked operation, ask the user to run it.

## Multi-statement bash and shell expansion

This is a sharp edge that is often misread as a sandbox refusal. Long compound commands -- especially ones with `&`, `$!`, here-docs, embedded quoting, and `for`-loops over `/proc/$BGPID/task/*` -- frequently fail because of how the command string is constructed, escaped, and re-entered into bash, not because the sandbox blocked anything.

The sandbox uses bubblewrap (Linux/WSL2) or Seatbelt (macOS) to isolate filesystem and network access. Neither tool intercepts bash, modifies its parser, or changes how variables expand. If `$!` or `$BGPID` is showing up literally in the output, that is a quoting problem in the command string, not the sandbox. Reasoning like "I'm sandboxed and `$!` isn't expanding" or "the sandbox is preventing variable expansion" is wrong and will lead you down a dead end -- there is no plausible mechanism for sandboxing to cause that symptom.

Telltale signs that the failure is shell-side and not sandbox-side:

- Variables appear literally in the output (`$BGPID`, `$!`) instead of expanding.
- `ps` rejects an argument with `process ID list syntax error` (the variable expanded to empty).
- `cat: '/proc/$!/wchan': No such file or directory` (path is literal).
- No "Operation not permitted" or "Permission denied" anywhere in the output.
- The same command works when broken into separate `Bash` calls.

When the diagnostic logic is non-trivial, write the script to a file under `$TMPDIR` with the `Write` tool and run it with `bash "$TMPDIR/diag.sh"`. That keeps quoting predictable and makes the script reusable and debuggable.

**Use the `Write` tool, not `cat <<'EOF'` inside a `Bash` call.** Writing a script via a heredoc inside `Bash` re-introduces the same quoting and indentation problems you are trying to escape: the heredoc body inherits any leading whitespace from the prompt formatting, which can shift the shebang off column 0 and cause the kernel to fall back to `/bin/sh` or fail to recognise the script entirely. The `Write` tool puts exact bytes on disk -- no quoting layer, no indentation leakage, no shebang offset.

```bash
# Anti-pattern: complex compound command relying on $! across statements
some_long_running_test & BGPID=$!; sleep 3; ps -p $BGPID; ...

# Anti-pattern: heredoc-via-Bash to write the script
# cat > /tmp/diag.sh <<'EOF'
#   #!/bin/bash
#   ...
# EOF
# Indentation in the surrounding prompt can prefix every line, including #!.

# Recommended: Write the script via the Write tool, then:
bash "$TMPDIR/diag.sh"

# Acceptable alternative: inline with single-quoted bash -c
bash -c '
  some_long_running_test > "$TMPDIR/bg.log" 2>&1 &
  PID=$!
  sleep 3
  ...
'
```

## When a command is refused

1. Read the rejection. The harness states which path or host was blocked.
2. Match it to the rules above. Most refusals fall into one of: denied write path, denied read path, non-allowlisted host, blocked git operation, or hook block.
3. Pick the correct response:
   - Denied write -> move the output to `$TMPDIR` or the project root.
   - Denied read -> stop. Ask the user.
   - Non-allowlisted host -> use `WebFetch` for docs, or ask the user to allow the host.
   - Blocked git write -> ask the user to run it.
   - Hook block -> the message will quote the rule; respect it.
4. Do not iterate variations of the same command hoping to slip past the sandbox. The constraints are stable for the session.
5. **Three-strikes rule.** If after three attempts you still cannot get the command through, stop. Ask the user to run it themselves, or describe what you were trying to do and ask how they would like to proceed. Continued retries do not help -- the policy will not change mid-session, and the wasted attempts consume context that would be better spent on the actual task.
