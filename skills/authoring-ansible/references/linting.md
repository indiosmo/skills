# Ansible Linting Reference

## ansible-lint Rule Categories

### Naming

| Rule | Description |
|------|-------------|
| `name[missing]` | All tasks and plays must be named |
| `name[casing]` | Enforce consistent task name casing |
| `name[template]` | Jinja templates must not be the only content of `name` |
| `role-name` | Role names must match `[a-z][a-z0-9_]+` |
| `var-naming[no-role-prefix]` | Role variables should be prefixed with role name |
| `var-naming[pattern]` | Variables must be lowercase + underscore, starting with letter or `_` |

### FQCN

| Rule | Description |
|------|-------------|
| `fqcn[action-core]` | Use `ansible.builtin.copy` not `copy` |
| `fqcn[action]` | Use FQCN for all modules |
| `fqcn[keyword]` | Do not use the `collections:` keyword; use FQCN everywhere |

### Command / Module

| Rule | Description |
|------|-------------|
| `command-instead-of-module` | Use a native module when one exists |
| `command-instead-of-shell` | Use `command` when shell features (pipes, redirects) are not needed |
| `no-free-form` | Use explicit `cmd:` parameter, not free-form syntax |
| `inline-env-var` | Use the `environment:` keyword, not inline env vars |

### Safety

| Rule | Description |
|------|-------------|
| `no-log-password` | Tasks with passwords must use `no_log: true` |
| `risky-file-permissions` | File-creating modules must set `mode` explicitly |
| `risky-octal` | Octal permissions must be quoted strings (`"0644"` not `0644`) |
| `risky-shell-pipe` | Shell pipes hide intermediate failures |
| `partial-become[task]` | When using `become`, also set `become_user` |

### Idempotency

| Rule | Description |
|------|-------------|
| `no-changed-when` | command/shell tasks must specify `changed_when` |
| `no-handler` | Use handlers instead of `when: result.changed` |
| `latest` | Use specific versions, not `state: latest` |

### YAML (via yamllint)

| Rule | Description |
|------|-------------|
| `yaml[truthy]` | Only `true`/`false`, not `yes`/`no`/`on`/`off` |
| `yaml[line-length]` | Default max 160 characters |
| `yaml[indentation]` | Consistent indentation |
| `yaml[octal-values]` | Proper octal handling |

### Syntax and Structure

| Rule | Description |
|------|-------------|
| `syntax-check` | Must pass `--syntax-check` |
| `no-jinja-when` | Do not wrap `when:` conditions in `{{ }}` |
| `jinja[spacing]` | Consistent spacing inside `{{ }}` |
| `key-order` | `name` first, `block`/`rescue`/`always` last |
| `ignore-errors` | Avoid `ignore_errors`; use `failed_when` or `rescue` |
| `no-relative-paths` | Do not use relative paths in tasks |

### Deprecation

| Rule | Description |
|------|-------------|
| `deprecated-module` | Do not use deprecated modules |
| `deprecated-bare-vars` | Wrap variables in `{{ }}` |
| `deprecated-local-action` | Use `delegate_to: localhost` |

## Profiles

Profiles are cumulative (each includes all rules from lower profiles):

| Profile | Description | Status |
|---------|-------------|--------|
| `min` | Syntax errors only | Fully implemented |
| `basic` | Standard style and formatting | Fully implemented |
| `moderate` | Readability and maintainability | Fully implemented |
| `safety` | Non-deterministic outcomes and security | Fully implemented |
| `shared` | Galaxy/Automation Hub publishing | Partially implemented (some rules aspirational) |
| `production` | AAP certified content | Partially implemented |

Use `safety` as the strictest fully-enforced profile. `shared` and `production` contain unimplemented rules.

## Configuration

Full `.ansible-lint` options:

```yaml
---
profile: moderate

exclude_paths:
  - .cache/
  - .git/
  - molecule/
  - roles/external/

# Completely skip (hidden from output)
skip_list:
  - yaml[line-length]

# Produce warnings instead of errors
warn_list:
  - experimental
  - name[casing]

# Enable opt-in rules
enable_list:
  - no-same-owner
  - no-log-password

# Variable naming pattern
var_naming_pattern: "^[a-z_][a-z0-9_]*$"

# Loop variable prefix
loop_var_prefix: "^(__|{role}_)"

# Kinds mapping
kinds:
  - playbook: "**/playbooks/*.yml"
  - tasks: "**/tasks/*.yml"
  - vars: "**/vars/*.yml"
  - meta: "**/meta/main.yml"

# Autofix targets
write_list:
  - all
```

## Skipping Rules

From most targeted to most broad:

1. **Inline `# noqa`** -- single task, always add a comment explaining why:
   ```yaml
   - name: Legacy script  # noqa: command-instead-of-module -- no module exists
     ansible.builtin.command: /opt/legacy/run.sh
   ```

2. **`.ansible-lint-ignore`** -- per-file, format is `filename rule-id`:
   ```
   roles/legacy/tasks/main.yml command-instead-of-module
   ```
   Generate automatically: `ansible-lint --generate-ignore`

3. **`warn_list`** -- global, produces warnings but non-fatal exit code.

4. **`skip_list`** -- global, completely hidden from output. Last resort.

## CI/CD Integration

### GitHub Actions

```yaml
name: Ansible Lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ansible/ansible-lint@main
```

### Pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/ansible/ansible-lint
    rev: v25.1.0
    hooks:
      - id: ansible-lint
```

## Autofixable Rules

Run `ansible-lint --fix` to auto-fix: `fqcn`, `jinja[spacing]`, `key-order`, `name` sub-rules, `no-free-form`, `no-jinja-when`, `no-log-password`, `partial-become`, `yaml` formatting, `command-instead-of-shell`, `deprecated-local-action`.
