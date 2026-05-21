- Avoid glyphs and icons in code, comments, and CLI/log output. Stick to plain text.
- Name variables using the vocabulary practitioners use, not generic substitutes. In algorithmic trading: `bid`, `ask`, `resting_price`, `top_of_book`, `aggressor`, `liquidity`, `taker`, `maker`, `rebate`. In clinical medicine: `encounter`, `triage`, `diagnosis`, `contraindication`, `dosage`, `specimen`, `lab_result`. In logistics: `shipment`, `consignment`, `carrier`, `waybill`, `fulfillment_center`, `pick_list`, `backorder`. In digital audio: `sample_rate`, `buffer_size`, `latency`, `gain`, `clipping`, `noise_floor`, `wet_signal`. When the domain language is unclear, look it up or ask the user before naming core concepts.
- Never abbreviate names just to shorten them. Use `playbook_file` not `pb_file`, `inventory` not `inv`, `environment_response` not `env_resp`, `patient_diagnosis` not `patient_dx`, `shipment_date` not `ship_dt`, `buffer_size` not `buf_sz`, `authorization_request` not `auth_req`. Abbreviate only when the short form is accepted in the domain and the name is local in scope: `sku` in commerce, `mrn` in clinical systems, `http` in web code, `cpu` in systems code.
- Comments and docs describe what the code in front of the reader does, and why when the why is non-obvious. They do not describe what the code used to do, what it no longer does, what lives elsewhere, or what the caller must handle. A first-time reader has no context for absent behavior; enumerating non-responsibilities only makes sense as contrast with a previous version they cannot see. The code shows what it does; git history shows what it used to do. If you cannot phrase a comment as a positive statement about the present code, delete it. This is the "negative documentation" anti-pattern, and it shows up most often during refactors.

  Watch for these tells -- any of them means the comment is describing absent behavior:
    - past-tense framing: "we used to ...", "previously ...", "this no longer ..."
    - delta framing: "now handled upstream", "dedup moved to ...", "X is no longer joined here"
    - non-responsibility framing: "X is the caller's responsibility", "Y is handled elsewhere", "this does not validate Z", "integration of the result is up to the caller"

  Examples:

    BAD (past-tense): `// we used to dedupe here, but the upstream stage now guarantees uniqueness`
    GOOD: delete the comment. The function dedupes or it doesn't; the code shows which.

    BAD (delta): `// status resolution moved to the runtime layer`
    GOOD: delete the comment. If the runtime layer's role needs explaining, document it where that layer lives.

    BAD (non-responsibility): `/* Stateless converters ... integration of the resulting events (e.g. routing, status resolution) is the caller's responsibility. */`
    GOOD: `/* Stateless converters from OnixS B3 UMDF messages to macuco market data domain types. */` -- describe what the functions do; do not enumerate what they don't.

    BAD (non-responsibility, inline): `// caller must hold the session mutex`
    GOOD: if the locking contract is non-obvious and load-bearing, that is a legitimate "why" -- phrase it as a precondition the function relies on, not a chore assigned to the caller: `// precondition: session mutex is held; we read session_.next_seq without locking`

- Treat `work-in-progress/` as ephemeral feature-work space: files there appear while a feature is in flight and are deleted when the work is done. Keep references to `work-in-progress/` out of code, durable documentation, and configuration.
- When several viable approaches exist, build a decision matrix. List the candidate options and the criteria that matter (complexity, performance, reversibility, blast radius, maintenance cost, ergonomics, testability, coupling), then score each option against each criterion. Present the matrix to the user, unless one option is a clear winner.
- You are running inside an OS-level sandbox that the local agent cannot loosen. Both Claude Code and Codex CLI block their escape hatches: Claude ignores `dangerouslyDisableSandbox`; Codex disallows `danger-full-access`. Do not try to work around the sandbox -- work with it. Constraints are stable within a session; when a command is rejected, read the rejection and adjust rather than retrying variations.
- Common friction points: (1) writes outside the project root or `$TMPDIR` -- use `$TMPDIR` (never `/tmp` directly) for scratch files; (2) reads under `~/.ssh`, `~/.aws`, `~/.config/gh`; (3) network calls from bash to hosts not on the allowlist; (4) git write operations (`push`, destructive resets, `--no-verify`), blocked by a managed `PreToolUse` hook; (5) edits to `.claude/settings.json`, `/etc/claude-code/managed-settings.*`, or the project's `config/` directory. When the path forward is not obvious, consult `claude_sandbox.md` or `codex_sandbox.md`.
- Three-strikes rule. If a command keeps getting refused or failing in a way you suspect is sandbox-related, stop after the third attempt. Either ask the user to run it, or describe what you were trying and ask how to proceed. The policy does not change within a session; a fourth try will not succeed, and continued attempts burn context.
- Distinguish sandbox refusals from shell-quoting failures. A sandbox refusal says "Operation not permitted" or "Permission denied", or names a path or host the allowlist blocks. A quoting failure shows variables appearing literally in output (`$!`, `$BGPID`), `process ID list syntax error` from `ps`, or commands behaving as if a variable was empty. The sandbox isolates filesystem and network; it does not change how bash parses or expands variables. For compound commands with background processes, here-docs, or variable interpolation across statements, write a script to `$TMPDIR` with the `Write` tool and run `bash "$TMPDIR/script.sh"` instead of inlining everything in one `Bash` call.
