"""Source ingestion for PDF, DOCX and plain-text study material."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .textutils import clean_text, split_sentences


@dataclass
class Section:
    title: str
    text: str
    level: int = 1
    start: int = 0


@dataclass
class SourceDocument:
    title: str
    text: str
    path: str
    pages: int
    words: int
    sections: list[Section] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def sentences(self) -> list[str]:
        return split_sentences(self.text)


def _pdf_text(path: Path) -> tuple[str, int, dict]:
    try:
        import pymupdf
    except ImportError:  # pragma: no cover - compatibility
        import fitz as pymupdf
    doc = pymupdf.open(path)
    chunks = []
    for page in doc:
        chunks.append(page.get_text("text"))
    meta = dict(doc.metadata or {})
    pages = doc.page_count
    doc.close()
    return "\n\n".join(chunks), pages, meta


def _docx_text(path: Path) -> tuple[str, int, dict]:
    import docx

    doc = docx.Document(path)
    chunks = [p.text for p in doc.paragraphs if p.text.strip()]
    for table in doc.tables:
        for row in table.rows:
            cells = [c.text.strip() for c in row.cells if c.text.strip()]
            if cells:
                chunks.append(" | ".join(cells))
    pages = max(1, len(chunks) // 42)
    props = doc.core_properties
    meta = {"title": props.title, "author": props.author, "created": str(props.created)}
    return "\n\n".join(chunks), pages, meta


def _txt_text(path: Path) -> tuple[str, int, dict]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return text, max(1, len(text) // 2800), {}


def _guess_title(text: str, path: Path) -> str:
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]
    candidates = [ln for ln in lines[:40] if 12 <= len(ln) <= 120 and not ln.lower().startswith(("contents", "table of"))]
    for line in candidates:
        if sum(w.isalpha() for w in line) > len(line) * 0.6:
            return line
    return path.stem.replace("_", " ").replace("-", " ").title()


_HEADING_PATTERNS = [
    re.compile(r"^(?:PART|Part)\s+\d+\s*[-–:]?\s*(.{4,90})$"),
    re.compile(r"^(?:Chapter|CHAPTER|Section|SECTION)\s+\d+\s*[-–:]?\s*(.{4,90})$"),
    re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,2})\.?\s+([A-Z][^.!?]{3,85})$"),
    re.compile(r"^([A-Z][A-Za-z0-9 ,&/:\-]{7,80})$"),
]


def detect_sections(text: str) -> list[Section]:
    """Detect likely headings while ignoring running headers and page numbers.

    The detector is intentionally conservative: a heading must be a short line
    without terminal punctuation, followed by a longer body line.  This keeps
    false positives out of the extracted study guide.
    """
    lines = text.splitlines()
    sections: list[Section] = []
    current_title = "Overview"
    current: list[str] = []
    cursor = 0

    def flush() -> None:
        nonlocal current
        body = "\n".join(current).strip()
        if len(body.split()) >= 25:
            sections.append(Section(current_title, body, 1, cursor))
        current = []

    for i, raw in enumerate(lines):
        line = re.sub(r"\s+", " ", raw).strip()
        if not line:
            if current:
                current.append("")
            continue
        # Skip page numbers, running headers, dotted TOC entries.
        if re.fullmatch(r"\d{1,3}", line) or "...." in line:
            continue
        if len(line) > 100 or line.endswith((".", "!", "?", ";", ",")):
            current.append(line)
            continue
        lookahead = ""
        for nxt in lines[i + 1:i + 5]:
            nxt = nxt.strip()
            if nxt and not re.fullmatch(r"\d{1,3}", nxt):
                lookahead = nxt
                break
        heading = None
        for pat in _HEADING_PATTERNS:
            m = pat.match(line)
            if m:
                heading = line
                break
        # Reject title-case sentences and very common running headers.
        if heading and len(lookahead.split()) >= 8 and not lookahead.endswith("."):
            if heading.lower() not in {"contents", "executive summary"}:
                flush()
                current_title = heading
                cursor += len(line)
                continue
        current.append(line)
        cursor += len(line)
    flush()

    if len(sections) < 2:
        # Fall back to paragraph blocks, grouping them into pseudo-sections.
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if len(p.split()) > 30]
        sections = []
        for idx in range(0, min(len(paragraphs), 40), 5):
            body = "\n\n".join(paragraphs[idx:idx + 5])
            first = split_sentences(paragraphs[idx])[0] if split_sentences(paragraphs[idx]) else f"Topic {idx // 5 + 1}"
            sections.append(Section(first[:80], body, 1, idx))
    return sections


def load_document(path: str | Path, fallback_title: str | None = None) -> SourceDocument:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        raw, pages, meta = _pdf_text(path)
    elif suffix in {".docx", ".doc"}:
        raw, pages, meta = _docx_text(path)
    elif suffix in {".txt", ".md"}:
        raw, pages, meta = _txt_text(path)
    else:
        raise ValueError(f"Unsupported input format: {suffix}. Use PDF, DOCX, TXT or MD.")

    text = clean_text(raw)
    if len(text.split()) < 120:
        raise ValueError("The uploaded document is too short to build a reliable content bundle.")

    title = (meta.get("title") or "").strip()
    if not title or len(title) < 8:
        title = fallback_title or _guess_title(text, path)
    sections = detect_sections(text)
    return SourceDocument(
        title=title,
        text=text,
        path=str(path),
        pages=pages,
        words=len(text.split()),
        sections=sections,
        metadata=meta,
    )
