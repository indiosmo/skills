# One Convergence Path Per Resource

For any resource a role manages -- a compose project, a systemd unit, a managed config file -- pick exactly one convergence path and stick to it:

- **Option A (in-flow converge):** an unconditional task at the end of the role brings the resource to the desired state, relying on the module's own idempotency for no-op runs.
- **Option B (handler-only converge):** templates/config tasks `notify:` a handler, and the handler is the only thing that brings the resource up.

Running both paths for the same resource is the recurring bug. Best case, you do redundant work on every change. Worst case -- with modules that are only partially idempotent -- every apply reports `changed` for reasons that have nothing to do with real config drift.

The canonical offender is `community.docker.docker_compose_v2`. The module documents itself as only partially idempotent, and compose projects with `restart: no` init containers (kafka-init-topics, elasticsearch-ilm-init, and similar one-shots) trip it every time: the init container exits cleanly, the next `docker compose up` sees "not running", emits a `Starting` event, and the module reports `changed=true`. Pair that with a handler-driven restart and every apply fires the handler on a stack that did not actually drift.

## Anti-pattern: cross-wired register + handler `when:`

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

## Anti-pattern: fallback task gated by "did anything change"

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

## Option A: always converge in flow

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

## Option B: handler-only convergence

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

## Decision heuristic

Inspect the compose file or service definition. Choose option B (handler-only) when any of these apply:

- The compose file has `restart: "no"` init/setup containers or one-shot jobs that exit after running (kafka-init-topics, `*-ilm-init`, schema-seeders). `docker_compose_v2` flags them as "not running" on every apply and reports `changed=true`.
- Startup ordering matters and services use `depends_on: condition: service_healthy`. `state: restarted` (docker compose restart) does not re-evaluate healthchecks; a stop+start handler pair does.
- The managed resource has any documented partial-idempotency caveat in its module docs.

Otherwise -- single-container stacks, straightforward systemd units, modules whose `state: present` is fully declarative -- option A is simpler and preferred.
