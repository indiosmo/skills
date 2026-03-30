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
4. **Dependencies** -- what this module depends on and what depends on it
5. **Variables / configuration** -- if this module exposes configuration, document it here with
   defaults. Use tables for structured variable documentation.
6. **Links to deeper documentation** -- if there are child READMEs or reference docs, point to
   them

### Variable and configuration documentation

When a module exposes configuration (environment variables, config knobs, build options, defaults),
document them in a table at the component level where they are defined:

```markdown
## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `LOG_LEVEL` | `info` | Minimum log level (`debug`, `info`, `warn`, `error`) |
| `MAX_CONNECTIONS` | `64` | Maximum concurrent client connections |
```

Configuration that comes from a higher level (project-wide settings, parent module defaults) should
be mentioned with a note about where it originates, not re-documented. "The `BUILD_TYPE` option is
set in the root CMake configuration; see the top-level README for details."

### Dependency documentation

When modules depend on each other, state it explicitly. This creates implicit reading order and
helps newcomers understand the build-up:

```markdown
## Dependencies

- **core/logging** -- this module uses the shared logging framework; initialize it first
- **core/config** -- configuration parsing must run before this module loads
  (config also initializes the thread pool that this module relies on)
```

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
