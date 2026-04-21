# Role Composition: Dependencies, Ordering, and Deduplication

How you compose roles -- what depends on what, what runs before what -- has significant consequences for predictability, performance, and maintainability. The patterns below are drawn from the Ansible 2.16+ docs and established community guidance.

## Table of Contents

- [Three Ways to Compose Roles](#three-ways-to-compose-roles)
- [When to Use Which](#when-to-use-which)
- [Two Meta-Dependency Gotchas](#two-meta-dependency-gotchas)
- [The "Base Role Runs N Times" Problem](#the-base-role-runs-n-times-problem)
- [Role Variable Surface](#role-variable-surface)
- [Circular Dependencies](#circular-dependencies)
- [Summary](#summary)
- [Sources](#sources)

## Three Ways to Compose Roles

### 1. `meta/main.yml` dependencies (static)

```yaml
# roles/web_app/meta/main.yml
dependencies:
  - role: common
  - role: nginx
```

Dependencies run *before* the main role's tasks. They cannot be conditioned with `when:`. They always fire when the role is invoked via `roles:`.

### 2. `roles:` keyword in a play (static)

```yaml
- hosts: webservers
  roles:
    - common
    - nginx
    - web_app
```

Roles run in listed order. Each role's `meta` dependencies still fire before the role itself.

### 3. `include_role` / `import_role` in tasks (static or dynamic)

```yaml
- hosts: webservers
  tasks:
    - name: Apply common baseline
      ansible.builtin.include_role:
        name: common
      when: apply_baseline | default(true)
```

Task-level inclusion supports `when:`, loops, and conditional name selection. `include_role` is dynamic (resolved at runtime); `import_role` is static (resolved at parse time). Notably, role *dependencies* are NOT executed when you use `include_role` or `import_role` -- only the `roles:` keyword triggers meta deps.

## When to Use Which

| Use | For |
|---|---|
| `meta/main.yml` deps | **Hard, unconditional prerequisites.** Role B genuinely cannot function without role A. Example: `aogw_telemetry` requires `vector` installed. |
| `roles:` in playbook | **Default composition.** Ordinary "apply these roles to these hosts" layering. Most visible ordering. |
| `include_role` in tasks | **Conditional or programmatic inclusion.** You need `when:`, loops, or to pass runtime-computed role names. |

Reserve `meta` deps for the first case. For everything else, compose at the playbook level -- the sequence is visible in one place, and operators can understand the apply order without jumping across role directories.

## Two Meta-Dependency Gotchas

### 1. Meta deps cannot be gated

From the Ansible docs: *"Ansible does not execute role dependencies when you include or import a role; you must use the `roles` keyword if you want Ansible to execute role dependencies."*

A `when:` at the meta level is ignored -- the dependency always runs. If you need conditional composition, use `include_role` in tasks, not `meta/main.yml`.

### 2. Silent deduplication via lazy evaluation

From the docs: *"Role de-duplication occurs before variable evaluation. This means that Lazy Evaluation may make seemingly different role invocations equivalently the same, preventing the role from running more than once."*

If you pass different variables to the same role from two places and expect it to run twice, dedup may still collapse both invocations because the variables haven't been evaluated yet at dedup time. Explicit playbook ordering makes the intended sequence obvious and is less prone to this class of surprise.

## The "Base Role Runs N Times" Problem

A common scenario: one host belongs to several functional groups (web, db, telemetry, ...), a top-level `site.yml` imports one `*-deploy.yml` per group, and each playbook has a `base` role in its `roles:` list. Result: `base` runs N times on that host in one apply.

From the docs: *"deduplication happens ONLY at the play level, so multiple plays in the same playbook may rerun the roles."*

Each imported playbook is a separate play, so Ansible's built-in dedup does not help across them.

### Idiomatic fix: one baseline play, function-specific plays without the base

```yaml
# site.yml
- name: Baseline every host
  hosts: all
  roles:
    - base

- name: Deploy web tier
  hosts: webservers
  roles:
    - web_app   # no base here; it ran above

- name: Deploy db tier
  hosts: dbservers
  roles:
    - db_app
```

`base` runs once per host, regardless of how many functional groups the host belongs to. The structure is explicit, visible, and needs no Ansible magic.

### Tradeoff

Running a single function-specific playbook standalone no longer implicitly baselines. Three acceptable ways to handle this:

- Document that baseline must run first. Cheapest, relies on operator discipline.
- Provide a wrapper (e.g., a `just` recipe) that chains baseline + the target playbook. Best UX.
- Accept that `site.yml` is the canonical entry point and standalone runs are only for tight-loop iteration on a single tier where re-baselining is unnecessary.

### Anti-patterns (don't reach for these first)

| Pattern | Why it's inferior |
|---|---|
| Play-scoped fact guard (`set_fact: base_applied: true` + `when:` skip) | Fragile; hides the structure problem; any forgotten `set_fact` reset breaks it. |
| `run_once: true` on base tasks | Wrong semantic -- runs once *across all hosts*, not once *per host*. |
| Tags + conditional invocation | Shifts the burden to every operator every time; easy to forget and silently re-run. |

Each of these can be made to work, but they paper over a structural issue that the play-level refactor solves cleanly and permanently.

## Role Variable Surface

A role consumes variables from two structurally different places, and each has its own home file:

- **Role-owned variables** (prefixed with the role name) live in `defaults/main.yml` with sensible defaults. This file is the single source of truth for what the role can be tuned with and what those defaults are.
- **Upstream variables** (values that come from `group_vars`, `host_vars`, or another role's output) are declared in `meta/argument_specs.yml` with a `type`, `required: true` (or `required: false` plus `default:` when the role must stay safe with the variable unset), and `choices` where applicable. They are NOT mirrored into `defaults/main.yml`.

Prefix every role-owned variable with the role name to avoid collisions across roles invoked in the same play:

```yaml
# BAD -- collides with other roles
port: 8080

# GOOD -- namespaced
myapp_port: 8080
```

### External contract via `meta/argument_specs.yml`

For upstream variables, declare them in `meta/argument_specs.yml`. Ansible validates the spec before `tasks/main.yml` runs, so a missing required variable or a wrong-typed value fails fast at the top of the role with a clear message, rather than surfacing later as an obscure Jinja traceback deep inside a template.

```yaml
# roles/consumer/meta/argument_specs.yml
---
argument_specs:
  main:
    short_description: Consume an upstream service port and deploy environment.
    options:
      upstream_service_port:
        description: TCP port the upstream service listens on.
        type: int
        required: true
      deploy_environment:
        description: Deployment environment name.
        type: str
        required: true
        choices:
          - dev
          - uat
          - prod
```

Tasks and templates then reference the upstream name directly: `{{ upstream_service_port }}`, `{{ deploy_environment }}`. Do not wrap upstream variables in a role-namespace alias (`consumer_upstream_service_port: "{{ upstream_service_port }}"`) inside `defaults/main.yml` just to document the dependency -- argument_specs is where that documentation belongs.

Keep descriptions short: state what the variable is for. Do not list which other roles consume the same variable (the argument_specs files themselves are the source of truth for that) and do not restate the convention in a file-header comment on every spec (it belongs in the skill, not in each role). `required: true` and `default:` are mutually exclusive at runtime -- if an upstream variable is optional, use `required: false` with a `default:`.

### Disjoint-keyset rule

`defaults/main.yml` and `meta/argument_specs.yml` must have disjoint key sets. A variable is either role-owned (defaults) or upstream (argument_specs), never both. Ansible does not enforce this -- drift between the two files is avoided by the convention itself, not by tooling. Treat a variable appearing in both as a review-time bug.

### What argument_specs catches

At role entry, Ansible checks that every `required: true` option is defined, that values match the declared `type`, and that they fall within declared `choices`. It does NOT catch a variable that is referenced in tasks/templates but declared in neither file, and it does not catch a variable listed only in `defaults/main.yml` that should have been in argument_specs (or vice versa).

### Linting

The ansible-lint `role-argument-spec` rule requires every role to ship a `meta/argument_specs.yml`. A role with no upstream dependencies still needs the file, even if `options:` is empty.

### Vault indirection is unchanged

argument_specs does not replace the vault pattern. Secrets still flow through a plaintext name in `group_vars/<group>/vars.yml` aliasing an encrypted value in `group_vars/<group>/vault.yml`. If a secret is also an upstream variable the role depends on, declare the plaintext name in argument_specs -- the encrypted `vault_*` name stays internal to the inventory.

## Circular Dependencies

If role A needs something from role B and role B needs something from role A, do not resolve the cycle with mutual `meta` deps. Ansible has no notion of "run A partially, then B, then A's remainder", and the cycle usually signals that the two roles share a concern that wants to live in a third place.

### Canonical fix: extract the shared concern

Factor the shared bits into a third role C, and have both A and B depend on (or sequence after) C. Neither depends on the other.

```
before:   A <-> B                (cycle)
after:    A --> C    B --> C     (both depend on shared base)
```

Typical extractable concerns: TLS trust stores, shared system users, directory layouts, lock files, shared variables.

### When extraction is wrong

If the "cycle" is actually a sequencing requirement -- A produces a value, then B consumes it, then A uses B's output -- split the work across ordered plays rather than forcing it into role metadata. Play 1 runs A's producer tasks; play 2 runs B; play 3 runs A's consumer tasks. Use `hostvars`, facts, or an external store to pass values between plays.

This is common with certificate authorities, service discovery, and secrets managers: the CA/bootstrap server must exist before its clients can trust it, and the clients' trust state must be set before any role that talks to the CA over TLS runs. Split across plays, not tangled meta deps.

## Summary

- `meta/main.yml` deps: hard, unconditional prereqs only.
- Everything else: sequence in the playbook, or use `include_role` in tasks for conditional inclusion.
- Base role shared across functional groups: one `hosts: all` baseline play, then function plays without the base.
- Role-owned variables live in `defaults/main.yml` with a role-name prefix; upstream variables live in `meta/argument_specs.yml` with type and `required`/`default`. Keep those two files' key sets disjoint.
- Circular deps: extract shared state into a third role, or split producer/consumer across ordered plays.

## Sources

- [Ansible Playbook Guide: Using role dependencies](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_reuse_roles.html#using-role-dependencies)
- [Ansible Playbook Guide: Running role dependencies multiple times in one play](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_reuse_roles.html#running-role-dependencies-multiple-times-in-one-play)
- [ansible.builtin.include_role module](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/include_role_module.html)
