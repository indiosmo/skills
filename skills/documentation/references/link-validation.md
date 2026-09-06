# Validate documentation links

Use this guide when reviewing links in source documents or an existing generated
site. Start with the changed pages and their relevant neighbors. Save the selected
inputs, command, checker version, raw report, and observation date with the
verification record so another reviewer can distinguish coverage from omissions.

## Run the checker

Use lychee 0.24.2, distributed by the pinned `lychee-bin` Python package:

```sh
uvx --from lychee-bin==0.24.2 lychee --version
uvx --from lychee-bin==0.24.2 lychee --config "$documentation_skill/assets/lychee/lychee.toml" -- docs/selected-page.md
```

Set `documentation_skill` to the absolute installed skill directory and run from
the consuming project. The config emits plain JSON suitable for a saved report.
An unavailable tool is an unchecked verification step. In restricted environments,
set uv's tool directory to permitted scratch space using `UV_TOOL_DIR` when needed.

For a local-only pass, add `--offline`. For generated HTML, first run the project's
existing build into temporary output, then check that output with its absolute
root and directory-index rules:

```sh
uvx --from lychee-bin==0.24.2 lychee --config "$documentation_skill/assets/lychee/lychee.toml" --offline --root-dir "$built_site" --index-files index.html -- "$built_site/**/*.html"
```

Set `built_site` to the absolute generated-site directory. The quoted glob is
expanded by lychee. Inspect the inputs and ignored-file scope; add `--no-ignore`
when a generated directory is intentionally ignored by the repository. Check
project URL prefixes against the generated directory layout. Use narrowly scoped
[URL remapping](https://lychee.cli.rs/recipes/local-folder/) for canonical site URLs that
must resolve into temporary output, and record the exact mapping.

Inventory the intended input files before running a glob and retain that inventory
with the report. Verify that it contains the selected pages, then inspect stderr
and JSON `total` and `successful`. An unmatched glob can exit 0 with a
`No files found` warning and `total = 0`: classify that run as unchecked because
it establishes no link coverage. A zero total for a real page with no links is
valid only after inspecting that page and recording why no links were expected.
Likewise, compare unexpectedly small totals with the input inventory and ignored
paths before accepting the result. Use explicit selected file paths when useful.
`--dump-inputs` records lychee's expanded input selection. A positive `total`
with `successful = 0` and every link excluded also leaves a scope requiring
checked links incomplete. Keep empty selection, inspected pages containing no
links, and all-excluded links distinct in the verification record. Automated
coverage gates must apply the expected scope as well as the command exit status.

## Coverage and ownership

| Link kind | Required evidence |
| --- | --- |
| Relative source file | lychee source-file pass, including a deliberately missing target |
| Source heading fragment | lychee fragment pass; inspect generator-specific heading syntax in built HTML |
| Doxygen symbol reference | Doxygen generation diagnostics and inspection of the rendered destination |
| MkDocs page or navigation target | Existing MkDocs build diagnostics, then built HTML checks |
| Generated HTML file and ID | lychee on generated output, with `--root-dir` and `--index-files` matching the site |
| External URL and fragment | Online lychee pass, with an accessible response containing the fragment |
| JavaScript-created destination | Browser inspection of the relevant page and action |

The baseline enables anchor and text fragments. Processor-specific anchors need
the generated HTML as evidence; JavaScript-generated anchors require browser
inspection. Follow the upstream [fragment guide](https://lychee.cli.rs/recipes/anchors/)
and [local-root guide](https://lychee.cli.rs/recipes/root-dir/) for supported syntax.
Use [generated-reference validation](generated-reference-validation.md) and
[MkDocs authoring](mkdocs-authoring.md) for source-to-rendered checks. Map a broken
generated URL back to the editable Markdown, template, or source comment.

## Interpret the report

Keep the raw JSON and add a short classified findings table. Include the source
page, target, observed response or error, classification, and next action.

| Observation | Classification and action |
| --- | --- |
| Target file or static fragment missing; HTTP 404 or 410 | Broken: repair the destination or link and rerun |
| Successful response with checked fragment | Verified for the observed response and date |
| Redirect ending at a valid target | Verified through redirect: inspect the final target for the intended content and update permanent canonical links where appropriate |
| Redirect loop or limit exceeded | Unverified redirect failure: inspect the chain before deciding which URL to repair |
| HTTP 401 or 403; login page returned with HTTP 200 | Unchecked access-controlled content: obtain permitted access or ask an authorized reviewer to verify |
| HTTP 429 or 5xx; DNS, connection, TLS, or timeout failure | Temporarily unreachable: record the actual error and retry when access or service recovers |
| Offline, excluded, unsupported, or cache-only result | Unchecked in this run: record why and who will complete verification |

A zero exit status can accompany excluded links. Check `excludes`, `excluded_map`, and the error
details alongside `successful`; a green local pass proves only the local scope.
HTTP reachability also needs a content check when redirects or access controls can
return a login or unrelated page.

The house baseline follows up to five redirects, retries twice with a two-second
minimum wait, and limits requests to eight concurrently and two per host. These
are conservative operating defaults, adjustable for the target's published limits.
Honor a server's retry guidance and schedule another pass after a rate-limit
window. Preserve exhausted retries as unresolved observations. The accepted range
is 2xx; treating 401, 403, 429, or 5xx as success would hide verification limits.

Final verification uses fresh responses (`cache = false`). Optional development
runs can enable caching, with a one-day maximum age and access, rate-limit, and
server-error statuses excluded from cache. Record cache use and age, then repeat
the final pass with the baseline. See upstream [caching](https://lychee.cli.rs/recipes/caching/)
and [configuration](https://lychee.cli.rs/guides/config/) for the options.

For authenticated checks, use the project's approved secret mechanism and
host-scoped credentials; review redirects and destinations before sending them.
Record access requirements without storing secrets in the skill or reports.
For an exclusion, record an anchored URL pattern, reason, evidence, owner, and
review date in the project's verification record. Scope exclusions to the
specific destination and retain them as unchecked items.

## Regression fixtures

From the skill repository, run:

```sh
uv run pytest skills/documentation/tests/style-links/test_links.py -q
```

The tests execute the pinned binary against valid and missing local files and
headings, HTML directory links, and a local HTTP server providing valid responses,
redirects, redirect loops, missing fragments, 404, 410, 401, 403, 429, and 503.
They assert connection failures remain unresolved and offline or explicitly
excluded URLs count as excluded. HTTP tests require permission
to bind a loopback socket; file and HTML tests can run without networking. Fixture
requests disable retries for predictable execution time; production uses the
configured retry policy. The environment suite separately exercises actual
MkDocs and Doxygen generation and their diagnostics. Run both suites to establish
source, generated symbol, and assembled-site coverage.

Sources above were consulted on 2026-09-06; commands target lychee 0.24.2.
