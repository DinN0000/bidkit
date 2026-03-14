"""Docling 기반 PDF 변환 및 요소 추출."""

from __future__ import annotations

import logging
from pathlib import Path

from docling_core.types.doc import PictureItem, TableItem
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableFormerMode,
    TableStructureOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption

from .pdf_utils import get_figure_category

logger = logging.getLogger("pdf_parser.converter")


class DoclingConverter:
    """PDF → Docling Document 변환 및 요소(텍스트/테이블/이미지) 추출."""

    def __init__(self, image_scale: float = 2.0, table_mode: str = "accurate"):
        opts = PdfPipelineOptions()
        opts.images_scale = image_scale
        opts.generate_page_images = True
        opts.generate_picture_images = True
        opts.generate_table_images = True
        opts.do_picture_classification = True
        opts.do_table_structure = True
        opts.table_structure_options = TableStructureOptions(
            mode=TableFormerMode.ACCURATE if table_mode == "accurate" else TableFormerMode.FAST,
            do_cell_matching=True,
        )
        self._converter = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
        )
        self.image_scale = image_scale

    def convert(self, pdf_path: str | Path) -> "ParsedDocument":
        """PDF를 변환하여 ParsedDocument 반환."""
        result = self._converter.convert(pdf_path)
        return ParsedDocument(result, self.image_scale)


class ParsedDocument:
    """변환된 문서에서 요소를 추출하는 래퍼."""

    def __init__(self, result, image_scale: float):
        self.doc = result.document
        self.doc_name = result.input.file.stem
        self.image_scale = image_scale

    def get_figures(self) -> list[tuple[int, PictureItem, str]]:
        """(1-based index, element, category) 리스트 반환. logo 제외."""
        figures = []
        idx = 0
        for element, _ in self.doc.iterate_items():
            if isinstance(element, PictureItem):
                idx += 1
                cat = get_figure_category(element)
                if cat == "logo":
                    continue
                figures.append((idx, element, cat))
        return figures

    def get_tables(self) -> list[tuple[int, TableItem]]:
        """(1-based index, element) 리스트 반환."""
        tables = []
        idx = 0
        for element, _ in self.doc.iterate_items():
            if isinstance(element, TableItem):
                idx += 1
                tables.append((idx, element))
        return tables

    def save_assets(self, output_dir: Path):
        """테이블 md/이미지, figure 이미지를 output_dir에 저장."""
        table_img_dir = output_dir / "table" / "img"
        table_md_dir = output_dir / "table" / "md"
        pictures_dir = output_dir / "pictures"
        for d in (table_img_dir, table_md_dir):
            d.mkdir(parents=True, exist_ok=True)

        # 테이블 저장
        for idx, tbl in self.get_tables():
            md_path = table_md_dir / f"{self.doc_name}_table_{idx}.md"
            md_path.write_text(tbl.export_to_markdown(doc=self.doc), encoding="utf-8")
            img = tbl.get_image(self.doc)
            if img:
                img_path = table_img_dir / f"{self.doc_name}_table_{idx}.png"
                img.save(str(img_path), "PNG")
            logger.debug("  Table %d saved", idx)

        # Figure 저장
        pic_idx = 0
        for element, _ in self.doc.iterate_items():
            if isinstance(element, PictureItem):
                pic_idx += 1
                cat = get_figure_category(element)
                if cat == "logo":
                    continue
                cat_dir = pictures_dir / cat
                cat_dir.mkdir(parents=True, exist_ok=True)
                img = element.get_image(self.doc)
                if img:
                    img.save(str(cat_dir / f"{self.doc_name}_picture_{pic_idx}.png"), "PNG")
                logger.debug("  Figure %d (%s) saved", pic_idx, cat)
