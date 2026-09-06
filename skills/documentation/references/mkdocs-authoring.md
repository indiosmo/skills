# Authoring within an existing MkDocs site

Use this guide when adding or changing a page in a consuming project's MkDocs
site. Read its configuration, dependency lock, build command and neighboring
pages before drafting. Establish the docs directory, navigation, theme, Markdown
extensions, plugins, asset conventions, generated reference location and CI
warning policy. Follow the site's current page structure and link conventions.

## Fit the page to its destination

Place the page where its audience will look, add the agreed navigation entry and
connect relevant parent and sibling pages. Use the site's supported syntax for
admonitions, code fences and diagrams. Give images useful alternative text and
diagrams a nearby explanation of the relationship they illustrate. Inspect
heading identifiers when editing linked headings. Preserve exact example
commands and verify them using the [example procedure](examples.md).

MkDocs documents [page and navigation authoring](https://www.mkdocs.org/user-guide/writing-your-docs/)
and its [configuration](https://www.mkdocs.org/user-guide/configuration/).
Consult the project's theme and extension documentation for syntax specific to
that environment. Record unavailable plugin documentation as a verification gap.

## Build and inspect

Use the existing locked environment and build command. For a direct MkDocs build,
run `mkdocs build --strict --config-file <project-config> --site-dir <absolute-temporary-output>`
from the project's expected working directory. Replace the placeholders with
recorded paths. An explicit config path preserves configuration-relative paths;
the working directory preserves custom hook expectations. Review plugin output
paths before running. Generate required API artifacts through the existing
project command before building pages that consume them.

Check the build log and inspect the generated page, navigation entry, headings,
code indentation, image paths, diagrams and admonitions. Follow representative
links between the changed page, its neighbors and generated reference. Open a
browser for responsive layout or client-rendered diagrams; record any browser
check that remains pending separately from structural HTML checks.

Strict mode fails on warnings produced by the active configuration. Establish
coverage with planted missing-page, missing-anchor and missing-asset examples:
the fixture explicitly enables anchor warnings, which is material to its result.
The [link-validation guide](link-validation.md) assigns remaining URL and built
site checks. A clean build is evidence for the enabled checks and inspected
rendering, with its scope recorded in the validation report.

## Fixture evidence

The [environment tests](../tests/environment/README.md) use an existing two-page
site with navigation, a linked heading, an SVG signal-flow diagram, fenced
commands and a note admonition. They inspect generated HTML and copied assets.
Each missing page, anchor, image and navigation target causes a strict-build
failure. Doxygen generation precedes the site build, and lychee checks the built
home page's link to its generated reference; a planted missing generated target
fails. The SVG is a static diagram; projects using client-rendered diagram
plugins need a browser check in their own configured environment. Correct source
Markdown, navigation or asset paths and repeat the affected checks.
