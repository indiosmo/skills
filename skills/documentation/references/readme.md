# READMEs

A README answers: what is this, why does it exist, and how do I get oriented?

Place a README in any directory that a newcomer might land in -- the project root, each major
module or service, and any directory whose purpose is not obvious from its name. Keep each README
focused on its own scope. The root README is the entry point; child READMEs explain their own
area.

## The hierarchy pattern

READMEs form a progressive refinement chain. Each level assumes the reader has read the parent
level and narrows the focus accordingly:

```
Root README        "Here is the forest"    -- what the project is, architecture, getting started
  Module README    "Here are the trees"    -- how this subsystem is organized, its mechanics
    Component README  "Here is one tree"   -- what this piece does, its variables, its dependencies
```

Each level covers what its parent cannot:

- **Root**: Project vision, overall architecture, key concepts, setup instructions, directory
  purpose map. Introduces major subsystems with a sentence or two and points the reader down.
- **Module/subsystem**: Narrows to its own domain. Explains directory layout, internal mechanics,
  patterns that recur within this subsystem. Does not re-explain concepts the root already covers.
- **Component**: Explains what this specific piece does, why it exists, what it depends on,
  and what variables or configuration it exposes. Assumes the reader understands the parent context.

The key discipline: each level **delegates down** rather than restating. When the root README
says "see the individual role READMEs for details," it is trusting the child documents to do
their job. This prevents duplication and keeps each document focused.

## Root README structure

1. **Project name and one-line description** -- what this project is, in one sentence
2. **Brief overview** -- what problem this solves, the key concepts a newcomer needs to know
   (2-3 paragraphs at most)
3. **Getting started** -- setup, prerequisites, first run. The commands someone types on day one.
4. **High-level architecture or repo layout** -- briefly describe how the project is organized,
   what each major directory or subsystem is responsible for, and link to deeper docs. A table
   mapping directory to purpose works well here. Do not enumerate every file -- describe the
   organizational pattern.
5. **Common workflows or commands** -- the handful of things people do most often
6. **Further reading** -- links to ADRs, runbooks, architecture docs, or external resources

The root README should be readable in under two minutes. If it is growing beyond that, content
is probably better placed in a child README or a dedicated guide.

## Module and component READMEs

These follow a simpler pattern:

1. **What this is and why it exists** -- one or two sentences justifying the module's existence
   within the larger system
2. **Key concepts and how the parts relate** -- the internal organization, how pieces interact,
   any patterns that repeat within this module
3. **How to extend or modify it** -- the steps for adding a new instance of whatever this module
   manages (a new role, a new source, a new handler)
4. **Dependencies that the tool cannot express** -- only if there are any. If
   `meta/main.yml`, `pyproject.toml`, `package.json`, dbt `ref()`, etc. already express the
   relationship, say nothing -- readers know where to look. Document only coupling the native
   mechanism can't capture (cross-tool ordering, implicit runtime prerequisites, non-code
   prerequisites, conditional deps, or a deliberate *non*-use of the native mechanism). See
   "Dependency documentation" below.
