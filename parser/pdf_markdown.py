"""최종 통합 마크다운 조립 — 페이지/이미지/테이블 메타데이터 HTML 테이블 삽입."""

from __future__ import annotations

import re
from pathlib import Path

from docling_core.types.doc import PictureItem, TableItem

from .pdf_utils import get_location, get_bbox_str, get_figure_category

PAGE_BREAK = "<!-- page-break -->"


def _html_row(key: str, value: str, indent: int = 2) -> str:
    sp = " " * indent
    return f"{sp}<tr>\n{sp}  <td>{key}</td>\n{sp}  <td>{value}</td>\n{sp}</tr>\n"


class MarkdownBuilder:
    """ParsedDocument + 요약 결과 → 최종 마크다운 생성."""

    def __init__(self, parsed_doc, output_dir: Path):
        self.parsed_doc = parsed_doc
        self.doc = parsed_doc.doc
        self.doc_name = parsed_doc.doc_name
        self.output_dir = output_dir
        self.table_img_dir = output_dir / "table" / "img"

    def build(
        self,
        page_summaries: dict[int, dict] | None = None,
        image_summaries: dict[int, dict] | None = None,
        table_summaries: dict[int, dict] | None = None,
    ) -> str:
        """최종 마크다운 문자열 반환."""
        page_summaries = page_summaries or {}
        image_summaries = image_summaries or {}
        table_summaries = table_summaries or {}
        md = self.doc.export_to_markdown(
            image_placeholder="<!-- image -->",
            page_break_placeholder=PAGE_BREAK,
            escape_html=False,
        )

        md = self._replace_figures(md, image_summaries)
        md = self._wrap_tables(md, table_summaries)
        md = self._wrap_pages(md, page_summaries)
        # logo figure 블록 제거
        md = re.sub(
            r'<table class="figure-meta">\n(?:(?!</table>).)*?<td>logo</td>.*?</table>',
            "", md, flags=re.DOTALL,
        )
        return md

    # ------------------------------------------------------------------
    def _replace_figures(self, md: str, image_summaries: dict) -> str:
        pic_idx = 0
        for element, _ in self.doc.iterate_items():
            if not isinstance(element, PictureItem):
                continue
            pic_idx += 1
            cat = get_figure_category(element)
            img_path = self.output_dir / "pictures" / cat / f"{self.doc_name}_picture_{pic_idx}.png"
            loc = get_location(element, self.doc)
            page_no = str(loc["page_no"]) if loc else ""
            bb = loc["bbox_tl"] if loc else {}
            bbox_str = f'l={bb["l"]:.1f} t={bb["t"]:.1f} r={bb["r"]:.1f} b={bb["b"]:.1f}' if bb else ""

            info = image_summaries.get(pic_idx, {"summary": "", "entities": []})
            img_rel = str(img_path.relative_to(self.output_dir)) if img_path.exists() else ""
            img_md = f"![figure-{pic_idx:03d}]({img_rel})" if img_rel else ""

            rows = (
                _html_row("image_id", f"figure-{pic_idx:03d}")
                + _html_row("category", cat)
                + _html_row("page_number", page_no)
                + _html_row("image_summary", info.get("summary", ""))
                + _html_row("entities", ", ".join(info.get("entities", [])))
                + _html_row("bbox", bbox_str)
                + _html_row("img_source", img_rel)
            )
            repl = f'<table class="figure-meta">\n{rows}</table>\n\n{img_md}'
            md = md.replace("<!-- image -->", repl, 1)
        return md

    # ------------------------------------------------------------------
    def _wrap_tables(self, md: str, table_summaries: dict) -> str:
        tbl_elements = [e for e, _ in self.doc.iterate_items() if isinstance(e, TableItem)]
        self._tbl_idx = 0
        self._tbl_elements = tbl_elements
        self._table_summaries = table_summaries

        def _replacer(m):
            if self._tbl_idx >= len(self._tbl_elements):
                return m.group(0)
            element = self._tbl_elements[self._tbl_idx]
            self._tbl_idx += 1
            idx = self._tbl_idx
            tag = f"table-{idx:03d}"
            img_path = self.table_img_dir / f"{self.doc_name}_table_{idx}.png"
            img_rel = str(img_path.relative_to(self.output_dir)) if img_path.exists() else ""
            img_md = f"![{tag}]({img_rel})" if img_rel else ""
            pn, bb = get_bbox_str(element, self.doc)
            info = self._table_summaries.get(idx, {"summary": "", "entities": [], "category": "other"})

            rows = (
                _html_row("table_id", tag)
                + _html_row("category", info.get("category", "other"))
                + _html_row("page_number", pn)
                + _html_row("table_summary", info.get("summary", ""))
                + _html_row("entities", ", ".join(info.get("entities", [])))
                + _html_row("bbox", bb)
                + _html_row("img_source", img_rel)
            )
            meta = f'<table class="table-meta">\n{rows}</table>\n\n{img_md}'
            return f"{meta}\n{m.group(0).strip()}"

        return re.sub(r"(?:^\|.+\n)+", _replacer, md, flags=re.MULTILINE)

    # ------------------------------------------------------------------
    def _wrap_pages(self, md: str, page_summaries: dict) -> str:
        pages = md.split(PAGE_BREAK)
        wrapped = []
        for i, page in enumerate(pages):
            if not page.strip():
                continue
            page_no = i + 1
            info = page_summaries.get(page_no, {"summary": "", "entities": []})
            summary = info.get("summary", "") if isinstance(info, dict) else str(info)
            entities = ", ".join(info.get("entities", [])) if isinstance(info, dict) else ""

            rows = (
                _html_row("page_number", str(page_no))
                + _html_row("page_summary", summary)
                + _html_row("entities", entities)
            )
            meta = f'<table class="page-meta">\n{rows}</table>\n'
            wrapped.append(f"<page-{page_no:03d}>\n{meta}{page.strip()}\n</page-{page_no:03d}>\n")
        return "\n\n".join(wrapped)
