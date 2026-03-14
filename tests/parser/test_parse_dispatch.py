"""Tests for parser auto-dispatch and validation."""
import pytest
from parser import parse, SUPPORTED_EXTENSIONS


def test_supported_extensions_complete():
    """All documented extensions are in SUPPORTED_EXTENSIONS."""
    assert '.pdf' in SUPPORTED_EXTENSIONS
    assert '.docx' in SUPPORTED_EXTENSIONS
    assert '.pptx' in SUPPORTED_EXTENSIONS
    assert '.xlsx' in SUPPORTED_EXTENSIONS
    assert '.rtf' in SUPPORTED_EXTENSIONS
    # ODF formats (.odt, .odp, .ods) intentionally excluded — no handler


def test_unsupported_extension_raises(tmp_path):
    unsupported = tmp_path / "test.xyz"
    unsupported.write_text("dummy")
    with pytest.raises(ValueError, match="Unsupported file extension"):
        parse(str(unsupported))


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        parse("nonexistent.pdf")


def test_supported_extensions_no_aws():
    """SUPPORTED_EXTENSIONS should not include any AWS-specific formats."""
    for ext in SUPPORTED_EXTENSIONS:
        assert ext not in {'.json', '.yaml', '.yml'}, f"Unexpected extension: {ext}"
