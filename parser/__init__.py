"""Unified document parser for the Proposal Harness.

Auto-dispatches between PDF and Office parsers based on file extension.
Supports: .pdf, .docx, .pptx, .xlsx, .rtf
"""

from __future__ import annotations

import os
from pathlib import Path

__all__ = ["parse", "SUPPORTED_EXTENSIONS", "OUTPUT_EXT_MAP"]

PDF_EXTENSIONS = {".pdf"}
OFFICE_EXTENSIONS = {".docx", ".pptx", ".xlsx", ".rtf"}
SUPPORTED_EXTENSIONS = PDF_EXTENSIONS | OFFICE_EXTENSIONS
OUTPUT_EXT_MAP = {"markdown": ".md", "html": ".html", "text": ".txt"}


def parse(
    file_path: str | os.PathLike,
    *,
    table_extraction: str = "accurate",
    output_format: str = "markdown",
) -> str:
    """Parse a document and return extracted content.

    Args:
        file_path: Path to the document file.
        table_extraction: PDF table extraction mode — "accurate" or "fast".
        output_format: Output content format — "markdown", "html", or "text".
            Note: PDF extraction always returns markdown regardless of
            output_format.

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
        return _parse_pdf(path, table_extraction=table_extraction)
    else:
        return _parse_office(path, output_format=output_format)


def _parse_pdf(
    path: Path,
    *,
    table_extraction: str = "accurate",
) -> str:
    """Parse PDF using Docling-based extraction."""
    from .pdf_converter import DoclingConverter
    from .pdf_markdown import MarkdownBuilder

    converter = DoclingConverter(table_mode=table_extraction)
    parsed = converter.convert(str(path))

    asset_dir = path.parent / f".parsed_{path.stem}"
    asset_dir.mkdir(parents=True, exist_ok=True)
    parsed.save_assets(asset_dir)

    builder = MarkdownBuilder(parsed, asset_dir)
    return builder.build()


def _parse_office(
    path: Path,
    *,
    output_format: str = "markdown",
) -> str:
    """Parse Office/ODF/RTF documents via AST-based extraction."""
    from .office_parser import OfficeParser
    from .office_types import OfficeParserConfig

    config = OfficeParserConfig(summarize=False, extract_attachments=True)
    ast = OfficeParser.parse_office(str(path), config)

    if output_format == "html":
        return ast.to_html()
    elif output_format == "text":
        return ast.to_text()
    else:
        return ast.to_markdown()
