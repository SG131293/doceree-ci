"""Tests for `runners.run_daily.write_artifacts` (Day 7 artifact writer)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from runners.run_daily import write_artifacts
from schema import (
    CollectionMethod,
    Finding,
    FindingStatus,
    SourceType,
)

_HTML_STUB = "<html><body>stub</body></html>"


def _finding(title: str = "T") -> Finding:
    return Finding(
        finding_id="abc12345" + "0" * 24,
        url="https://www.deepintent.com/x",
        source_type=SourceType.PRESS_RELEASE,
        collection_method=CollectionMethod.RSS,
        competitor="deepintent",
        title=title,
        summary="A short summary that is long enough.",
        evidence_quote="A quote.",
        signal_type="product_launch",
        products=["premium_programmatic"],
        raw_severity=4,
        raw_confidence=4,
        status=FindingStatus.VERIFIED,
        captured_at=datetime.now(timezone.utc),
    )


class TestWriteArtifacts:
    def test_creates_directory(self, tmp_path: Path) -> None:
        out = tmp_path / "doesnt_exist_yet" / "out"
        write_artifacts(out, findings=[], plaintext="body", html=_HTML_STUB, subject="subj")
        assert out.is_dir()

    def test_writes_four_files(self, tmp_path: Path) -> None:
        write_artifacts(
            tmp_path,
            findings=[_finding()],
            plaintext="hello body",
            html=_HTML_STUB,
            subject="subject line",
        )
        assert (tmp_path / "findings.jsonl").is_file()
        assert (tmp_path / "digest.txt").is_file()
        assert (tmp_path / "digest.html").is_file()
        assert (tmp_path / "subject.txt").is_file()

    def test_jsonl_one_per_line(self, tmp_path: Path) -> None:
        findings = [_finding(title="A"), _finding(title="B"), _finding(title="C")]
        write_artifacts(tmp_path, findings=findings, plaintext="x", html=_HTML_STUB, subject="y")
        text = (tmp_path / "findings.jsonl").read_text(encoding="utf-8")
        # Each non-empty line is a finding.
        lines = [line for line in text.split("\n") if line]
        assert len(lines) == 3
        # All lines parse as JSON.
        for line in lines:
            parsed = json.loads(line)
            assert "finding_id" in parsed
            assert "competitor" in parsed
            assert parsed["competitor"] == "deepintent"

    def test_jsonl_empty_when_no_findings(self, tmp_path: Path) -> None:
        write_artifacts(tmp_path, findings=[], plaintext="x", html=_HTML_STUB, subject="y")
        text = (tmp_path / "findings.jsonl").read_text(encoding="utf-8")
        assert text == ""

    def test_digest_text_round_trip(self, tmp_path: Path) -> None:
        body = "Doceree CI - 2026-04-30 - 1 finding\n\n== deepintent (1) ==\n..."
        write_artifacts(tmp_path, findings=[], plaintext=body, html=_HTML_STUB, subject="x")
        assert (tmp_path / "digest.txt").read_text(encoding="utf-8") == body

    def test_digest_html_round_trip(self, tmp_path: Path) -> None:
        html = "<html><body><h1>Test</h1></body></html>"
        write_artifacts(tmp_path, findings=[], plaintext="b", html=html, subject="x")
        assert (tmp_path / "digest.html").read_text(encoding="utf-8") == html

    def test_subject_round_trip(self, tmp_path: Path) -> None:
        subject = "Doceree CI - 2026-04-30 - 5 findings - 1 URGENT"
        write_artifacts(tmp_path, findings=[], plaintext="b", html=_HTML_STUB, subject=subject)
        assert (tmp_path / "subject.txt").read_text(encoding="utf-8") == subject
