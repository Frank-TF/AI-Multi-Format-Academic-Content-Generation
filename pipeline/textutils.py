"""Small, dependency-free NLP helpers used by every phase.

The functions here deliberately avoid heavyweight models so that the whole
pipeline can run offline inside a Streamlit container.  They provide sentence
segmentation, tokenisation, TF-IDF scoring, keyword extraction and readability
metrics.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Sequence

from .config import STOPWORDS

_ABBREV = {
    "e.g.", "i.e.", "etc.", "vs.", "fig.", "figs.", "no.", "dr.", "prof.",
    "mr.", "mrs.", "ms.", "al.", "cf.", "pp.", "vol.", "inc.", "ltd.", "st.",
}

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(\[\"'“])")
_WORD = re.compile(r"[A-Za-z][A-Za-z0-9\-']+")
_ACRONYM = re.compile(r"\b[A-Z]{2,6}\b")
_NUMBER_FACT = re.compile(
    r"(\b\d[\d,.]*\s*(?:%|percent|billion|million|thousand|trillion|"
    r"microcontrollers?|devices?|nodes?|years?)\b|\b(?:19|20)\d{2}\b)",
    re.IGNORECASE,
)


def clean_text(text: str) -> str:
    """Normalise PDF whitespace, ligatures and line-break hyphenation."""
    text = text.replace("\u00ad", "")
    text = text.replace("\ufb01", "fi").replace("\ufb02", "fl")
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_paragraphs(text: str) -> list[str]:
    parts = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text)]
    return [p for p in parts if len(p) > 40]


_PAGE_FURNITURE = [
    re.compile(r"^PART\s+[IVX]+\s*[_\-–]\s*The Internet of Things \(IoT\)\s*\d{1,3}\s+", re.I),
    re.compile(r"^\d{1,3}\s*[_\-–]\s*IoT\s+[A-Za-z&,\s]{3,70}\d{1,3}\s+"),
    re.compile(r"^(?:WHITE BOOK\s*N[°o]?\s*0?5\s*)", re.I),
    re.compile(r"^Data Cleaning & Duplicate Resolution Tool\s*[-–]\s*Academic Report\s+", re.I),
]


def sanitise_sentence(text: str) -> str:
    """Remove page furniture and PDF artefacts from an extracted sentence."""
    s = re.sub(r"\s+", " ", text).strip()
    for pat in _PAGE_FURNITURE:
        s = pat.sub("", s)
    s = re.sub(r"^[\d\s._\-–]+(?=[A-Z][a-z])", "", s) if re.match(r"^\d{1,3}\s+[A-Z][a-z]", s) else s
    s = re.sub(r"\s*[•�]\s*Inria\s*/\s*Photo[^.]*\.", "", s)
    s = re.sub(r"\s+", " ", s).strip(" ;")
    return s


def is_good_sentence(text: str, min_words: int = 10, max_words: int = 55) -> bool:
    s = text.strip()
    if not s or len(s) < 55:
        return False
    n = len(s.split())
    if not (min_words <= n <= max_words):
        return False
    if "...." in s or "Traceback" in s or "http://" in s or "https://" in s:
        return False
    low = s.lower()
    if low.startswith(("contents", "figure ", "table ", "chapter ", "references")):
        return False
    if sum(ch.isdigit() for ch in s) > len(s) * 0.35:
        return False
    if not re.search(r"[a-z]{3,}\s+[a-z]{3,}", s):
        return False
    return True


def split_sentences(text: str) -> list[str]:
    """Rule-based sentence splitter that protects common abbreviations."""
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    protected = text
    for i, abbr in enumerate(sorted(_ABBREV, key=len, reverse=True)):
        protected = protected.replace(abbr, abbr.replace(".", f"@@{i}@@"))
    protected = re.sub(r"(\b[A-Z]\.){2,}", lambda m: m.group(0).replace(".", "@@"), protected)
    raw = _SENT_SPLIT.split(protected)
    out: list[str] = []
    for chunk in raw:
        chunk = re.sub(r"@@\d+@@", ".", chunk).strip()
        chunk = re.sub(r"\s+", " ", chunk)
        if len(chunk) >= 30 and re.search(r"[A-Za-z]", chunk):
            out.append(chunk)
    return out


def words(text: str) -> list[str]:
    return [w.lower() for w in _WORD.findall(text)]


def content_words(text: str) -> list[str]:
    return [w for w in words(text) if w not in STOPWORDS and len(w) > 2]


def title_case_heading(text: str) -> str:
    small = {"and", "or", "of", "for", "the", "in", "on", "with", "to", "a", "an", "as", "at", "by"}
    parts = re.split(r"(\s+|-|/)", text.strip())
    out, first = [], True
    for part in parts:
        if not part or part.isspace() or part in "-/":
            out.append(part)
            continue
        low = part.lower()
        if not first and low in small:
            out.append(low)
        elif part.isupper() and len(part) <= 5:
            out.append(part)
        else:
            out.append(part[:1].upper() + part[1:].lower() if part.isupper() else part[:1].upper() + part[1:])
        first = False
    return "".join(out)


def truncate(text: str, limit: int = 220, ellipsis: str = "...") -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + ellipsis


def sentence_key(s: str) -> str:
    return re.sub(r"\W+", "", s.lower())[:160]


@dataclass
class ScoredSentence:
    text: str
    score: float
    index: int
    section: str = ""


class TfidfIndex:
    """A compact TF-IDF vector space over sentences."""

    def __init__(self, sentences: Sequence[str]):
        self.sentences = list(sentences)
        self.tokens = [content_words(s) for s in self.sentences]
        self.df: Counter = Counter()
        for toks in self.tokens:
            self.df.update(set(toks))
        self.n = max(1, len(self.sentences))
        self.idf = {
            term: math.log((1 + self.n) / (1 + df)) + 1.0 for term, df in self.df.items()
        }
        self.vectors = [self._vector(toks) for toks in self.tokens]

    def _vector(self, toks: Sequence[str]) -> dict[str, float]:
        counts = Counter(toks)
        total = max(1, len(toks))
        return {
            t: (c / total) * self.idf.get(t, 1.0)
            for t, c in counts.items()
            if t in self.idf
        }

    @staticmethod
    def cosine(a: dict[str, float], b: dict[str, float]) -> float:
        if not a or not b:
            return 0.0
        common = set(a) & set(b)
        num = sum(a[t] * b[t] for t in common)
        den = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values()))
        return num / den if den else 0.0

    def rank(
        self,
        query: str | None = None,
        limit: int = 8,
        diversity: float = 0.25,
        section: str | None = None,
    ) -> list[ScoredSentence]:
        qvec = self._vector(content_words(query)) if query else None
        scored: list[ScoredSentence] = []
        for i, sent in enumerate(self.sentences):
            vec = self.vectors[i]
            if qvec:
                base = self.cosine(qvec, vec)
            else:
                base = sum(vec.values()) / math.sqrt(max(1, len(vec)))
            # Prefer informative but not over-long sentences.
            length_penalty = 1.0 if 18 <= len(words(sent)) <= 48 else 0.82
            scored.append(ScoredSentence(sent, base * length_penalty, i, section or ""))
        scored.sort(key=lambda s: s.score, reverse=True)

        chosen: list[ScoredSentence] = []
        for cand in scored:
            if len(chosen) >= limit:
                break
            if section and cand.section and cand.section != section:
                continue
            if any(self.cosine(self.vectors[cand.index], self.vectors[c.index]) > diversity for c in chosen):
                continue
            chosen.append(cand)
        return chosen


def extract_keywords(text: str, limit: int = 12) -> list[tuple[str, int]]:
    toks = content_words(text)
    counts = Counter(toks)
    # Add frequent bigrams whose parts are both content words.
    bigrams: Counter = Counter()
    raw = [w.lower() for w in _WORD.findall(text)]
    for a, b in zip(raw, raw[1:]):
        if a not in STOPWORDS and b not in STOPWORDS and len(a) > 2 and len(b) > 2:
            bigrams[f"{a} {b}"] += 1
    merged = Counter({k: v for k, v in counts.items()})
    for phrase, count in bigrams.items():
        if count >= 3:
            merged[phrase] = count * 2
    return merged.most_common(limit)


def extract_acronyms(text: str) -> dict[str, int]:
    return Counter(_ACRONYM.findall(text))


def is_fact_sentence(sentence: str) -> bool:
    if _NUMBER_FACT.search(sentence):
        return True
    markers = (
        "key", "important", "critical", "challenge", "must", "should", "requires",
        "enables", "allows", "provides", "primary", "main", "significant",
    )
    low = sentence.lower()
    return any(m in low for m in markers)


def readability(text: str) -> dict[str, float]:
    sents = split_sentences(text) or [text]
    toks = words(text)
    if not toks:
        return {"words": 0, "sentences": 0, "avg_sentence_length": 0.0,
                "flesch_reading_ease": 0.0, "flesch_kincaid_grade": 0.0,
                "lexical_density": 0.0}
    syllables = sum(count_syllables(w) for w in toks)
    asl = len(toks) / len(sents)
    asw = syllables / len(toks)
    fre = 206.835 - 1.015 * asl - 84.6 * asw
    fkgl = 0.39 * asl + 11.8 * asw - 15.59
    content = [w for w in toks if w not in STOPWORDS]
    return {
        "words": len(toks),
        "sentences": len(sents),
        "avg_sentence_length": round(asl, 2),
        "flesch_reading_ease": round(fre, 1),
        "flesch_kincaid_grade": round(fkgl, 1),
        "lexical_density": round(100 * len(content) / len(toks), 1),
    }


def count_syllables(word: str) -> int:
    word = word.lower().strip("'-")
    if not word:
        return 0
    vowels = "aeiouy"
    count, prev = 0, False
    for ch in word:
        is_v = ch in vowels
        if is_v and not prev:
            count += 1
        prev = is_v
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def jaccard(a: str, b: str) -> float:
    sa, sb = set(content_words(a)), set(content_words(b))
    return len(sa & sb) / max(1, len(sa | sb))


def unique_sentences(sentences: Iterable[str], threshold: float = 0.72) -> list[str]:
    out: list[str] = []
    for s in sentences:
        if s and all(jaccard(s, o) < threshold for o in out):
            out.append(s)
    return out


def dedupe_preserve_order(items: Iterable[str]) -> list[str]:
    seen, out = set(), []
    for item in items:
        key = item.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(item)
    return out
