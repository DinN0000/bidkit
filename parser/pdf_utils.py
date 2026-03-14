"""bbox / 위치 정보 헬퍼 유틸리티."""

from __future__ import annotations


def get_location(element, doc) -> dict | None:
    """element의 위치 정보를 딕셔너리로 반환.

    Returns:
        page_no, page_w, page_h, bbox_raw(BOTTOMLEFT), bbox_tl(TOPLEFT)
    """
    if not element.prov:
        return None
    p = element.prov[0]
    page = doc.pages.get(p.page_no)
    if page is None:
        return None
    bbox_tl = p.bbox.to_top_left_origin(page.size.height)
    return {
        "page_no": p.page_no,
        "page_w": page.size.width,
        "page_h": page.size.height,
        "bbox_raw": {"l": p.bbox.l, "t": p.bbox.t, "r": p.bbox.r, "b": p.bbox.b},
        "bbox_tl": {"l": bbox_tl.l, "t": bbox_tl.t, "r": bbox_tl.r, "b": bbox_tl.b},
    }


def get_bbox_str(element, doc) -> tuple[str, str]:
    """element의 (page_no 문자열, bbox 문자열) 튜플 반환."""
    loc = get_location(element, doc)
    if not loc:
        return "", ""
    bb = loc["bbox_tl"]
    return str(loc["page_no"]), f'l={bb["l"]:.1f} t={bb["t"]:.1f} r={bb["r"]:.1f} b={bb["b"]:.1f}'


def get_figure_category(element) -> str:
    """PictureItem의 분류 카테고리 반환."""
    for ann in element.get_annotations():
        if hasattr(ann, "predicted_classes") and ann.predicted_classes:
            return ann.predicted_classes[0].class_name
    return "unknown"
