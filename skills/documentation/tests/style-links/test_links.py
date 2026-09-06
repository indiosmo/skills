"""Exercise the pinned link checker against files and a controlled HTTP origin."""

from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import socket
import subprocess
from threading import Thread

import pytest


SKILL_DIRECTORY = Path(__file__).resolve().parents[2]
CONFIGURATION = SKILL_DIRECTORY / "assets/lychee/lychee.toml"
FIXTURES = SKILL_DIRECTORY / "assets/lychee/fixtures"


def check_links(input_file: Path, *options: str) -> tuple[int, dict]:
    completed = subprocess.run(
        ["uvx", "--from", "lychee-bin==0.24.2", "lychee", "--config",
         str(CONFIGURATION), "--max-retries", "0", *options, "--", str(input_file)],
        capture_output=True, text=True, timeout=60,
    )
    assert completed.returncode in (0, 2), completed.stderr + completed.stdout
    return completed.returncode, json.loads(completed.stdout)


@pytest.fixture(scope="module")
def http_origin() -> Iterator[str]:
    class LinkFixtureHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            status = {"/missing": 404, "/gone": 410, "/auth": 401,
                      "/forbidden": 403, "/limited": 429, "/temporary": 503,
                      "/redirect": 301, "/loop": 301}.get(self.path, 200)
            self.send_response(status)
            self.send_header("Content-Type", "text/html")
            if status == 301:
                self.send_header("Location", "/loop" if self.path == "/loop" else "/valid")
            self.end_headers()
            self.wfile.write(b'<html><h1 id="install">Install</h1></html>')

        def log_message(self, format: str, *arguments: object) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), LinkFixtureHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


@pytest.mark.parametrize("filename,exit_status", [
    ("valid.md", 0), ("broken-file.md", 2), ("broken-anchor.md", 2),
])
def test_local_files_and_headings(filename: str, exit_status: int) -> None:
    status, report = check_links(FIXTURES / filename, "--offline")
    assert status == exit_status, report
    assert report["successful"] == (1 if exit_status == 0 else 0)


@pytest.mark.parametrize("route,exit_status", [
    ("valid#install", 0), ("redirect", 0), ("valid#missing", 2),
    ("missing", 2), ("gone", 2), ("auth", 2), ("forbidden", 2),
    ("limited", 2), ("temporary", 2), ("loop", 2),
])
def test_http_links_keep_failures_visible(
    tmp_path: Path, http_origin: str, route: str, exit_status: int,
) -> None:
    input_file = tmp_path / "links.md"
    input_file.write_text(f"[Target]({http_origin}/{route})\n", encoding="utf-8")
    status, report = check_links(input_file)
    assert status == exit_status, report
    assert report["successful"] == (1 if exit_status == 0 else 0)
    if route in {"missing", "gone", "auth", "forbidden", "limited", "temporary"}:
        expected_code = {"missing": 404, "gone": 410, "auth": 401,
                         "forbidden": 403, "limited": 429, "temporary": 503}[route]
        assert str(expected_code) in json.dumps(report["error_map"])


def test_offline_links_are_excluded(tmp_path: Path) -> None:
    input_file = tmp_path / "offline.md"
    input_file.write_text("[Unchecked](https://example.invalid/missing)\n", encoding="utf-8")
    status, report = check_links(input_file, "--offline")
    assert status == 0, report
    assert report["successful"] == 0
    assert report["excludes"] == 1
    assert report["excluded_map"]


def test_unmatched_glob_warns_and_reports_zero_coverage(tmp_path: Path) -> None:
    completed = subprocess.run(
        ["uvx", "--from", "lychee-bin==0.24.2", "lychee", "--config",
         str(CONFIGURATION), "--offline", "--", str(tmp_path / "missing" / "**/*.html")],
        capture_output=True, text=True, timeout=60,
    )
    assert completed.returncode == 0
    report = json.loads(completed.stdout)
    assert report["total"] == 0
    assert report["successful"] == 0
    assert "No files found" in completed.stderr


def test_selected_page_without_links_has_zero_link_coverage(tmp_path: Path) -> None:
    input_file = tmp_path / "no-links.md"
    input_file.write_text("# Local observation\n\nThe sample contains two newlines.\n", encoding="utf-8")
    status, report = check_links(input_file, "--offline")
    assert input_file.is_file()
    assert status == 0
    assert report["total"] == 0
    assert report["successful"] == 0
    assert report["excludes"] == 0


def test_explicit_exclusion_stays_visible(tmp_path: Path) -> None:
    input_file = tmp_path / "excluded.md"
    input_file.write_text("[Unchecked](https://example.invalid/private)\n", encoding="utf-8")
    status, report = check_links(input_file, "--exclude", r"^https://example\.invalid/private$")
    assert status == 0, report
    assert report["successful"] == 0
    assert report["excludes"] == 1
    assert report["excluded_map"]


def test_connection_failure_remains_unresolved(tmp_path: Path) -> None:
    with socket.socket() as reserved_port:
        reserved_port.bind(("127.0.0.1", 0))
        port = reserved_port.getsockname()[1]
        input_file = tmp_path / "unreachable.md"
        input_file.write_text(f"[Unreachable](http://127.0.0.1:{port}/)\n", encoding="utf-8")
        status, report = check_links(input_file)
    assert status == 2, report
    assert report["successful"] == 0
    assert report["errors"] == 1
    assert report["error_map"]


@pytest.mark.parametrize("fragment,exit_status", [("install", 0), ("missing", 2)])
def test_built_html_root_and_directory_links(
    tmp_path: Path, fragment: str, exit_status: int,
) -> None:
    guide = tmp_path / "guide"
    guide.mkdir()
    (guide / "index.html").write_text('<h1 id="install">Install</h1>', encoding="utf-8")
    input_file = tmp_path / "index.html"
    input_file.write_text(f'<a href="/guide/#{fragment}">Guide</a>', encoding="utf-8")
    status, report = check_links(input_file, "--offline", "--root-dir", str(tmp_path),
                                 "--index-files", "index.html")
    assert status == exit_status, report
