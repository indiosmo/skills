"""Exercise the adopted Vale package at editable source positions."""

import json
import subprocess
from pathlib import Path

import pytest

ASSETS = Path(__file__).resolve().parents[2] / "assets" / "vale"
VALE = ASSETS / "bin" / "vale"


def lint(document: Path) -> tuple[int, list[dict]]:
    result = subprocess.run(
        [str(VALE), "--no-global", f"--config={ASSETS / '.vale.ini'}", "--output=JSON", str(document)],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode in (0, 1), result.stderr
    return result.returncode, json.loads(result.stdout).get(str(document), [])


def test_pinned_vale_binary() -> None:
    assert VALE.is_file(), "Run assets/vale/setup.sh before this integration suite."
    result = subprocess.run(
        [str(VALE), "--version"], capture_output=True, text=True, check=True, timeout=10
    )
    assert result.stdout.strip() == "vale version 3.20.0"


@pytest.mark.parametrize("document_name", ["accepted.md", "accepted.cpp"])
def test_accepted_vocabulary_and_code_exclusions(document_name: str) -> None:
    status, findings = lint(ASSETS / "fixtures" / document_name)
    assert status == 0
    assert findings == []


@pytest.mark.parametrize(
    ("document_name", "expected_positions"),
    [
        ("prose.md", {(3, 1), (19, 1)}),
        ("comments.c", {(4, 11), (13, 5)}),
        ("comments.cpp", {(4, 11), (16, 5), (19, 5), (22, 24), (24, 46)}),
    ],
)
def test_google_style_uses_original_positions(
    document_name: str, expected_positions: set[tuple[int, int]]
) -> None:
    status, findings = lint(ASSETS / "fixtures" / document_name)
    assert status == 1
    positions = {
        (finding["Line"], finding["Span"][0])
        for finding in findings
        if finding["Check"] == "Google.We"
    }
    assert positions == expected_positions


def test_rejected_vocabulary_and_scoped_exception() -> None:
    _, findings = lint(ASSETS / "fixtures" / "prose.md")
    assert {
        finding["Match"] for finding in findings if finding["Check"] == "Vale.Avoid"
    } == {"DoxyGen", "Mkdocs"}
    assert all(finding["Line"] != 16 for finding in findings)
    assert any(finding["Line"] == 19 for finding in findings)


def test_parameter_description_is_linted_after_ignored_identifier(tmp_path: Path) -> None:
    document = tmp_path / "cache.cpp"
    document.write_text(
        "/**\n * @param DoxyGen We use the cache.\n */\nint read_cache(int DoxyGen);\n",
        encoding="utf-8",
    )
    _, findings = lint(document)
    assert [(finding["Check"], finding["Line"], finding["Span"]) for finding in findings] == [
        ("Google.We", 2, [19, 20])
    ]


def test_source_comment_exception_restores_rule(tmp_path: Path) -> None:
    document = tmp_path / "cache.cpp"
    document.write_text(
        "/**\n * <!-- vale Google.We = NO -->\n * We use the quoted label.\n"
        " * <!-- vale Google.We = YES -->\n * We inspect the result.\n */\n",
        encoding="utf-8",
    )
    _, findings = lint(document)
    assert [(finding["Check"], finding["Line"], finding["Span"]) for finding in findings] == [
        ("Google.We", 5, [4, 5])
    ]


@pytest.mark.parametrize(
    "directive",
    ["@see apply_gain(float)", "@see apply_gain(float, float)", "@snippet gain.cpp scale_sample"],
)
def test_directive_arguments_preserve_following_prose(tmp_path: Path, directive: str) -> None:
    document = tmp_path / "gain.cpp"
    document.write_text(f"/** {directive} We inspect the result. */\n", encoding="utf-8")
    _, findings = lint(document)
    assert [(finding["Check"], finding["Match"]) for finding in findings] == [
        ("Google.We", "We")
    ]


@pytest.mark.parametrize("prefix", ["@", "\\"])
@pytest.mark.parametrize("spacing", ["", " "])
def test_parameter_direction_preserves_description(
    tmp_path: Path, prefix: str, spacing: str
) -> None:
    document = tmp_path / "gain.cpp"
    directive = f"{prefix}param{spacing}[in] DoxyGen"
    document.write_text(f"/** {directive} We inspect the result. */\n", encoding="utf-8")
    _, findings = lint(document)
    assert [(finding["Check"], finding["Line"], finding["Span"]) for finding in findings] == [
        ("Google.We", 1, [len(directive) + 6, len(directive) + 7])
    ]


@pytest.mark.parametrize("prefix", ["@", "\\"])
def test_verbatim_payload_is_excluded_and_following_prose_keeps_position(
    tmp_path: Path, prefix: str
) -> None:
    document = tmp_path / "gain.cpp"
    document.write_text(
        f"/**\n * {prefix}verbatim\n * We use DoxyGen.\n * {prefix}endverbatim\n"
        " * We inspect the result.\n */\n",
        encoding="utf-8",
    )
    _, findings = lint(document)
    assert [(finding["Check"], finding["Line"], finding["Span"]) for finding in findings] == [
        ("Google.We", 5, [4, 5])
    ]


@pytest.mark.parametrize("extension", ["h", "cc", "hpp", "cxx"])
def test_configured_extensions_keep_comment_scope(tmp_path: Path, extension: str) -> None:
    document = tmp_path / f"cache.{extension}"
    document.write_text(
        'const char *text = "We use DoxyGen";\n/// We use DoxyGen.\n',
        encoding="utf-8",
    )
    _, findings = lint(document)
    assert {(finding["Line"], finding["Span"][0]) for finding in findings} == {
        (2, 5), (2, 12)
    }
