# Subscription access review input

This small, original Python service selects subscriptions for an access roster
and a payment recovery roster. Its local policy grants access to subscriptions
in the active and grace-period states. The [contract](contract.md) specifies
selection behavior, ordering, and consumer results.

## Setup and execution

Use Python 3.10 or later and its standard library. From this directory, run:

```sh
python3 callers.py
python3 -m doctest contract.md
```

The caller demonstration prints:

```text
Service access: account-copper, account-maple
Payment recovery: account-maple
```

## Input packet

The review input consists of these five files:

- [subscriptions.py](subscriptions.py): state values, records, and selection.
- [callers.py](callers.py): service access and payment recovery consumers.
- [GLOSSARY.md](GLOSSARY.md): local subscription terminology.
- [contract.md](contract.md): behavior and executable usage examples.
- This README: setup and input orientation.

A task prompt supplies the operation and naming question to review. Read these
files as evidence of the service's current behavior and vocabulary; running the
examples supplies additional observable evidence. Apply the task prompt's scope
when deciding whether to recommend a name or edit code.
