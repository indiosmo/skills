# Service access contract

This original scenario models a subscription service that retains access during
payment recovery. A lifecycle process supplies each subscription's current state.

## Selection

`select_access_subscriptions(subscriptions)` consumes an iterable of
`Subscription` values and returns a tuple of the input records whose state grants
service access.

| State | Included in service access | Included in payment recovery roster |
| --- | --- | --- |
| `ACTIVE` | Yes | No |
| `GRACE_PERIOD` | Yes | Yes |
| `SUSPENDED` | No | No |
| `CANCELED` | No | No |

The returned tuple preserves input order and repeated occurrences. Each result
is the original subscription object. Empty input produces an empty tuple. A
single-pass iterable is consumed once. Subscription values are immutable.

## Consumers

`access_roster` extracts identifiers from the access selection for provisioning.
`payment_recovery_roster` narrows that selection to subscriptions in the grace
period for recovery follow-up. A grace-period agreement therefore appears in
both views.

The example below runs with `python3 -m doctest contract.md` from this directory:

```pycon
>>> from subscriptions import Subscription, SubscriptionState, select_access_subscriptions
>>> from callers import access_roster, payment_recovery_roster
>>> subscriptions = (
...     Subscription("account-copper", SubscriptionState.ACTIVE),
...     Subscription("account-maple", SubscriptionState.GRACE_PERIOD),
...     Subscription("account-slate", SubscriptionState.SUSPENDED),
...     Subscription("account-birch", SubscriptionState.CANCELED),
... )
>>> tuple(subscription.identifier for subscription in select_access_subscriptions(subscriptions))
('account-copper', 'account-maple')
>>> access_roster(subscriptions)
('account-copper', 'account-maple')
>>> payment_recovery_roster(subscriptions)
('account-maple',)
>>> select_access_subscriptions(())
()

```

See the [glossary](GLOSSARY.md) for the service's state vocabulary.
