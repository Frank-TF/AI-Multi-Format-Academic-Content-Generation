"""Streamlit front-end for the AI-Assisted Multi-Format Content Studio.

Run locally:
    streamlit run app.py
"""

from __future__ import annotations

import io
import json
import tempfile
import time
from pathlib import Path

import pandas as pd
import streamlit as st

from pipeline import ProjectMeta, RunResult, run_pipeline
from pipeline.config import (
    AMBER, DEFAULT_AUTHOR, DEFAULT_COURSE, DEFAULT_INSTITUTION, DEFAULT_TITLE,
    DEFAULT_UID, NAVY, SAMPLE_PDF, SLATE, TEAL,
)
from pipeline.orchestrator import load_manifest

st.set_page_config(
    page_title="Content Studio | IoT",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap');
:root {{
  --navy: {NAVY}; --teal: {TEAL}; --amber: {AMBER}; --slate: {SLATE};
  --mist: #EEF3F6; --line: #D8E2E9;
}}
html, body, [class*="css"] {{ font-family: 'Inter', 'Segoe UI', sans-serif; }}
.stApp {{ background: #F7F9FB; }}
.block-container {{ padding-top: 1.1rem; padding-bottom: 2.5rem; max-width: 1320px; }}
[data-testid="stSidebar"] {{ background: #0E1F36; }}
[data-testid="stSidebar"] * {{ color: #EAF2F6; }}
[data-testid="stSidebar"] .stTextInput input, [data-testid="stSidebar"] textarea {{
  background: #17324F !important; color: #fff !important; border: 1px solid #2C4C6B !important;
}}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {{
  background: #17324F; border: 1px dashed #3B6384;
}}
.hero {{
  background: linear-gradient(120deg, {NAVY} 0%, #1B3F63 58%, {TEAL} 140%);
  color: white; padding: 30px 34px 28px 34px; border-radius: 18px;
  position: relative; overflow: hidden; margin-bottom: 22px;
  box-shadow: 0 12px 34px rgba(19,41,75,.18);
}}
.hero:after {{
  content: ""; position: absolute; right: -70px; top: -110px; width: 340px; height: 340px;
  border: 1px solid rgba(127,209,206,.35); border-radius: 50%;
}}
.hero .kicker {{ color: #7FD1CE; font-size: .74rem; letter-spacing: .18em; font-weight: 700; }}
.hero h1 {{ font-size: 2.05rem; line-height: 1.14; margin: .38rem 0 .55rem 0; font-weight: 800; letter-spacing: -.02em; }}
.hero p {{ color: #D6E4EC; max-width: 810px; font-size: .97rem; margin: 0; }}
.hero .meta {{ color: #9FC9D6; font-size: .78rem; margin-top: 14px; letter-spacing: .02em; }}
.pill {{ display:inline-block; background:rgba(127,209,206,.14); color:#BDEBE7; border:1px solid rgba(127,209,206,.4);
        padding: 4px 10px; border-radius: 999px; font-size:.72rem; font-weight:600; margin-right:6px; }}
.card {{
  background: white; border: 1px solid var(--line); border-radius: 14px; padding: 18px 18px 15px 18px;
  height: 100%; box-shadow: 0 3px 12px rgba(19,41,75,.04);
}}
.card .num {{ font-size: .68rem; font-weight: 800; color: var(--teal); letter-spacing: .14em; }}
.card h4 {{ margin: .35rem 0 .35rem 0; color: var(--navy); font-size: .99rem; }}
.card p {{ color: #5B6770; font-size: .82rem; line-height: 1.45; margin: 0; }}
.metric {{ background:#fff; border:1px solid var(--line); border-radius:14px; padding:16px 18px; }}
.metric .v {{ font-size:1.75rem; font-weight:800; color:var(--navy); line-height:1.1; }}
.metric .l {{ font-size:.74rem; color:#6B7A85; text-transform:uppercase; letter-spacing:.08em; font-weight:600; margin-top:5px; }}
.section-title {{ font-size:1.05rem; font-weight:800; color:var(--navy); margin: 10px 0 10px 0; }}
.small {{ color:#6B7A85; font-size:.8rem; }}
.badge {{ display:inline-block; padding:3px 9px; border-radius:999px; font-size:.7rem; font-weight:700; }}
.badge.ok {{ background:#E3F4EF; color:#0B6B53; }}
.badge.warn {{ background:#FFF3DC; color:#8B5A0A; }}
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
.stTabs [data-baseweb="tab"] {{ height: 42px; background: #EDF2F5; border-radius: 10px 10px 0 0; padding: 0 16px; font-size:.86rem; font-weight:600; }}
.stTabs [aria-selected="true"] {{ background: white; color: {NAVY}; border-bottom: 3px solid {TEAL}; }}
div[data-testid="stMetricValue"] {{ color: {NAVY}; }}
.stDownloadButton button {{ border-radius: 9px; border: 1px solid {TEAL}; color: {TEAL}; font-weight:600; }}
.stButton > button[kind="primary"] {{ background: {TEAL}; border: 0; border-radius: 10px; font-weight: 700; }}
h2, h3 {{ color: {NAVY}; }}
code {{ color: #0B6B53; }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def hero():
    st.markdown(
        f"""
        <div class="hero">
          <div class="kicker">AI-ASSISTED MULTI-FORMAT ACADEMIC CONTENT GENERATION</div>
          <h1>One source document. Four scholarly formats.</h1>
          <p>An offline-first content pipeline that turns a long technical document into a structured
          study guide, a ten-slide academic deck, an A4 infographic and a refined scholarly text,
          with a quality audit at every step.</p>
          <div style="margin-top:14px">
            <span class="pill">Phase 1 · Summarise</span>
            <span class="pill">Phase 2 · Present</span>
            <span class="pill">Phase 3 · Visualise</span>
            <span class="pill">Phase 4 · Refine</span>
          </div>
          <div class="meta">TEGUIA FRANK · UID 26MCA20153 · 26CAP-608 · Chandigarh University</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def phase_cards():
    cards = [
        ("PHASE 01", "Summarisation & Structuring",
         "TF-IDF extractive ranking, topic clustering, glossary mining and an exam-oriented question bank."),
        ("PHASE 02", "Presentation Deck",
         "A designed 16:9 deck with ten slides, comparison tables, a SUIT process flow and a timeline."),
        ("PHASE 03", "Visual Infographic",
         "A print-ready A4 poster with problem statistics, cause-effect mapping and stakeholder actions."),
        ("PHASE 04", "Scholarly Refinement",
         "Formal-tone rewriting, citation insertion, readability measurement and a peer-review audit."),
    ]
    cols = st.columns(4)
    for col, (num, title, body) in zip(cols, cards):
        with col:
            st.markdown(
                f'<div class="card"><div class="num">{num}</div><h4>{title}</h4><p>{body}</p></div>',
                unsafe_allow_html=True,
            )


def metric_row(result: RunResult):
    stats = result.guide.stats
    cols = st.columns(5)
    values = [
        (f"{result.source.pages}", "Source pages"),
        (f"{stats['summary_words']:,}", "Study-guide words"),
        ("10", "Designed slides"),
        (f"{result.refinement.audit_score:.0f}%", "Audit score"),
        (f"{sum(result.timings.values()):.1f}s", "Pipeline time"),
    ]
    for col, (v, l) in zip(cols, values):
        with col:
            st.markdown(f'<div class="metric"><div class="v">{v}</div><div class="l">{l}</div></div>',
                        unsafe_allow_html=True)


def run_with_progress(source, meta):
    bar = st.progress(0.0)
    status = st.status("Starting the content pipeline…", expanded=True)

    def progress(pct, msg):
        bar.progress(min(1.0, max(0.0, pct)))
        status.write(msg)

    try:
        result = run_pipeline(source, meta, progress=progress)
        status.update(label="Content bundle generated", state="complete", expanded=False)
        bar.progress(1.0)
        st.session_state["result"] = result
        st.session_state["run_id"] = time.time()
        return result
    except Exception as exc:  # pragma: no cover - UI guard
        status.update(label="Pipeline failed", state="error", expanded=True)
        st.exception(exc)
        return None


def sidebar():
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding:6px 0 18px 0">
              <div style="font-size:.68rem;letter-spacing:.2em;color:#7FD1CE;font-weight:800">CONTENT STUDIO</div>
              <div style="font-size:1.18rem;font-weight:800;color:#fff;margin-top:3px">IoT Edition</div>
              <div style="font-size:.74rem;color:#9FB6C8;margin-top:5px">Streamlit · Python 3.13</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("##### 1 · Source document")
        source_mode = st.radio(
            "Choose an input",
            ["Built-in Inria White Book", "Upload PDF / DOCX / TXT"],
            label_visibility="collapsed",
        )
        uploaded = None
        if source_mode == "Upload PDF / DOCX / TXT":
            uploaded = st.file_uploader(
                "Upload a source", type=["pdf", "docx", "txt", "md"],
                help="The pipeline works best with 1,000+ words of technical prose.",
            )
        st.caption("Built-in source: Inria White Book No. 05, 92 pages, November 2021.")

        st.markdown("##### 2 · Author metadata")
        with st.expander("Edit metadata", expanded=False):
            author = st.text_input("Author", DEFAULT_AUTHOR)
            uid = st.text_input("UID", DEFAULT_UID)
            course = st.text_input("Subject code", DEFAULT_COURSE)
            institution = st.text_input("Institution", DEFAULT_INSTITUTION)
            title = st.text_input("Topic title", DEFAULT_TITLE)
        if "author" not in locals():
            author, uid, course, institution, title = (
                DEFAULT_AUTHOR, DEFAULT_UID, DEFAULT_COURSE, DEFAULT_INSTITUTION, DEFAULT_TITLE,
            )

        st.markdown("##### 3 · Generate")
        disabled = source_mode.startswith("Upload") and uploaded is None
        if st.button("◈  Generate content bundle", type="primary", use_container_width=True, disabled=disabled):
            meta = ProjectMeta(
                author=author, uid=uid, course=course, institution=institution, title=title,
            )
            if uploaded is not None:
                suffix = Path(uploaded.name).suffix or ".pdf"
                temp = Path(tempfile.gettempdir()) / f"uploaded_source{suffix}"
                temp.write_bytes(uploaded.getvalue())
                source = temp
            else:
                source = SAMPLE_PDF
            run_with_progress(source, meta)

        st.markdown("---")
        st.caption("All processing is local. No source text leaves this machine.")
        st.caption("v1.0 · 4 phases · 8 export formats")


def dashboard(result: RunResult):
    metric_row(result)
    st.write("")
    left, right = st.columns([1.55, 1])
    with left:
        st.markdown('<div class="section-title">Pipeline performance</div>', unsafe_allow_html=True)
        timing = pd.DataFrame(
            {"Phase": ["Extraction", "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Export"],
             "Seconds": [result.timings.get(k, 0) for k in
                         ("extraction", "phase1", "phase2", "phase3", "phase4", "export")]}
        )
        st.bar_chart(timing.set_index("Phase"), color=TEAL, height=250)
        st.markdown(
            f'<div class="small">Source: <b>{result.source.title}</b> · '
            f'{result.source.words:,} words · {result.source.pages} pages</div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown('<div class="section-title">Bundle contents</div>', unsafe_allow_html=True)
        manifest = load_manifest(result.run_dir)
        rows = [
            ("Study guide", "DOCX + Markdown", "Phase 1"),
            ("Presentation", "10-slide PPTX", "Phase 2"),
            ("Infographic", "A4 PNG + PDF", "Phase 3"),
            ("Refinement", "DOCX + Markdown", "Phase 4"),
            ("Archive", "ZIP bundle", "All"),
        ]
        st.dataframe(pd.DataFrame(rows, columns=["Deliverable", "Format", "Phase"]),
                     hide_index=True, use_container_width=True, height=230)
    st.write("")
    st.markdown('<div class="section-title">Generated outputs</div>', unsafe_allow_html=True)
    phase_cards()


def phase1_tab(result: RunResult):
    stats = result.guide.stats
    c1, c2, c3, c4 = st.columns(4)
    for col, (v, l) in zip([c1, c2, c3, c4], [
        (stats["topics"], "Core topics"),
        (stats["definitions"], "Glossary terms"),
        (stats["questions"], "Exam questions"),
        (stats["matrix_rows"], "Research fields"),
    ]):
        with col:
            st.markdown(f'<div class="metric"><div class="v">{v}</div><div class="l">{l}</div></div>',
                        unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([2.1, 1])
    with left:
        with st.container(border=True, height=560):
            st.markdown(result.guide.markdown)
    with right:
        st.markdown('<div class="section-title">Download</div>', unsafe_allow_html=True)
        for key, label, mime in [
            ("study_guide_docx", "Study guide · DOCX",
             "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            ("study_guide_md", "Study guide · Markdown", "text/markdown"),
        ]:
            p = result.file(key)
            st.download_button(label, p.read_bytes(), file_name=p.name, mime=mime,
                               use_container_width=True)
        st.write("")
        st.markdown('<div class="section-title">Extracted keywords</div>', unsafe_allow_html=True)
        for kw in result.guide.keywords:
            st.markdown(f'<span class="badge ok" style="margin:3px 4px 3px 0">{kw}</span>',
                        unsafe_allow_html=True)
        st.write("")
        st.markdown('<div class="section-title">Compression</div>', unsafe_allow_html=True)
        st.progress(min(1.0, stats["compression_ratio"] / 20))
        st.caption(f'{stats["summary_words"]:,} words from {stats["source_words"]:,} '
                   f'({stats["compression_ratio"]}% of the source).')


def phase2_tab(result: RunResult):
    from pptx import Presentation
    prs = Presentation(result.file("deck_pptx"))
    st.markdown('<div class="section-title">Deck storyboard · 10 slides · 16:9</div>',
                unsafe_allow_html=True)
    for row in range(2):
        cols = st.columns(5)
        for col in range(5):
            i = row * 5 + col
            if i >= len(prs.slides):
                break
            slide = prs.slides[i]
            texts = [s.text_frame.text.strip() for s in slide.shapes
                     if s.has_text_frame and s.text_frame.text.strip()]
            title = texts[1] if len(texts) > 1 else f"Slide {i+1}"
            body = next((t for t in texts if t not in title and len(t) > 50), "")
            with cols[col]:
                st.markdown(
                    f"""<div class="card" style="min-height:190px">
                    <div class="num">SLIDE {i+1:02d}</div>
                    <h4 style="font-size:.88rem">{title[:58]}</h4>
                    <p>{body[:120]}{'…' if len(body)>120 else ''}</p></div>""",
                    unsafe_allow_html=True,
                )
    st.write("")
    c1, c2 = st.columns([1, 2])
    with c1:
        p = result.file("deck_pptx")
        st.download_button("Download deck · PPTX", p.read_bytes(), file_name=p.name,
                           mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                           use_container_width=True)
    with c2:
        st.info("Every slide includes speaker notes with a visual-design suggestion, as required by the Phase 2 prompt.")
    st.markdown('<div class="section-title">Speaker notes</div>', unsafe_allow_html=True)
    for i, slide in enumerate(prs.slides, 1):
        note = slide.notes_slide.notes_text_frame.text.strip()
        if note:
            st.markdown(f"**{i:02d}.** {note}")


def phase3_tab(result: RunResult):
    left, right = st.columns([1.35, 1])
    with left:
        st.image(str(result.file("poster_png")), use_container_width=True)
    with right:
        st.markdown('<div class="section-title">A4 academic infographic</div>', unsafe_allow_html=True)
        st.caption("1654 × 2339 px · 200 dpi · print-ready A4 portrait")
        st.markdown(
            """
            **Sections generated**
            1. The problem, with three evidence cards
            2. Causes → consequences mapping
            3. Four sustainable technical solutions
            4. Stakeholder action plan
            5. Key takeaway and author footer
            """
        )
        for key, label, mime in [
            ("poster_png", "Download poster · PNG", "image/png"),
            ("poster_pdf", "Download poster · PDF", "application/pdf"),
        ]:
            p = result.file(key)
            st.download_button(label, p.read_bytes(), file_name=p.name, mime=mime,
                               use_container_width=True)
        st.write("")
        st.markdown('<div class="section-title">Design tokens</div>', unsafe_allow_html=True)
        cols = st.columns(5)
        for col, (name, color) in zip(cols, [("Navy", NAVY), ("Teal", TEAL), ("Amber", AMBER),
                                             ("Slate", SLATE), ("Mist", "#EEF3F6")]):
            with col:
                st.markdown(
                    f'<div style="height:34px;background:{color};border-radius:7px"></div>'
                    f'<div class="small" style="margin-top:4px">{name}</div>',
                    unsafe_allow_html=True,
                )


def phase4_tab(result: RunResult):
    ref = result.refinement
    c1, c2, c3, c4 = st.columns(4)
    for col, (v, l) in zip([c1, c2, c3, c4], [
        (ref.audit_score, "Audit score"),
        (len(ref.glossary), "Glossary terms"),
        (ref.metrics_after["avg_sentence_length"], "Avg. sentence length"),
        (ref.metrics_after["lexical_density"], "Lexical density (%)"),
    ]):
        with col:
            st.markdown(f'<div class="metric"><div class="v">{v}</div><div class="l">{l}</div></div>',
                        unsafe_allow_html=True)
    st.write("")
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="section-title">Before · source summary</div>', unsafe_allow_html=True)
        st.info(ref.original)
        st.caption(f"Flesch reading ease {ref.metrics_before['flesch_reading_ease']} · "
                   f"{ref.metrics_before['words']} words")
    with right:
        st.markdown('<div class="section-title">After · refined abstract</div>', unsafe_allow_html=True)
        st.success(ref.refined)
        st.caption(f"Flesch reading ease {ref.metrics_after['flesch_reading_ease']} · "
                   f"{ref.metrics_after['words']} words")
    st.write("")
    st.markdown('<div class="section-title">Peer-review audit</div>', unsafe_allow_html=True)
    df = pd.DataFrame([{"Criterion": r.criterion, "Status": r.status, "Evidence": r.evidence}
                       for r in ref.audit])
    st.dataframe(df, hide_index=True, use_container_width=True)
    p = result.file("refinement_docx")
    st.download_button("Download refinement · DOCX", p.read_bytes(), file_name=p.name,
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                       use_container_width=False)


def downloads_tab(result: RunResult):
    st.markdown('<div class="section-title">Complete content bundle</div>', unsafe_allow_html=True)
    st.caption(f"Generated {result.generated} · {result.run_dir}")
    labels = {
        "study_guide_docx": ("Comprehensive study guide", "DOCX"),
        "study_guide_md": ("Comprehensive study guide", "Markdown"),
        "deck_pptx": ("Academic presentation", "PPTX"),
        "poster_png": ("A4 infographic", "PNG"),
        "poster_pdf": ("A4 infographic", "PDF"),
        "refinement_docx": ("Academic refinement", "DOCX"),
        "refinement_md": ("Academic refinement", "Markdown"),
        "manifest": ("Run manifest", "JSON"),
    }
    mimes = {
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "md": "text/markdown", "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "png": "image/png", "pdf": "application/pdf", "json": "application/json",
    }
    for key, (label, fmt) in labels.items():
        p = result.file(key)
        c1, c2, c3 = st.columns([3, 2, 1.3])
        with c1:
            st.markdown(f"**{label}**")
            st.caption(p.name)
        with c2:
            st.caption(f"{p.stat().st_size/1024:.0f} KB · {fmt}")
        with c3:
            st.download_button("Download", p.read_bytes(), file_name=p.name,
                               mime=mimes.get(p.suffix.lstrip("."), "application/octet-stream"),
                               key=f"dl_{key}", use_container_width=True)
    st.write("")
    bundle = result.file("bundle_zip")
    st.download_button("⬇  Download everything · ZIP bundle", bundle.read_bytes(),
                       file_name=bundle.name, mime="application/zip", type="primary",
                       use_container_width=True)


def about_tab():
    st.markdown(
        """
        ### How the pipeline works
        The system is intentionally deterministic and offline: every sentence it reports can be traced
        back to the uploaded source. That makes the outputs reproducible and safe to submit.

        | Phase | Technique | Output |
        |---|---|---|
        | 1 | TF-IDF sentence ranking, MMR-style diversity, definition mining, template question generation | Study guide (DOCX/MD) |
        | 2 | Structured slide plan, python-pptx vector layouts, speaker notes | 10-slide deck (PPTX) |
        | 3 | Pillow composition, A4 grid system, evidence cards, cause-effect map | Poster (PNG/PDF) |
        | 4 | Rule-based formalisation, citation insertion, readability metrics, audit checklist | Refined text (DOCX/MD) |

        ### Run locally
        ```bash
        pip install -r requirements.txt
        streamlit run app.py
        ```
        ### Deploy
        Push the folder to GitHub and create a Streamlit Community Cloud app with `app.py`
        as the entry point. No API key is required.
        """
    )


def main():
    sidebar()
    hero()
    result: RunResult | None = st.session_state.get("result")

    if result is None:
        phase_cards()
        st.write("")
        st.info("Choose the built-in Inria white book in the sidebar, then press **Generate content bundle**.")
        st.markdown('<div class="section-title">What you will get</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        for col, (v, l) in zip(cols, [("4", "Academic formats"), ("10", "Slides"), ("A4", "Poster"),
                                      ("100%", "Local processing")]):
            with col:
                st.markdown(f'<div class="metric"><div class="v">{v}</div><div class="l">{l}</div></div>',
                            unsafe_allow_html=True)
        return

    tabs = st.tabs(["  Dashboard  ", "  Phase 1 · Notes  ", "  Phase 2 · Slides  ",
                    "  Phase 3 · Poster  ", "  Phase 4 · Refinement  ", "  Downloads  ", "  About  "])
    with tabs[0]:
        dashboard(result)
    with tabs[1]:
        phase1_tab(result)
    with tabs[2]:
        phase2_tab(result)
    with tabs[3]:
        phase3_tab(result)
    with tabs[4]:
        phase4_tab(result)
    with tabs[5]:
        downloads_tab(result)
    with tabs[6]:
        about_tab()

    st.markdown(
        f'<div style="text-align:center;color:#8A9AA6;font-size:.74rem;margin-top:26px">'
        f'AI-Assisted Multi-Format Content Studio · {DEFAULT_AUTHOR} · {DEFAULT_UID}</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
