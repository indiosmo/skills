"""Exercise native generation and example checks with planted defects."""

from pathlib import Path
import re
import shutil
import subprocess
import sys

import pytest


@pytest.fixture
def project(tmp_path: Path) -> Path:
    return Path(shutil.copytree(Path(__file__).parent / "fixture", tmp_path / "project"))


def generate_reference(project: Path, output: Path) -> subprocess.CompletedProcess[str]:
    configuration = (project / "Doxyfile").read_text() + f'\nOUTPUT_DIRECTORY = "{output}"\n'
    return subprocess.run(
        ["doxygen", "-"], input=configuration, cwd=project,
        text=True, capture_output=True, timeout=30, check=False,
    )


def build_site(project: Path, output: Path) -> subprocess.CompletedProcess[str]:
    reference = generate_reference(project, project / "docs/reference")
    assert reference.returncode == 0, reference.stderr
    return subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "--config-file",
         str(project / "mkdocs.yml"), "--site-dir", str(output)],
        cwd=project, text=True, capture_output=True, timeout=30, check=False,
    )


def test_generated_reference(project: Path, tmp_path: Path) -> None:
    output = tmp_path / "reference"
    result = generate_reference(project, output)
    assert result.returncode == 0, result.stderr
    rendered = (output / "html" / "gain_8hpp.html").read_text()
    assert "[1/2]" in rendered and "[2/2]" in rendered
    assert "Linear gain factor." in rendered
    assert "Input sample amplitude." in rendered
    assert "Scaled sample amplitude." in rendered
    assert "wet_signal" in rendered and "0.25" in rendered
    assert 'class="el" href="gain_8hpp.html#' in rendered
    symbol_targets = re.findall(r'class="el" href="gain_8hpp.html#([^"]+)"', rendered)
    assert len(set(symbol_targets)) == 2
    assert all(f'id="{target}"' in rendered for target in symbol_targets)
    assert 'class="paramname">sample' in rendered
    assert 'class="paramname">gain' in rendered


@pytest.mark.parametrize("original,replacement,diagnostic", [
    ("@param gain", "@param missing_gain", "missing_gain"),
    ("@see apply_gain(float)", "@see @ref missing_symbol", "missing_symbol"),
])
def test_comment_defects(project: Path, tmp_path: Path, original: str,
                        replacement: str, diagnostic: str) -> None:
    source = project / "include/gain.hpp"
    source.write_text(source.read_text().replace(original, replacement))
    result = generate_reference(project, tmp_path / "reference")
    assert result.returncode != 0
    assert diagnostic in result.stderr and "gain.hpp:" in result.stderr


def test_site_rendering(project: Path, tmp_path: Path) -> None:
    output = tmp_path / "site"
    result = build_site(project, output)
    assert result.returncode == 0, result.stderr
    home = (output / "index.html").read_text()
    procedure = (output / "gain/index.html").read_text()
    assert 'href="gain/#verify-the-result"' in home
    assert 'id="verify-the-result"' in procedure
    assert 'class="admonition note"' in procedure
    assert 'src="assets/gain.svg"' in home
    assert "A sample enters gain processing" in home
    assert (output / "assets/gain.svg").is_file()
    assert 'href="gain/"' in home and "Apply gain" in home
    assert 'href="reference/html/gain_8hpp.html"' in home
    assert (output / "reference/html/gain_8hpp.html").is_file()


@pytest.mark.parametrize("filename,original,replacement,diagnostic", [
    ("docs/index.md", "#verify-the-result", "#missing-anchor", "missing-anchor"),
    ("docs/index.md", "gain.md#verify-the-result", "missing.md", "missing.md"),
    ("docs/index.md", "assets/gain.svg", "assets/missing.svg", "missing.svg"),
    ("mkdocs.yml", "Apply gain: gain.md", "Apply gain: missing.md", "missing.md"),
])
def test_site_defects(project: Path, tmp_path: Path, filename: str, original: str,
                      replacement: str, diagnostic: str) -> None:
    source = project / filename
    source.write_text(source.read_text().replace(original, replacement))
    result = build_site(project, tmp_path / "site")
    assert result.returncode != 0
    assert diagnostic in result.stderr


@pytest.mark.parametrize("broken", [False, True])
def test_combined_reference_links(project: Path, tmp_path: Path, broken: bool) -> None:
    output = tmp_path / "site"
    built = build_site(project, output)
    assert built.returncode == 0, built.stderr
    home = output / "index.html"
    if broken:
        home.write_text(home.read_text().replace(
            "reference/html/gain_8hpp.html", "reference/html/missing-symbol.html"))
    configuration = Path(__file__).resolve().parents[2] / "assets/lychee/lychee.toml"
    checked = subprocess.run(
        ["lychee", "--config", str(configuration), "--offline", "--root-dir",
         str(output), "--index-files", "index.html", "--", str(home)],
        cwd=tmp_path, text=True, capture_output=True, timeout=30, check=False,
    )
    if broken:
        assert checked.returncode != 0
        assert "missing-symbol.html" in checked.stdout + checked.stderr
    else:
        assert checked.returncode == 0, checked.stdout + checked.stderr


@pytest.mark.parametrize("broken", [False, True])
def test_runnable_example(project: Path, tmp_path: Path, broken: bool) -> None:
    if broken:
        source = project / "include/gain.hpp"
        source.write_text(source.read_text().replace("sample * gain", "sample + gain"))
    executable = tmp_path / "gain-example"
    compiled = subprocess.run(
        ["c++", "-std=c++17", "-Iinclude", "examples/gain.cpp", "-o", str(executable)],
        cwd=project, text=True, capture_output=True, timeout=30, check=False,
    )
    assert compiled.returncode == 0, compiled.stderr
    executed = subprocess.run([str(executable)], text=True, capture_output=True,
                              timeout=5, check=False)
    if broken:
        assert executed.returncode != 0
        assert executed.stdout != "0.5\n"
    else:
        assert executed.returncode == 0
        assert executed.stdout == "0.5\n"
