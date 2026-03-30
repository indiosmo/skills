# Runbooks

A runbook is a step-by-step procedure for an operational task. It answers: how do I do this
specific thing, right now, without having to figure it out from scratch?

Runbooks are for tasks that are performed infrequently enough that the steps will be forgotten
between occurrences, or that touch shared systems where getting a step wrong has real
consequences. The reader is often in the middle of doing the thing -- they need clear, actionable
steps, not background reading.

## When to write a runbook

Write a runbook when a procedure:

- Involves multiple steps that must happen in order
- Touches production, shared infrastructure, or other people's environments
- Is performed rarely enough that the operator will not remember the steps
- Has consequences if done wrong (data loss, downtime, inconsistent state)
- Currently lives only in one person's head

Common triggers: server setup, emergency config changes, certificate rotation, database
migrations, disaster recovery, service deployments, export/import workflows, on-call handoff
procedures.

Do not write a runbook for a single command. If the procedure is `just deploy`, document that
in the README's common workflows section, not in a separate runbook.

## Structure

A runbook has two parts: context (what this is and how it works) and procedure (what to do).

### Context first

Start with a brief paragraph explaining what the procedure operates on and how the system
behaves. This is not background reading -- it is operational context that prevents the reader
from blindly following steps without understanding what they are doing.

Good context answers: what is the mechanism? Where do the relevant files live? What is the source
of truth?

**Example:**
```markdown
# Grafana Dashboard Workflow

Provisioned dashboards live in `infra/grafana/dashboards/<folder>/` and are loaded on
startup. Each folder corresponds to a provider defined in the provisioning config. UI-created
dashboards are unaffected -- you can freely create and edit them.
```

This tells the reader: what provisioned dashboards are, where they live, how they load, and what
is safe to touch. Now the numbered steps make sense.

### Procedures as numbered steps

After the context, break the runbook into self-contained procedures, each under its own heading.
A runbook can contain several related procedures -- for example, "exporting dashboards," "adding
a new dashboard," and "editing a provisioned dashboard" are all part of the same workflow.

Each procedure uses numbered steps:

```markdown
## Adding a new provisioned dashboard

1. Build the dashboard in the Grafana UI (create panels, queries, etc.)
2. Run `just grafana-export` to pull it to disk, or manually export the JSON and save it to
   `infra/grafana/dashboards/<folder>/<name>.json`
3. Commit and push
4. On next `docker compose up`, Grafana loads it automatically into the corresponding folder
5. Delete the UI draft if you want to avoid duplicates
```

Guidelines for steps:

- **One action per step.** "Edit the file and restart the service" is two steps.
- **Include the exact command** with placeholders for variable parts (hostname, environment,
  file path). Use `<placeholder>` notation.
- **State what success looks like** after non-trivial steps. "The output should show `Status:
  active`." This gives the operator a checkpoint before proceeding.
- **Use inline code** for commands, paths, environment variables, and config values.
- **Use code blocks** when showing a multi-line command or output example.

### Prerequisites

If the procedure requires specific tools, access, or environment state, mention it early --
either as a note right after the context paragraph or as the first step. Do not bury
prerequisites in step 4.

**Inline prerequisite:**
```markdown
Requires `GRAFANA_ADMIN_PASSWORD` set in `.env`.
```

**First-step prerequisite:**
```markdown
1. Ensure you have SSH access to the target server and sudo privileges
2. ...
```

Keep prerequisites minimal. If the reader needs a full setup guide before they can run the
procedure, link to the getting-started docs rather than restating them.

### Fallback procedures

When the primary procedure depends on tooling that might not be available (a CLI tool, local
setup, network access), provide a manual fallback. Frame it as an alternative, not an
afterthought:

```markdown
### Manual export

If you cannot run `just grafana-export` (e.g., no local tooling, remote-only access):

1. Open the dashboard in Grafana
2. Go to Dashboard settings > JSON Model (or Share > Export > Save to file)
3. Remove the `id` and `version` fields from the JSON to keep diffs clean
4. Save to `infra/grafana/dashboards/<folder>/<name>.json`
```

This pattern -- automated path first, manual path as a named alternative with an explicit
condition -- respects the reader's time while covering the failure mode.

### Behavior documentation

For procedures that interact with automated systems (init containers, provisioning, cron jobs),
include a section that explains what the system does on its own. This prevents the operator from
manually doing something the system already handles, or from being surprised when the system
overwrites their work.

```markdown
## Behavior on restart

- Empty `.ndjson` (no exports yet): init container logs a skip message and exits
- Non-empty `.ndjson`: imports all objects, overwriting any with matching IDs
- UI edits not re-exported: overwritten on next restart (git is the source of truth)
```

### Convergence warnings

When a procedure involves a manual change to a system that is also managed by automation
(Ansible, Terraform, CI/CD), warn about convergence. If the operator edits a config file by
hand but does not update the automation source, the next automated run will overwrite the change.

```markdown
**Important:** Update the Ansible role/template to match, then re-run the playbook to confirm
convergence. Otherwise the next Ansible run will overwrite your change.
```

### File reference section

End the runbook with a section listing the key files involved. This gives the reader a quick
reference for where to look when debugging or extending the procedure.

```markdown
## Files

- Saved objects export: `infra/elk/kibana/saved-objects/all.ndjson`
- Init script: `infra/elk/init/init-kibana-objects.sh`
- Init container: `kibana-init` in `infra/elk/docker-compose.yml`
```

## Naming and organization

Store runbooks in `docs/runbooks/` (or wherever the project keeps them). Use descriptive
kebab-case filenames that communicate the procedure:

```
docs/runbooks/
  new-server-setup.md
  emergency-config-edit.md
  grafana-dashboard-workflow.md
  certificate-rotation.md
```

Name runbooks after the task, not the system. "certificate-rotation" is better than "ssl-stuff"
because the reader scans by what they need to do, not what system they happen to be touching.

## Scope

Keep each runbook focused on one procedure or one tightly related set of procedures. A runbook
for "Grafana Dashboard Workflow" that covers exporting, adding, and editing dashboards is
cohesive. A runbook that covers "all Grafana things" (dashboards, alerts, users, datasources)
is too broad -- split it.

If a procedure has a sub-procedure that is also performed independently, give the sub-procedure
its own runbook and link to it. Do not nest runbooks inside runbooks.

## Tone

Runbooks are written for someone who is in the middle of doing something. Be direct. Use
imperative mood. Do not explain the history of the system or justify the architecture -- that
belongs in a README or ADR.

Good: "Run the bootstrap playbook from the control machine."
Bad: "The bootstrap playbook, which was introduced in Q2 to streamline the server provisioning
process, should be executed from the control machine."

The reader is an operator, not a student. Give them what they need to act.
