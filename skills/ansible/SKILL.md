---
name: ansible
description: "Write, review, and debug Ansible automation: playbooks, roles, inventories, and using collections with idiomatic patterns, security hardening, and testing. Use when creating or modifying Ansible playbooks and roles, reviewing Ansible code for best practices, setting up ansible-lint or Molecule testing, organizing Ansible repositories, managing secrets with Vault, hardening privilege escalation, or troubleshooting Ansible automation. Triggers on: Ansible playbooks, roles, inventories, YAML automation files, ansible-lint configs, Molecule test scenarios, Ansible Vault, group_vars, host_vars."
---

# Authoring Ansible

## Project Layout

Roles are the primary organizational unit. Use dimensional groups (what/where/when) in a single inventory and target with `--limit`.

```
ansible-project/
  ansible.cfg
  requirements.yml          # pinned collection/role versions
  site.yml                  # master playbook (imports tier playbooks)
  playbooks/
    webservers.yml
    dbservers.yml
  inventory/
    hosts.yml               # dimensional groups: what/where/when
    group_vars/
      all/
        vars.yml            # plaintext variables
        vault.yml           # ansible-vault encrypted
      webservers.yml
    host_vars/
      db01.yml
  roles/
    common/
      defaults/main.yml     # user-overridable defaults (low precedence)
      tasks/main.yml
      handlers/main.yml
      templates/
      files/
      vars/main.yml         # internal constants (high precedence)
      meta/main.yml
    nginx/
    myapp/
  molecule/                 # or per-role molecule/ dirs
  .ansible-lint
  .yamllint
```

- `group_vars/{group}/vars.yml` + `vault.yml` keeps variable names visible while values stay encrypted (vault indirection pattern).
- `site.yml` imports tier playbooks; run `ansible-playbook site.yml --limit webservers` for targeted execution.

## Inventory Management

Prefer YAML over INI -- INI has inconsistent type parsing between inline host vars and `:vars` sections.

Always use aliases for hosts. The left-hand inventory name is what you reference in playbooks, logs, and `--limit`; `ansible_host` holds the actual connection target. This decouples automation logic from infrastructure details.

Organize hosts along three dimensions -- function (webservers, dbservers), location (east, west), and lifecycle (prod, staging) -- then target with intersection patterns (`--limit "webservers:&prod"`) instead of creating combinatorial group names. Use `children:` only when one group genuinely contains another.

Debug inventory with `ansible-inventory --graph` (hierarchy), `--list` (full JSON), or `--host <name>` (merged variables). Add `-vvv` to trace variable sources.

See [references/inventory.md](references/inventory.md) for YAML/INI syntax, aliases, group hierarchies, host patterns, debugging, group design patterns, and common mistakes.

## Linting Setup

### .ansible-lint

```yaml
---
profile: moderate  # good starting point; bump to safety for stricter enforcement

exclude_paths:
  - .cache/
  - .git/
  - molecule/

warn_list:
  - experimental
```

The `safety` profile is the strictest fully-implemented profile. `shared` and `production` contain rules not yet enforced.

Run: `ansible-lint` (auto-discovers playbooks). Fix auto-fixable violations: `ansible-lint --fix`.

### .yamllint

ansible-lint runs yamllint internally. A separate `.yamllint` is only needed to customize YAML rules beyond ansible-lint defaults:

```yaml
---
extends: default
rules:
  line-length:
    max: 160
    level: warning
  truthy:
    allowed-values: ["true", "false"]
    check-keys: false
  indentation:
    spaces: 2
    indent-sequences: true
  comments:
    min-spaces-from-content: 1
  comments-indentation: disable
  document-start: disable
  octal-values:
    forbid-implicit-octal: true
    forbid-explicit-octal: true
  braces:
    min-spaces-inside: 0
    max-spaces-inside: 1
```

When providing a custom `.yamllint`, the `braces`, `comments.min-spaces-from-content`, and `octal-values` settings above are required for ansible-lint compatibility.

