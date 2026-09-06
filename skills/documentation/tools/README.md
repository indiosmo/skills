# Documentation verification tools

These tools help an author or maintainer check documentation from a terminal or
an existing CI verification job. Each tool has its own README with installation,
manual usage, configuration and diagnostic details.

| Tool | Purpose | How it works |
| --- | --- | --- |
| [Doxygen linter](doxygen_linter/README.md) | Check adopted source-comment conventions in C and C++ files or directories | Parse source to locate comments and declarations, apply documented structural checks, and report source locations plus coverage limits |
| [Validation runner](validation/README.md) | Run a project's selected documentation checks and retain their outcomes | Execute configured commands in dependency order, preserve native diagnostics, and distinguish passing, failing and unavailable checks |

The [validation guide](../references/validation.md) explains how to combine these
with Vale, Doxygen generation, MkDocs, lychee and the project's example commands.
The consuming project's existing configuration determines source scope and
rendering behavior. Start with the tool-specific README for direct use, then
consult that guide when assembling a document's verification record.
