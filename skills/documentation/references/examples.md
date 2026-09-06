# Keeping examples reproducible

Use this guide when a document teaches a reader to run code or commands. Keep
runnable code in a source file that participates in the project's build or tests.
Include or link that file through the site's existing mechanism. Record the
example's source and page location with the [manifest template](../templates/example-manifest.toml).
The manifest is a review record: invoke its recorded project commands through
the project's normal command surface.

## Choose the smallest sufficient mechanism

First run the project's existing example target, test command or language-native
test facility. Doxygen's [snippet command](https://www.doxygen.nl/manual/commands.html#cmdsnippet)
can include a marked portion of a compiled source file. In the environment
fixture, Doxygen includes the `scale_sample` region from `examples/gain.cpp`;
the C++ compiler builds that same file and the program checks its output value.
This directly satisfies inclusion and execution, so native mechanisms are the
clear choice for this fixture and require no extraction or execution adapter.

For MkDocs, use the project's established inclusion plugin if present, or link
the runnable source. When authored fences are the source of truth, mark runnable
fences explicitly and evaluate the project's existing Markdown testing tools
against them. Introduce extraction only after recording a concrete coverage gap,
including source locations, indentation and language handling. Partial snippets
must name their source context or executable wrapper.

## Define the execution contract

Record language and dialect, target product version or revision, dependencies
and setup, working directory, inputs, placeholder substitutions, exact commands,
expected exit status and output or state assertions, timeout and cleanup. Choose
isolated output paths and synthetic data. A useful assertion checks the taught
behavior: the fixture asserts that gain `2.0` applied to sample `0.25` produces
`0.5`, and catches addition mistakenly replacing multiplication.

Keep command quoting, indentation, flags, identifiers and assertions intact
through editorial review. Compare included code with its source, rebuild the
page, rerun the example and inspect output after meaning-sensitive edits. A
compilation check establishes syntax and linking; execution assertions establish
the recorded behavior for the chosen inputs.

## Record examples that need other checks

Label pseudocode as pseudocode and review its logic against cited behavior.
Label fragments as partial and compile them in an identified wrapper where
feasible. For interactive steps, record the operator's actions, expected visible
state and actual observation. For service-dependent examples, record required
service versions, access and cleanup; report blocked execution when unavailable.
Human execution has a named reviewer, date and observed result. Every example
ends with an execution result or an explicit limit; an unexecuted example remains
unverified. See the [environment fixture results](../tests/environment/README.md)
for tested commands and coverage.
