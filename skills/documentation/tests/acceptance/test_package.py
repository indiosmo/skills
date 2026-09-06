"""Check the assembled documentation skill's resource contracts."""

from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import markdown
import pytest
import yaml


SKILL_DIRECTORY = Path(__file__).resolve().parents[2]


class DocumentLinks(HTMLParser):
    """Collect rendered link destinations and explicit heading identifiers."""

    def __init__(self) -> None:
        super().__init__()
        self.destinations: list[str] = []
        self.identifiers: set[str] = set()

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        values = dict(attributes)
        if tag == "a" and values.get("href"):
            self.destinations.append(str(values["href"]))
        if values.get("id"):
            self.identifiers.add(str(values["id"]))


def parse_document(document: Path) -> DocumentLinks:
    parser = DocumentLinks()
    parser.feed(markdown.markdown(document.read_text(), extensions=["fenced_code", "tables", "toc"]))
    return parser


RESOURCE_DOCUMENTS = [SKILL_DIRECTORY / "SKILL.md", *sorted((SKILL_DIRECTORY / "references").glob("*.md")),
                      *sorted((SKILL_DIRECTORY / "templates").glob("*.md")),
                      SKILL_DIRECTORY / "tools/README.md",
                      *sorted((SKILL_DIRECTORY / "tools").glob("*/README.md")),
                      *sorted((SKILL_DIRECTORY / "examples").rglob("*.md"))]


@pytest.mark.parametrize("document", RESOURCE_DOCUMENTS, ids=lambda document: document.name)
def test_local_resource_links(document: Path) -> None:
    for destination in parse_document(document).destinations:
        address = urlsplit(destination)
        if address.scheme or address.netloc:
            continue
        target = (document.parent / unquote(address.path)).resolve() if address.path else document
        assert target.exists(), f"{document}: missing {destination}"
        if address.fragment and target.suffix == ".md":
            assert unquote(address.fragment) in parse_document(target).identifiers, (
                f"{document}: missing section {destination}"
            )


def test_progressive_loading_and_durable_references() -> None:
    entry = (SKILL_DIRECTORY / "SKILL.md").read_text()
    metadata = yaml.safe_load(entry.split("---", 2)[1])
    assert metadata["name"] == "documentation"
    assert isinstance(metadata["description"], str) and len(metadata["description"]) <= 1024
    assert len(entry.splitlines()) < 500
    for document in RESOURCE_DOCUMENTS:
        prose = document.read_text()
        assert "work-in-progress/" not in prose, document
        if len(prose.splitlines()) > 300:
            assert re.search(r"(?im)^#{1,3} (contents|table of contents)$", prose), document


def test_final_review_contract_has_exact_categories() -> None:
    reference = (SKILL_DIRECTORY / "references/final-verification.md").read_text()
    categories = re.findall(r"(?m)^\d\. (.+)$", reference)
    assert categories == [
        "Unsupported claims",
        "Missing prerequisites",
        "Ambiguous actions",
        "Steps unverifiable from the supplied source material",
        "Inconsistent product terminology",
        "Content belonging in another Diataxis quadrant",
        "Google-style issues in titles, headings, voice, and word choice",
        "Risks of changing meaning in code samples",
    ]
    assert "exactly `[]`" in reference


def test_document_type_commands() -> None:
    import json
    import subprocess

    examples = SKILL_DIRECTORY / "examples/document-types"
    manifest = json.loads((examples / "commands.json").read_text())
    for command in manifest["commands"]:
        result = subprocess.run(command["arguments"], cwd=examples, capture_output=True,
                                text=True, timeout=manifest["timeout_seconds"], check=False)
        assert result.returncode == command["exit_status"], result.stderr
        if "stdout" in command:
            assert result.stdout == command["stdout"]
        if "stdout_number" in command:
            assert int(result.stdout.strip()) == command["stdout_number"]
        if "stderr" in command:
            assert result.stderr == command["stderr"]


def test_tool_readmes_explain_manual_use() -> None:
    tool_directory = SKILL_DIRECTORY / "tools"
    assert (tool_directory / "README.md").is_file()
    for tool in sorted(tool_directory.iterdir()):
        if tool.is_dir() and (tool / "pyproject.toml").is_file():
            readme = tool / "README.md"
            assert readme.is_file(), f"Human usage guide missing: {readme}"
            text = readme.read_text()
            assert "uv " in text, f"Missing manual invocation: {readme}"
