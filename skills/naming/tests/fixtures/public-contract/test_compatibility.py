"""Exercise retry policy values and the established JSON client contract."""

import json
import unittest
from pathlib import Path

from api import RetryPolicy, from_json, to_json
from client import retry_is_enabled


class CompatibilityTests(unittest.TestCase):
    def test_omitted_setting_defaults_to_false(self) -> None:
        self.assertIs(RetryPolicy().retry, False)
        self.assertIs(from_json("{}").retry, False)
        self.assertEqual(json.loads(to_json(from_json("{}"))), {"retry": False})
        self.assertIs(retry_is_enabled("{}"), False)

    def test_explicit_settings_round_trip_and_reach_existing_client(self) -> None:
        for document, expected in (('{"retry": false}', False), ('{"retry": true}', True)):
            with self.subTest(document=document):
                policy = from_json(document)
                self.assertIs(policy.retry, expected)
                self.assertEqual(policy, RetryPolicy(retry=expected))
                response = to_json(policy)
                self.assertEqual(json.loads(response), {"retry": expected})
                self.assertIs(retry_is_enabled(response), expected)
                self.assertEqual(from_json(response), policy)

    def test_internal_construction_round_trips(self) -> None:
        for setting in (False, True):
            with self.subTest(setting=setting):
                policy = RetryPolicy(retry=setting)
                self.assertEqual(from_json(to_json(policy)), policy)

    def test_nonboolean_settings_are_rejected(self) -> None:
        for value in (None, 0, 1, 0.0, 1.0, "false", "true", [], {}):
            with self.subTest(value=value):
                document = json.dumps({"retry": value})
                with self.assertRaises(TypeError):
                    from_json(document)
                with self.assertRaises(TypeError):
                    retry_is_enabled(document)
                with self.assertRaises(TypeError):
                    RetryPolicy(retry=value)  # pyright: ignore[reportArgumentType]

    def test_nonobject_documents_are_rejected(self) -> None:
        for document in ("null", "false", "true", "0", '"retry"', "[]"):
            with self.subTest(document=document):
                with self.assertRaises(TypeError):
                    from_json(document)
                with self.assertRaises(TypeError):
                    retry_is_enabled(document)

    def test_malformed_json_is_rejected(self) -> None:
        for document in ("", "{", '{"retry": False}'):
            with self.subTest(document=document):
                with self.assertRaises(json.JSONDecodeError):
                    from_json(document)
                with self.assertRaises(json.JSONDecodeError):
                    retry_is_enabled(document)

    def test_unknown_fields_are_rejected_by_adapter(self) -> None:
        for document in ('{"unexpected": true}', '{"retry": true, "unexpected": false}'):
            with self.subTest(document=document):
                with self.assertRaises(ValueError):
                    from_json(document)
        self.assertIs(retry_is_enabled('{"retry": true, "unexpected": false}'), True)

    def test_declared_schema_matches_supported_representation(self) -> None:
        schema = json.loads(Path(__file__).with_name("schema.json").read_text())
        self.assertEqual(schema["type"], "object")
        self.assertIs(schema["additionalProperties"], False)
        self.assertEqual(set(schema["properties"]), {"retry"})
        self.assertEqual(schema["properties"]["retry"]["type"], "boolean")
        self.assertIs(schema["properties"]["retry"]["default"], False)
        self.assertEqual(schema.get("required", []), [])


if __name__ == "__main__":
    unittest.main()
