"""End-to-end orchestration of the four content phases."""

from __future__ import annotations

import json
import shutil
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable

from .config import DEFAULT_TITLE, OUTPUT_DIR, ProjectMeta
from .exporters import export_bundle, export_refinement, export_study_guide
from .extract import SourceDocument, load_document
from .phase1_notes import StudyGuide, generate_study_guide
from .phase2_slides import generate_deck
from .phase3_infographic import generate_poster
from .phase4_refine import RefinementResult, generate_refinement

Progress = Callable[[float, str], None]


@dataclass
class RunResult:
    run_dir: Path
    source: SourceDocument
    guide: StudyGuide
    refinement: RefinementResult
    files: dict[str, str] = field(default_factory=dict)
    timings: dict[str, float] = field(default_factory=dict)
    generated: str = ""

    def file(self, key: str) -> Path:
        return self.run_dir / self.files[key]


def _noop(_pct: float, _msg: str) -> None:
    return None


def run_pipeline(
    source_path: str | Path,
    meta: ProjectMeta | None = None,
    out_root: str | Path | None = None,
    progress: Progress | None = None,
    run_name: str | None = None,
) -> RunResult:
    """Run extraction, Phase 1-4 and all exporters, returning a manifest."""
    progress = progress or _noop
    meta = meta or ProjectMeta()
    source_path = Path(source_path)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(out_root or OUTPUT_DIR) / (run_name or f"run_{stamp}")
    run_dir.mkdir(parents=True, exist_ok=True)
    timings: dict[str, float] = {}

    progress(0.03, "Reading and cleaning the source document")
    t0 = time.perf_counter()
    doc = load_document(source_path, fallback_title=meta.title or DEFAULT_TITLE)
    timings["extraction"] = round(time.perf_counter() - t0, 2)

    progress(0.18, "Phase 1 - summarising and structuring study notes")
    t0 = time.perf_counter()
    guide = generate_study_guide(doc, meta)
    timings["phase1"] = round(time.perf_counter() - t0, 2)

    progress(0.45, "Phase 2 - composing the ten-slide academic deck")
    t0 = time.perf_counter()
    deck_path = generate_deck(guide, meta, run_dir / "IoT_Foundations_Deck.pptx")
    timings["phase2"] = round(time.perf_counter() - t0, 2)

    progress(0.62, "Phase 3 - synthesising the A4 infographic poster")
    t0 = time.perf_counter()
    poster_path = generate_poster(guide, meta, run_dir / "IoT_Academic_Infographic.png")
    timings["phase3"] = round(time.perf_counter() - t0, 2)

    progress(0.78, "Phase 4 - refining scholarly tone and auditing quality")
    t0 = time.perf_counter()
    refinement = generate_refinement(guide, meta)
    timings["phase4"] = round(time.perf_counter() - t0, 2)

    progress(0.88, "Exporting DOCX, Markdown and archive files")
    t0 = time.perf_counter()
    guide_md = run_dir / "Comprehensive_Study_Guide.md"
    guide_md.write_text(guide.to_markdown(), encoding="utf-8")
    guide_docx = export_study_guide(guide, meta, run_dir / "Comprehensive_Study_Guide.docx")
    refine_md = run_dir / "Phase4_Academic_Refinement.md"
    refine_md.write_text(refinement.markdown, encoding="utf-8")
    refine_docx = export_refinement(refinement, meta, run_dir / "Phase4_Academic_Refinement.docx")

    core_files = [
        guide_docx, guide_md, deck_path, poster_path,
        poster_path.with_suffix(".pdf"), refine_docx, refine_md,
    ]
    bundle = export_bundle(core_files, run_dir / "IoT_Content_Bundle.zip")
    timings["export"] = round(time.perf_counter() - t0, 2)

    files = {
        "study_guide_docx": guide_docx.name,
        "study_guide_md": guide_md.name,
        "deck_pptx": deck_path.name,
        "poster_png": poster_path.name,
        "poster_pdf": poster_path.with_suffix(".pdf").name,
        "refinement_docx": refine_docx.name,
        "refinement_md": refine_md.name,
        "bundle_zip": bundle.name,
    }

    manifest = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "source": {
            "file": source_path.name,
            "title": doc.title,
            "pages": doc.pages,
            "words": doc.words,
            "characters": len(doc.text),
            "sections_detected": len(doc.sections),
        },
        "meta": {
            "author": meta.author, "uid": meta.uid, "course": meta.course,
            "title": meta.title, "institution": meta.institution,
        },
        "phases": {
            "phase1": {
                "name": "Summarisation and structuring",
                "stats": guide.stats,
                "topics": [t.title for t in guide.topics],
                "keywords": guide.keywords,
            },
            "phase2": {
                "name": "Presentation deck generation",
                "slides": 10,
                "file": deck_path.name,
                "bytes": deck_path.stat().st_size,
            },
            "phase3": {
                "name": "Visual infographic synthesis",
                "file": poster_path.name,
                "width": 1654, "height": 2339, "dpi": 200,
                "bytes": poster_path.stat().st_size,
            },
            "phase4": {
                "name": "Scholarly writing refinement",
                "metrics_before": refinement.metrics_before,
                "metrics_after": refinement.metrics_after,
                "changes": refinement.changes,
                "audit_score": refinement.audit_score,
                "glossary_terms": len(refinement.glossary),
            },
        },
        "timings_seconds": timings,
        "total_seconds": round(sum(timings.values()), 2),
        "files": files,
    }
    manifest_path = run_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    files["manifest"] = manifest_path.name

    progress(1.0, "Content bundle complete")
    return RunResult(
        run_dir=run_dir,
        source=doc,
        guide=guide,
        refinement=refinement,
        files=files,
        timings=timings,
        generated=manifest["generated"],
    )


def load_manifest(run_dir: str | Path) -> dict:
    path = Path(run_dir) / "manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))
