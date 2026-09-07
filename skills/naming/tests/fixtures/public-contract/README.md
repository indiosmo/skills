# Public retry configuration fixture

This Python adapter reads and writes a small JSON configuration object. The
stored boolean means that configuration enables automatic retries after failures.
Execution code uses this setting together with failure classification and retry
budget when deciding whether to make another attempt.

Read `api.py`, `client.py`, `schema.json`, and `test_compatibility.py` together.
`RetryPolicy` is an internal value. `from_json` and `to_json` form the adapter
boundary. `client.py` represents an existing deployed consumer, and `schema.json`
declares the supported JSON representation.

## Behavior

| Input document | Adapter result | Emitted JSON value | Existing client result |
| --- | --- | --- | --- |
| `{}` | Default configuration | `{"retry": false}` | false |
| `{"retry": false}` | Retries disabled by configuration | `{"retry": false}` | false |
| `{"retry": true}` | Retries enabled by configuration | `{"retry": true}` | true |
| `{"retry": null}` | `TypeError` | Rejected | `TypeError` |
| `{"retry": 0}` or another nonboolean field value | `TypeError` | Rejected | `TypeError` |
| A JSON value with a non-object root | `TypeError` | Rejected | `TypeError` |
| An object with an unknown field | `ValueError` | Rejected | Extra fields are ignored |
| Malformed JSON | `json.JSONDecodeError` | Rejected | `json.JSONDecodeError` |

The adapter emits exactly one field, `retry`, with a JSON boolean value. Input
omission has an effective false value; serialization writes that value explicitly.
Construction of the internal policy also requires an actual Python `bool`.

## Authorized naming work

For an internal-rename request, improve the `RetryPolicy.retry` field name and
update its bound constructor keywords, reads, and assertions. Edit `api.py`,
`test_compatibility.py`, and the relevant internal-name prose in this README.
Keep the type and adapter function names, behavior, public JSON spelling,
`client.py`, and `schema.json` stable. Show the internal symbol mapping and
verification evidence separately from the name rationale.

For a migration-recommendation request, provide a proposal with its compatibility
assumptions and verification gates. The request's scope determines whether edits
are authorized.

## Run the fixture

Use Python 3.11 or newer. Copy these five files together into a disposable
directory and run the following command from that directory:

```sh
python3 -m unittest -v test_compatibility
```

The fixture uses the Python standard library. Tests exercise effective defaults,
strict booleans, errors, round trips, the declared schema fields, and the existing
client. Run the same command after an authorized edit and inspect the changed
bindings and wire representation.