See [references/linting.md](references/linting.md) for the full rule catalog, profiles, CI/CD integration, and skip mechanisms.

## Playbook Authoring

### Essentials

Always use FQCN (Fully Qualified Collection Name), name every task, use `true`/`false` (not `yes`/`no`), quote file modes, set explicit state:

```yaml
---
- name: Deploy web application
  hosts: webservers
  gather_facts: true

  tasks:
    - name: Install nginx
      ansible.builtin.apt:
        name: nginx
        state: present    # always explicit, even when it's the default
        update_cache: true
        cache_valid_time: 3600
      become: true

    - name: Deploy nginx config
      ansible.builtin.template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        mode: "0644"       # always quoted string
        owner: root
        group: root
      become: true
      notify: Restart nginx

  handlers:
    - name: Restart nginx
      ansible.builtin.systemd:
        name: nginx
        state: restarted
      become: true
```

### Variable precedence

Know these tiers (lowest to highest):

| Tier | Where | Use for |
|------|-------|---------|
| Role defaults | `roles/x/defaults/main.yml` | Sensible defaults users override |
| Inventory group vars | `group_vars/` | Environment/group-specific values |
| Inventory host vars | `host_vars/` | Host-specific overrides |
| Play vars / vars_files | `vars:` in play | Play-scoped values |
| Role vars | `roles/x/vars/main.yml` | Internal constants (hard to override) |
| include_vars / set_fact | Dynamic | Runtime-computed values |
| Extra vars (`-e`) | CLI | Always wins |

Gotchas:
- `defaults/main.yml` (tier 1) vs `vars/main.yml` (tier 5) -- vastly different precedence despite similar locations. Use `defaults/` for user-configurable values; `vars/` for constants.
- `set_fact` beats almost everything except extra vars. A stray `set_fact` can silently override inventory variables.
- Child groups beat parent groups. `group_vars/webservers.yml` beats `group_vars/all.yml`.

### import_tasks vs include_tasks

| | `import_tasks` (static) | `include_tasks` (dynamic) |
|---|---|---|
| Parsed at | Playbook load time | Runtime |
| Works with `--list-tasks` | Yes | No |
| Supports loops | No | Yes |
| `when:` behavior | Applied to every imported task individually | Evaluated once on the include itself |
| Handler visibility | Visible outside | NOT visible outside -- handlers defined in a dynamically included file cannot be notified from tasks outside that include |

Use `import_tasks` by default. Switch to `include_tasks` only when you need loops or conditional file selection.

### Handlers

- Handlers run once at end of play, even if notified multiple times. Use `meta: flush_handlers` when a later task depends on the handler having run.
- Handlers only fire when explicitly notified. Listing a second handler below a first in `handlers/main.yml` does not chain them. A "reporter" handler that's supposed to surface failures from an earlier handler has to be notified by that earlier handler (or collapsed into it).
- Never use variables in handler names -- they template too early and fail. Put variables in handler task parameters instead.
- Use `listen` to decouple notification name from handler name:

```yaml
- name: Restart nginx
  ansible.builtin.systemd:
    name: nginx
    state: restarted
  listen: restart web stack

- name: Clear nginx cache
  ansible.builtin.file:
    path: /var/cache/nginx
    state: absent
  listen: restart web stack
```

### One convergence path per resource

For any resource a role manages -- a compose project, a systemd unit, a managed config file -- pick exactly one convergence path and stick to it:

- **Option A (in-flow converge):** an unconditional task at the end of the role brings the resource to the desired state, relying on the module's own idempotency for no-op runs.
- **Option B (handler-only converge):** templates/config tasks `notify:` a handler, and the handler is the only thing that brings the resource up.

Running both paths for the same resource is the recurring bug. Best case, you do redundant work on every change. Worst case -- with modules that are only partially idempotent -- every apply reports `changed` for reasons that have nothing to do with real config drift.

