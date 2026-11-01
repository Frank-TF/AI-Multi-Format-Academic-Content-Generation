"""Generate the report figures from the demo run and the Streamlit screenshots."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "report" / "figures"
RUN = ROOT / "outputs" / "demo_run"
MANIFEST = json.loads((RUN / "manifest.json").read_text(encoding="utf-8"))

NAVY = "#13294B"
NAVY2 = "#1F3D5C"
TEAL = "#0F8B8D"
TEAL_L = "#7FD1CE"
AMBER = "#E9A23B"
SLATE = "#5B6770"
MIST = "#EEF3F6"
LINE = "#D8E2E9"
INK = "#1A1A1A"

plt.rcParams.update({
    "font.family": "Segoe UI",
    "font.size": 8.5,
    "axes.edgecolor": LINE,
    "axes.labelcolor": SLATE,
    "text.color": INK,
    "xtick.color": SLATE,
    "ytick.color": SLATE,
    "figure.dpi": 200,
    "savefig.dpi": 200,
})


def rounded(ax, x, y, w, h, fc, ec="none", lw=0.8, radius=0.025, z=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                       facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z)
    ax.add_patch(p)
    return p


def arrow(ax, a, b, color=TEAL, lw=1.4, style="-|>", rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=9,
                                 color=color, linewidth=lw, connectionstyle=f"arc3,rad={rad}",
                                 zorder=3, shrinkA=2, shrinkB=2))


def fig_architecture():
    fig, ax = plt.subplots(figsize=(6.45, 3.55))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 56)
    ax.axis("off")

    # Column backgrounds
    rounded(ax, 1, 2, 23, 52, "#F4F7F9", LINE, radius=0.8)
    rounded(ax, 27, 2, 45, 52, "#FFFFFF", LINE, radius=0.8)
    rounded(ax, 75, 2, 24, 52, "#F4F7F9", LINE, radius=0.8)

    ax.text(2.8, 51, "I N P U T", fontsize=6.6, weight="bold", color=TEAL)
    ax.text(28.8, 51, "PYTHON PIPELINE", fontsize=6.6, weight="bold", color=TEAL)
    ax.text(76.8, 51, "DELIVERY", fontsize=6.6, weight="bold", color=TEAL)

    # Input
    rounded(ax, 4, 36, 17.5, 10, NAVY, radius=0.5)
    ax.text(12.75, 42.4, "Inria White Book", ha="center", va="center", color="white", fontsize=7.6, weight="bold")
    ax.text(12.75, 39.4, "92 pages · 24,972 words", ha="center", va="center", color="#C9D9E8", fontsize=5.9)
    rounded(ax, 4, 25, 17.5, 8.2, "#E4F2F1", TEAL, radius=0.5)
    ax.text(12.75, 30.5, "Optional upload", ha="center", va="center", color=NAVY, fontsize=7.0, weight="bold")
    ax.text(12.75, 27.6, "PDF · DOCX · TXT · MD", ha="center", va="center", color=SLATE, fontsize=5.8)
    rounded(ax, 4, 15, 17.5, 7.2, "#FDF3E3", AMBER, radius=0.5)
    ax.text(12.75, 19.4, "Author metadata", ha="center", va="center", color=NAVY, fontsize=6.8, weight="bold")
    ax.text(12.75, 16.9, "name · UID · course", ha="center", va="center", color=SLATE, fontsize=5.6)

    # Extraction
    rounded(ax, 29, 42.5, 41, 6.6, "#E8EEF4", "#B9CAD9", radius=0.4)
    ax.text(49.5, 47.1, "0 · Extraction and cleanup", ha="center", va="center", fontsize=7.2, weight="bold", color=NAVY)
    ax.text(49.5, 44.4, "PyMuPDF text layer · sentence segmentation · boilerplate filter · 204 sections",
            ha="center", va="center", fontsize=5.5, color=SLATE)

    phases = [
        ("PHASE 1", "Summarise", "TF-IDF + MMR\nstudy guide"),
        ("PHASE 2", "Present", "Slide plan +\nPPTX layout"),
        ("PHASE 3", "Visualise", "A4 grid +\nPillow poster"),
        ("PHASE 4", "Refine", "Formal rules +\naudit checklist"),
    ]
    width = 9.1
    gap = 1.7
    x0 = 29.3
    for i, (kicker, title, body) in enumerate(phases):
        x = x0 + i * (width + gap)
        rounded(ax, x, 26, width, 12.8, "#FFFFFF", "#C7D5E0", radius=0.45)
        rounded(ax, x, 35.4, width, 3.4, TEAL if i % 2 == 0 else NAVY2, radius=0.45)
        ax.text(x + width / 2, 37.1, kicker, ha="center", va="center", color="white", fontsize=5.3, weight="bold")
        ax.text(x + width / 2, 32.6, title, ha="center", va="center", color=NAVY, fontsize=7.6, weight="bold")
        ax.text(x + width / 2, 29.2, body, ha="center", va="center", color=SLATE, fontsize=5.6, linespacing=1.3)
        if i < 3:
            arrow(ax, (x + width + 0.1, 32.4), (x + width + gap - 0.15, 32.4), color=TEAL, lw=1.0)

    # Shared services
    rounded(ax, 29.3, 17.6, 20.1, 6.2, "#F4F7F9", LINE, radius=0.4)
    ax.text(39.35, 20.7, "Manifest + timings", ha="center", va="center", fontsize=6.4, weight="bold", color=NAVY)
    rounded(ax, 50.6, 17.6, 19.7, 6.2, "#F4F7F9", LINE, radius=0.4)
    ax.text(60.45, 20.7, "ZIP · DOCX · PPTX · PNG · PDF", ha="center", va="center", fontsize=5.7, weight="bold", color=NAVY)

    arrow(ax, (12.75, 36), (12.75, 33.5), color=AMBER, lw=1.0)
    arrow(ax, (18.4, 41), (28.6, 45.0), color=AMBER, lw=1.1)
    arrow(ax, (49.5, 42.3), (49.5, 39.2), color=TEAL, lw=1.1)

    # Delivery
    rounded(ax, 77.5, 33.5, 19, 10, NAVY, radius=0.5)
    ax.text(87, 39.9, "Streamlit UI", ha="center", va="center", color="white", fontsize=7.6, weight="bold")
    ax.text(87, 36.6, "live preview · downloads", ha="center", va="center", color="#C9D9E8", fontsize=5.6)
    rounded(ax, 77.5, 22.5, 19, 8.4, "#FFFFFF", "#C7D5E0", radius=0.5)
    ax.text(87, 27.9, "Eight files + manifest", ha="center", va="center", color=NAVY, fontsize=6.7, weight="bold")
    ax.text(87, 25.1, "reproducible bundle", ha="center", va="center", color=SLATE, fontsize=5.6)
    rounded(ax, 77.5, 12.6, 19, 7.4, "#E4F2F1", TEAL, radius=0.5)
    ax.text(87, 17.1, "Local by default", ha="center", va="center", color=NAVY, fontsize=6.7, weight="bold")
    ax.text(87, 14.6, "no API key · no data egress", ha="center", va="center", color=SLATE, fontsize=5.3)

    arrow(ax, (70.5, 32.4), (76.6, 37.4), color=TEAL, lw=1.1)
    arrow(ax, (87, 33.3), (87, 31.2), color=TEAL, lw=1.0)
    arrow(ax, (87, 22.3), (87, 20.2), color=TEAL, lw=1.0)

    ax.text(50, 4.6, "Deterministic, extractive generation: every sentence in the bundle can be traced to the source or to a curated domain fact.",
            ha="center", va="center", fontsize=5.7, color=SLATE, style="italic")
    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(FIG / "fig1_architecture.png", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def fig_phase1():
    stats = MANIFEST["phases"]["phase1"]["stats"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.45, 2.75), gridspec_kw={"width_ratios": [1.05, 1]})
    for ax in (a1, a2):
        ax.set_facecolor("#FFFFFF")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(axis="both", length=0)

    # Word budget
    vals = [stats["source_words"], stats["summary_words"]]
    labels = ["Source\n(92 pages)", "Study guide\n(8 sections)"]
    bars = a1.barh(labels, vals, color=[NAVY, TEAL], height=0.5)
    a1.set_xlim(0, 28500)
    a1.invert_yaxis()
    a1.set_title("Word budget", loc="left", fontsize=8.4, weight="bold", color=NAVY, pad=6)
    for b, v in zip(bars, vals):
        a1.text(v + 700, b.get_y() + b.get_height() / 2, f"{v:,}", va="center", fontsize=7.2, color=INK)
    a1.text(0.98, 0.08, f'{stats["compression_ratio"]}% of source', transform=a1.transAxes,
            ha="right", fontsize=7.2, weight="bold", color=TEAL)
    a1.set_xlabel("Words", fontsize=7)

    # Inventory
    items = ["Core topics", "Glossary terms", "Research fields", "Key facts", "Exam questions"]
    values = [stats["topics"], stats["definitions"], stats["matrix_rows"],
              stats["revision_points"], stats["questions"]]
    colors = [NAVY, TEAL, TEAL, AMBER, SLATE]
    y = np.arange(len(items))
    a2.barh(y, values, color=colors, height=0.56)
    a2.set_yticks(y, items, fontsize=7)
    a2.invert_yaxis()
    a2.set_xlim(0, 14)
    a2.set_title("Generated inventory", loc="left", fontsize=8.4, weight="bold", color=NAVY, pad=6)
    for yy, v in zip(y, values):
        a2.text(v + 0.25, yy, str(v), va="center", fontsize=7.2, weight="bold", color=INK)
    a2.set_xlabel("Items", fontsize=7)
    fig.text(0.5, -0.02, "The guide keeps 8.9% of the source words while covering four topics and twelve assessed facts.",
             ha="center", fontsize=5.8, color=SLATE, style="italic")
    fig.tight_layout(pad=0.4)
    fig.savefig(FIG / "fig2_phase1.png", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def fig_deck():
    slides = [
        ("00", "COVER", "Internet of Things:\nFoundations and Challenges"),
        ("01", "CONTEXT", "From Ubiquitous Computing\nto a Global IoT"),
        ("02", "OBJECTIVES", "Objectives of\nthe Analysis"),
        ("03", "METHOD", "A Four-Step\nEvidence Pipeline"),
        ("04", "COMPARISON", "Developed vs\nConstrained Environments"),
        ("05", "PROBLEM", "Challenges and\nSocietal Impact"),
        ("06", "PROCESS", "Secure Firmware\nUpdate Lifecycle"),
        ("07", "TIMELINE", "Evolution of IoT\nand Standards"),
        ("08", "SOLUTIONS", "Design and\nImplementation Advice"),
        ("09", "CONCLUSION", "Sovereignty\nby Design"),
    ]
    fig, ax = plt.subplots(figsize=(6.45, 3.9))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 62)
    ax.axis("off")
    w, h = 17.8, 24.5
    gx, gy = 2.1, 3.2
    for i, (num, kicker, title) in enumerate(slides):
        row, col = divmod(i, 5)
        x = 1.6 + col * (w + gx)
        y = 33.5 - row * (h + gy)
        rounded(ax, x, y, w, h, "#FFFFFF", "#CBD8E2", radius=0.6)
        rounded(ax, x, y + h - 5.2, w, 5.2, NAVY if i == 0 else (TEAL if i % 2 else NAVY2), radius=0.6)
        ax.text(x + 1.5, y + h - 2.6, f"{num}  {kicker}", va="center", fontsize=5.3,
                color="white", weight="bold")
        ax.text(x + 1.5, y + h - 9.0, title, va="top", fontsize=5.9, color=NAVY, weight="bold",
                wrap=True, linespacing=1.3)
        # Abstract content lines
        for k in range(3):
            yy = y + 6.8 - k * 2.2
            ax.add_patch(Rectangle((x + 1.5, yy), w - 3.0 - (k % 2) * 2.6, 0.75,
                                   facecolor="#E3EAEF", edgecolor="none"))
        ax.text(x + 1.5, y + 2.2, "speaker note", fontsize=4.6, color=TEAL, style="italic")
    ax.text(50, 61.2, "Ten-slide academic deck · 16:9 · every slide carries a speaker note and a visual suggestion",
            ha="center", va="top", fontsize=6.2, color=SLATE)
    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(FIG / "fig3_deck.png", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def fig_eval():
    timings = MANIFEST["timings_seconds"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.45, 2.55), gridspec_kw={"width_ratios": [1.55, 1]})
    for ax in (a1, a2):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(length=0)

    names = ["Extract", "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Export"]
    keys = ["extraction", "phase1", "phase2", "phase3", "phase4", "export"]
    vals = [timings.get(k, 0) for k in keys]
    colors = [SLATE, TEAL, NAVY2, NAVY2, NAVY2, AMBER]
    bars = a1.bar(names, vals, color=colors, width=0.62)
    a1.set_ylim(0, 12.2)
    a1.set_title("Runtime profile (seconds)", loc="left", fontsize=8.2, weight="bold", color=NAVY, pad=6)
    for b, v in zip(bars, vals):
        a1.text(b.get_x() + b.get_width() / 2, v + 0.28, f"{v:.2f}", ha="center", fontsize=6.6, color=INK)
    a1.set_ylabel("Seconds", fontsize=7)
    a1.tick_params(axis="x", labelsize=6.8)

    verified, total = 5, 6
    a2.pie([verified, total - verified], colors=[TEAL, "#E9EEF3"], startangle=90,
           counterclock=False, wedgeprops=dict(width=0.30, edgecolor="white", linewidth=1.5))
    a2.text(0, 0.10, f"{MANIFEST['phases']['phase4']['audit_score']:.0f}%", ha="center", va="center",
            fontsize=15, weight="bold", color=NAVY)
    a2.text(0, -0.24, "audit score", ha="center", va="center", fontsize=6.0, color=SLATE)
    a2.set_title("Peer-review checklist", loc="center", fontsize=8.2, weight="bold", color=NAVY, pad=4)
    a2.text(0, -1.28, "5 verified · 1 partially verified", ha="center", fontsize=5.9, color=SLATE)
    fig.tight_layout(pad=0.5)
    fig.savefig(FIG / "fig6_evaluation.png", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def poster_preview():
    src = Image.open(RUN / "IoT_Academic_Infographic.png").convert("RGB")
    src.thumbnail((900, 1273), Image.LANCZOS)
    canvas = Image.new("RGB", (src.width + 16, src.height + 16), "#FFFFFF")
    canvas.paste(src, (8, 8))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([7, 7, canvas.width - 8, canvas.height - 8], outline="#C7D5E0", width=2)
    canvas.save(FIG / "fig4_poster.png", optimize=True)
    print("poster preview", canvas.size)


def app_composite():
    home = Image.open(FIG / "streamlit_home.png").convert("RGB")
    dash = Image.open(FIG / "streamlit_dashboard.png").convert("RGB")

    def crop(im, top=0, bottom=None):
        w, h = im.size
        return im.crop((0, top, w, bottom or h))

    # Keep the informative upper part of each view (hero, metrics, phase tabs).
    home = crop(home, 90, 930)
    dash = crop(dash, 90, 930)
    width = 720
    home = home.resize((width, int(home.height * width / home.width)), Image.LANCZOS)
    dash = dash.resize((width, int(dash.height * width / dash.width)), Image.LANCZOS)
    gap = 16
    canvas = Image.new("RGB", (home.width + dash.width + gap + 2,
                                max(home.height, dash.height) + 2), "#FFFFFF")
    canvas.paste(home, (1, 1))
    canvas.paste(dash, (home.width + gap + 1, 1))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, canvas.width - 2, canvas.height - 2], outline="#C7D5E0", width=2)
    canvas.save(FIG / "fig5_app.png", optimize=True)
    print("app composite", canvas.size)


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    fig_architecture()
    fig_phase1()
    fig_deck()
    fig_eval()
    poster_preview()
    app_composite()
    for p in sorted(FIG.glob("fig*.png")):
        print(p.name, p.stat().st_size)


if __name__ == "__main__":
    main()
