"""Unified document parser for the Proposal Harness.

Auto-dispatches between PDF and Office parsers based on file extension.
Supports: .pdf, .docx, .pptx, .xlsx, .odt, .odp, .ods, .rtf
"""

from __future__ import annotations

import os
from pathlib import Path

__all__ = ["parse"]

PDF_EXTENSIONS = {".pdf"}
OFFICE_EXTENSIONS = {".docx", ".pptx", ".xlsx", ".odt", ".odp", ".ods", ".rtf"}
SUPPORTED_EXTENSIONS = PDF_EXTENSIONS | OFFICE_EXTENSIONS


def parse(
    file_path: str | os.PathLike,
    *,
    table_mode: str = "markdown",
    output_format: str = "markdown",
) -> str:
    """Parse a document and return extracted content.

    Args:
        file_path: Path to the document file.
        table_mode: How to render tables — "markdown", "html", or "csv".
        output_format: Output content format — "markdown", "html", or "text".

    Returns:
        Extracted content as a string in the requested format.

    Raises:
        FileNotFoundError: If *file_path* does not exist.
        ValueError: If the file extension is not supported.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file extension: {ext!r}. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if ext in PDF_EXTENSIONS:
        return _parse_pdf(path, table_mode=table_mode, output_format=output_format)
    else:
        return _parse_office(path, table_mode=table_mode, output_format=output_format)


def _parse_pdf(
    path: Path,
    *,
    table_mode: str = "markdown",
    output_format: str = "markdown",
) -> str:
    """Delegate PDF parsing to the pdf submodule."""
    from parser.pdf import extract  # noqa: F811

    return extract(path, table_mode=table_mode, output_format=output_format)


def _parse_office(
    path: Path,
    *,
    table_mode: str = "markdown",
    output_format: str = "markdown",
) -> str:
    """Delegate Office/ODF/RTF parsing to the office submodule."""
    from parser.office import extract  # noqa: F811

    return extract(path, table_mode=table_mode, output_format=output_format)
