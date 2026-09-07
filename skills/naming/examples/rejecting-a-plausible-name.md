# Rejecting a plausible name after selection

A maintainer proposes `select_active_subscriptions` for the operation currently
called `select_access_subscriptions`. The initial naming request describes it as
"select the subscriptions that currently receive service." The candidate has a
clear action, full words, and a plural object. A preliminary selection favors it
because "active" sounds like a natural description of current service.

That selection is a hypothesis. This original scenario has an executable
[input packet](../tests/fixtures/contextual-review/README.md), including a
[local glossary](../tests/fixtures/contextual-review/GLOSSARY.md). Its vocabulary
settles the meaning more precisely than everyday usage of "active."

The plausible alternatives are `select_active_subscriptions`,
`select_access_subscriptions`, and `select_entitled_subscriptions`. The last
candidate would require evidence that this service uses "entitled" for its access
policy. The supplied glossary already defines "access subscription."

The proposed call below is illustrative; it shows the expectation being reviewed:

```text
service_access = select_active_subscriptions(subscriptions)
```

A reader who knows the enum can reasonably expect records in `ACTIVE`. The
distinct contextual review reads the implementation, both callers, glossary, and
contract independently of the preliminary preference:

| Evidence | Observation | Naming consequence |
| --- | --- | --- |
| [Selection](../tests/fixtures/contextual-review/subscriptions.py) | Membership includes `ACTIVE` and `GRACE_PERIOD` | `active` narrows the apparent membership |
| [Payment recovery caller](../tests/fixtures/contextual-review/callers.py) | Narrows the selected records to `GRACE_PERIOD` | Grace-period records are a required consumer input |
| [Glossary](../tests/fixtures/contextual-review/GLOSSARY.md) | Active means payment settled; grace period retains access during recovery | The local state distinction is explicit |
| [Contract](../tests/fixtures/contextual-review/contract.md) | Both states belong to service access; only grace period belongs to recovery | The broader access concept agrees across code and prose |

**Review outcome: reject `select_active_subscriptions`; retain
`select_access_subscriptions`.** The context makes access the clear winner. Its
meaning covers both required states and uses the service's established term.
Changing the membership predicate to rescue the proposed name would break the
documented recovery behavior.

The retained call in `access_roster` is:

```text
tuple(subscription.identifier for subscription in select_access_subscriptions(subscriptions))
```

Verification ran in an isolated copy of the five-file packet on 2026-09-06. From
that copy, `python3 callers.py` printed:

```text
Service access: account-copper, account-maple
Payment recovery: account-maple
```

`python3 -m doctest -v contract.md` reported **7 passed and 0 failed**. This
executes selection, both rosters, and empty input. Static inspection additionally
supports the contract's ordering and repeated-record behavior; these seven
examples give narrower execution coverage than the full written contract.

The recheck compares the retained name with both consumers and the state table:
all three express access eligibility. The packaged fixture remains unchanged.
The naming judgment is local to this modeled subscription service; a different
service's use of "active" needs its own evidence. Human review of this example
remains pending. See [contextual validation](../references/contextual-validation.md)
for the procedure and [validation report](../templates/validation-report.md) for
recording selection and review separately.
