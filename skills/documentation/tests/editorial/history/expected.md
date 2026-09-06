# Expected history outputs

## Code changelog

- Improve the invalid-UTF-8 error message to identify the required input format
  (`fixture-01`, `fixture-04`).

## Documentation changelog

- Add an empty-file example to the line-count guide (`fixture-01`).

## Release notes

The counter identifies invalid UTF-8 input with the message "Provide a UTF-8 text
file". The line-count guide includes an empty-file example with output `0`.

## Review record

The Python 3.15 compatibility assertion in `fixture-04` is unverified: the
fixture contains no runtime test or approved compatibility metadata. Binary
input is absent from the shipped changes because `fixture-03` fully reverts
`fixture-02`. Human release and factual review remains pending.
