from pathlib import Path

from doxygen_linter.checks import lint


FIXTURES = Path(__file__).parent / "fixtures"


def test_representative_c_and_cpp():
    for filename, language in [("representative.c", "c"), ("representative.hpp", "cpp")]:
        diagnostics, coverage = lint((FIXTURES / filename).read_bytes(), filename, language)
        assert diagnostics == []
        assert not any(item.status == "blocked" for item in coverage)
    assert any("macros" in item.reason for item in coverage)


def test_invalid_fixture_expected_diagnostics():
    diagnostics, _ = lint((FIXTURES / "invalid.cpp").read_bytes(), "invalid.cpp", "cpp")
    assert {(item.rule, item.line, item.column) for item in diagnostics} == {
        ("DOX003", 2, 4),
        ("DOX006", 3, 4),
        ("DOX007", 3, 4),
        ("DOX012", 1, 1),
    }
