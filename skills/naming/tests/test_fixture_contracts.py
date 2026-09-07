"""Exercise initial fixture contracts in isolated copies with trusted assertions."""

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

FIXTURE_DIRECTORY = Path(__file__).resolve().parent / "fixtures"
CONTRACTS = {
    "contextual-review": """
from dataclasses import FrozenInstanceError
from subscriptions import Subscription, SubscriptionState, select_access_subscriptions
from callers import access_roster, payment_recovery_roster
import doctest

active = Subscription("active", SubscriptionState.ACTIVE)
grace = Subscription("grace", SubscriptionState.GRACE_PERIOD)
suspended = Subscription("suspended", SubscriptionState.SUSPENDED)
canceled = Subscription("canceled", SubscriptionState.CANCELED)
records = (suspended, grace, active, canceled, grace)

class SinglePassSubscriptions:
    def __init__(self):
        self.iterated = False

    def __iter__(self):
        assert not self.iterated, "Subscription iterable was consumed more than once"
        self.iterated = True
        return iter(records)

selected = select_access_subscriptions(SinglePassSubscriptions())
assert selected == (grace, active, grace)
assert selected[0] is grace and selected[1] is active and selected[2] is grace
assert access_roster(iter(records)) == ("grace", "active", "grace")
assert payment_recovery_roster(iter(records)) == ("grace", "grace")
assert select_access_subscriptions(iter(())) == ()
assert access_roster(()) == () and payment_recovery_roster(()) == ()
for state, expected in ((SubscriptionState.ACTIVE, True), (SubscriptionState.GRACE_PERIOD, True),
                        (SubscriptionState.SUSPENDED, False), (SubscriptionState.CANCELED, False)):
    record = Subscription(state.value, state)
    assert bool(select_access_subscriptions((record,))) is expected
try:
    active.identifier = "changed"
except FrozenInstanceError:
    pass
else:
    raise AssertionError("Subscription values must remain immutable")
assert doctest.testfile("contract.md", module_relative=False).failed == 0
""",
    "local-rename": """
from retry_policy import retry_ok
from callers import next_action
import unrelated
import re
from pathlib import Path

rows = (
    (False, True, 1, 3, True, "retry"), (False, True, 3, 3, False, "stop"),
    (False, False, 1, 3, False, "stop"), (False, False, 3, 3, False, "stop"),
    (True, True, 1, 3, False, "stop"), (True, True, 3, 3, False, "stop"),
    (True, False, 1, 3, False, "stop"), (True, False, 3, 3, False, "stop"),
    (False, True, 0, 0, False, "stop"), (False, True, 4, 3, False, "stop"),
    (False, True, 2, 3, True, "retry"),
)
for disabled, transient_failure, attempt_count, attempt_limit, expected, action in rows:
    assert retry_ok(disabled=disabled, transient_failure=transient_failure,
                    attempt_count=attempt_count, attempt_limit=attempt_limit) is expected
    assert next_action(retry_disabled=disabled, transient_failure=transient_failure,
                       attempt_count=attempt_count, attempt_limit=attempt_limit) == action
assert unrelated.retry_ok(()) is False
assert unrelated.retry_ok((True, True)) is True
assert unrelated.retry_ok((True, False)) is False
examples = re.findall(r"^```python\\n(.*?)^```", Path("usage.md").read_text(), flags=re.MULTILINE | re.DOTALL)
assert len(examples) == 1
exec(compile(examples[0], "usage.md", "exec"), {})
""",
    "public-contract": """
import json
from pathlib import Path
from api import RetryPolicy, from_json, to_json
from client import retry_is_enabled

assert RetryPolicy().retry is False
for document, expected in (("{}", False), ('{"retry": false}', False), ('{"retry": true}', True)):
    policy = from_json(document)
    assert policy.retry is expected
    assert json.loads(to_json(policy)) == {"retry": expected}
    assert retry_is_enabled(to_json(policy)) is expected
    assert from_json(to_json(policy)) == policy
for invalid_value in (None, 0, 1, 0.0, 1.0, "false", "true", [], {}):
    document = json.dumps({"retry": invalid_value})
    for operation, argument in ((from_json, document), (retry_is_enabled, document), (RetryPolicy, invalid_value)):
        try:
            operation(argument)
        except TypeError:
            pass
        else:
            raise AssertionError(f"Accepted invalid boolean: {invalid_value!r}")
for document in ("null", "false", "true", "0", '"retry"', "[]"):
    for operation in (from_json, retry_is_enabled):
        try:
            operation(document)
        except TypeError:
            pass
        else:
            raise AssertionError(f"Accepted nonobject document: {document}")
for document in ("", "{", '{"retry": False}'):
    for operation in (from_json, retry_is_enabled):
        try:
            operation(document)
        except json.JSONDecodeError:
            pass
        else:
            raise AssertionError("Accepted malformed JSON")
for document in ('{"unexpected": true}', '{"retry": true, "unexpected": false}'):
    try:
        from_json(document)
    except ValueError:
        pass
    else:
        raise AssertionError("Accepted unknown adapter field")
assert retry_is_enabled('{"retry": true, "unexpected": false}') is True
schema = json.loads(Path("schema.json").read_text())
assert schema["type"] == "object" and schema["additionalProperties"] is False
assert set(schema["properties"]) == {"retry"}
assert schema["properties"]["retry"]["type"] == "boolean"
assert schema["properties"]["retry"]["default"] is False
assert schema.get("required", []) == []
""",
}


def fixture_hashes(directory: Path) -> dict[str, str]:
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in directory.iterdir() if path.is_file()}


@pytest.mark.parametrize("scenario", list(CONTRACTS))
def test_initial_fixture_contract(scenario: str, tmp_path: Path) -> None:
    source = FIXTURE_DIRECTORY / scenario
    assert source.is_dir(), f"Fixture input missing: {scenario}"
    original_hashes = fixture_hashes(source)
    assert original_hashes, f"Fixture input selection is empty: {scenario}"
    checkout = tmp_path / scenario
    checkout.mkdir()
    for filename in original_hashes:
        shutil.copy2(source / filename, checkout / filename)
    try:
        result = subprocess.run(
            [sys.executable, "-B", "-c", CONTRACTS[scenario]],
            cwd=checkout,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
    finally:
        assert fixture_hashes(source) == original_hashes, "Packaged fixture inputs changed"
