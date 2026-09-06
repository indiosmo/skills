from pathlib import Path

import pytest
from doxygen_linter.checks import lint

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    "filename,language", [("representative.c", "c"), ("representative.hpp", "cpp")], ids=["c", "cpp"]
)
def test_representative_c_and_cpp(filename: str, language: str) -> None:
    diagnostics, coverage = lint((FIXTURES / filename).read_bytes(), filename, language)
    assert diagnostics == []
    assert not any(item.status == "blocked" for item in coverage)
    if language == "cpp":
        assert any("macros" in item.reason for item in coverage)


def test_invalid_fixture_expected_diagnostics():
    diagnostics, _ = lint((FIXTURES / "invalid.cpp").read_bytes(), "invalid.cpp", "cpp")
    assert {(item.rule, item.line, item.column) for item in diagnostics} == {
        ("DOX003", 2, 4),
        ("DOX006", 3, 4),
        ("DOX007", 3, 4),
        ("DOX012", 1, 1),
    }
