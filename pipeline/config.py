"""Central configuration for the AI-assisted multi-format content studio."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SOURCE_DIR = ASSETS / "source"
OUTPUT_DIR = ROOT / "outputs"
FIGURE_DIR = ROOT / "report" / "figures"

SAMPLE_PDF = SOURCE_DIR / "whitebook_iot.pdf"

# ---------------------------------------------------------------- metadata --
DEFAULT_AUTHOR = "TEGUIA FRANK"
DEFAULT_UID = "26MCA20153"
DEFAULT_COURSE = "26CAP-608"
DEFAULT_INSTITUTION = "Chandigarh University"
DEFAULT_TITLE = "Internet of Things (IoT): Societal, Scientific, and Technical Foundations"
DEFAULT_SUBTITLE = (
    "A Multi-Disciplinary Analysis of IoT Architecture, Security, and Ecosystem Challenges"
)

# ------------------------------------------------------------------ palette --
NAVY = "#13294B"
NAVY_2 = "#1F3D5C"
TEAL = "#0F8B8D"
TEAL_LIGHT = "#7FD1CE"
AMBER = "#E9A23B"
SLATE = "#5B6770"
MIST = "#EEF3F6"
WHITE = "#FFFFFF"
INK = "#1A1A1A"

PALETTE_HEX = [NAVY, TEAL, AMBER, SLATE, TEAL_LIGHT]

# --------------------------------------------------------------- stopwords --
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "also", "am",
    "an", "and", "any", "are", "as", "at", "be", "because", "been", "before",
    "being", "below", "between", "both", "but", "by", "can", "could", "did",
    "do", "does", "doing", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "her", "here", "hers",
    "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is",
    "it", "its", "itself", "just", "me", "more", "most", "my", "myself", "no",
    "nor", "not", "now", "of", "off", "on", "once", "only", "or", "other",
    "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should",
    "so", "some", "such", "than", "that", "the", "their", "theirs", "them",
    "themselves", "then", "there", "these", "they", "this", "those", "through",
    "to", "too", "under", "until", "up", "very", "was", "we", "were", "what",
    "when", "where", "which", "while", "who", "whom", "why", "will", "with",
    "would", "you", "your", "yours", "yourself", "yourselves", "may", "might",
    "must", "shall", "within", "without", "however", "therefore", "thus",
    "hence", "among", "upon", "across", "via", "per", "yet", "still", "much",
    "many", "one", "two", "three", "first", "second", "third", "new", "use",
    "used", "using", "make", "made", "like", "well", "way", "part", "based",
}

DOMAIN_TERMS = {
    "iot": "Internet of Things",
    "cps": "Cyber-Physical Systems",
    "wot": "Web of Things",
    "suit": "Software Updates for Internet of Things",
    "riot": "RIOT operating system",
    "lpwan": "Low-Power Wide-Area Network",
    "6lowpan": "IPv6 over Low-Power Wireless Personal Area Networks",
    "coap": "Constrained Application Protocol",
    "fl": "Federated Learning",
    "gdpr": "General Data Protection Regulation",
    "mcu": "Microcontroller Unit",
    "nvram": "Non-Volatile Random-Access Memory",
    "ecc": "Elliptic Curve Cryptography",
    "aes": "Advanced Encryption Standard",
    "dlt": "Distributed Ledger Technology",
}


@dataclass
class ProjectMeta:
    """Author and course metadata embedded in every deliverable."""

    author: str = DEFAULT_AUTHOR
    uid: str = DEFAULT_UID
    course: str = DEFAULT_COURSE
    institution: str = DEFAULT_INSTITUTION
    title: str = DEFAULT_TITLE
    subtitle: str = DEFAULT_SUBTITLE
    date: str = "October 2026"
    supervisor: str = "Dr. Nisha Sharma"
    extra: dict = field(default_factory=dict)

    @property
    def byline(self) -> str:
        return f"{self.author}  |  UID: {self.uid}  |  {self.course}"
