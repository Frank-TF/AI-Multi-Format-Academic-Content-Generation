"""Phase 2 - structured 10-slide academic deck generation with python-pptx."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from .config import NAVY, NAVY_2, TEAL, TEAL_LIGHT, AMBER, SLATE, MIST, WHITE, ProjectMeta
from .domain import IOT_SOLUTIONS, IOT_STAKEHOLDERS, IOT_TAKEAWAY, IOT_TIMELINE
from .phase1_notes import StudyGuide


def _rgb(hex_color: str) -> RGBColor:
    h = hex_color.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


NAVY_C, TEAL_C, AMBER_C, SLATE_C = _rgb(NAVY), _rgb(TEAL), _rgb(AMBER), _rgb(SLATE)
MIST_C, WHITE_C, LIGHT_C = _rgb(MIST), _rgb(WHITE), _rgb(TEAL_LIGHT)


@dataclass
class SlidePlan:
    number: int
    title: str
    kicker: str
    bullets: list[str]
    layout: str = "bullets"
    visual: str = ""
    notes: str = ""


def build_plan(guide: StudyGuide) -> list[SlidePlan]:
    topics = guide.topics
    plans = [
        SlidePlan(1, guide.title, "ACADEMIC PRESENTATION", [
            guide.title,
            "A Multi-Disciplinary Analysis of IoT Architecture, Security, and Ecosystem Challenges",
            f"{guide.author}  |  UID: {guide.uid}  |  {guide.course}",
        ], "title", "Full-bleed navy cover with a subtle circuit-board line pattern; white title; teal rule.",
        "Open with the scope: one white book, four formats, one consistent evidence base."),
        SlidePlan(2, "Introduction: From Ubiquitous Computing to a Global IoT", "01  CONTEXT", [
            "IoT extends Internet connectivity from people to everyday objects fitted with sensors and actuators.",
            "The installed base reached roughly 10 billion devices in 2020, growing about 1,000% in a decade.",
            "IoT crossed the tipping point: more than 50% of connected devices are now IoT devices.",
            "The cloud-edge-thing continuum links tiny nodes, local gateways and central data centres.",
        ], "bullets", "A three-tier cloud-edge-thing diagram with device icons and data-flow arrows.",
        "Stress the scale and the digital-physical bridge, not product names."),
        SlidePlan(3, "Objectives of the Analysis", "02  OBJECTIVES", [
            "Trace the architectural evolution of IoT from domotics and RFID to IP-based constrained networks.",
            "Examine the energy, memory and bandwidth constraints that shape low-end device design.",
            "Analyse security and privacy paradigms for cyber-physical systems.",
            "Evaluate the societal and environmental footprint of pervasive deployment.",
        ], "objectives", "Four numbered cards, each with a thin teal icon strip.",
        "Map each objective to the four sections of the study guide."),
        SlidePlan(4, "Methodology: A Four-Step Evidence Pipeline", "03  METHOD", [
            "Literature ingestion: extract and clean the 92-page source into sentences and sections.",
            "Layer analysis: classify evidence across the cloud, edge and thing tiers.",
            "Synthesis: cluster findings into societal, technical and research-field themes.",
            "Framework formulation: produce notes, slides, a poster and a refined academic text.",
        ], "process", "Horizontal four-stage arrow with document, layers, synthesis and output icons.",
        "The method is reproducible: each stage has a prompt, a module and a validation check."),
        SlidePlan(5, "Developed vs Constrained Environments", "04  COMPARISON", [
            "High-end / cloud: watt-range power, rich memory, high throughput, centralised processing.",
            "Low-end / edge: milliWatt to microWatt budgets, kilobytes of RAM, low-bandwidth links.",
            "The gap explains why cloud security and programming models cannot simply be copied.",
            "Edge computing recovers latency and bandwidth while preserving local privacy.",
        ], "comparison", "Split-screen comparison: data-centre rack on the left, mote and gateway on the right.",
        "Use the table to justify lightweight protocols and cryptography."),
        SlidePlan(6, "Challenges and Their Societal Impact", "05  PROBLEM", [
            "Security: large attack surfaces, insecure updates and long device lifetimes.",
            "Privacy: pervasive sensing enables surveillance and behavioural profiling.",
            "Resources: tight energy and memory budgets limit conventional defences.",
            "Society: dependency, lock-in and the environmental cost of billions of devices.",
        ], "two_column", "Two columns linked by a red risk arrow; icons for security, privacy, energy and policy.",
        "Pair every technical cause with a societal consequence."),
        SlidePlan(7, "Secure Firmware Update Lifecycle (SUIT)", "06  PROCESS", [
            "Commission the device with a public key and master credentials out of band.",
            "Build the firmware image and publish a signed manifest containing hashes.",
            "The device downloads the package and verifies the signature and SHA-256 digest.",
            "Install atomically on success; abort and alert on any verification failure.",
        ], "flow", "Five chevrons: Commission -> Build -> Sign -> Verify -> Install/Abort.",
        "SUIT turns an untrusted network into a verifiable update channel."),
        SlidePlan(8, "Evolution of IoT and Standards", "07  TIMELINE", [
            "Pre-2000s: domotics and the early ubiquitous-computing vision.",
            "2000s: RFID and wireless sensor networks make low-power sensing practical.",
            "2010s: 6LoWPAN, CoAP and the Web of Things standardise IP-based IoT.",
            "2020s and beyond: edge AI, post-quantum cryptography, smart dust and net-zero design.",
        ], "timeline", "Horizontal timeline with five milestone nodes and short labels.",
        "Standards are the mechanism that turns prototypes into interoperable infrastructure."),
        SlidePlan(9, "Design and Implementation Recommendations", "08  SOLUTIONS", [
            "Use lightweight symmetric ciphers such as ChaCha20 for bulk data on constrained MCUs.",
            "Adopt open, vendor-independent platforms such as RIOT OS and standard update manifests.",
            "Process data at the edge and apply federated learning to avoid moving raw personal data.",
            "Design for energy harvesting, intermittent operation and a measurable life-cycle footprint.",
        ], "solutions", "Four solution cards with icons: cipher, open-source chip, edge node, leaf.",
        "Recommendations should be feasible for a small engineering team, not aspirational."),
        SlidePlan(10, "Conclusion: Sovereignty by Design", "09  CONCLUSION", [
            "IoT is infrastructure, not a gadget category: its failures are physical and societal.",
            "Security, privacy and energy must be co-designed under real resource constraints.",
            "Open standards and open source reduce lock-in and extend device lifetimes.",
            "Digital sovereignty and public trust are the conditions for sustainable adoption.",
        ], "conclusion", "Bold closing statement on a navy panel with a teal keyline and author footer.",
        "Close with the call to action: secure by design, open by default, accountable by law."),
    ]
    return plans


class DeckBuilder:
    def __init__(self, meta: ProjectMeta):
        self.meta = meta
        self.prs = Presentation()
        self.prs.slide_width = Inches(13.333)
        self.prs.slide_height = Inches(7.5)
        self.blank = self.prs.slide_layouts[6]

    # ------------------------------------------------------------- helpers --
    def _bg(self, slide, color: str = WHITE) -> None:
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = _rgb(color)

    def _rect(self, slide, x, y, w, h, color, line=None, shape=MSO_SHAPE.RECTANGLE):
        shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        shp.fill.solid()
        shp.fill.fore_color.rgb = _rgb(color)
        if line:
            shp.line.color.rgb = _rgb(line)
            shp.line.width = Pt(0.75)
        else:
            shp.line.fill.background()
        shp.shadow.inherit = False
        return shp

    def _text(self, slide, x, y, w, h, text, size=18, color=NAVY, bold=False,
              align=PP_ALIGN.LEFT, font="Calibri", anchor=MSO_ANCHOR.TOP,
              italic=False, spacing=1.0):
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = anchor
        tf.margin_left = 0
        tf.margin_right = 0
        tf.margin_top = 0
        tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = align
        p.line_spacing = spacing
        run = p.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = _rgb(color)
        run.font.name = font
        return box

    def _bullets(self, slide, x, y, w, h, items, size=17, color=NAVY, bullet_color=TEAL):
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = 0
        tf.margin_right = 0
        tf.margin_top = 0
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(11)
            p.line_spacing = 1.08
            p.level = 0
            marker = p.add_run()
            marker.text = "▸  "
            marker.font.size = Pt(size)
            marker.font.color.rgb = _rgb(bullet_color)
            marker.font.name = "Calibri"
            run = p.add_run()
            run.text = item
            run.font.size = Pt(size)
            run.font.color.rgb = _rgb(color)
            run.font.name = "Calibri"
        return box

    def _chrome(self, slide, plan: SlidePlan) -> None:
        self._rect(slide, 0, 0, 13.333, 1.42, NAVY)
        self._rect(slide, 0, 1.42, 13.333, 0.06, TEAL)
        self._text(slide, 0.62, 0.23, 8.4, 0.34, plan.kicker, 11, TEAL_LIGHT, True)
        self._text(slide, 0.62, 0.55, 11.8, 0.75, plan.title, 25, WHITE, True)
        self._text(slide, 11.55, 0.33, 1.15, 0.4, f"{plan.number:02d}/10", 12, TEAL_LIGHT, True, PP_ALIGN.RIGHT)
        # footer
        self._rect(slide, 0.62, 7.03, 12.09, 0.012, "#C9D6DE")
        self._text(slide, 0.62, 7.1, 7.4, 0.26,
                   f"{self.meta.author}  |  UID: {self.meta.uid}  |  {self.meta.course}",
                   9.5, SLATE)
        self._text(slide, 8.5, 7.1, 4.2, 0.26, "AI-Assisted Multi-Format Content Studio", 9.5, SLATE,
                   align=PP_ALIGN.RIGHT)
        if plan.visual:
            self._text(slide, 0.62, 6.66, 12.0, 0.26, "Visual: " + plan.visual, 9.5, SLATE, italic=True)

    # -------------------------------------------------------------- slides --
    def _cover(self, plan: SlidePlan):
        slide = self.prs.slides.add_slide(self.blank)
        self._bg(slide, NAVY)
        # decorative bars
        self._rect(slide, 0, 0, 0.22, 7.5, TEAL)
        self._rect(slide, 9.7, 0, 3.633, 7.5, NAVY_2)
        for i in range(5):
            self._rect(slide, 10.15 + i * 0.16, 1.0 + i * 0.55, 2.6 - i * 0.3, 0.035, TEAL_LIGHT)
        self._text(slide, 0.85, 0.95, 8.6, 0.4, "MINI PROJECT  ·  " + self.meta.course, 12, TEAL_LIGHT, True)
        self._text(slide, 0.85, 1.55, 8.7, 2.2, plan.bullets[0], 33, WHITE, True, spacing=0.95)
        self._rect(slide, 0.87, 3.95, 1.5, 0.06, TEAL)
        self._text(slide, 0.85, 4.2, 8.6, 1.0, plan.bullets[1], 16, "#D6E4EC", italic=True)
        self._text(slide, 0.85, 5.55, 8.5, 0.35, plan.bullets[2], 14, WHITE, True)
        self._text(slide, 0.85, 6.05, 8.5, 0.8,
                   f"{self.meta.institution}  ·  {self.meta.date}", 11.5, TEAL_LIGHT)
        self._text(slide, 10.15, 5.9, 2.55, 0.9,
                   "One source.\nFour academic formats.", 12, WHITE, True, PP_ALIGN.CENTER)
        return slide

    def _standard(self, plan: SlidePlan):
        slide = self.prs.slides.add_slide(self.blank)
        self._bg(slide, WHITE)
        self._chrome(slide, plan)
        if plan.layout == "bullets":
            self._bullets(slide, 0.75, 1.85, 7.5, 4.6, plan.bullets, 18)
            self._side_stats(slide, plan)
        elif plan.layout == "objectives":
            self._cards(slide, plan.bullets, 1.85, 4.4)
        elif plan.layout == "process":
            self._process(slide, plan.bullets)
        elif plan.layout == "comparison":
            self._comparison(slide)
        elif plan.layout == "two_column":
            self._two_column(slide)
        elif plan.layout == "flow":
            self._flow(slide)
        elif plan.layout == "timeline":
            self._timeline(slide)
        elif plan.layout == "solutions":
            self._cards(slide, plan.bullets, 1.85, 4.4, numbered=False)
        elif plan.layout == "conclusion":
            self._conclusion(slide, plan)
        return slide

    def _side_stats(self, slide, plan):
        x = 8.75
        self._rect(slide, x, 1.85, 3.95, 4.35, MIST, "#D6E2E8")
        self._text(slide, x + 0.3, 2.1, 3.35, 0.35, "EVIDENCE SNAPSHOT", 11, TEAL, True)
        stats = [("~10 bn", "IoT devices in 2020"), ("50%+", "of connected devices"), ("1,000%", "growth 2010-2020"), ("92", "source pages")]
        for i, (big, small) in enumerate(stats):
            y = 2.55 + i * 0.9
            self._text(slide, x + 0.3, y, 1.45, 0.55, big, 22, NAVY, True)
            self._text(slide, x + 1.75, y + 0.1, 1.95, 0.55, small, 11.5, SLATE)

    def _cards(self, slide, items, y, h, w=2.86, gap=0.2, numbered=True):
        xs = [0.75 + i * (w + gap) for i in range(4)]
        for i, item in enumerate(items[:4]):
            x = xs[i]
            self._rect(slide, x, y, w, h, MIST if i % 2 == 0 else "#F7FAFB", "#D6E2E8")
            self._rect(slide, x, y, w, 0.09, TEAL if i % 2 == 0 else AMBER)
            if numbered:
                self._text(slide, x + 0.28, y + 0.28, 0.7, 0.55, f"0{i+1}", 24, TEAL, True)
            self._text(slide, x + 0.28, y + 0.95, w - 0.56, h - 1.15, item, 13.5, NAVY, spacing=1.05)

    def _process(self, slide, items):
        y = 2.2
        for i, item in enumerate(items):
            x = 0.75 + i * 3.08
            color = [NAVY, NAVY_2, TEAL, AMBER][i]
            self._rect(slide, x, y, 2.68, 3.5, color if i < 2 else (TEAL if i == 2 else AMBER))
            self._text(slide, x + 0.22, y + 0.22, 0.7, 0.45, f"0{i+1}", 20, WHITE, True)
            self._text(slide, x + 0.22, y + 0.85, 2.26, 2.4, item.split(": ", 1)[-1], 13, WHITE)
            if i < 3:
                self._text(slide, x + 2.7, y + 1.35, 0.35, 0.5, "→", 25, SLATE, True, PP_ALIGN.CENTER)

    def _comparison(self, slide):
        left = ["Watt-range power budget", "Rich RAM and storage", "High network throughput", "Centralised cloud processing", "Conventional security stacks"]
        right = ["MicroWatt to milliWatt power", "Kilobytes of RAM and flash", "Low-bandwidth wireless links", "Intermittent edge processing", "Lightweight cryptography"]
        for i, (title, items, color) in enumerate([
            ("HIGH-END / CLOUD", left, NAVY),
            ("LOW-END / CONSTRAINED EDGE", right, TEAL),
        ]):
            x = 0.75 + i * 6.15
            self._rect(slide, x, 1.85, 5.75, 4.35, MIST, "#D6E2E8")
            self._rect(slide, x, 1.85, 5.75, 0.72, color)
            self._text(slide, x + 0.3, 2.0, 5.15, 0.4, title, 14, WHITE, True)
            for j, item in enumerate(items):
                self._text(slide, x + 0.32, 2.85 + j * 0.6, 5.05, 0.45, "•  " + item, 14, NAVY)
        self._text(slide, 6.32, 3.55, 0.55, 0.6, "VS", 15, AMBER, True, PP_ALIGN.CENTER)

    def _two_column(self, slide):
        cols = [
            ("CORE CHALLENGES", ["Security vulnerabilities", "Privacy erosion", "Power and memory limits", "Protocol mismatch"], NAVY),
            ("SOCIETAL & TECHNICAL IMPACT", ["Cyber-physical threats", "Surveillance risk", "Unmaintainable devices", "Environmental footprint"], TEAL),
        ]
        for i, (title, items, color) in enumerate(cols):
            x = 0.75 + i * 6.15
            self._rect(slide, x, 1.85, 5.75, 4.35, "#F7FAFB", "#D6E2E8")
            self._rect(slide, x, 1.85, 0.12, 4.35, color)
            self._text(slide, x + 0.38, 2.05, 5.0, 0.4, title, 14, color, True)
            for j, item in enumerate(items):
                self._rect(slide, x + 0.45, 2.75 + j * 0.72, 0.1, 0.1, AMBER, shape=MSO_SHAPE.OVAL)
                self._text(slide, x + 0.72, 2.64 + j * 0.72, 4.7, 0.4, item, 14.5, NAVY)
        self._text(slide, 6.38, 3.85, 0.5, 0.5, "⇢", 26, AMBER, True, PP_ALIGN.CENTER)

    def _flow(self, slide):
        labels = ["Commission", "Build", "Sign manifest", "Verify", "Install / abort"]
        colors = [NAVY, NAVY_2, TEAL, TEAL, AMBER]
        for i, (label, color) in enumerate(zip(labels, colors)):
            x = 0.55 + i * 2.52
            shp = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x), Inches(2.25), Inches(2.55), Inches(1.15))
            shp.fill.solid(); shp.fill.fore_color.rgb = _rgb(color)
            shp.line.fill.background(); shp.shadow.inherit = False
            tf = shp.text_frame; tf.word_wrap = True
            tf.margin_left = Inches(0.3)
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            r = p.add_run(); r.text = label
            r.font.size = Pt(12.5); r.font.bold = True; r.font.color.rgb = _rgb(WHITE); r.font.name = "Calibri"
            self._text(slide, x + 0.2, 3.65, 2.15, 1.7,
                       ["Key + credentials provisioned out of band",
                        "Firmware image compiled and versioned",
                        "Signed manifest with SHA-256 hashes",
                        "Signature and integrity checked on device",
                        "Atomic install or safe abort + alert"][i], 11.5, NAVY)
        self._rect(slide, 0.75, 5.45, 11.85, 0.9, MIST, "#D6E2E8")
        self._text(slide, 0.95, 5.62, 11.45, 0.55,
                   "Security property: an untrusted network becomes a verifiable delivery channel.",
                   14, NAVY, True, PP_ALIGN.CENTER)

    def _timeline(self, slide):
        y = 3.25
        self._rect(slide, 0.85, y, 11.55, 0.04, "#C9D6DE")
        phases = list(IOT_TIMELINE)
        xs = [1.1, 3.5, 5.9, 8.3, 10.7]
        for i, ((label, detail), x) in enumerate(zip(phases, xs)):
            color = [SLATE, TEAL, NAVY, AMBER, TEAL][i]
            self._rect(slide, x - 0.13, y - 0.13, 0.26, 0.26, color, shape=MSO_SHAPE.OVAL)
            above = i % 2 == 0
            self._text(slide, x - 1.1, (y - 1.35) if above else (y + 0.3), 2.2, 0.38, label, 13, color, True, PP_ALIGN.CENTER)
            self._text(slide, x - 1.1, (y - 0.95) if above else (y + 0.7), 2.2, 0.9, detail, 9.8, NAVY, align=PP_ALIGN.CENTER)

    def _conclusion(self, slide, plan):
        self._rect(slide, 0.75, 1.85, 11.85, 2.3, NAVY)
        self._text(slide, 1.05, 2.05, 1.0, 0.5, "→", 26, TEAL_LIGHT, True)
        self._text(slide, 1.05, 2.55, 11.2, 1.3, IOT_TAKEAWAY, 21, WHITE, True, spacing=1.02)
        self._bullets(slide, 0.85, 4.45, 11.7, 1.8, plan.bullets[:3], 15.5)
        self._text(slide, 0.85, 6.2, 11.7, 0.35,
                   "Secure by design. Open by default. Accountable by law.", 15, TEAL, True, PP_ALIGN.CENTER)

    # ---------------------------------------------------------------- build --
    def build(self, guide: StudyGuide) -> Presentation:
        for plan in build_plan(guide):
            slide = self._cover(plan) if plan.layout == "title" else self._standard(plan)
            if plan.notes:
                slide.notes_slide.notes_text_frame.text = plan.notes
        return self.prs

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.prs.save(path)
        return path


def generate_deck(guide: StudyGuide, meta: ProjectMeta, out_path: str | Path) -> Path:
    builder = DeckBuilder(meta)
    builder.build(guide)
    return builder.save(out_path)
