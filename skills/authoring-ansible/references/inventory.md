# Ansible Inventory Reference

## Format: YAML vs INI

Prefer YAML. INI has a type-safety trap: inline host variables (`host1 http_port=80`) are parsed as Python literals via `ast.literal_eval`, but `:vars` section values are always strings. YAML gives consistent native types everywhere.

**INI:**
```ini
[webservers]
web01 http_port=80 maxRequestsPerChild=808

[webservers:vars]
ntp_server=ntp.example.com

[southeast:children]
atlanta
raleigh
```

**YAML (equivalent):**
```yaml
webservers:
  hosts:
    web01:
      http_port: 80
      maxRequestsPerChild: 808
  vars:
    ntp_server: ntp.example.com
southeast:
  children:
    atlanta:
    raleigh:
```

INI-specific gotchas:
- Inline `enabled=False` is boolean. `:vars` section `enabled=False` is the string `"False"`.
- Non-standard SSH port shorthand works only in INI: `host1:5309`.
- Spaces in values must be quoted: `key="value with spaces"`.

## Default Groups

Ansible automatically creates two groups:
- **`all`** -- every host.
- **`ungrouped`** -- hosts not in any named group (besides `all`).

Every host belongs to `all` plus either `ungrouped` or one or more named groups.

Empty groups (no hosts) are discarded after processing.

If setting `all` group vars inside a YAML inventory file, `all` must be the first top-level key.

### implicit_localhost

When `delegate_to: localhost` is used and `localhost` is not explicitly in inventory, Ansible creates an implicit localhost with `ansible_connection: local` and `ansible_python_interpreter` set to the control node's Python. This implicit host receives `group_vars/all` and `host_vars/localhost`, but does not belong to any other inventory groups. This is a common source of "variable not found" confusion when delegating to localhost.

To control localhost behavior explicitly, add it to inventory:
```yaml
all:
  hosts:
    localhost:
      ansible_connection: local
```

## Host Ranges

Numeric and alphabetic ranges avoid listing similar hosts individually. Ranges are inclusive on both ends. Leading zeros are preserved.

```yaml
webservers:
  hosts:
    www[01:50].example.com:       # www01 through www50
    www[01:50:2].example.com:     # stride of 2: www01, www03, ..., www49
databases:
  hosts:
    db-[a:f].example.com:         # db-a through db-f
```

## Inventory Aliases and Connection Variables

Always use aliases. The left-hand name in inventory is what you reference in playbooks, logs, and `--limit`. `ansible_host` is only used by the connection layer. This decouples your automation logic from infrastructure details like IPs and ports.

```yaml
all:
  hosts:
    jumper:                                  # alias -- use this in playbooks
      ansible_host: 192.0.2.50              # actual connection target
      ansible_port: 5555
    db_primary:                              # alias
      ansible_host: 10.0.1.100              # actual connection target
      ansible_user: dbadmin
      ansible_ssh_private_key_file: /path/to/key
```

`inventory_hostname` always resolves to the alias (`jumper`, `db_primary`), never the `ansible_host` value. This holds true everywhere: playbooks, templates, conditionals, and log output.

```yaml
# In a playbook, target by alias:
- hosts: jumper
  tasks:
    - name: Show which host is running
      ansible.builtin.debug:
        msg: "Running on {{ inventory_hostname }} ({{ ansible_host }})"
      # Output: "Running on jumper (192.0.2.50)"
```

### Key connection variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `ansible_host` | inventory hostname | Actual IP/hostname to connect to |
| `ansible_port` | 22 | SSH port |
| `ansible_user` | control node user | Login username |
| `ansible_connection` | ssh | Connection type (ssh, local, docker, winrm) |
| `ansible_ssh_private_key_file` | -- | Path to SSH private key |
| `ansible_python_interpreter` | auto (probes target) | Python path on target |
| `ansible_become` | false | Enable privilege escalation |
| `ansible_become_method` | sudo | Escalation method |
| `ansible_become_user` | root | Target user after escalation |
| `ansible_ssh_common_args` | -- | Extra args for sftp, scp, and ssh (ProxyCommand, etc.) |
| `ansible_host_key_checking` | true | SSH host key verification |

Never store `ansible_password` or `ansible_become_password` in plaintext. Use Vault (see [security.md](security.md) for vault indirection pattern and Vault IDs).

## Inventory Organization

### Group design: what / where / when

Organize hosts along three dimensions instead of creating combinatorial group names like `prod_webservers_us_east`. Use `children:` only when one group genuinely contains another, not to create artificial hierarchy. Use YAML comments as section headings:

```yaml
# -- What (function) --
webservers:
  hosts:
    web01:
    web02:
dbservers:
  hosts:
    db01:
    db02:
    db03:

# -- Where (location) --
east:
  hosts:
    web01:
    db01:
    db02:
west:
  hosts:
    web02:
    db03:

# -- When (lifecycle) --
prod:
  children:
    east:
test:
  children:
    west:
```

Hosts listed in multiple groups are a single host with merged variables from all groups. Child group members automatically become members of all parent groups. Circular relationships are forbidden.

Target with intersection patterns instead of dedicated groups:

```bash
ansible-playbook deploy.yml -i inventory/ --limit "webservers:&prod"    # production webservers
ansible-playbook drain.yml -i inventory/ --limit "east:&prod"           # production east
ansible-playbook update.yml -i inventory/ --limit "webservers:!test"    # webservers except test
```

### Group hierarchy rules

Keep hierarchies flat (2-3 levels max). Use intersection patterns instead of deep nesting.

