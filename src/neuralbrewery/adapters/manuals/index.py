"""The manuals of the components, searched with BM25, in plain Python.

The words half of the hybrid search of lesson 7, with the tags of lesson 6
as the filter. No embedding and no rerank: they would need a dependency or
a key more (docs/decisioni.md, "RAG sui manuali").

The text is what scripts/extract_manuals.py wrote in data/manuals/text/:
a header from manuals/manifest.toml (id, product, component, tags), then a
mark per page, <!-- page N -->. It is read once, when the app starts, and
cut into passages:
- each page on its own, then by paragraphs up to about MAX_CHARS;
- each row of a Markdown table on its own, under the title and the header
  of its table: a code and its meaning stay together, and apart from the
  next row. The tables that matter were fixed by hand on the PDF.

BM25 with words in lower case, k1 = 1.5 and b = 0.75: the IDF over every
passage, then the filter by tag. Deterministic: ties go to the document,
the page and the place in the page, in this order.
"""

import math
import re
from collections import Counter
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Self

from neuralbrewery.core.manuals.schemas import ManualPassage

K1 = 1.5
B = 0.75
MAX_CHARS = 1000
LIMIT = 3

PAGE = re.compile(r"^<!-- page (\d+) -->$", re.MULTILINE)
COMMENT = re.compile(r"<!--.*-->")
SEPARATOR = re.compile(r"\|[\s:|-]+\|")
HEADER = ("id", "product", "tags")


def words(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def read_manual(text: str, name: str) -> list[ManualPassage]:
    """The passages of one manual: its header, then page by page."""
    lines = text.split("\n")
    fields = {}
    if lines[0].strip() == "---" and "---" in lines[1:]:
        end = lines.index("---", 1)
        fields = dict(line.split(": ", 1) for line in lines[1:end])
        lines = lines[end + 1 :]
    if any(key not in fields for key in HEADER):
        raise ValueError(
            f"{name}: the header (id, product, tags) is missing. Rerun "
            "python scripts/extract_manuals.py for it"
        )
    tags = tuple(tag.strip() for tag in fields["tags"].split(","))
    # Before the first mark: nothing. Then the number and the text of each page
    parts = PAGE.split("\n".join(lines))[1:]
    return [
        ManualPassage(fields["id"], fields["product"], tags, int(number), passage)
        for number, page in zip(parts[::2], parts[1::2], strict=True)
        for passage in passages(page)
    ]


def passages(page: str) -> list[str]:
    """A page cut into passages: the rows of its tables, and the rest packed."""
    lines = [
        line.strip() for line in page.split("\n") if not COMMENT.fullmatch(line.strip())
    ]
    found: list[str] = []
    prose: list[str] = []
    title = ""
    at = 0
    while at < len(lines):
        if (
            _row(lines[at])
            and at + 1 < len(lines)
            and SEPARATOR.fullmatch(lines[at + 1])
        ):
            found += _packed(prose)
            prose = []
            header = lines[at]
            at += 2
            while at < len(lines) and _row(lines[at]):
                found.append(f"{title}\n{header}\n{lines[at]}".lstrip())
                at += 1
            continue
        if lines[at]:
            title = lines[at].lstrip("#").strip()
        prose.append(lines[at])
        at += 1
    return found + _packed(prose)


def _row(line: str) -> bool:
    return len(line) > 1 and line.startswith("|") and line.endswith("|")


def _packed(lines: Sequence[str]) -> list[str]:
    """Paragraphs joined up to MAX_CHARS; a longer one cut between words."""
    pieces = [
        piece
        for paragraph in "\n".join(lines).split("\n\n")
        if paragraph.strip()
        for piece in _cut(paragraph.strip())
    ]
    packed: list[str] = []
    for piece in pieces:
        if packed and len(packed[-1]) + 2 + len(piece) <= MAX_CHARS:
            packed[-1] += "\n\n" + piece
        else:
            packed.append(piece)
    return packed


def _cut(paragraph: str) -> list[str]:
    if len(paragraph) <= MAX_CHARS:
        return [paragraph]
    cut: list[str] = []
    for word in paragraph.split():
        if cut and len(cut[-1]) + 1 + len(word) <= MAX_CHARS:
            cut[-1] += " " + word
        else:
            cut.append(word)
    return cut


class ManualIndex:
    """The ManualSearch port, over the passages of every manual, in memory."""

    def __init__(self, manual_passages: Iterable[ManualPassage]) -> None:
        self._passages = tuple(manual_passages)
        self._counts = [Counter(words(passage.text)) for passage in self._passages]
        self._lengths = [sum(counts.values()) for counts in self._counts]
        self._average = (
            sum(self._lengths) / len(self._lengths) if self._lengths else 0.0
        )
        size = len(self._passages)
        holding = Counter(word for counts in self._counts for word in counts)
        self._idf = {
            word: math.log(1 + (size - n + 0.5) / (n + 0.5))
            for word, n in holding.items()
        }
        self._tags = frozenset(
            tag for passage in self._passages for tag in passage.tags
        )
        self._folded = [
            frozenset(tag.casefold() for tag in passage.tags)
            for passage in self._passages
        ]

    @classmethod
    def from_folder(cls, folder: Path) -> Self:
        """Every <id>.md of the folder, in the order of their names."""
        return cls(
            passage
            for path in sorted(folder.glob("*.md"))
            for passage in read_manual(path.read_text(encoding="utf-8"), path.name)
        )

    def tags(self) -> frozenset[str]:
        return self._tags

    def search(
        self, query: str, tag: str = "", limit: int = LIMIT
    ) -> list[ManualPassage]:
        wanted = tag.strip().casefold()
        terms = set(words(query))
        scored = []
        for place, counts in enumerate(self._counts):
            if wanted and wanted not in self._folded[place]:
                continue
            score = sum(
                self._weight(term, counts, place) for term in terms if term in counts
            )
            if score > 0:
                scored.append((-score, place))
        return [self._passages[place] for _, place in sorted(scored)[:limit]]

    def _weight(self, term: str, counts: Counter[str], place: int) -> float:
        frequency = counts[term]
        norm = K1 * (1 - B + B * self._lengths[place] / self._average)
        return self._idf[term] * frequency * (K1 + 1) / (frequency + norm)
