"""Translate the retry configuration JSON contract into a local policy value."""

import json
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Store whether configuration enables automatic retries after failures."""

    retry: bool = False

    def __post_init__(self) -> None:
        if type(self.retry) is not bool:
            raise TypeError("retry must be a boolean")


def from_json(document: str) -> RetryPolicy:
    """Read a policy object, applying the false default for an omitted field."""
    configuration = json.loads(document)
    if not isinstance(configuration, dict):
        raise TypeError("retry configuration must be an object")
    if configuration.keys() - {"retry"}:
        raise ValueError("unknown retry configuration field")
    return RetryPolicy(retry=configuration.get("retry", False))


def to_json(policy: RetryPolicy) -> str:
    """Emit the established public field with its effective boolean value."""
    return json.dumps({"retry": policy.retry}, sort_keys=True)
