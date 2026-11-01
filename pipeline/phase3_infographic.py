"""Phase 3 - A4 academic infographic synthesis with Pillow.

The poster is generated programmatically so that every number and label is
traceable to the Phase 1 evidence base.  It is exported as PNG and PDF.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .config import AMBER, INK, MIST, NAVY, NAVY_2, SLATE, TEAL, TEAL_LIGHT, WHITE, ProjectMeta
from .domain import IOT_SOLUTIONS, IOT_STAKEHOLDERS, IOT_TAKEAWAY
from .phase1_notes import StudyGuide

W, H = 1654, 2339  # A4 at 200 dpi
M = 76


def _rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


NAVY_C, NAVY2_C, TEAL_C, TEALL_C = _rgb(NAVY), _rgb(NAVY_2), _rgb(TEAL), _rgb(TEAL_LIGHT)
AMBER_C, SLATE_C, MIST_C, WHITE_C, INK_C = _rgb(AMBER), _rgb(SLATE), _rgb(MIST), _rgb(WHITE), _rgb(INK)


def _font(size: int, bold: bool = False, serif: bool = False) -> ImageFont.FreeTypeFont:
    candidates = []
    if serif:
        candidates = ["timesbd.ttf" if bold else "times.ttf", "georgiab.ttf" if bold else "georgia.ttf"]
    else:
        candidates = ["seguisb.ttf" if bold else "segoeui.ttf", "arialbd.ttf" if bold else "arial.ttf"]
    for name in candidates:
        for base in (r"C:\Windows\Fonts", "/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/truetype/liberation"):
            p = Path(base) / name
            if p.exists():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def _text(draw, xy, text, font, fill, max_width=None, line_gap=1.15, align="left"):
    x, y = xy
    lines = _wrap(draw, text, font, max_width) if max_width else [text]
    lh = int(font.size * line_gap)
    for line in lines:
        if align == "center":
            draw.text((x - draw.textlength(line, font=font) / 2, y), line, font=font, fill=fill)
        else:
            draw.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def _rounded(draw, box, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _circle_num(draw, x, y, n, color=TEAL_C, r=18, fg=WHITE_C):
    draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
    f = _font(18, True)
    draw.text((x, y), str(n), font=f, fill=fg, anchor="mm")


class PosterBuilder:
    def __init__(self, guide: StudyGuide, meta: ProjectMeta):
        self.guide = guide
        self.meta = meta
        self.img = Image.new("RGB", (W, H), WHITE)
        self.d = ImageDraw.Draw(self.img)

    # ------------------------------------------------------------- sections --
    def header(self) -> int:
        d = self.d
        d.rectangle((0, 0, W, 500), fill=NAVY_C)
        d.rectangle((0, 500, W, 512), fill=TEAL_C)
        _text(d, (M, 62), "ACADEMIC INFOGRAPHIC  ·  " + self.meta.course, _font(20, True), TEALL_C)
        y = _text(d, (M, 112), self.guide.title, _font(50, True), WHITE, max_width=980, line_gap=1.03)
        _text(d, (M, y + 14), "Societal challenges, technical constraints and research fields for a sustainable IoT",
              _font(22), TEALL_C, max_width=960)
        _text(d, (M, 430), f"{self.meta.author}  |  UID: {self.meta.uid}  |  {self.meta.institution}",
              _font(18, True), WHITE)
        self._chart(1120, 92, 458, 330)
        return 556

    def _chart(self, x, y, w, h):
        d = self.d
        _rounded(d, (x, y, x + w, y + h), 18, WHITE)
        _text(d, (x + 24, y + 18), "THE TIPPING POINT", _font(15, True), TEAL_C)
        _text(d, (x + 24, y + 42), "Share of IoT among connected devices", _font(13), SLATE_C, max_width=w - 48)
        base_y = y + h - 58
        bars = [("2010", 10, 0.10), ("2020", 55, 1.0)]
        for i, (label, pct, frac) in enumerate(bars):
            bx = x + 52 + i * 160
            bh = int(150 * frac)
            d.rounded_rectangle((bx, base_y - bh, bx + 78, base_y), radius=8,
                                fill=TEAL_C if i else SLATE_C)
            d.text((bx + 39, base_y - bh - 24), f"{pct}%", font=_font(17, True), fill=NAVY_C, anchor="mm")
            d.text((bx + 39, base_y + 14), label, font=_font(13, True), fill=SLATE_C, anchor="mm")
        d.line((x + 36, base_y + 1, x + w - 26, base_y + 1), fill="#C9D6DE", width=2)
        d.text((x + w - 28, base_y - 168), "10 bn", font=_font(20, True), fill=AMBER_C, anchor="rm")
        d.text((x + w - 28, base_y - 144), "devices", font=_font(11), fill=SLATE_C, anchor="rm")

    def problem(self, y: int) -> int:
        d = self.d
        _text(d, (M, y), "01  THE PROBLEM", _font(24, True), TEAL_C)
        cards = [
            ("~10 bn", "IoT devices installed worldwide by 2020, a tenfold decade of growth."),
            ("50%+", "of all connected devices are now IoT, so failures reach the physical world."),
            ("0.001%", "of a conventional memory budget is available on some constrained nodes."),
        ]
        cw = (W - 2 * M - 2 * 26) // 3
        for i, (big, small) in enumerate(cards):
            x = M + i * (cw + 26)
            _rounded(d, (x, y + 40, x + cw, y + 278), 16, MIST_C, "#D6E2E8")
            d.rectangle((x, y + 40, x + cw, y + 48), fill=AMBER_C if i == 1 else TEAL_C)
            d.text((x + 26, y + 70), big, font=_font(44, True), fill=NAVY_C)
            _text(d, (x + 26, y + 132), small, _font(16), INK_C, max_width=cw - 52, line_gap=1.12)
        return y + 300

    def causes(self, y: int) -> int:
        d = self.d
        _text(d, (M, y), "02  CAUSES  →  CONSEQUENCES", _font(24, True), TEAL_C)
        top = y + 42
        h = 430
        _rounded(d, (M, top, W // 2 - 40, top + h), 16, "#F7FAFB", "#D6E2E8")
        _rounded(d, (W // 2 + 40, top, W - M, top + h), 16, "#F7FAFB", "#D6E2E8")
        _text(d, (M + 26, top + 18), "ROOT CAUSES", _font(15, True), NAVY_C)
        _text(d, (W // 2 + 66, top + 18), "CONSEQUENCES", _font(15, True), NAVY_C)
        causes = [
            ("Resource limits", "MicroWatt energy, kilobytes of RAM, slow CPUs"),
            ("Insecure updates", "Long-lived firmware without signed manifests"),
            ("Pervasive sensing", "Continuous collection of behavioural data"),
            ("Fragmented standards", "Vendor lock-in and non-interoperable stacks"),
        ]
        effects = [
            ("Weak defences", "Conventional cryptography does not fit"),
            ("Cyber-physical harm", "Compromised devices can actuate the real world"),
            ("Privacy erosion", "Surveillance and behavioural monetisation"),
            ("E-waste and dependency", "Short lifetimes and foreign supply chains"),
        ]
        for i in range(4):
            cy = top + 60 + i * 88
            _circle_num(d, M + 46, cy + 12, i + 1, TEAL_C)
            _text(d, (M + 76, cy), causes[i][0], _font(16, True), NAVY_C)
            _text(d, (M + 76, cy + 24), causes[i][1], _font(13), SLATE_C, max_width=500)
            d.line((W // 2 - 34, cy + 12, W // 2 + 30, cy + 12), fill=AMBER_C, width=3)
            d.polygon([(W // 2 + 30, cy + 6), (W // 2 + 40, cy + 12), (W // 2 + 30, cy + 18)], fill=AMBER_C)
            _circle_num(d, W // 2 + 66, cy + 12, i + 1, AMBER_C)
            _text(d, (W // 2 + 96, cy), effects[i][0], _font(16, True), NAVY_C)
            _text(d, (W // 2 + 96, cy + 24), effects[i][1], _font(13), SLATE_C, max_width=500)
        return top + h + 34

    def solutions(self, y: int) -> int:
        d = self.d
        _text(d, (M, y), "03  SUSTAINABLE & TECHNICAL SOLUTIONS", _font(24, True), TEAL_C)
        top = y + 42
        cw = (W - 2 * M - 26) // 2
        ch = 168
        for i, (title, detail) in enumerate(IOT_SOLUTIONS):
            col, row = i % 2, i // 2
            x = M + col * (cw + 26)
            yy = top + row * (ch + 18)
            _rounded(d, (x, yy, x + cw, yy + ch), 14, WHITE, "#CBD9E1")
            d.rectangle((x, yy, x + 8, yy + ch), fill=TEAL_C if i % 2 == 0 else AMBER_C)
            _circle_num(d, x + 42, yy + 34, i + 1, TEAL_C if i % 2 == 0 else AMBER_C)
            _text(d, (x + 68, yy + 20), title, _font(18, True), NAVY_C)
            _text(d, (x + 24, yy + 62), detail, _font(14), SLATE_C, max_width=cw - 48, line_gap=1.12)
            if i == 3:
                _text(d, (x + 24, yy + 120), "Open standards · vendor independence", _font(12, True), TEAL_C)
        return top + 2 * ch + 18 + 34

    def stakeholders(self, y: int) -> int:
        d = self.d
        _text(d, (M, y), "04  ACTION PLAN BY STAKEHOLDER", _font(24, True), TEAL_C)
        top = y + 42
        rowh = 88
        for i, (who, action) in enumerate(IOT_STAKEHOLDERS):
            yy = top + i * (rowh + 10)
            _rounded(d, (M, yy, W - M, yy + rowh), 12, MIST_C if i % 2 == 0 else WHITE, "#D6E2E8")
            d.rectangle((M, yy, M + 10, yy + rowh), fill=[NAVY_C, TEAL_C, AMBER_C, SLATE_C][i])
            _text(d, (M + 28, yy + 20), who, _font(15, True), NAVY_C)
            _text(d, (M + 420, yy + 20), action, _font(14), SLATE_C, max_width=W - 2 * M - 450)
        return top + 4 * (rowh + 10) + 24

    def footer(self, y: int):
        d = self.d
        _rounded(d, (M, y, W - M, y + 108), 16, NAVY_C)
        _text(d, (M + 30, y + 20), "KEY TAKEAWAY", _font(13, True), TEALL_C)
        _text(d, (M + 30, y + 40), IOT_TAKEAWAY, _font(16, True), WHITE, max_width=W - 2 * M - 60, line_gap=1.06)
        d.text((W / 2, H - 38), f"{self.meta.author}  |  UID: {self.meta.uid}  |  {self.meta.course}  |  {self.meta.date}",
               font=_font(13), fill=SLATE_C, anchor="mm")

    def build(self) -> Image.Image:
        y = self.header()
        y = self.problem(y)
        y = self.causes(y)
        y = self.solutions(y)
        y = self.stakeholders(y)
        self.footer(min(y, H - 150))
        return self.img

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.img.save(path, "PNG", optimize=True)
        if path.suffix.lower() == ".png":
            self.img.save(path.with_suffix(".pdf"), "PDF", resolution=200.0)
        return path


def generate_poster(guide: StudyGuide, meta: ProjectMeta, out_path: str | Path) -> Path:
    builder = PosterBuilder(guide, meta)
    builder.build()
    return builder.save(out_path)