**Variable precedence within groups:** child groups beat parent groups. `group_vars/webservers.yml` beats `group_vars/all.yml`. Same-level groups merge alphabetically (last group alphabetically wins).

Override alphabetical ordering with `ansible_group_priority` (higher number = higher precedence, default 1). This can only be set in inventory sources, not in `group_vars/` files:

```yaml
critical_group:
  vars:
    ansible_group_priority: 10
    shared_var: "I win over alphabetically-later groups"
```

Group names should use only letters, numbers, and underscores. Hyphens produce deprecation warnings and will be rejected in a future Ansible version.

### group_vars and host_vars

Split variables into `group_vars/` and `host_vars/` directories rather than inlining them in inventory files. Use either a single file per group/host (`webservers.yml`) or a directory with multiple files (`dbservers/main.yml`, `dbservers/backup.yml`).

```
inventory/
  hosts.yml
  group_vars/
    all/
      vars.yml
      vault.yml           # encrypted with ansible-vault
    webservers.yml
    dbservers/
      main.yml
      backup.yml          # multiple files load alphabetically
  host_vars/
    db01.example.com.yml
```

Playbook-relative `group_vars/` and `host_vars/` override inventory-relative ones (playbook positions 5/7/10 beat inventory positions 4/6/9 in the precedence chain).

## Host Patterns

| Pattern | Meaning |
|---------|---------|
| `all` or `*` | All hosts |
| `host1` | Single host |
| `host1,host2` or `host1:host2` | Union (prefer comma for IPv6 clarity) |
| `webservers:dbservers` | Union of groups |
| `webservers:!atlanta` | Webservers except atlanta members |
| `webservers:&staging` | Hosts in both webservers AND staging |
| `192.0.*` / `*.example.com` | Wildcard |
| `~(web\|db).*\.example\.com` | Regex (prefix with `~`) |
| `webservers[0]` | First host in group |
| `webservers[-1]` | Last host in group |
| `webservers[0:2]` | Hosts at indices 0, 1, 2 |

**Processing order:** Ansible evaluates all operators in a fixed sequence regardless of position in the pattern string: union (`:`, `,`) first, then intersection (`&`), then exclusion (`!`). This is sequential filtering, not algebraic precedence -- `a:b:&c:!d` means "combine a and b, keep only those also in c, then remove those in d."

**`--limit` flag:**
```bash
ansible-playbook site.yml --limit "host1,host2"
ansible-playbook site.yml --limit 'all:!host1'       # single-quote for shell safety
ansible-playbook site.yml --limit @retry_hosts.txt    # read from file
```

Patterns only match hosts/groups in the loaded inventory. Using a raw IP when the inventory defines an alias produces a warning, not a match.

## Debugging with ansible-inventory

```bash
# Show full merged inventory as JSON
ansible-inventory -i inventory/ --list

# Show group hierarchy as a tree
ansible-inventory -i inventory/ --graph
```

Sample `--graph` output:
```
@all:
  |--@ungrouped:
  |  |--mail.example.com
  |--@webservers:
  |  |--foo.example.com
  |  |--bar.example.com
  |--@southeast:
  |  |--@atlanta:
  |  |  |--host1
  |  |  |--host2
```

```bash
# Show tree with all variables
ansible-inventory -i inventory/ --graph --vars

# Show all merged variables for a specific host (most useful for debugging)
ansible-inventory -i inventory/ --host web01.example.com

# Trace variable loading sources -- shows which files loaded and in what order
ansible-inventory -i inventory/ --host web01.example.com -vvv
```

### Validate inventory variables with a debug playbook

```yaml
- hosts: all
  gather_facts: false
  tasks:
    - name: Assert required variables are set
      ansible.builtin.assert:
        that:
          - ansible_host is defined
          - env is defined
          - env in ['prod', 'staging', 'dev']
        fail_msg: "Missing or invalid variable on {{ inventory_hostname }}"
```

## Inventory Special Variables

| Variable | Description |
|----------|-------------|
| `inventory_hostname` | Name of current host as defined in inventory |
| `inventory_hostname_short` | First part before the first dot |
| `inventory_file` | Filename of the inventory source |
| `inventory_dir` | Directory of the inventory source |
| `groups` | Dict of all groups and their host lists |
| `group_names` | List of groups the current host belongs to |
| `hostvars` | Dict enabling cross-host variable access |
| `ansible_play_hosts` | Active hosts in current play (excludes failed) |
| `ansible_play_hosts_all` | All hosts targeted by play (includes failed) |
| `ansible_play_batch` | Current batch of hosts in a serial play |

## Common Mistakes

**Forgotten `--limit` hits production.** When all environments share one inventory, a missing `--limit` targets everything. Fix: use specific groups in `hosts:` directives (e.g., `hosts: webservers:&staging`) and treat `--limit` as an additional guardrail, not the sole safeguard.

**Combinatorial group names** like `prod_webservers_us_east`. Fix: use three-dimensional groups (what/where/when) with intersection patterns.

**Deeply nested group hierarchies.** Increases variable resolution overhead and complexity. Fix: keep hierarchies flat (2-3 levels max) and use intersection patterns.

**`.ini` files in inventory directories.** Files ending in `.ini` are silently ignored by default. Rename to plain text or `.yml`.

## Inventory-Specific Performance

For inventories exceeding 5,000 hosts:

- **Split inventories by region** -- avoid loading the entire fleet when targeting a single region.
- **Flatten group hierarchies** -- reduces variable resolution overhead. Use 2-3 levels max with intersection patterns.
- **Targeted execution** -- `--limit` and group intersections instead of `hosts: all`.

General Ansible performance tuning (forks, pipelining, fact caching, strategy) is covered in the main skill.