5. **Non-obvious operational notes** -- behaviors that surprise a reader (e.g., "disabling
   `feature_x` does not remove an existing deployment"); cross-references to relevant ADRs
6. **Links to deeper documentation** -- if there are child READMEs or reference docs, point to
   them

### Variable and configuration documentation

The file that defines a variable owns its documentation. A README does not list variables,
defaults, or required inputs -- not even a short list of "the ones you must set". The
definition file already shows which variables are required (no default, a `CHANGE_ME`
sentinel, or an `assert` at module entry); restating that in prose creates a second source of
truth that drifts on every add, rename, removal, or default change.

The README's job is to describe the *convention*: where variables live, how required ones are
signalled, where secrets belong. The reader who needs the list reads the definition file --
the only place the list stays correct.

**Bad** (transcribed table -- drifts on every default change):

```markdown
## Configuration

| Option            | Default | Description                       |
|-------------------|---------|-----------------------------------|
| `LOG_LEVEL`       | `info`  | Minimum log level                 |
| `MAX_CONNECTIONS` | `64`    | Maximum concurrent connections    |
```

**Also bad** (still drifts the moment a new required input is added):

```markdown
## Required variables

`DATABASE_URL` and `API_KEY` must be set. See `defaults/main.yml` for the full list.
```

**Good** (no variable names; the definition file carries the truth):

```markdown
## Configuration

See `defaults/main.yml` for variables and defaults. Variables without a default
(or set to `CHANGE_ME`) must be supplied by the caller; secrets belong in the host
vault and are referenced via the `vault_` prefix convention.
```

The same rule applies to Helm `values.yaml`, `.env.sample`, schema files, type definitions --
any file that defines configuration in one place. Let that file own its documentation, with
inline comments next to each value. Configuration that originates higher up (project-wide
settings, parent-module defaults) should be mentioned with a one-line pointer to where it is
defined, not re-documented.

### Dependency documentation

When the tool or framework can express a relationship natively, let that file own the truth and
do not transcribe it into the README. Ansible `meta/main.yml`, `pyproject.toml`, `package.json`,
`go.mod`, `Cargo.toml`, Compose `depends_on`, dbt `ref()`, Dagster asset deps, Terraform resource
references -- all are machine-read, always current, and usually introspectable from a CLI
(`dbt ls`, `dagster asset list`, `terraform graph`, `ansible-galaxy role list`). A README that
copies this information drifts the moment a dependency is added, removed, or reshaped. Point the
reader at the native source, or simply say nothing -- readers of an Ansible role know where
`meta/main.yml` lives.

Document a dependency in the README only when the relationship **cannot** be expressed in the
tool's own config. Representative cases:

- **Cross-tool ordering.** The coupling spans systems that can't see each other. "This role
  renders configs that a separate Terraform workspace consumes, so that workspace must apply
  after this role has run." Neither side's dependency graph captures the other.
- **Implicit runtime prerequisites.** State that must already exist but that the tool neither
  creates nor declares. "This role assumes the `msi` user already exists on the host (the
  `server` role creates it earlier in the playbook); no meta edge enforces the order."
- **Non-code prerequisites.** Things the system has no hook for at all: a manual SSH key
  placement, a DNS record in an unrelated change-management system, firewall rules provisioned
  outside this repo, a SaaS onboarding step.
- **Configuration-conditional dependencies.** "When `feature_x` is enabled, this module also
  requires the `vault_backend` service reachable on the network." Meta dependencies cannot be
  conditional on a variable, so a short note is warranted.
- **Deliberate non-use of a native mechanism.** When the *absence* of something a reader would
  expect is intentional, one sentence explains the absence. "Telegraf is included from
  `server/tasks/main.yml` rather than declared in `meta/main.yml` so it applies only when the
  server baseline applies on a host."

Keep these notes short and specific. Do not list **dependents** ("roles X, Y, Z depend on this
one") -- the dependent's own file is the source of truth and any list will drift the moment a
new dependent appears.

## Cross-referencing

Use relative links to connect documents within the hierarchy:

- Parent to child: "Each module under `src/` has its own README documenting purpose,
  dependencies, and configuration."
- Child to parent: "For the overall build configuration, see the
  [project README](../README.md#building)."
- Sibling to sibling: "This module depends on
  [networking](../networking/README.md) for transport."

Avoid deep links into sibling documents when a section reference would suffice -- sections get
renamed, but documents are more stable.

## Common mistakes

- **The root README that tries to be everything.** If the root README documents every module in
  detail, child READMEs become redundant or contradictory. Keep the root as a map, not an
  encyclopedia.
- **The orphan directory.** A directory with no README and a non-obvious name forces the reader
  to infer its purpose from the files inside. Add a brief README or at minimum a one-line
  comment in the parent README's directory table.
- **The stale setup section.** Getting-started instructions rot faster than anything else. Keep
  them minimal and executable -- ideally a single bootstrap command that handles the details.
  The more steps you list, the more likely one is outdated.
- **Restating the parent.** If the parent README explains that the project has three environments
  (dev, uat, prod), the child README should not re-explain that. Reference it and move on.
