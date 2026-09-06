# Check prose and source comments with Vale

Use this guide to run the same Google-based style checks on a selected document
and its C/C++ comments. The [configuration](../assets/vale/.vale.ini) associates
comments with Markdown so formatting and code exclusions apply inside comments.
It uses the published Google package directly and adds project vocabulary.

## Install the pinned tools

On Linux x86_64, run these commands from the skill repository root:

```bash
bash skills/documentation/assets/vale/setup.sh
skills/documentation/assets/vale/bin/vale --version
```

Setup requires Bash 4.4+, curl, sha256sum, tar, and unzip. It installs into ignored
`bin/` and `styles/Google/` directories beside the configuration. The script
verifies SHA-256 before extracting either archive. Vale **3.20.0** uses the
digest from its official release checksum file; Google **v0.7.1** uses the digest
recorded from that release archive on 2026-09-06. A changed archive fails setup.
Download permission or unavailable network access is a setup blocker.

For another platform, obtain the matching Vale 3.20.0 archive and checksum from
the [official release](https://github.com/vale-cli/vale/releases/tag/v3.20.0),
install it in the same `bin/` location, and install the pinned Google archive.
Verify the platform installation before reporting it as supported. Keep the
upstream licenses with redistributed binaries and rule packages.

Copy the asset directory into the consuming project's chosen tooling location
when adopting the configuration. `StylesPath` resolves beside `.vale.ini`.
Keep project vocabulary in `styles/config/vocabularies/Documentation/`; add
domain terms only after checking their spelling and meaning with a domain source.
The supplied accepted names are documentation tools and the Diataxis framework.
Rejected names demonstrate incorrect Doxygen and MkDocs capitalization.

## Run selected files

```bash
skills/documentation/assets/vale/bin/vale --no-global \
  --config=skills/documentation/assets/vale/.vale.ini --output=JSON \
  docs/cache.md include/cache.hpp
```

Replace the final paths with existing project files. `--no-global` isolates the
run from personal Vale configuration. Archive JSON with tool and package versions,
configuration, selected paths, and exit status. Findings include rule, severity,
original file, line, and inclusive column span. A normal lint exit of 1 indicates
findings; inspect other failures as tool errors. The configuration includes
suggestions, warnings, and errors. Review suggestions and resolve or justify each
finding before recording the stage as passed. Preserve upstream severity levels;
project policy can establish a stricter gate after examining its diagnostics.

## Scope and exceptions

Verified extensions are `.md`, `.c`, `.h`, `.cc`, `.cpp`, `.hpp`, and `.cxx`.
Source fixtures cover C/C++ block comments, `///`, `//!`, trailing `///<`, and
ordinary comments. Vale also checks ordinary comments because its C/C++ grammar
selects comment nodes. These fixtures establish prose extraction, not complete
language or preprocessor validation. Record unfamiliar dialects as unverified.

Vale 3.20.0 does not identify `.hxx` as C++ through the supplied association.
Inventory extensions before the run and report other extensions as unchecked.
Adding an extension-to-Markdown mapping alone can cause program text to be linted
as prose. Validate both planted prose errors and excluded string literals before
extending support.

The source-only `TokenIgnores` handles Doxygen command tokens, parameter names,
and selected symbol arguments. It preserves parameter descriptions for linting.
`BlockIgnores` handles `@code`/`@endcode`, `@verbatim`/`@endverbatim`, and their
backslash forms. Parameter directions support both `@param[in]` and
`@param [in]`. Markdown
fences, inline code, and link destinations use Vale's markup parser. Write other
literal identifiers and commands in code spans; verify custom Doxygen aliases
against fixtures before adding narrow exclusions.

Use an upstream [rule-scoped suppression](https://docs.vale.sh/formats/markdown)
when a necessary quotation, product name, or document intent conflicts with a
rule. Record the reason in the review evidence and restore the rule immediately:

```markdown
<!-- vale Google.We = NO -->
We will use a bounded cache.
<!-- vale Google.We = YES -->
```

This example preserves an ADR's decision voice. The same markup works inside
a Doxygen block comment; review its rendering when changing generated reference.
Avoid suppressing an entire file for one sentence. The fixture proves the rule
resumes after the exception in Markdown and C++ comments.

## Verification and editorial coverage

Run the integration fixtures after changing the configuration, vocabulary, or
tool pins:

```bash
uv run --no-project --with pytest==8.3.5 pytest -q \
  skills/documentation/tests/style-links/test_vale.py
```

Tests fail if setup is missing. They prove accepted and rejected vocabulary,
Google rule behavior, original line/column mapping, literal exclusion, parameter
description linting, and scoped suppression. Intentionally invalid fixtures
produce lint findings; the pytest assertions expect those findings.

Google owns its rule implementation. Local custom lexical rules are unnecessary
for this baseline. Editorial review still assesses audience fit, terminology
meaning, prerequisites, warning placement, evidence, explanation quality, and
meaning preservation. For example, the pinned package does not flag every
dismissive difficulty qualifier. Assess these in prose review instead of claiming
that a clean Vale run proves the house style in full.

Upstream references: [code-aware linting](https://vale.sh/features/code),
[Google package](https://vale.sh/explorer/google),
[token exclusions](https://docs.vale.sh/keys/tokenignores), and
[block exclusions](https://docs.vale.sh/keys/blockignores).
