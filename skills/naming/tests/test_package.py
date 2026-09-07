"""Verify naming package resources, selected inputs, and local dependencies."""

import json
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import markdown
import pytest
import yaml

SKILL_DIRECTORY = Path(__file__).resolve().parents[1]
SIBLING_DIRECTORY = SKILL_DIRECTORY.parent
REQUIRED_RESOURCES = (
    "SKILL.md",
    "references/README.md",
    "references/sources.md",
    "references/evidence.md",
    "references/empirical-research.md",
    "references/foundations.md",
    "references/domain-vocabulary.md",
    "references/elicitation.md",
    "references/candidate-generation.md",
    "references/selection.md",
    "references/variables-and-state.md",
    "references/functions-and-methods.md",
    "references/types-and-messages.md",
    "references/modules-packages-and-files.md",
    "references/apis-schemas-and-configuration.md",
    "references/language-conventions.md",
    "references/contextual-validation.md",
    "references/renaming.md",
    "references/maintenance.md",
    "templates/naming-brief.md",
    "templates/candidate-comparison.md",
    "templates/naming-decision.md",
    "templates/validation-report.md",
    "templates/rename-plan.md",
    "examples/README.md",
    "examples/eliciting-a-concept.md",
    "examples/comparing-candidates.md",
    "examples/candidate-matrix.html",
    "examples/rejecting-a-plausible-name.md",
    "examples/retaining-an-existing-name.md",
    "examples/boolean-polarity.md",
    "examples/units-and-cardinality.md",
    "examples/domain-vocabulary.md",
    "examples/bounded-contexts.md",
    "examples/functions-and-side-effects.md",
    "examples/types-roles-and-events.md",
    "examples/modules-packages-and-files.md",
    "examples/public-contract-rename.md",
    "examples/unclear-abstraction.md",
    "tests/README.md",
    "tests/test_package.py",
    "tests/test_fixture_contracts.py",
    "tests/fixtures/contextual-review/README.md",
    "tests/fixtures/contextual-review/subscriptions.py",
    "tests/fixtures/contextual-review/callers.py",
    "tests/fixtures/contextual-review/GLOSSARY.md",
    "tests/fixtures/contextual-review/contract.md",
    "tests/fixtures/local-rename/README.md",
    "tests/fixtures/local-rename/retry_policy.py",
    "tests/fixtures/local-rename/callers.py",
    "tests/fixtures/local-rename/test_retry_policy.py",
    "tests/fixtures/local-rename/usage.md",
    "tests/fixtures/local-rename/unrelated.py",
    "tests/fixtures/public-contract/README.md",
    "tests/fixtures/public-contract/api.py",
    "tests/fixtures/public-contract/client.py",
    "tests/fixtures/public-contract/schema.json",
    "tests/fixtures/public-contract/test_compatibility.py",
    "evals/README.md",
    "evals/evals.json",
    "evals/trigger-evals.json",
    "evals/reviewer-notes.md",
    "evals/check_rename_outcomes.py",
    "tests/test_rename_outcome_checks.py",
    "evals/results.md",
)


def require_files(directory: Path, resources: tuple[str, ...]) -> None:
    missing = [resource for resource in resources if not (directory / resource).is_file()]
    assert not missing, f"Missing required resources: {missing}"


def test_required_resources() -> None:
    require_files(SKILL_DIRECTORY, tuple(resource for resource in REQUIRED_RESOURCES if resource != "evals/results.md"))


def test_release_required_resources() -> None:
    require_files(SKILL_DIRECTORY, REQUIRED_RESOURCES)


def test_missing_resource_is_detected(tmp_path: Path) -> None:
    with pytest.raises(AssertionError, match="chapter.md"):
        require_files(tmp_path, ("chapter.md",))
    (tmp_path / "chapter.md").write_text("# Chapter\n", encoding="utf-8")
    require_files(tmp_path, ("chapter.md",))


