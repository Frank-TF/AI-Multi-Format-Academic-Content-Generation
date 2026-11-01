"""DOCX, Markdown and ZIP exporters for the generated content bundle."""

from __future__ import annotations

import zipfile
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from .config import INK, MIST, NAVY, SLATE, TEAL, ProjectMeta
from .phase1_notes import StudyGuide
from .phase4_refine import RefinementResult


def _rgb(hex_color: str) -> RGBColor:
    h = hex_color.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _shade(cell, color: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color.lstrip("#"))
    tcPr.append(shd)


def _set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in("w:tcMar")
    if tcMar is None:
        tcMar = OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for tag, value in (("top", top), ("bottom", bottom), ("start", left), ("end", right)):
        node = tcMar.find(qn(f"w:{tag}"))
        if node is None:
            node = OxmlElement(f"w:{tag}")
            tcMar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def _page_field(paragraph):
    run = paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_end)


def _style_document(doc: Document):
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(1.8)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = _rgb(INK)
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.line_spacing = 1.12

    for name, size, color in (("Heading 1", 15, NAVY), ("Heading 2", 12, NAVY), ("Heading 3", 11, TEAL)):
        st = doc.styles[name]
        st.font.name = "Arial"
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = _rgb(color)
        st.paragraph_format.space_before = Pt(12)
        st.paragraph_format.space_after = Pt(4)
        st.paragraph_format.keep_with_next = True


def _header_footer(doc: Document, meta: ProjectMeta, label: str):
    section = doc.sections[0]
    header = section.header
    table = header.add_table(rows=1, cols=2, width=Cm(17.0))
    table.autofit = True
    left, right = table.rows[0].cells
    p = left.paragraphs[0]
    r = p.add_run(label)
    r.font.name = "Arial"; r.font.size = Pt(8); r.font.color.rgb = _rgb(SLATE); r.italic = True
    p2 = right.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r2 = p2.add_run(f"{meta.author}  |  {meta.uid}  |  {meta.course}")
    r2.font.name = "Arial"; r2.font.size = Pt(8); r2.font.bold = True; r2.font.color.rgb = _rgb(NAVY)
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp.add_run("Page ")
    run.font.name = "Arial"; run.font.size = Pt(8); run.font.color.rgb = _rgb(SLATE)
    _page_field(fp)


def _title_block(doc: Document, title: str, subtitle: str, meta: ProjectMeta):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    r = p.add_run(title)
    r.font.name = "Arial"; r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = _rgb(NAVY)
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run(subtitle)
    r2.font.name = "Arial"; r2.font.size = Pt(11); r2.italic = True; r2.font.color.rgb = _rgb(TEAL)
    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = p3.add_run(f"{meta.author}  |  UID: {meta.uid}  |  Subject Code: {meta.course}  |  {meta.date}")
    r3.font.name = "Arial"; r3.font.size = Pt(9); r3.font.color.rgb = _rgb(SLATE)


def _table(doc: Document, headers: list[str], rows: list[list[str]], widths: list[float] | None = None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Arial"; r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = _rgb("#FFFFFF")
        _shade(hdr[i], NAVY)
        _set_cell_margins(hdr[i])
    for ri, row in enumerate(rows):
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            r = p.add_run(str(val))
            r.font.name = "Arial"; r.font.size = Pt(8.2); r.font.color.rgb = _rgb(INK)
            if ri % 2 == 0:
                _shade(cells[i], "F4F7F9")
            _set_cell_margins(cells[i])
            if widths:
                cells[i].width = Cm(widths[i])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def export_study_guide(guide: StudyGuide, meta: ProjectMeta, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    _style_document(doc)
    _header_footer(doc, meta, "Comprehensive Study Guide")

    _title_block(doc, "COMPREHENSIVE STUDY GUIDE", guide.title, meta)
    doc.add_heading("Abstract", level=1)
    doc.add_paragraph(guide.abstract)
    p = doc.add_paragraph()
    r = p.add_run("Keywords: " + "; ".join(guide.keywords))
    r.italic = True; r.font.size = Pt(9)

    doc.add_heading("1. Study Notes and Core Concepts", level=1)
    for i, topic in enumerate(guide.topics, 1):
        doc.add_heading(f"Topic {i}: {topic.title}", level=2)
        p = doc.add_paragraph()
        p.add_run("Core concept. ").bold = True
        p.add_run(topic.core)
        for term, definition in topic.definitions:
            p = doc.add_paragraph(style="List Bullet")
            p.add_run(f"{term}: ").bold = True
            p.add_run(definition)
        for pill in topic.bullets:
            doc.add_paragraph(pill, style="List Bullet")
        p = doc.add_paragraph()
        p.add_run("Practical example. ").bold = True
        p.add_run(topic.example)

    doc.add_heading("2. Structured Revision Points", level=1)
    doc.add_heading("Key facts and statistics", level=2)
    for point in guide.revision_points:
        doc.add_paragraph(point, style="List Bullet")

    doc.add_heading("3. Quick Revision Matrix", level=1)
    _table(doc, ["Research field / domain", "Core definition", "Primary use cases"],
           [[a, b, c] for a, b, c in guide.matrix], [3.8, 7.0, 6.2])

    doc.add_heading("4. Exam-Oriented Question Bank", level=1)
    for kind in ("Short-Answer / Conceptual", "Practical / Scenario-Based", "Multiple-Choice"):
        doc.add_heading(f"{kind} Questions", level=2)
        n = 0
        for q in guide.questions:
            if q.kind != kind:
                continue
            n += 1
            p = doc.add_paragraph()
            p.add_run(f"{n}. ").bold = True
            p.add_run(q.prompt)
            if q.options:
                for opt in q.options:
                    doc.add_paragraph(opt, style="List Bullet")
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.75)
            p.add_run("Answer: ").bold = True
            p.add_run(q.answer)

    doc.add_heading("5. Last-Minute Reviser", level=1)
    for point in guide.reviser:
        doc.add_paragraph(point, style="List Bullet")

    doc.save(path)
    return path


def export_refinement(result: RefinementResult, meta: ProjectMeta, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    _style_document(doc)
    _header_footer(doc, meta, "Phase 4 - Academic Writing Refinement")

    _title_block(doc, "PHASE 4: ACADEMIC WRITING REFINEMENT", result.title, meta)
    doc.add_heading("1. Executive Abstract", level=1)
    doc.add_paragraph(result.refined)

    doc.add_heading("2. Glossary of Key Academic Terms", level=1)
    for i, (term, definition) in enumerate(result.glossary, 1):
        p = doc.add_paragraph()
        p.add_run(f"{i}. {term}: ").bold = True
        p.add_run(definition)

    doc.add_heading("3. Peer-Review Quality Audit Checklist", level=1)
    _table(doc, ["Quality criterion", "Audit status", "Execution details and verification"],
           [[r.criterion, r.status, r.evidence] for r in result.audit], [4.0, 2.8, 10.2])

    doc.add_heading("4. References", level=1)
    for i, ref in enumerate(result.references, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.7)
        p.paragraph_format.first_line_indent = Cm(-0.7)
        p.add_run(f"[{i}] {ref}").font.size = Pt(9)

    doc.save(path)
    return path


def export_bundle(files: list[Path], path: str | Path) -> Path:
    path = Path(path)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            if f.exists():
                zf.write(f, f.name)
    return path
