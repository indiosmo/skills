"""Read retry configuration responses using the established client contract."""

import json


def retry_is_enabled(document: str) -> bool:
    """Return the configured retry setting, defaulting omission to false."""
    configuration = json.loads(document)
    if not isinstance(configuration, dict):
        raise TypeError("retry configuration must be an object")
    retry = configuration.get("retry", False)
    if type(retry) is not bool:
        raise TypeError("retry must be a boolean")
    return retry
