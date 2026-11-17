"""Tests for the search over the manuals, through its port.

Under test: src/neuralbrewery/adapters/manuals/index.py
Port: src/neuralbrewery/core/manuals/protocols.py

WHY these tests exist: the plant agent cites what this search gives it,
with the page. A table read across its columns gives one code the meaning
of another, with a page that looks right: worse than no manual. Here, on
small manuals written in the test: how a text becomes passages, how BM25
ranks them, the filter by tag, and that a search with no answer is an
empty list, never an error. test_retrieval.py measures the real manuals.
"""

from pathlib import Path

import pytest

from neuralbrewery.adapters.manuals.index import MAX_CHARS, ManualIndex, read_manual
from neuralbrewery.core.manuals.protocols import ManualSearch

DRIVE = """\
---
id: drive
product: Drive X
component: Inverter
tags: M1
---

<!-- page 1 -->

Fault and warning codes

<!-- table fixed by hand, checked on the PDF -->

Fault code list

| Fault | Description |
|---|---|
| F11 | Motor overtemperature |
| F20 | DC ripple too high |

The fault icon remains lit until the fault is acknowledged.

<!-- page 2 -->

Cooling: keep 100 mm above and below the drive. The heatsink must stay
below 90 °C.
"""

PROBE = """\
---
id: probe
product: Probe Y
component: Probe
tags: TT1, TT5a
---

<!-- page 7 -->

|t| = Temperature absolute value in °C

Class A tolerance of the sensor.
"""


def write(folder: Path, name: str, text: str) -> None:
    (folder / name).write_text(text, encoding="utf-8")


@pytest.fixture
def manuals(tmp_path: Path) -> ManualIndex:
    write(tmp_path, "drive.md", DRIVE)
    write(tmp_path, "probe.md", PROBE)
    return ManualIndex.from_folder(tmp_path)


class TestPassages:
    def test_a_row_of_a_table_is_a_passage_with_its_title(self):
        """[HP] One row, under the title and the header of its table."""
        passages = read_manual(DRIVE, "drive.md")

        rows = [p.text for p in passages if "| F" in p.text]
        assert rows == [
            "Fault code list\n| Fault | Description |\n| F11 | Motor overtemperature |",
            "Fault code list\n| Fault | Description |\n| F20 | DC ripple too high |",
        ]

    def test_every_passage_says_where_it_comes_from(self):
        """[HP] Document, product, tags and page, from the header and the marks."""
        passages = read_manual(DRIVE, "drive.md")

        assert {(p.document, p.product, p.tags) for p in passages} == {
            ("drive", "Drive X", ("M1",))
        }
        assert [p.page for p in passages] == [1, 1, 1, 1, 2]
        assert "remains lit" in passages[3].text
        assert "heatsink" in passages[4].text

    def test_comments_are_no_text(self):
        """[EC] The page marks and the notes on the tables are not read."""
        passages = read_manual(DRIVE, "drive.md")

        assert not any("<!--" in p.text for p in passages)

    def test_a_line_between_bars_is_no_table_without_its_separator(self):
        """[EC] |t| in a formula is text: a table has its |---| row."""
        [passage] = read_manual(PROBE, "probe.md")

        assert passage.text.startswith("|t| = Temperature")
        assert passage.tags == ("TT1", "TT5a")
        assert passage.page == 7

    def test_long_text_is_cut_near_the_limit(self):
        """[EC] Paragraphs are packed up to the limit, and a long one is cut.

        WHY: pdftotext gives a whole table of contents as one line.
        """
        long_line = " ".join(f"word{n}" for n in range(600))
        short = "A short paragraph."
        text = DRIVE.replace(
            "Cooling:", f"{long_line}\n\n{short}\n\n{short}\n\nCooling:"
        )

        page_two = [p for p in read_manual(text, "drive.md") if p.page == 2]

        assert len(page_two) > 3
        assert all(len(p.text) <= MAX_CHARS for p in page_two)
        assert (
            " ".join(p.text for p in page_two).split()
            == (
                f"{long_line} {short} {short} " + DRIVE.split("<!-- page 2 -->")[1]
            ).split()
        )

    @pytest.mark.parametrize(
        "text",
        [
            pytest.param("<!-- page 1 -->\n\nNo header.", id="no header"),
            pytest.param("---\nid: drive\ntags: M1\n---\n", id="no product"),
        ],
    )
    def test_a_text_without_its_header_is_refused(self, text):
        """[EC] Without the header a passage could not say where it comes from."""
        with pytest.raises(ValueError, match=r"broken\.md.*extract_manuals"):
            read_manual(text, "broken.md")


class TestSearch:
    def test_is_the_port_of_the_agent(self, manuals):
        """[HP] The adapter implements ManualSearch."""
        assert isinstance(manuals, ManualSearch)

    def test_a_code_finds_its_own_row(self, manuals):
        """[HP] F11 gives the row of F11 first, not the row next to it."""
        [first, *_] = manuals.search("F11 fault", tag="M1")

        assert "Motor overtemperature" in first.text
        assert "DC ripple" not in first.text
        assert (first.document, first.page) == ("drive", 1)

    def test_at_most_the_limit_the_best_first(self, manuals):
        """[HP] Three by default; the passages with more of the words first."""
        found = manuals.search("fault code description drive heatsink cooling")

        assert len(found) == 3
        assert len(manuals.search("fault", limit=1)) == 1

    def test_the_tag_keeps_the_manuals_of_that_component(self, manuals):
        """[HP] Any case, any spaces: tt5a is TT5a."""
        query = "class tolerance heatsink"

        assert {p.document for p in manuals.search(query)} == {"probe", "drive"}
        assert {p.document for p in manuals.search(query, tag=" tt5a ")} == {"probe"}
        assert {p.document for p in manuals.search(query, tag="M1")} == {"drive"}

    @pytest.mark.parametrize(
        ("query", "tag"),
        [
            pytest.param("F99 unknown", "", id="no word matches"),
            pytest.param("", "", id="empty query"),
            pytest.param("F11", "P1", id="tag with no manual"),
            pytest.param("tolerance", "M1", id="word of another manual"),
        ],
    )
    def test_no_match_is_an_empty_list(self, manuals, query, tag):
        """[EC] Never an error, never a passage that shares no word."""
        assert manuals.search(query, tag=tag) == []

    def test_knows_the_tags_it_has_manuals_for(self, manuals):
        """[HP] What the tool tells the agent when a tag has no manual."""
        assert manuals.tags() == frozenset({"M1", "TT1", "TT5a"})

    def test_the_same_search_gives_the_same_answer(self, tmp_path):
        """[EC] Ties broken by document, page and place: the evals count on it."""
        write(tmp_path, "b.md", DRIVE.replace("id: drive", "id: b"))
        write(tmp_path, "a.md", DRIVE.replace("id: drive", "id: a"))

        found = [
            [(p.document, p.page) for p in ManualIndex.from_folder(tmp_path).search(q)]
            for q in ("F11", "F11")
        ]

        assert found[0] == found[1] == [("a", 1), ("b", 1)]

    def test_an_empty_folder_finds_nothing(self, tmp_path):
        """[EC] No manual, no passage: the settings refuse it before the app."""
        empty = ManualIndex.from_folder(tmp_path)

        assert empty.search("F11") == []
        assert empty.tags() == frozenset()
