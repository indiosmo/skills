# Name modules, packages, and files

A module or package name helps a reader find a capability and understand an
import. Choose it from the responsibilities that belong together, then inspect
the complete path as readers and tools encounter it. A directory listing, an
import statement, and an installed package can expose different amounts of
context.

The boundary and review procedures below are local engineering judgment.
Language-specific spelling follows the attributed conventions in
[language conventions](language-conventions.md); the
[evidence register](evidence.md#lang-12) separates those rules from general advice.

## Start with the boundary

Describe the module's exported behavior in one sentence and list its important
neighbors. A module called `audio.buffering` could own allocation and reuse of
audio buffers. If it also starts a web server and provisions accounts, inspect
why those responsibilities share a boundary before selecting a broader name.
A vague name raises a question about cohesion; it establishes no architectural
defect by itself. A small `utilities` module may accurately collect a few local
helpers when its scope and consumers make the contents clear.

Use a domain or capability name when that is the stable subject visible to
consumers. Use a technology name when the technology defines the contract:
`protobuf_encoding` can distinguish an encoding adapter, while a module that
selects shipment carriers should express that capability even if its current
implementation queries PostgreSQL. The judgment depends on what changes would
still fit the module's purpose. This is a design test, not a claim about measured
rates of technology change. See [EMP-007](evidence.md#emp-007) and
[domain boundaries](evidence.md#con-003).

Different bounded contexts can legitimately assign different meanings to one
term. A package path such as `transport.consignment` helps identify the model
in which a name applies. Inspect translations between contexts before merging
similarly named packages. [Domain vocabulary](domain-vocabulary.md) explains how
to establish that meaning.

## Read the complete import

Namespace context can carry words that a member would otherwise need. Remove
repetition only after checking the forms callers actually use, including direct
imports and aliases. A qualified call and an unqualified call give the reader
different clues.

Consider an original Python-shaped pseudocode example. Both alternatives below
encode an audio buffer as bytes; the module owns this encoding capability.
These are illustrative use sites, unexecuted because the application is fictional.

Before:

```text
from audio import audio_encoding
encoded_buffer = audio_encoding.encode_audio_buffer(buffer)
```

After:

```text
from audio import encoding
encoded_buffer = encoding.encode_buffer(buffer)
```

The after form makes the capability visible in `audio.encoding` and preserves
`buffer` as the operation's subject. This is a clear winner for the stipulated
qualified-import convention. If consumers commonly import the function directly,
inspect `encode_buffer(buffer)` beside other encoders: retaining `audio` in the
function name or requiring qualification may make the distinction clearer.
The recommended spelling remains provisional until actual callers and the
public import contract support it. [Selection](selection.md) covers comparisons
when those alternatives have meaningful tradeoffs.

## Check collisions at each resolution boundary

A plausible path can conflict with a dependency, another generated identifier,
or another filename. For example, a local Python module named `json.py` can
shadow the standard-library `json` module when the local directory is searched
first. If its purpose is encoding audio metadata, `audio_metadata_encoding.py`
expresses that role while distinguishing the module. This scenario assumes that
import-path ordering; verify resolution in the intended environment before
claiming a collision. PEP 8 supplies the
[module and package spelling convention](https://peps.python.org/pep-0008/#package-and-module-names),
while collision inspection is local verification policy.

Inspect the actual lookup surface:

- Compare the proposed import path with project modules and declared dependencies.
  Review import aliases and module-qualified references together.
- Compare filenames under the target filesystem's case rules. A case-only
  distinction can work on one deployment filesystem and collide on another;
  test the supported checkout, build, and install environments.
- Generate schema bindings where the project uses code generation. Distinct
  source names can transform into the same generated spelling. The
  [Protobuf style guide](https://protobuf.dev/programming-guides/style/#identifier-naming-styles)
  describes this concern for its generators.
- Examine package registry names, source package names, installed imports and
  executable names as separate surfaces. Record their mapping when they differ.

Google's C++ guide recommends descriptive
[file names](https://google.github.io/styleguide/cppguide.html#File_Names) and
[namespace names](https://google.github.io/styleguide/cppguide.html#Namespace_Names)
that reduce collision risk in its projects. Python uses short lowercase module
names and discourages underscores in package names. These are scoped conventions;
use the project's declared casing and packaging rules for other ecosystems.

## Validate discoverability and deployment

Ask a reader to locate the module from its purpose and explain an import from
its path. Compare the proposal with nearby modules, search terms in documentation,
and the actual exports. A name that fits today's single function should still
accurately describe the agreed boundary; speculative future capabilities supply
weak justification for a broad name.

For a proposed path change, inspect build manifests, package-data rules,
entry points, deployment configuration, plugins, generated imports, and installed
consumers. Python's [pickle naming rules](https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled)
can also make a qualified class or function name relevant to stored objects.
A source-tree import test supports that tree; an installed-artifact test supports
the tested deployment layout. Report the environment actually checked.

Recommend the path and explain its boundary, import readability, and collision
assessment. Record caller and deployment evidence separately from the spelling
judgment. Use [renaming](renaming.md) for authorized changes, compatibility
choices and rollout verification, and
[contextual validation](contextual-validation.md) for the distinct review of the
chosen name.
