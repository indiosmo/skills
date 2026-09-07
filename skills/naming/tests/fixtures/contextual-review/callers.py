"""Access roster and payment recovery views for the example service."""

from collections.abc import Iterable

from subscriptions import Subscription, SubscriptionState, select_access_subscriptions


def access_roster(subscriptions: Iterable[Subscription]) -> tuple[str, ...]:
    """Return subscription identifiers for the service access roster."""
    return tuple(subscription.identifier for subscription in select_access_subscriptions(subscriptions))


def payment_recovery_roster(
    subscriptions: Iterable[Subscription],
) -> tuple[str, ...]:
    """Return grace-period subscriptions that retain access during recovery."""
    return tuple(
        subscription.identifier
        for subscription in select_access_subscriptions(subscriptions=subscriptions)
        if subscription.state is SubscriptionState.GRACE_PERIOD
    )


if __name__ == "__main__":
    subscriptions = (
        Subscription("account-copper", SubscriptionState.ACTIVE),
        Subscription("account-maple", SubscriptionState.GRACE_PERIOD),
        Subscription("account-slate", SubscriptionState.SUSPENDED),
        Subscription("account-birch", SubscriptionState.CANCELED),
    )
    print("Service access:", ", ".join(access_roster(subscriptions)))
    print("Payment recovery:", ", ".join(payment_recovery_roster(subscriptions)))