The canonical offender is `community.docker.docker_compose_v2`. The module documents itself as only partially idempotent, and compose projects with `restart: no` init containers (kafka-init-topics, elasticsearch-ilm-init, and similar one-shots) trip it every time: the init container exits cleanly, the next `docker compose up` sees "not running", emits a `Starting` event, and the module reports `changed=true`. Pair that with a handler-driven restart and every apply fires the handler on a stack that did not actually drift.

**Bad -- cross-wired register + handler `when:`**

```yaml
# tasks/main.yml
- name: Template compose file
  ansible.builtin.template:
    src: docker-compose.yml.j2
    dest: "{{ deploy_dir }}/docker-compose.yml"
    mode: "0644"
  notify: Restart stack

- name: Start stack
  community.docker.docker_compose_v2:
    project_src: "{{ deploy_dir }}"
    state: present
  register: stack_start

# handlers/main.yml
- name: Restart stack
  community.docker.docker_compose_v2:
    project_src: "{{ deploy_dir }}"
    state: restarted
  when: not stack_start.changed   # cross-wire: handler reads task-scoped register
```

Two things are wrong here. First, the handler's `when:` references a task-scoped register from outside the handler -- a brittle coupling that's easy to invert, leaving either a handler that never runs or one that duplicates the in-flow task. Second, `state: restarted` maps to `docker compose restart`, which does not re-read the compose file; any template change is actually being applied by the unconditional `state: present` above. The handler is effectively dead code dressed up as a safety net.

**Bad -- fallback task gated by "did anything change"**

```yaml
- name: Template compose file
  ansible.builtin.template:
    src: docker-compose.yml.j2
    dest: "{{ deploy_dir }}/docker-compose.yml"
    mode: "0644"
  notify: Restart stack

- name: Ensure stack is up
  community.docker.docker_compose_v2:
    project_src: "{{ deploy_dir }}"
    state: present
  when: not (repo is changed or config is changed)
```

The intent ("converge only when nothing triggered a handler") is reasonable but the implementation leaks: if the module reports spurious `changed` on an unrelated converged run, the fallback task shows up as `changed` in every apply with no real drift, and operators stop trusting `--diff` output.

**Good (option A) -- always converge in flow**

```yaml
- name: Template compose file
  ansible.builtin.template:
    src: docker-compose.yml.j2
    dest: "{{ deploy_dir }}/docker-compose.yml"
    mode: "0644"

- name: Converge stack
  community.docker.docker_compose_v2:
    project_src: "{{ deploy_dir }}"
    state: present
```

Use when the module is reliably idempotent for this stack shape (no init containers, no restart-on-every-apply churn). Simplest to reason about; the template change is picked up by `state: present` on the next apply.

**Good (option B) -- handler-only convergence**

```yaml
# tasks/main.yml
- name: Template compose file
  ansible.builtin.template:
    src: docker-compose.yml.j2
    dest: "{{ deploy_dir }}/docker-compose.yml"
    mode: "0644"
  notify: Restart stack

# handlers/main.yml -- stop+start under one listen so depends_on re-evaluates
- name: Stop stack
  community.docker.docker_compose_v2:
    project_src: "{{ deploy_dir }}"
    state: stopped
  listen: Restart stack

- name: Start stack
  community.docker.docker_compose_v2:
    project_src: "{{ deploy_dir }}"
    state: present
  listen: Restart stack
```

Use when the in-flow path would be non-idempotent (partial-idempotency modules, init containers). The stop+start pair under a shared `listen:` forces `depends_on` and healthcheck conditions to be re-evaluated, which `state: restarted` alone does not do. Tradeoff: a first-ever install still needs at least one change notification to start the stack -- usually satisfied by the first template write.

**Decision heuristic.** Inspect the compose file or service definition. Choose option B (handler-only) when any of these apply:

