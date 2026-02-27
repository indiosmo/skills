---
name: authoring-ansible
description: "Write, review, and debug Ansible automation: playbooks, roles, inventories, and collections with idiomatic patterns, security hardening, and testing. Use when creating or modifying Ansible playbooks and roles, reviewing Ansible code for best practices, setting up ansible-lint or Molecule testing, organizing Ansible repositories, managing secrets with Vault, hardening privilege escalation, or troubleshooting Ansible automation. Triggers on: Ansible playbooks, roles, inventories, YAML automation files, ansible-lint configs, Molecule test scenarios, Ansible Vault, group_vars, host_vars."
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

Always use FQCN, name every task, use `true`/`false` (not `yes`/`no`), quote file modes, set explicit state:

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
| Handler visibility | Visible outside | NOT visible outside |

Use `import_tasks` by default. Switch to `include_tasks` only when you need loops or conditional file selection.

### Handlers

- Handlers run once at end of play, even if notified multiple times. Use `meta: flush_handlers` when a later task depends on the handler having run.
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

### Prefix role variables

```yaml
# BAD -- collides with other roles
port: 8080

# GOOD -- namespaced to role
myapp_port: 8080
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
