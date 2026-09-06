# Documentation environment regression fixtures

These fixtures model an existing MkDocs and Doxygen project and a runnable C++
example. Tests copy the fixture to a temporary project directory, preserving its
relative paths, and generate output in separate temporary directories.

From the skills repository root, run:

```sh
uv run --project skills/documentation/tests/environment --frozen pytest skills/documentation/tests/environment -q
```

The scoped `pyproject.toml` and `uv.lock` pin Python test dependencies. Provide
`doxygen` and `c++` on PATH. Missing dependencies produce a failed check with the
missing executable identified; report this as blocked environment verification.
The native commands used by the tests are Doxygen with configuration on standard
input, `mkdocs build --strict` with an explicit config and temporary site directory,
and a C++17 compilation followed by execution with a five-second timeout.

## Recorded verification

On 2026-09-06, Python 3.13.3, MkDocs 1.6.1, Doxygen 1.9.8, lychee 0.24.2
and GCC 13.3.0 produced `12 passed in 3.02s` for the command above.

| Case | Evidence |
| --- | --- |
| Valid generated reference | Both overload labels, signature parameter names, parameter/return descriptions, snippet content and symbol href present in generated HTML |
| Incorrect parameter tag | Doxygen nonzero status and `gain.hpp` source diagnostic naming `missing_gain` |
| Unresolved symbol | Doxygen nonzero status and `gain.hpp` source diagnostic naming `missing_symbol` |
| Valid MkDocs site | Strict build succeeds; navigation, heading anchor, relative link, SVG image and alt text, note admonition present |
| Missing local page | Strict build fails and names `missing.md` |
| Missing heading anchor | Strict build fails and names `missing-anchor` |
| Missing image | Strict build fails and names `missing.svg` |
| Missing navigation target | Strict build fails and names `missing.md` |
| Combined reference link | Doxygen generates into the fixture docs directory before MkDocs builds; lychee offline accepts the built home page's reference link |
| Missing generated target | The built home page's reference link points to `missing-symbol.html`; lychee exits nonzero and names that target |
| Valid runnable source | Compiles, prints `0.5`, exits 0 |
| Planted arithmetic defect | Compiles, prints a different value, exits nonzero |

The negative cases mutate only isolated fixture copies. The Python tests assert
that those commands fail for the planted defect, so an overall passing suite
means both valid and invalid behavior matched their expectations.

## Boundaries and review

Rendering checks inspect generated HTML and copied SVG content structurally.
Human review should assess visual layout in the consuming site's browser and
theme. The fixture uses a static SVG diagram; client-side diagram behavior needs
its project's browser environment. External URLs use the link-validation workflow
in the consuming project's network environment. The combined fixture generates
reference into `docs/reference`, then builds MkDocs and invokes pinned lychee
with the shared asset configuration, `--offline`, the built site as `--root-dir`,
and `--index-files index.html`. The fixture's local layout establishes the tested
integration; consuming projects should verify their own configured paths.
Native Doxygen snippet inclusion and C++
compilation/execution satisfy this example's needs without a custom adapter.
