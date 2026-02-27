# Molecule Testing Reference

## Ansible-Native Configuration (Molecule 6+)

Molecule 6 replaced driver-based configuration with the ansible-native approach. Instead of configuring a `driver:` block, write standard Ansible playbooks for instance lifecycle.

### Custom create/destroy playbooks

For container-based testing, write create.yml and destroy.yml using collection modules:

```yaml
# molecule/default/create.yml
---
- name: Create test containers
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create container instances
      containers.podman.podman_container:
        name: "{{ item.name }}"
        image: "{{ item.image }}"
        state: started
        command: sleep 1d
        published_ports: "{{ item.ports | default(omit) }}"
      loop: "{{ molecule_yml.platforms }}"

    - name: Add containers to molecule inventory
      ansible.builtin.add_host:
        name: "{{ item.name }}"
        ansible_connection: containers.podman.podman
      loop: "{{ molecule_yml.platforms }}"
```

```yaml
# molecule/default/destroy.yml
---
- name: Destroy test containers
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Remove containers
      containers.podman.podman_container:
        name: "{{ item.name }}"
        state: absent
      loop: "{{ molecule_yml.platforms | default([]) }}"
      failed_when: false  # destroy must proceed even if container already absent
```

### molecule.yml with platforms

```yaml
---
platforms:
  - name: ubuntu-test
    image: ubuntu:22.04
  - name: rhel-test
    image: redhat/ubi9

dependency:
  name: galaxy
  options:
    requirements-file: requirements.yml

scenario:
  test_sequence:
    - dependency
    - destroy
    - create
    - prepare
    - converge
    - idempotence
    - verify
    - cleanup
    - destroy
```

## Multi-Platform Testing

Test across OS families by grouping platforms:

```yaml
# molecule.yml
platforms:
  - name: centos-9
    image: quay.io/centos/centos:stream9
    groups:
      - rhel_family
  - name: ubuntu-2204
    image: ubuntu:22.04
    groups:
      - debian_family
  - name: debian-12
    image: debian:bookworm
    groups:
      - debian_family
```

Use groups in converge.yml or verify.yml for OS-specific logic:

```yaml
# verify.yml
- name: Verify (Debian family)
  hosts: debian_family
  tasks:
    - name: Check apt package
      ansible.builtin.command: dpkg -l nginx
      changed_when: false

- name: Verify (RHEL family)
  hosts: rhel_family
  tasks:
    - name: Check rpm package
      ansible.builtin.command: rpm -q nginx
      changed_when: false
```

## Multiple Scenarios

Use separate scenarios for distinct test cases:

```
molecule/
  default/           # basic functionality
    molecule.yml
    converge.yml
    verify.yml
  cluster/           # multi-node deployment
    molecule.yml
    converge.yml
    verify.yml
  upgrade/           # upgrade path testing
    molecule.yml
    converge.yml
```

Run specific scenarios: `molecule test -s cluster`. Run all: `molecule test --all`.

Share common playbooks via symlinks or by copying create/destroy playbooks between scenario directories. Alternatively, keep a shared `molecule/_shared/` directory and symlink into each scenario:

```bash
# molecule/cluster/
ln -s ../default/create.yml create.yml
ln -s ../default/destroy.yml destroy.yml
```

## Verify Playbook Patterns

### Check packages, services, ports, files

```yaml
---
- name: Verify
  hosts: all
  gather_facts: true
  tasks:
    - name: Gather package facts
      ansible.builtin.package_facts:

    - name: Assert required packages
      ansible.builtin.assert:
        that: "'{{ item }}' in ansible_facts.packages"
        fail_msg: "{{ item }} not installed"
      loop:
        - nginx
        - curl

    - name: Gather service facts
      ansible.builtin.service_facts:

    - name: Assert services running
      ansible.builtin.assert:
        that: ansible_facts.services['{{ item }}.service'].state == 'running'
      loop:
        - nginx

    - name: Check config file exists with correct permissions
      ansible.builtin.stat:
        path: /etc/nginx/nginx.conf
      register: config_stat

    - name: Assert config file
      ansible.builtin.assert:
        that:
          - config_stat.stat.exists
          - config_stat.stat.mode == '0644'

    - name: Check port 80 is listening
      ansible.builtin.wait_for:
        port: 80
        timeout: 5

    - name: Verify HTTP response
      ansible.builtin.uri:
        url: http://localhost
        status_code: 200
```

### Use check_mode for idempotency verification

```yaml
- name: Verify config is as expected (check mode)
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    mode: "0644"
  check_mode: true
  register: config_check

- name: Assert config unchanged
  ansible.builtin.assert:
    that: config_check is not changed
    fail_msg: "Config file does not match expected template"
```

## Prepare Playbook

Use prepare.yml for prerequisites that are NOT part of the role being tested:

```yaml
# molecule/default/prepare.yml
---
- name: Prepare
  hosts: all
  become: true
  tasks:
    - name: Install Python (needed for Ansible modules)
      ansible.builtin.raw: apt-get update && apt-get install -y python3
      changed_when: true

    - name: Install systemd (for service testing in containers)
      ansible.builtin.apt:
        name: systemd
        state: present
```

## Idempotence

Molecule's idempotence check runs converge twice and fails if the second run reports `changed > 0`.

For tasks that legitimately change every run (timestamps, random values):
- Tag with `molecule-idempotence-notest` to skip during idempotence check only.
- Tag with `molecule-notest` to skip entirely during Molecule runs.

```yaml
- name: Generate session token
  ansible.builtin.command: /opt/generate-token.sh
  register: token
  changed_when: true
  tags:
    - molecule-idempotence-notest
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Molecule Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        distro: [ubuntu:22.04, debian:bookworm, quay.io/centos/centos:stream9]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install molecule ansible-core "molecule-plugins[podman]"
      - name: Run molecule
        run: molecule test
        env:
          MOLECULE_DISTRO: ${{ matrix.distro }}
          PY_COLORS: "1"
```

### GitLab CI

```yaml
molecule:
  image: ghcr.io/ansible/community-ansible-dev-tools
  stage: test
  services:
    - docker:dind
  script:
    - molecule test
```

## Development Commands

| Command | Purpose |
|---------|---------|
| `molecule create` | Provision instances |
| `molecule converge` | Apply role/playbook |
| `molecule login` | SSH into instance for debugging |
| `molecule verify` | Run verification tests |
| `molecule idempotence` | Re-run converge, check changed=0 |
| `molecule test` | Full lifecycle (create through destroy) |
| `molecule test --all` | All scenarios |
| `molecule test --parallel` | Parallel scenario execution |
| `molecule destroy` | Tear down instances |