- The compose file has `restart: "no"` init/setup containers or one-shot jobs that exit after running (kafka-init-topics, `*-ilm-init`, schema-seeders). `docker_compose_v2` flags them as "not running" on every apply and reports `changed=true`.
- Startup ordering matters and services use `depends_on: condition: service_healthy`. `state: restarted` (docker compose restart) does not re-evaluate healthchecks; a stop+start handler pair does.
- The managed resource has any documented partial-idempotency caveat in its module docs.

Otherwise -- single-container stacks, straightforward systemd units, modules whose `state: present` is fully declarative -- option A is simpler and preferred.

### Error handling

```yaml
- name: Risky deployment with rollback
  block:
    - name: Deploy new version
      ansible.builtin.copy:
        src: app-v2.tar.gz
        dest: /opt/app/app.tar.gz
        mode: "0644"

    - name: Extract and restart
      ansible.builtin.shell: |
        cd /opt/app && tar xzf app.tar.gz && ./restart.sh
      changed_when: true

  rescue:
    - name: Rollback to previous version
      ansible.builtin.copy:
        src: /opt/app/backup/app.tar.gz
        dest: /opt/app/app.tar.gz
        mode: "0644"

  always:
    - name: Ensure service is running
      ansible.builtin.systemd:
        name: myapp
        state: started
```

Avoid `ignore_errors: true` -- it masks real failures. Use `failed_when: false` when you truly want to suppress all errors, as it is explicit about intent.

## Role Composition

Roles compose through three mechanisms: `meta/main.yml` dependencies, the play-level `roles:` keyword, and `include_role`/`import_role` in tasks.

Reserve `meta/main.yml` dependencies for **hard, unconditional prerequisites** -- role B genuinely cannot function without role A. For everything else, sequence roles at the playbook level. Playbook sequencing is more visible (one place to read the apply order), supports `when:`, and sidesteps two subtle meta-dep gotchas:

1. **Meta deps cannot be gated.** A `when:` at the meta level is ignored -- the dependency always runs. Use `include_role` in tasks if you need conditional composition.
2. **Silent deduplication via lazy evaluation.** Ansible's role dedup happens *before* variable evaluation, so two role invocations with different variables can still collapse into one unexpected run.

### One baseline play, many function plays

When a host belongs to several functional groups and each group's playbook lists the same base role, the base role runs once per group per apply. Role deduplication only happens within a single play, not across plays in a playbook, so this redundancy is real.

The idiomatic fix is to structure the top-level playbook as one `hosts: all` baseline play followed by function-specific plays that do not re-list the base:

```yaml
# site.yml
- hosts: all
  roles: [base]

- hosts: webservers
  roles: [web_app]    # no base here; it ran above

- hosts: dbservers
  roles: [db_app]
```

Tradeoff: running a single function playbook standalone no longer implicitly baselines. Handle it with documentation, a wrapper recipe, or by treating `site.yml` as the canonical entry point. Avoid workarounds like play-scoped `set_fact` guards, `run_once`, or tag gating -- they paper over a structural issue that the play-level refactor solves cleanly.

### Role variable surface

A role consumes variables from two structurally different places, and each has its own home file:

