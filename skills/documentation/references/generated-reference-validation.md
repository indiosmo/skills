# Checking generated API reference

Use this procedure when changing source comments that affect API presentation.
Start with the consuming project's documented generation command and inspect its
Doxygen configuration, input scope, exclusions, aliases, filters, example paths,
tag files, warning policy and reference integration. Record the working directory
and tool version. Discover configuration from the selected project's build files
and documentation; inspect included configuration files as well.

## Choose the check

Vale and the source-comment linter suit wording and supported style checks. Run
generation for changed tags, declarations, overloads, parameter descriptions,
snippets, symbol links or markup; also run it when the project's required check
calls for generation. A prose-only correction can reuse an established rendering
baseline if the project permits that scope. Record the reason and remaining limit.

## Preserve project inputs

Run the existing command from its expected working directory. Prefer its output
override to a temporary absolute directory. If direct Doxygen invocation is the
project command, an equivalent temporary configuration can retain the original
settings and append `OUTPUT_DIRECTORY`. Keep relative `INPUT`, `EXAMPLE_PATH`,
`@INCLUDE` and filter paths resolving from the original command's directory.
Inspect explicit log and auxiliary output paths so they also stay in the selected
scratch area. Preserve generation features needed by the project's reference
consumer. See Doxygen's [configuration reference](https://www.doxygen.nl/manual/config.html)
for the settings supported by the installed version.

The [environment fixture](../tests/environment/README.md) copies a project to an
isolated temporary directory, runs Doxygen from that project's root, and supplies
its configuration through standard input with an absolute output override. Its
relative header and snippet paths resolve successfully. A consuming project with
preprocessing or custom build steps should use those existing steps.

## Inspect and correct

Inspect generated pages for every changed symbol: signature and qualifiers,
overload distinction, parameter names and descriptions, return contract, complete
examples and resolved cross-references. Follow links to the actual symbol and
overload. Review layout in a browser when visual presentation matters; an HTML
assertion establishes structure and content only.

Map findings back to source path, line, symbol and tag. In the fixture, replacing
`@param gain` with `@param missing_gain` produces a source-located diagnostic;
correct the tag to the declaration's parameter name. Replacing the overload link
with `@ref missing_symbol` produces an unresolved-reference diagnostic; restore
the intended overload reference. Rerun generation after the source correction.
Review broader dependencies when a symbol rename affects other pages.

Report command, version, input scope, output location, exit status, warning
diagnostics and inspected symbols. Missing configuration, headers, filters,
tag files or dependencies receive a blocked or skipped result with the specific
unverified behavior and owner. Preserve existing warnings in the report even
when a project permits them; distinguish them from findings introduced by the
change. Use [link validation](link-validation.md) for the combined site.
