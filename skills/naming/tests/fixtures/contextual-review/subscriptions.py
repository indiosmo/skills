"""Subscription access selection for the example service."""

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum


class SubscriptionState(Enum):
    ACTIVE = "active"
    GRACE_PERIOD = "grace_period"
    SUSPENDED = "suspended"
    CANCELED = "canceled"


@dataclass(frozen=True, slots=True)
class Subscription:
    identifier: str
    state: SubscriptionState


def select_access_subscriptions(
    subscriptions: Iterable[Subscription],
) -> tuple[Subscription, ...]:
    """Return subscriptions whose current state grants service access."""
    return tuple(
        subscription
        for subscription in subscriptions
        if subscription.state in {SubscriptionState.ACTIVE, SubscriptionState.GRACE_PERIOD}
    )