def check_links(documents: list[Path]) -> subprocess.CompletedProcess[str]:
    assert documents, "Link input selection is empty"
    assert all(document.is_file() for document in documents), "Link input file is missing"
    executable = shutil.which("lychee")
    assert executable, "The project environment must supply lychee"
    return subprocess.run(
        [
            executable,
            "--config",
            str(SIBLING_DIRECTORY / "documentation/assets/lychee/lychee.toml"),
            "--offline",
            "--",
            *map(str, documents),
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


def test_local_links_and_fragments() -> None:
    documents = sorted(path for path in SKILL_DIRECTORY.rglob("*") if path.suffix in {".md", ".html"})
    result = check_links(documents)
    report = json.loads(result.stdout)
    assert result.returncode == 0, json.dumps(report.get("error_map", report), indent=2) + result.stderr
    assert report["total"] > 0 and report["successful"] > 0, report


@pytest.mark.parametrize(
    "destination,valid", [("chapter.md#section", True), ("missing.md", False), ("chapter.md#missing", False)]
)
def test_link_checker_detects_broken_targets(tmp_path: Path, destination: str, valid: bool) -> None:
    (tmp_path / "chapter.md").write_text("# Chapter\n\n## Section\n", encoding="utf-8")
    document = tmp_path / "index.md"
    document.write_text(f"[Chapter]({destination})\n", encoding="utf-8")
    result = check_links([document])
    assert (result.returncode == 0) is valid, result.stdout + result.stderr


def test_link_input_selection_is_visible(tmp_path: Path) -> None:
    with pytest.raises(AssertionError, match="empty"):
        check_links([])
    with pytest.raises(AssertionError, match="missing"):
        check_links([tmp_path / "missing.md"])


class DocumentLinks(HTMLParser):
    """Collect actual rendered links for selective-loading checks."""

    def __init__(self) -> None:
        super().__init__()
        self.destinations: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        destination = dict(attrs).get("href")
        if tag == "a" and destination:
            self.destinations.append(destination)


def local_targets(document: Path) -> set[Path]:
    parser = DocumentLinks()
    parser.feed(markdown.markdown(document.read_text(encoding="utf-8"), extensions=["fenced_code", "tables"]))
    targets: set[Path] = set()
    for destination in parser.destinations:
        address = urlsplit(destination)
        if not address.scheme and not address.netloc:
            targets.add((document.parent / unquote(address.path)).resolve() if address.path else document)
    return targets


def test_entry_metadata() -> None:
    result = subprocess.run(
        [sys.executable, str(SIBLING_DIRECTORY / "creating-skills/scripts/quick_validate.py"), str(SKILL_DIRECTORY)],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    entry = (SKILL_DIRECTORY / "SKILL.md").read_text(encoding="utf-8")
    metadata = yaml.safe_load(entry.split("---", 2)[1])
    assert metadata["name"] == "naming"
    assert metadata["description"].strip()


def test_progressive_loading() -> None:
    entry = SKILL_DIRECTORY / "SKILL.md"
    assert len(entry.read_text(encoding="utf-8").splitlines()) < 500
    references = {path.resolve() for path in (SKILL_DIRECTORY / "references").glob("*.md")}
    assert references, "Reference input selection is empty"
    entry_targets = local_targets(entry)
    assert entry_targets & references, "Entry point must select human references"
    navigation = SKILL_DIRECTORY / "references/README.md"
    reachable = local_targets(navigation) | entry_targets | {navigation.resolve()}
    assert references <= reachable, f"Unreachable references: {references - reachable}"
    for document in (SKILL_DIRECTORY / "references").glob("*.md"):
        prose = document.read_text(encoding="utf-8")
        if len(prose.splitlines()) > 300:
            assert re.search(r"(?im)^#{1,3} (contents|table of contents)$", prose), document


def test_durable_resource_paths() -> None:
    forbidden_paths = ("work" + "-in-progress/", "/home/" + "msi/")
    resources = [
        path
        for path in SKILL_DIRECTORY.rglob("*")
        if path.suffix in {".md", ".html", ".json", ".py"} and "__pycache__" not in path.parts
    ]
    assert resources, "Durable resource selection is empty"
    for resource in resources:
        content = resource.read_text(encoding="utf-8")
        for forbidden_path in forbidden_paths:
            assert forbidden_path not in content, f"Temporary or machine-specific dependency in {resource}"
        if resource.suffix == ".md":
            for target in local_targets(resource):
                assert "naming" + "-workspace" not in target.parts, f"Temporary result link in {resource}"


def validate_evaluation_inputs(definition: dict, directory: Path) -> None:
    assert definition.get("skill_name") == "naming"
    cases = definition.get("evals")
    assert isinstance(cases, list) and cases, "Evaluation selection is empty"
    identifiers: set[int] = set()
    for case in cases:
        assert isinstance(case, dict)
        identifier = case.get("id")
        assert type(identifier) is int and identifier > 0 and identifier not in identifiers
        identifiers.add(identifier)
        for field in ("prompt", "expected_output"):
            assert isinstance(case.get(field), str) and case[field].strip(), (identifier, field)
        expectations = case.get("expectations")
        assert isinstance(expectations, list) and expectations, (identifier, "expectations")
        assert all(isinstance(expectation, str) and expectation.strip() for expectation in expectations)
        assert "assertions" not in case, "Source cases use expectations; run metadata maps assertions"
        files = case.get("files")
        assert isinstance(files, list), (identifier, "files")
        assert len(files) == len(set(files)), (identifier, "duplicate files")
        for filename in files:
            assert isinstance(filename, str) and filename
            assert not Path(filename).is_absolute() and ".." not in Path(filename).parts, (identifier, filename)
            target = (directory / filename).resolve()
            assert target.is_relative_to((directory / "tests/fixtures").resolve()), (identifier, filename)
            assert target.is_file(), f"Evaluation input missing: {filename}"


def test_evaluation_inputs() -> None:
    definition = json.loads((SKILL_DIRECTORY / "evals/evals.json").read_text(encoding="utf-8"))
    validate_evaluation_inputs(definition, SKILL_DIRECTORY)
    assert any(case["files"] for case in definition["evals"]), "Fixture input selection is empty"


def test_evaluation_input_failures(tmp_path: Path) -> None:
    case = {
        "id": 1,
        "prompt": "Validate this supplied concept.",
        "expected_output": "Evidence and judgment.",
        "expectations": ["States its evidence."],
        "files": [],
    }
    definition = {"skill_name": "naming", "evals": [case]}
    validate_evaluation_inputs(definition, tmp_path)
    case["files"] = ["tests/fixtures/missing.py"]
    with pytest.raises(AssertionError, match="Evaluation input missing"):
        validate_evaluation_inputs(definition, tmp_path)
    case["files"] = ["evals/reviewer-notes.md"]
    with pytest.raises(AssertionError):
        validate_evaluation_inputs(definition, tmp_path)
    fixture = tmp_path / "tests/fixtures/input.py"
    fixture.parent.mkdir(parents=True)
    fixture.write_text("value = True\n", encoding="utf-8")
    for unsafe_path in (str(fixture), "tests/fixtures/../fixtures/input.py"):
        case["files"] = [unsafe_path]
        with pytest.raises(AssertionError):
            validate_evaluation_inputs(definition, tmp_path)
    with pytest.raises(AssertionError, match="Evaluation selection is empty"):
        validate_evaluation_inputs({"skill_name": "naming", "evals": []}, tmp_path)


def test_trigger_inputs() -> None:
    cases = json.loads((SKILL_DIRECTORY / "evals/trigger-evals.json").read_text(encoding="utf-8"))
    assert isinstance(cases, list) and len(cases) == 20
    assert all(isinstance(case.get("query"), str) and case["query"].strip() for case in cases)
    assert len({case["query"] for case in cases}) == len(cases)
    assert all(type(case.get("should_trigger")) is bool for case in cases)
    assert sum(case["should_trigger"] for case in cases) == 10
