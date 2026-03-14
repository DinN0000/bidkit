#!/usr/bin/env python3
"""CLI entry point for the document parser.

Usage:
    python -m parser.run INPUT [-o OUTPUT] [--workers N] [--table-mode MODE] [--format FMT]

Supports single-file and batch-directory modes.  In batch mode files are
processed in parallel via ProcessPoolExecutor.
"""

from __future__ import annotations

import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from parser import SUPPORTED_EXTENSIONS, parse


def _build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="parser",
        description="Extract text/tables from PDF and Office documents.",
    )
    ap.add_argument(
        "input",
        help="Path to a single file or a directory for batch processing.",
    )
    ap.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file (single mode) or directory (batch mode). "
        "Defaults to stdout / <input_dir>_parsed/.",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of parallel workers for batch mode (default: CPU count).",
    )
    ap.add_argument(
        "--table-extraction",
        choices=["accurate", "fast"],
        default="accurate",
        help="PDF table extraction mode (default: accurate).",
    )
    ap.add_argument(
        "--format",
        dest="output_format",
        choices=["markdown", "html", "text"],
        default="markdown",
        help="Output content format (default: markdown).",
    )
    return ap


def _parse_single(
    file_path: Path,
    output_path: Path | None,
    *,
    table_extraction: str,
    output_format: str,
) -> None:
    """Parse one file and write result to *output_path* or stdout."""
    content = parse(file_path, table_extraction=table_extraction, output_format=output_format)
    if output_path is None:
        sys.stdout.write(content)
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        print(f"  {file_path.name} -> {output_path}", file=sys.stderr)


def _worker(
    file_path: str,
    output_path: str,
    table_extraction: str,
    output_format: str,
) -> str:
    """Top-level function so it is picklable for ProcessPoolExecutor."""
    content = parse(file_path, table_extraction=table_extraction, output_format=output_format)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return f"{Path(file_path).name} -> {out}"


def _parse_batch(
    input_dir: Path,
    output_dir: Path | None,
    *,
    workers: int | None,
    table_extraction: str,
    output_format: str,
) -> None:
    """Parse every supported file in *input_dir* using a process pool."""
    files = sorted(
        f
        for f in input_dir.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not files:
        print(f"No supported files found in {input_dir}", file=sys.stderr)
        return

    if output_dir is None:
        output_dir = input_dir.parent / f"{input_dir.name}_parsed"
    output_dir.mkdir(parents=True, exist_ok=True)

    ext_map = {"markdown": ".md", "html": ".html", "text": ".txt"}
    out_ext = ext_map.get(output_format, ".md")

    futures = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for f in files:
            out_file = output_dir / f"{f.stem}{out_ext}"
            future = pool.submit(
                _worker,
                str(f),
                str(out_file),
                table_extraction,
                output_format,
            )
            futures[future] = f

        for future in as_completed(futures):
            src = futures[future]
            try:
                msg = future.result()
                print(f"  {msg}", file=sys.stderr)
            except Exception as exc:
                print(f"  ERROR {src.name}: {exc}", file=sys.stderr)


def main(argv: list[str] | None = None) -> None:
    args = _build_arg_parser().parse_args(argv)
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: {input_path} does not exist.", file=sys.stderr)
        sys.exit(1)

    if input_path.is_file():
        output_path = Path(args.output) if args.output else None
        _parse_single(
            input_path,
            output_path,
            table_extraction=args.table_extraction,
            output_format=args.output_format,
        )
    elif input_path.is_dir():
        output_dir = Path(args.output) if args.output else None
        _parse_batch(
            input_path,
            output_dir,
            workers=args.workers,
            table_extraction=args.table_extraction,
            output_format=args.output_format,
        )
    else:
        print(f"Error: {input_path} is neither a file nor a directory.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
