# A returned value can accompany mutation

An engineer asks for a clearer name than `validate_import` while writing an
internal catalog-import command. This original scenario supplies the operation
contract and the two callers below. The request authorizes a naming recommendation.

The operation parses catalog rows, collects malformed-row issues, and writes
accepted rows in one transaction. It returns an `ImportReport` after that
transaction commits, including accepted-row count and rejected-row issues.
If storage fails, the transaction rolls back and raises `ImportCommitError`.
An input containing only rejected rows produces a report with zero accepted rows.
An empty input produces a report with zero accepted rows and no issues.

The available evidence is this stipulated contract and the pseudocode. Catalog,
row, transaction, and report are local software concepts here. The action/result
review follows [functions and methods](../references/functions-and-methods.md);
it applies [local contextual-review policy](../references/evidence.md#local-005).
No repository implementation, external consumer, or storage adapter is supplied.

## Establish the operation and its uses

Illustrative pseudocode, not an executable implementation:

```text
operation validate_import(rows, catalog_store) -> ImportReport
    accepted_rows, rejected_row_issues = parse_catalog_rows(rows)
    within catalog_store.transaction():
        catalog_store.write_rows(accepted_rows)
    return ImportReport(count(accepted_rows), rejected_row_issues)

command import_catalog_file(path):
    try:
        import_report = validate_import(read_rows(path), catalog_store)
        display_import_report(import_report)
    on ImportCommitError:
        display_commit_failure()

screen preview_import(path):
    import_report = validate_import(read_rows(path), catalog_store)
    display_rejected_rows(import_report.rejected_row_issues)
```

The preview caller is material evidence: it invokes the same write transaction
as the import command. The supplied contract settles the current effects. The
product intent of the preview screen remains unresolved. Ask its owner whether
opening a preview is supposed to commit accepted rows; that answer determines a
behavior change, independently of the function's current naming decision.

## Choose a name for the established behavior

`validate_catalog_rows` focuses on checking, which is only one stage of the
supplied operation. `parse_catalog_rows` already names the parsing helper and
would collapse two different contracts. `import_catalog_rows` describes the
transactional action on accepted catalog rows. It is the clear winner among
these candidates because committing rows is a decisive requirement; scoring
ineligible candidates would add no useful comparison.

Recommended illustrative use sites:

```text
try:
    import_report = import_catalog_rows(rows, catalog_store)
    display_import_report(import_report)
on ImportCommitError:
    display_commit_failure()

import_report = import_catalog_rows([], catalog_store)
assert import_report.accepted_row_count == 0
```

The assignment names a report, and the operation names an import. Together with
the `ImportReport` result and `ImportCommitError` branch, the call communicates
action, result, and failure. The contract defines completion at transaction
commit. Keep the existing result name `import_report`: its consumer reads both
counts and issues, making it an accurate, proportionate retention decision.

## Distinct contextual review

After selection, review the recommendation against each supplied context.

| Examined evidence | Finding | Outcome |
| --- | --- | --- |
| Transaction followed by return in the operation sketch | Returning the report follows the write boundary | `import_catalog_rows` fits the supplied mutation and completion contract |
| Rejected-only and empty-input contracts | A completed import can have zero accepted rows | Keep the result as a report; a name promising every row succeeded would overstate the contract |
| Import command's error branch | Storage failure is distinguishable from row rejection | Retain `ImportCommitError` for this stipulated failure boundary |
| Preview caller | Displaying rejected rows invokes a commit-producing action | Flag the preview's behavior for an intent decision; the selected operation name exposes the mismatch |
| Parsing helper | Parsing and transactional importing have distinct declarations | The recommended name preserves their distinction |

Assessment: recommend `import_catalog_rows` for the described current operation
and retain `import_report`. The preview finding remains open; changing the name
alone leaves the stated effects intact. A proposed checking-only preview needs
its own contract and implementation decision, as explored in
[unclear abstraction](unclear-abstraction.md).

These findings come from static review of original pseudocode and stated cases.
Runnable behavior, rollback guarantees, actual exception translation, and affected
uses remain unverified. Before an applied rename, inspect the real implementation
and both caller paths, exercise empty/rejected/mixed inputs and a failing commit,
and check the resulting stored rows as well as the report or exception. The
[rename guide](../references/renaming.md) supplies that change workflow.