- **Role-owned variables** (prefixed with the role name) live in `defaults/main.yml` with sensible defaults. This file is the single source of truth for what the role can be tuned with and what those defaults are.
- **Upstream variables** (values that come from `group_vars`, `host_vars`, or another role's output) are declared in `meta/argument_specs.yml` with `required: true`, a `type`, and `choices` where applicable. They are NOT mirrored into `defaults/main.yml`.

Prefix every role-owned variable with the role name to avoid collisions across roles invoked in the same play:

```yaml
# BAD -- collides with other roles
port: 8080

# GOOD -- namespaced
myapp_port: 8080
```

#### External contract via `meta/argument_specs.yml`

For upstream variables, declare them in `meta/argument_specs.yml`. Ansible validates the spec before `tasks/main.yml` runs, so a missing required variable or a wrong-typed value fails fast at the top of the role with a clear message, rather than surfacing later as an obscure Jinja traceback deep inside a template.

```yaml
# roles/consumer/meta/argument_specs.yml
---
argument_specs:
  main:
    short_description: Consume an upstream service port owned by the networking layer.
    options:
      upstream_service_port:
        description:
          - TCP port the upstream service listens on. Owned by
            group_vars/all/networking.yml; also consumed by the gateway role.
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

**Disjoint-keyset rule.** `defaults/main.yml` and `meta/argument_specs.yml` must have disjoint key sets. A variable is either role-owned (defaults) or upstream (argument_specs), never both. Ansible does not enforce this -- drift between the two files is avoided by the convention itself, not by tooling. Treat a variable appearing in both as a review-time bug.

**What argument_specs catches.** At role entry, Ansible checks that every `required: true` option is defined, that values match the declared `type`, and that they fall within declared `choices`. It does NOT catch a variable that is referenced in tasks/templates but declared in neither file, and it does not catch a variable listed only in `defaults/main.yml` that should have been in argument_specs (or vice versa).

**Linting.** The ansible-lint `role-argument-spec` rule requires every role to ship an `meta/argument_specs.yml`. A role with no upstream dependencies still needs the file, even if `options:` is empty.

**Vault indirection is unchanged.** argument_specs does not replace the vault pattern. Secrets still flow through a plaintext name in `group_vars/<group>/vars.yml` aliasing an encrypted value in `group_vars/<group>/vault.yml` (see Security Essentials below). If a secret is also an upstream variable the role depends on, declare the plaintext name in argument_specs -- the encrypted `vault_*` name stays internal to the inventory.

### Circular dependencies

If role A and role B depend on each other, do not resolve with mutual `meta` deps. Extract the shared concern into a third role C and have both depend on C. If the "cycle" is actually a sequencing requirement (A produces, B consumes, A uses B's output), split the work across ordered plays rather than forcing it into role metadata -- common with CAs, service discovery, and secrets managers where clients can't trust the server until it exists and the server can't run on clients until trust is set.

See [references/role-composition.md](references/role-composition.md) for the full patterns, Ansible docs citations, and the anti-pattern breakdown.

## Idempotency and Best Practices

Every task must be idempotent: running it N times produces the same result as running it once, with `changed=0` on subsequent runs.

### Use modules, not shell commands

```yaml
# BAD
- name: Install nginx
  ansible.builtin.shell: apt-get install -y nginx

# GOOD
- name: Install nginx
  ansible.builtin.apt:
    name: nginx
    state: present
```

When shell/command is unavoidable, always set `changed_when` and prefer `command` over `shell` (no shell injection surface). Guard interpolated variables with the `quote` filter:

```yaml
# DANGEROUS
- ansible.builtin.shell: "grep {{ username }} /etc/passwd"

# SAFE
- ansible.builtin.shell: "grep {{ username | quote }} /etc/passwd"

# BEST -- use creates/removes guards
- name: Run database migration
  ansible.builtin.command:
    cmd: /opt/app/bin/migrate --up
    creates: /opt/app/.migrated
  register: migrate_result
  changed_when: "'Applied' in migrate_result.stdout"
```

### Notify handlers instead of inline restarts

```yaml
# BAD -- restarts every run
- name: Deploy config
  ansible.builtin.template:
    src: app.conf.j2
    dest: /etc/app/app.conf
- name: Restart app
  ansible.builtin.systemd:
    name: myapp
    state: restarted

# GOOD -- restart only when config changes
- name: Deploy config
  ansible.builtin.template:
    src: app.conf.j2
    dest: /etc/app/app.conf
  notify: Restart app
```

### Set become per-task, not per-play

```yaml
# BAD -- everything runs as root
- hosts: webservers
  become: true
  tasks:
    - name: Read status (does NOT need root)
      ansible.builtin.command: /opt/app/status
      changed_when: false

# GOOD -- least privilege
- hosts: webservers
  tasks:
    - name: Read status
      ansible.builtin.command: /opt/app/status
      changed_when: false
    - name: Restart nginx (needs root)
      ansible.builtin.systemd:
        name: nginx
        state: restarted
      become: true
```

### Common idempotency breakers

| Pattern | Problem | Fix |
|---------|---------|-----|
| `shell: echo "line" >> file` | Appends on every run | `lineinfile` with `line:` |
| `command: useradd foo` | Fails if user exists | `ansible.builtin.user: state: present` |
| `shell: curl ... \| bash` | Re-runs every time | `get_url` + `creates:` guard |
| Unconditional service restart | `changed` every run | `notify` handler |
| `set_fact` with timestamps | Always different | Tag `molecule-idempotence-notest` |
| Converge-in-flow task **plus** notify-driven handler for the same resource | Double-apply; partially-idempotent modules (e.g. `docker_compose_v2` with init containers) report `changed` every run | Pick one path -- see "One convergence path per resource" |

### Verify idempotency with Molecule

Use `molecule converge && molecule idempotence` to iterate quickly. `molecule test` runs the full lifecycle including the idempotence step. For tasks that legitimately cannot be idempotent, tag with `molecule-idempotence-notest`. See [references/testing.md](references/testing.md).

## Common Gotchas

**`{{ }}` in `when:`** -- `when:` already evaluates Jinja. Double-wrapping causes errors:
```yaml
# BAD
when: "{{ my_var == 'foo' }}"
# GOOD
when: my_var == 'foo'
```

**Bare booleans in YAML** -- Unquoted `yes`, `no`, `on`, `off` are parsed as booleans, not strings:
```yaml
# BAD -- 'on' becomes boolean True
feature_flags:
  on: enabled
# GOOD
feature_flags:
  "on": enabled
```

**`collections:` keyword** -- Do not use `collections:` at play level. It breaks portability, hides module origins, and ansible-lint rejects it (`fqcn[keyword]`). Always use full FQCN.

**`set_fact` persists for the host** -- Facts survive across plays in the same run. A `set_fact` in play 1 can override an inventory variable in play 2. Prefer `vars:` at play/task level when values do not need to persist.

**`delegate_to` + `become`** -- `become` applies on the delegated host. A task delegated to localhost with `become: true` escalates on localhost, which may be unintended.

**Dictionary merging** -- Ansible replaces dictionaries entirely rather than merging. If `group_vars/all` defines `app_config: {port: 80, workers: 4}` and a host overrides `app_config: {port: 9090}`, `workers` is gone. Use flat variables or the `combine` filter.

**`register` on skipped tasks** -- A registered variable from a skipped task has `.skipped == true` but no `.stdout`. Always check `result is not skipped` before accessing attributes.

## Jinja2 Templating

### Common Filters

| Filter | Purpose | Example |
|--------|---------|---------|
| `default(value)` | Provide fallback when variable is undefined | `{{ my_var \| default('fallback') }}` |
| `mandatory` | Fail with a clear error if variable is undefined | `{{ my_var \| mandatory }}` |
| `combine(dict)` | Merge dictionaries (right side wins) | `{{ defaults \| combine(overrides) }}` |
| `selectattr(attr, test, value)` | Filter list of dicts by attribute | `{{ users \| selectattr('active', 'equalto', true) }}` |
| `map(attribute=name)` | Extract a single attribute from list of dicts | `{{ users \| map(attribute='name') \| list }}` |

### Whitespace Control

Jinja2 tags produce blank lines in rendered output. Use dash-trimming to remove them:

```yaml
# Without control -- leaves blank lines
{% if enable_ssl %}
ssl_certificate /etc/ssl/cert.pem;
{% endif %}

# With control -- clean output
{%- if enable_ssl %}
ssl_certificate /etc/ssl/cert.pem;
{%- endif %}
```

`{%-` trims whitespace before the tag. `-%}` trims whitespace after the tag. Use on control-flow tags (`if`, `for`, `endif`, `endfor`), not on expression tags (`{{ }}`).

### The `omit` Sentinel

Use `omit` with `default` to conditionally exclude a module parameter entirely, as if it were never specified:

```yaml
- name: Create user with optional groups
  ansible.builtin.user:
    name: "{{ username }}"
    groups: "{{ user_groups | default(omit) }}"
```

When `user_groups` is undefined, the `groups` parameter is omitted from the module call and the module uses its own default behavior. This is different from passing an empty string or `None`.

## Security Essentials

### Vault indirection pattern

```yaml
# group_vars/production/vars.yml (plaintext, grep-able)
db_password: "{{ vault_db_password }}"

# group_vars/production/vault.yml (encrypted: ansible-vault encrypt)
vault_db_password: "s3cret"
```

`ansible-vault rekey` works on file-level encryption only, NOT on inline `encrypt_string` values. For frequently rotated secrets, use an external secrets manager.

### no_log on sensitive tasks

```yaml
- name: Set database password
  ansible.builtin.user:
    name: dbuser
    password: "{{ db_password | password_hash('sha512') }}"
  no_log: true
```

`no_log` does not prevent exposure in `-vvvv` tracebacks, some callback plugins, or loop results on older versions. Treat it as defense-in-depth, not sole protection.

### ansible.cfg security

Never run Ansible from untrusted directories -- Ansible loads `ansible.cfg` from the current directory. Set `ANSIBLE_CONFIG` explicitly in CI. Keep `host_key_checking = True` (the default).

See [references/security.md](references/security.md) for Vault IDs, external secrets managers, SSH hardening, audit logging, and supply chain security.

## Molecule Testing

Molecule tests roles in ephemeral environments. Use the ansible-native approach (Molecule 6+) where create/destroy are standard Ansible playbooks.

### Minimal role test setup

```
roles/myrole/molecule/default/
  molecule.yml
  converge.yml
  verify.yml
```

```yaml
# molecule.yml
---
dependency:
  name: galaxy
  options:
    requirements-file: requirements.yml
```

```yaml
# converge.yml
---
- name: Converge
  hosts: all
  tasks:
    - name: Include the role
      ansible.builtin.include_role:
        name: myrole
```

```yaml
# verify.yml
---
- name: Verify
  hosts: all
  gather_facts: true
  tasks:
    - name: Gather package facts
      ansible.builtin.package_facts:

    - name: Assert nginx is installed
      ansible.builtin.assert:
        that: "'nginx' in ansible_facts.packages"

    - name: Check nginx is running
      ansible.builtin.service_facts:

    - name: Assert nginx service active
      ansible.builtin.assert:
        that: ansible_facts.services['nginx.service'].state == 'running'
```

Development workflow: `molecule converge` (iterate), `molecule idempotence` (confirm no changes on re-run), `molecule test` (full lifecycle).

See [references/testing.md](references/testing.md) for multi-platform testing, custom create/destroy playbooks, CI/CD integration, and advanced scenarios.

## Performance

- **Forks**: Increase `forks` in `ansible.cfg` (default 5). Set to ~20-50 for large inventories.
- **Pipelining**: Set `pipelining = True` under `[ssh_connection]`. Requires `Defaults !requiretty` in sudoers.
- **Fact caching**: `fact_caching = jsonfile` with `fact_caching_connection = /tmp/ansible_facts`.
- **gather_subset**: Use `gather_subset: [min]` or `gather_facts: false` when full facts are not needed.
- **Strategy**: Use `strategy: free` to let fast hosts proceed independently (default `linear` waits for all hosts per task).
- **Async**: For long tasks, `async: 3600` + `poll: 0` for fire-and-forget, then check with `async_status`.

## Validation Pipeline

```bash
yamllint .                                      # YAML syntax
ansible-lint                                    # Ansible best practices
ansible-playbook site.yml --syntax-check        # playbook structure
ansible-playbook site.yml --check --diff        # dry run
molecule test                                   # integration test
```
