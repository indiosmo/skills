# Ansible Security Reference

## Ansible Vault

### Vault IDs for multi-environment encryption

Label vault passwords by environment to avoid decryption confusion:

```bash
# Encrypt with environment-specific vault IDs
ansible-vault encrypt --vault-id dev@~/.vault_dev_pass group_vars/dev/vault.yml
ansible-vault encrypt --vault-id prod@~/.vault_prod_pass group_vars/production/vault.yml

# Run playbook with multiple vault IDs
ansible-playbook site.yml \
  --vault-id dev@~/.vault_dev_pass \
  --vault-id prod@~/.vault_prod_pass

# Or set in ansible.cfg
# [defaults]
# vault_identity_list = dev@~/.vault_dev_pass, prod@~/.vault_prod_pass
```

### Vault password client scripts

For production, fetch the vault password from an external secrets manager:

```python
#!/usr/bin/env python3
# vault_password_client.py -- chmod 700, set as vault_password_file
import hvac
client = hvac.Client(url='https://vault.example.com:8200')
secret = client.secrets.kv.v2.read_secret_version(path='ansible/vault-password')
print(secret['data']['data']['password'])
```

```ini
# ansible.cfg
[defaults]
vault_password_file = ./vault_password_client.py
```

### Rekeying

`ansible-vault rekey` works on file-level encryption only. It does NOT work on inline `encrypt_string` values embedded in YAML files. Plan accordingly: if you need to rotate vault passwords, file-level encryption is easier to manage.

## External Secrets Managers

### HashiCorp Vault

```bash
ansible-galaxy collection install community.hashi_vault
pip install hvac
```

```yaml
- name: Get DB password from HashiCorp Vault
  ansible.builtin.set_fact:
    db_password: "{{ lookup('community.hashi_vault.hashi_vault',
                      'secret/data/production/db',
                      token=vault_token,
                      url='https://vault.example.com:8200') }}"
  no_log: true
```

### AWS Secrets Manager / SSM

```yaml
# Secrets Manager
- ansible.builtin.set_fact:
    api_key: "{{ lookup('amazon.aws.secretsmanager_secret', 'prod/api_key') }}"
  no_log: true

# SSM Parameter Store
- ansible.builtin.set_fact:
    db_host: "{{ lookup('amazon.aws.ssm_parameter', '/prod/database/host') }}"
```

Best practices: Use hierarchical paths (`/app/env/component/key`), always `SecureString` type for sensitive SSM parameters, and fine-grained IAM policies.

## no_log Limitations

`no_log: true` suppresses task output in normal operation. It does NOT protect against:

1. **Exception tracebacks** -- Ansible internal errors may include task args in stack traces.
2. **Callback plugins** -- Not all callback plugins respect `no_log`. Audit any custom or third-party callbacks.
3. **Loop results** -- On older Ansible versions, loop iteration results may leak despite `no_log` on the parent task.
4. **Debug mode** -- `-vvvv` may expose information in edge cases.

Mitigations:
- Use external secrets managers so secrets never exist in playbook variables.
- Restrict log file permissions (`chmod 600 /var/log/ansible/ansible.log`).
- Audit callback plugin behavior in your environment.
- Use `display_args_to_stdout = False` in ansible.cfg (the default).

## Privilege Escalation

### Targeted sudo rules

Restrict what the Ansible service account can do:

```
# /etc/sudoers.d/ansible
ansible_svc ALL=(ALL) NOPASSWD: /usr/bin/apt-get, /usr/bin/systemctl, /usr/bin/cp, /usr/bin/tee
```

### Encrypt become passwords

```yaml
# group_vars/production/vault.yml (encrypted)
vault_become_pass: "s3cure_sudo_pa$$"

# group_vars/production/vars.yml
ansible_become_pass: "{{ vault_become_pass }}"
```

### Pipelining conflict

