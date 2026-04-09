"""Tests for VERSION file."""

from pathlib import Path


def test_version_file_exists() -> None:
    """Test that VERSION file exists at project root."""
    version_file = Path(__file__).parent.parent / "VERSION"
    assert version_file.exists(), "VERSION file should exist at project root"


def test_version_file_content() -> None:
    """Test that VERSION file contains correct version string."""
    version_file = Path(__file__).parent.parent / "VERSION"
    content = version_file.read_text().strip()
    assert content == "1.0.0", f"VERSION file should contain '1.0.0', but got '{content}'"


def test_version_file_format() -> None:
    """Test that VERSION file contains only version number without extra whitespace."""
    version_file = Path(__file__).parent.parent / "VERSION"
    content = version_file.read_text()
    lines = content.splitlines()
    assert len(lines) == 1, "VERSION file should contain exactly one line"
    assert content.strip() == content.rstrip(), "VERSION file should not have trailing whitespace"