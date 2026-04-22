# Architectural Decision Records

An ADR is a short document that captures one significant technical decision along with its context
and consequences. ADRs exist because architecture knowledge evaporates -- the people who made a
decision move on, and six months later nobody remembers why the team chose PostgreSQL over DynamoDB
or why the API uses gRPC instead of REST. An ADR is a conversation with a future developer who
was not in the room.

ADRs are immutable once accepted. If circumstances change, write a new ADR that supersedes the old
one. The old record remains as a historical artifact -- it explains what the team knew and believed
at the time.

## Contents

- [When to write an ADR](#when-to-write-an-adr)
- [Template](#template) -- Nygard default and [MADR extended](#extended-template-madr-style)
- [Naming convention](#naming-convention) -- filename pattern, [bootstrap ADR](#the-bootstrap-adr)
- [Directory organization](#directory-organization) -- [large projects and monorepos](#large-projects-and-monorepos)
- [Lifecycle and statuses](#lifecycle-and-statuses) -- [immutability](#immutability), [linking between ADRs](#linking-between-adrs)
- [Writing style](#writing-style)
- [Example: a well-written ADR](#example-a-well-written-adr)
- [Retrofitting decisions](#retrofitting-decisions)
- [Setting up ADRs in a new project](#setting-up-adrs-in-a-new-project)

## When to write an ADR

Write an ADR when a decision:

- Has alternatives worth recording (there was a real choice to make)
- Is non-obvious or will be questioned by someone who was not in the room
- Is hard or expensive to reverse later
- Affects the system's structure, quality attributes, dependencies, or interfaces
- Establishes a pattern that the rest of the codebase should follow

Common triggers: choosing a database, adopting a framework, defining an API style, selecting a
messaging pattern, picking a deployment strategy, establishing testing practices, deciding on a
data model, choosing between build-vs-buy.

Do not write an ADR for trivial choices that no one will question, or for decisions that are
easily reversed with a one-line change. The goal is to capture decisions where future context
matters -- not to create bureaucracy.

## Template

Use the Nygard template as the default. It is the most widely adopted format, used by projects
like Backstage, Home Assistant, and the majority of open source projects that maintain ADRs. It
keeps records focused and short.

```markdown
# NUMBER. Title of Decision

**Status:** proposed | accepted | rejected | deprecated | superseded by [ADR-NUMBER](link)

**Date:** YYYY-MM-DD

## Context

Neutral description of the forces at play -- technical constraints, business requirements,
team capabilities, timeline pressures, and any other factors that shaped the decision. Describe
the problem without advocating for a solution. A reader should understand why this decision was
necessary.

## Decision

What was decided, stated in active voice. "We will use PostgreSQL as the primary data store."
Not "PostgreSQL was chosen" or "It was decided that..."

Include the key reasons that tipped the balance toward this option. If alternatives were
seriously considered, name them and briefly explain why they were not chosen.

## Consequences

All outcomes that follow from this decision -- positive, negative, and neutral. Be honest about
tradeoffs. Every significant decision has downsides; acknowledging them builds trust in the
record and helps future developers understand the constraints they inherited.
```

### Extended template (MADR style)

When a decision involves multiple viable alternatives that each deserve detailed evaluation, use
the MADR (Markdown Any Decision Records) extended format. This adds structured options analysis
to the Nygard base.

```markdown
# NUMBER. Title of Decision

**Status:** proposed | accepted | rejected | deprecated | superseded by [ADR-NUMBER](link)

**Date:** YYYY-MM-DD

## Context and Problem Statement

Describe the problem in 2-3 sentences, possibly framed as a question.
Example: "How should we handle authentication for the public API?"

## Decision Drivers

- Driver 1 (e.g., "Must support SSO for enterprise customers")
- Driver 2 (e.g., "Team has no experience with SAML")
- Driver 3 (e.g., "Budget constraint: no paid identity providers")

## Considered Options

1. Option A
2. Option B
3. Option C

## Decision Outcome

Chosen option: "Option B", because it best satisfies the decision drivers
[explain the key reasoning].

### Consequences

- Good, because [positive outcome]
- Bad, because [negative outcome]
- Neutral, because [side effect that is neither clearly good nor bad]

### Confirmation

How the team will verify that this decision is implemented correctly and achieving its intended
effect. Example: "Integration tests cover the OAuth flow; monitoring alerts on auth failure
rate exceeding 1%."

## Pros and Cons of the Options

### Option A

- Good, because [argument]
- Bad, because [argument]

### Option B

- Good, because [argument]
- Good, because [argument]
- Bad, because [argument]

### Option C

- Good, because [argument]
- Bad, because [argument]

## More Information

Links to research, spike results, relevant RFCs, meeting notes, or related ADRs.
```

Use the Nygard template for straightforward decisions where the reasoning is clear. Use the MADR
template when stakeholders need to see a structured comparison of alternatives -- for instance,
a database selection with five candidates, or a framework choice that affects the whole team.

## Naming convention

Files follow this pattern:

```
NNNN-short-title-in-kebab-case.md
```

Rules:
- **Number**: Zero-padded, monotonically increasing, never reused (0001, 0002, 0003...)
- **Title**: Lowercase with dashes (kebab-case), using a present-tense imperative verb phrase
- **Extension**: `.md`

Good names:
```
0001-record-architecture-decisions.md
0002-use-postgresql-for-persistence.md
0003-adopt-grpc-for-service-communication.md
0004-handle-authentication-with-oauth2.md
0012-replace-rabbitmq-with-kafka.md
```

The title should communicate the decision itself, not just the topic. "Use PostgreSQL for
persistence" is better than "database-choice" because it tells the reader the outcome at a
glance. The imperative verb reinforces that this is an action taken.

Some projects use a category prefix (as Dapr does: `API-005-state-store-behavior.md`,
`ARC-001-refactor-for-modularity.md`). This works well for large projects with many ADRs across
distinct domains. For most projects, sequential numbering without a prefix is sufficient.

### The bootstrap ADR

The first ADR in a project should document the decision to use ADRs themselves:

```
0001-record-architecture-decisions.md
```

This is a widely adopted convention (originated by adr-tools) that serves two purposes: it
establishes the format, and it gives new team members a concrete example of what an ADR looks
like.

## Directory organization

Store ADRs in a dedicated directory within the repository, close to the code they describe.
Common locations:

| Path | Notes |
|------|-------|
| `doc/adr/` | adr-tools default |
| `docs/adr/` | log4brains default, common in many projects |
| `docs/decisions/` | Used by MADR project itself |
| `docs/architecture-decisions/` | Used by Backstage |

Pick one and stay consistent. For most projects, `docs/adr/` is a reasonable default.

### Large projects and monorepos

For projects with many ADRs spanning distinct domains, organize by category:

```
docs/adr/
  api/
    API-001-use-rest-for-public-api.md
    API-002-pagination-strategy.md
  architecture/
    ARC-001-adopt-hexagonal-architecture.md
    ARC-002-event-sourcing-for-orders.md
  engineering/
    ENG-001-ci-pipeline-design.md
```

Dapr uses this pattern with prefixes (API, ARC, CLI, SDK, ENG) and a central
`decision_records.md` index file. This scales well when a project accumulates dozens of ADRs.

For monorepos, keep global ADRs at the root and package-specific ADRs alongside each package:

```
docs/adr/                          # Cross-cutting decisions
packages/auth/docs/adr/            # Auth-service-specific decisions
packages/billing/docs/adr/         # Billing-service-specific decisions
```

## Lifecycle and statuses

| Status | Meaning |
|--------|---------|
| **proposed** | Under discussion, not yet approved |
| **accepted** | Approved by the team; the decision is in effect |
| **rejected** | The team evaluated and declined this approach |
| **deprecated** | No longer relevant (context changed, but no replacement needed) |
| **superseded** | Replaced by a newer ADR (must link to the replacement) |

Typical flow:

```
proposed --> accepted --> superseded by ADR-NNNN
         \-> rejected
accepted --> deprecated
```

### Immutability

Once an ADR is accepted, its body is never modified. Only the **Status** field changes (to
deprecated or superseded). If a decision needs to change, write a new ADR that:

1. References the old ADR it supersedes
2. Explains what changed and why
3. States the new decision

Then update the old ADR's status to "Superseded by [ADR-NNNN](link)". The old record stays
in the log as a historical artifact.

This immutability is the core property that makes ADRs trustworthy. If people edit old records,
the log becomes unreliable -- you can never be sure whether the text reflects the original
reasoning or a retroactive justification.

### Linking between ADRs

Reference related ADRs by number in the Context or Consequences sections. When one ADR
supersedes another, both records should cross-reference each other:

- The new ADR: "This supersedes [ADR-0003](0003-use-rabbitmq.md), which chose RabbitMQ."
- The old ADR status: "Superseded by [ADR-0012](0012-replace-rabbitmq-with-kafka.md)"

## Writing style

- **Keep it short.** One to two pages maximum. An ADR captures a single decision, not a design
  document. If you are writing more than two pages, the scope is probably too broad -- split it
  into multiple ADRs.
- **Write at decision time.** Context fades fast. Capture the reasoning while the discussion is
  fresh. Retroactive ADRs are better than nothing but inevitably lose nuance.
- **Use value-neutral language in the Context section.** Describe forces and facts objectively.
  The Context should not advocate for a particular solution -- that belongs in the Decision
  section.
- **State the decision in active voice.** "We will use X" rather than "X was chosen" or "It
  was decided to use X." Active voice makes it clear that the team took a deliberate action.
- **Document alternatives.** If you considered other options, name them and briefly explain why
  they were not chosen. This prevents future developers from re-evaluating options that were
  already ruled out.
- **Be honest about tradeoffs.** Every significant decision has downsides. Acknowledging them
  makes the record credible and helps future developers understand the constraints they
  inherited.
- **One decision per record.** If you find yourself writing "We also decided to..." -- stop.
  That is a separate ADR.
- **Use full sentences.** ADRs are prose, not bullet-point dumps. Write in a way that a future
  team member can read and understand without additional context.

## Example: a well-written ADR

```markdown
# 7. Use PostgreSQL for order persistence

**Status:** accepted

**Date:** 2025-11-15

## Context

The order service needs a persistent data store. Current requirements include ACID transactions
for order state transitions, complex queries for reporting (joins across orders, line items, and
customers), and a projected volume of ~50,000 orders per day within 18 months.

The team has production experience with PostgreSQL and MySQL. We evaluated DynamoDB as a managed
alternative to reduce operational overhead.

## Decision

We will use PostgreSQL as the primary data store for the order service.

PostgreSQL was chosen over DynamoDB because the order domain relies heavily on relational queries
and multi-table transactions, which DynamoDB handles poorly without significant denormalization.
MySQL was not chosen because the team's existing tooling and deployment automation targets
PostgreSQL, and the feature differences between the two are not significant for this use case.

We will run PostgreSQL on RDS to reduce operational burden while retaining full SQL compatibility.

## Consequences

- The order service gets full ACID guarantees and rich query support out of the box
- RDS handles backups, patching, and failover, reducing on-call load
- We inherit RDS pricing, which at projected volumes will cost ~$400/month for a db.r6g.large
  Multi-AZ instance
- If order volume grows beyond PostgreSQL's vertical scaling limits, we will need to consider
  read replicas or sharding -- this is unlikely within the 18-month horizon but should be
  revisited if projections change
- Schema migrations must be managed carefully to avoid downtime; we will use a migration tool
  (to be decided in a separate ADR)
```

Notice: the Context is factual and does not advocate. The Decision is in active voice and names
the alternatives. The Consequences are specific and include both benefits and costs.

## Retrofitting decisions

Sometimes significant decisions were made weeks or months ago without an ADR. It is still
valuable to capture them retroactively. When writing a retrospective ADR:

- State clearly in the Context that this decision was made on a prior date and is being
  documented after the fact
- Reconstruct the reasoning as faithfully as possible -- talk to the people involved if they
  are still available
- Set the status to **accepted** (it is already in effect)
- Set the date to the original decision date, not the date the ADR was written

A retroactive ADR with imperfect context is better than no record at all.

## Setting up ADRs in a new project

1. Create the directory: `mkdir -p docs/adr`
2. Write the bootstrap ADR (`0001-record-architecture-decisions.md`)
3. Add a brief mention in the project README pointing to the ADR directory
4. Agree on a review process -- ADRs should go through pull requests just like code

No special tooling is needed. ADRs are just markdown files written by hand and managed through
git and pull requests.