Pipelining (`pipelining = True`) improves performance but conflicts with `requiretty` in sudoers. Either disable `requiretty` on managed hosts or disable pipelining:

```ini
[ssh_connection]
pipelining = True  # only if: Defaults !requiretty in sudoers
```

## SSH Hardening

### Dedicated keys

Use SSH keys created specifically for Ansible automation. Never reuse personal keys.

```yaml
- name: Deploy Ansible SSH key
  ansible.posix.authorized_key:
    user: ansible_svc
    key: "{{ lookup('file', '/path/to/ansible_svc.pub') }}"
    state: present
    key_options: 'no-port-forwarding,no-X11-forwarding'
```

### Connection settings

```ini
# ansible.cfg
[defaults]
host_key_checking = True          # NEVER disable in production

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=yes
```

### SSH hardening on managed hosts

```yaml
- name: Harden SSH config
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: "{{ item.regexp }}"
    line: "{{ item.line }}"
  loop:
    - { regexp: '^#?PasswordAuthentication', line: 'PasswordAuthentication no' }
    - { regexp: '^#?PermitRootLogin', line: 'PermitRootLogin no' }
    - { regexp: '^#?MaxAuthTries', line: 'MaxAuthTries 3' }
  become: true
  notify: Restart sshd
```

## ansible.cfg Security Settings

```ini
[defaults]
display_args_to_stdout = False    # prevent task args in stdout
host_key_checking = True
inject_facts_as_vars = False      # prevent fact/variable name collisions
log_path = /var/log/ansible/ansible.log

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=yes
pipelining = True

[privilege_escalation]
become = False                    # do NOT default to become
become_method = sudo
```

**Critical**: Ansible loads `ansible.cfg` from the current working directory. A malicious `ansible.cfg` in a cloned repository can hijack Ansible behavior (run arbitrary callback plugins, change module paths). Always set `ANSIBLE_CONFIG` explicitly in CI/CD. Ansible refuses to load config from a world-writable directory.

## Supply Chain Security

### Pin collection versions

```yaml
# requirements.yml
collections:
  - name: community.general
    version: "8.6.0"           # exact version, not >=
  - name: ansible.posix
    version: "1.5.4"
roles:
  - name: geerlingguy.docker
    version: "6.1.0"
```

Unpinned collections (`version: ">=1.0.0"`) can break playbooks silently when upstream releases breaking changes.

### Audit before adoption

Before adopting a Galaxy role or collection:
- Review source code, especially for `shell`/`command` usage.
- Check maintainer reputation and recent commit activity.
- Verify no deprecated or unsafe patterns.
- For production, use a private Automation Hub to curate approved content.

### Collection signing (AAP 2.2+)

```bash
ansible-sign project gpg-sign .
ansible-sign project gpg-verify .
```

## Audit Logging

### Callback plugins

```ini
# ansible.cfg
[defaults]
log_path = /var/log/ansible/ansible.log
callbacks_enabled = log_plays, profile_tasks
```

Built-in options:
- `log_plays` -- per-host log files in `/var/log/ansible/hosts/`
- `syslog` -- sends events to syslog for centralized collection
- `logstash` -- sends to Logstash/ELK
- `splunk` -- sends to Splunk HEC
- `profile_tasks` -- adds timing per task

## File Permissions

```bash
chmod 600 ~/.vault_pass*              # vault password files
chmod 600 ~/.ssh/ansible_*            # SSH private keys
chmod 640 ansible.cfg                 # config
chmod 640 inventories/*/hosts.yml     # inventory (may contain IPs)
```

### .gitignore

```gitignore
.vault_pass*
*.vault_pass
*.pem
*.key
*.retry
*.log
```

## AWX / AAP Note

When running through AWX or Ansible Automation Platform, credentials are injected at runtime via the platform's credential system. Do not embed vault passwords or SSH keys in playbook repositories. The patterns in this document apply to CLI-based Ansible execution.
