# Read a module name at the import site

A developer is adding a private catalog-export package to an internal Python
application. The new module serializes one catalog row as JSON text; a separate
module will encode complete export manifests. The developer proposes `json.py`
at the application root because that is the row's current output format.

This original scenario supplies the module boundary, proposed layout, and the
runnable miniature below. Catalog rows and export manifests are application
concepts. Python's applicable spelling guidance is recorded under
[LANG-03](../references/evidence.md#lang-03). Collision checks and capability
boundaries follow the package's
[module guidance](../references/modules-packages-and-files.md). This is new
private code, so the naming choice has no stipulated existing import consumers.

## Candidates in context

The existing application root needs an ordinary `import json` for manifest
serialization. The proposed root `json.py` occupies that same import spelling.
Under the root-first search path used below, that is a disqualifying collision.
Moving the proposed implementation to `catalog/json.py` would resolve that
particular root collision, but the public subject would still be its encoding
technology. The stated boundary is row encoding, with manifests handled
separately.

Consider the actual forms readers will use:

```text
from catalog import row_encoding
encoded_row = row_encoding.encode_row(row)

from catalog import manifest_encoding
encoded_manifest = manifest_encoding.encode_manifest(manifest)
```

These import and call pairs illustrate the application; the complete
row implementation is executable below. `catalog/encoding.py` would be accurate
for a combined encoding boundary. The stipulated separation makes
`catalog/row_encoding.py` the clear winner for this module: its path identifies
both the catalog context and the row-specific capability. Retain `encode_row`
as the function name because the qualified call already supplies the module
context. The package name is `catalog`, the module is `row_encoding`, and the
source filename is `row_encoding.py`.

There is no unresolved semantic question in this miniature's scope. Installed
package resolution and any future distribution name need separate evidence from
the real project. A future JSON-specific adapter with a representation-defined
boundary could reasonably make a different naming choice.

## Execute the import and collision scenario

This complete Python program creates temporary source trees, runs each import in
a fresh interpreter, and removes the trees on completion. Save the block as
`check_module_example.py` and run `python check_module_example.py` in a Python
environment, or `uv run python check_module_example.py` in this repository.

```python
import subprocess
import sys
import tempfile
from pathlib import Path


def run_import_check(source_directory: Path, source: str) -> None:
    subprocess.run(
        [sys.executable, "-S", "-c", source],
        cwd=source_directory,
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )


with tempfile.TemporaryDirectory() as temporary_directory:
    source_root = Path(temporary_directory)
    collision_directory = source_root / "collision"
    collision_directory.mkdir()
    (collision_directory / "json.py").write_text(
        'module_purpose = "catalog row encoding"\n', encoding="utf-8"
    )
    run_import_check(
        collision_directory,
        "import json\n"
        "from pathlib import Path\n"
        "assert Path(json.__file__).resolve() == Path('json.py').resolve()\n"
        "assert json.module_purpose == 'catalog row encoding'\n"
        "assert not hasattr(json, 'dumps')\n",
    )

    application_directory = source_root / "application"
    catalog_directory = application_directory / "catalog"
    catalog_directory.mkdir(parents=True)
    (catalog_directory / "__init__.py").write_text("", encoding="utf-8")
    (catalog_directory / "row_encoding.py").write_text(
        "import json\n\n"
        "def encode_row(row: dict[str, str]) -> str:\n"
        "    return json.dumps(row, sort_keys=True)\n",
        encoding="utf-8",
    )
    run_import_check(
        application_directory,
        "import json\n"
        "from catalog import row_encoding\n"
        "row = {'title': 'Example', 'identifier': 'row-7'}\n"
        "encoded_row = row_encoding.encode_row(row)\n"
        "assert isinstance(encoded_row, str)\n"
        "assert json.loads(encoded_row) == row\n"
        "assert row_encoding.encode_row({}) == '{}'\n"
        "assert row_encoding.__name__ == 'catalog.row_encoding'\n",
    )

print("Module example: collision and qualified import checks passed")
```

The child interpreters use `-S` to omit site initialization. Their current source
directory supplies the tested root-first import path. The assertions establish
the selected module identity, JSON round-trip for a populated row, the empty-row
case, and the competing root module's lack of `dumps`.

## Distinct contextual review

After selecting the path, review its whole import and the competing resolution
surface separately from the naming rationale.

| Context examined | Finding | Evidence type |
| --- | --- | --- |
| Qualified row call | `row_encoding.encode_row(row)` names the capability and one-row operation | Static reading of the executed call |
| Manifest neighbor sketch | `manifest_encoding` describes a different exported subject | Static review of the stipulated boundary |
| Root `json.py` proposal | Fresh interpreter resolves the local module and finds no `dumps` | Executed identity and attribute assertions |
| `catalog.row_encoding` layout | Qualified import resolves and standard JSON round-trips the encoded row | Executed module-name and behavior assertions |
| File/package mapping | The selected source filename agrees with the imported module | Inspection of the created tree and executed import |

Assessment: recommend `catalog/row_encoding.py` and retain `encode_row` under
the supplied qualified-import convention. The demonstration was executed
successfully through `uv run python` with Python 3.13.3, producing the single
success line shown in the program. That result covers the temporary source
layouts and two encoding cases.
The name's readability remains an engineering judgment supported by those use
sites.

An installed wheel, registry collision, case-insensitive filesystem, plugin
loader, and existing consumer migration are outside the demonstrated evidence.
Inspect the real build manifest and installed imports before claiming deployment
compatibility. For an existing public module, use the
[rename workflow](../references/renaming.md) to determine whether retention,
an alias, or a path migration is appropriate.
