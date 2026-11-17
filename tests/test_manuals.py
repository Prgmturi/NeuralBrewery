"""Tests for the list of manuals, the script that downloads them, and their text.

Under test: manuals/manifest.toml, scripts/download_manuals.py,
scripts/extract_manuals.py and data/manuals/text/

WHY these tests exist: the script reads some fields of every entry with no
default, so an entry that misses one fails only when someone runs the
download. No check does: it needs the network. The text is what the app
reads: the image holds no manifest and no PDF, so its header is where the
product and the tags come from at run time, and must say what the manifest
says.
"""

import importlib.util
import re
import tomllib
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).parent.parent
MANIFEST = ROOT / "manuals" / "manifest.toml"
SCRIPT = ROOT / "scripts" / "download_manuals.py"
EXTRACT = ROOT / "scripts" / "extract_manuals.py"
MANUALS = ROOT / "data" / "manuals"
TEXT = MANUALS / "text"

DOCS = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))["doc"]
BY_ID = [pytest.param(doc, id=str(doc.get("id"))) for doc in DOCS]

# What download_manuals.py reads from every entry, with no default
REQUIRED = {"id", "component", "product", "tags", "doc_type", "source", "auto"}
# Where a copy comes from, as the head of the manifest explains
SOURCES = {"ufficiale", "distributore", "terzi"}


def load(path: Path) -> ModuleType:
    """A script as a module: scripts/ is a folder, not a package."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def script() -> ModuleType:
    return load(SCRIPT)


class TestManifest:
    def test_lists_some_documents(self):
        """[HP] The manifest is a list of [[doc]] entries."""
        assert DOCS

    @pytest.mark.parametrize("doc", BY_ID)
    def test_every_entry_has_what_the_script_reads(self, doc):
        """[EC] No field the script reads without a default is missing."""
        assert REQUIRED - doc.keys() == set()

    def test_ids_are_unique(self):
        """[EC] The id names the file: two entries with one id share a file."""
        ids = [doc["id"] for doc in DOCS]

        assert sorted(ids) == sorted(set(ids))

    @pytest.mark.parametrize("doc", BY_ID)
    def test_every_entry_says_where_to_find_it(self, doc):
        """[EC] A url for the script, or a page for whoever downloads by hand.

        WHY: with auto = true the script reads url, and with auto = false it
        prints page; neither has a default.
        """
        where = doc["url"] if doc["auto"] else doc["page"]

        assert where.startswith("https://")

    @pytest.mark.parametrize("doc", BY_ID)
    def test_every_entry_names_its_components(self, doc):
        """[EC] The tags are the filter of the search: at least one each."""
        assert doc["tags"]
        assert all(isinstance(tag, str) and tag for tag in doc["tags"])

    @pytest.mark.parametrize("doc", BY_ID)
    def test_every_source_is_a_known_one(self, doc):
        """[EC] A misspelt source would pass into the index as it is."""
        assert doc["source"] in SOURCES


class TestScript:
    def test_reads_this_manifest_and_writes_under_data(self, script):
        """[HP] The script finds the manifest from its own place in the repo."""
        assert MANIFEST.resolve() == script.MANIFEST
        assert (ROOT / "data" / "manuals").resolve() == script.OUT

    @pytest.mark.parametrize(
        ("data", "kind"),
        [
            pytest.param(b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n", "pdf", id="pdf"),
            pytest.param("# iSpindel\nDensità".encode(), "md", id="text"),
            pytest.param(b"<!DOCTYPE html><html></html>", None, id="html page"),
            pytest.param(b"\n  <HTML lang='en'>", None, id="html after spaces"),
            pytest.param(b"\xff\xfe\x00\x01", None, id="not text"),
        ],
    )
    def test_detect_kind_looks_at_the_content(self, script, data, kind):
        """[EC] A PDF, a text, or nothing: never the page of an error.

        WHY: many sites answer a missing document with an HTML page and
        status 200, which would be saved under the name of the manual.
        """
        assert script.detect_kind(data) == kind


# The documents in data/manuals/, by id: what the download left there
DOWNLOADED = sorted(
    path.stem for path in MANUALS.iterdir() if path.suffix in {".pdf", ".md"}
)
TEXTS = sorted(path.stem for path in TEXT.glob("*.md"))
# The tables fixed by hand on the PDF: --force would lose them
FIXED_BY_HAND = {
    # The parameter list, one mark a page, p. 45-53; fault and alarm codes, p. 55-56
    "vfd-siemens-v20-getting-started": 11,
    "transmitter-itemp-tmt80": 1,  # signal on alarm, p. 2
    "level-sick-lfp-cubic-instructions": 2,  # 11.3 and 11.4, p. 54
    "valve-ussolid-motorized": 1,  # troubleshooting, p. 8
}


class TestText:
    def test_every_document_has_its_text_and_no_more(self):
        """[HP] One text per document downloaded, named by its id."""
        assert TEXTS == DOWNLOADED
        assert set(TEXTS) <= {doc["id"] for doc in DOCS}

    @pytest.mark.parametrize("doc_id", TEXTS)
    def test_the_header_says_what_the_manifest_says(self, doc_id):
        """[EC] Id, product, component and tags, as extract_manuals.py writes them.

        WHY: the image ships the text alone. An entry of the manifest
        changed by hand, and not in the text, would give the agent another
        product or other tags than the manifest says.
        """
        [doc] = [doc for doc in DOCS if doc["id"] == doc_id]
        text = (TEXT / f"{doc_id}.md").read_text(encoding="utf-8")

        assert text.startswith(load(EXTRACT).header(doc))

    @pytest.mark.parametrize("doc_id", TEXTS)
    def test_the_pages_are_marked_in_order(self, doc_id):
        """[EC] One mark per page, from 1: the page the agent cites."""
        text = (TEXT / f"{doc_id}.md").read_text(encoding="utf-8")

        pages = [int(n) for n in re.findall(r"^<!-- page (\d+) -->$", text, re.M)]

        assert pages == list(range(1, len(pages) + 1))

    @pytest.mark.parametrize(("doc_id", "tables"), FIXED_BY_HAND.items())
    def test_the_tables_fixed_by_hand_are_there(self, doc_id, tables):
        """[EC] Regenerated with --force, the text reads the tables across."""
        text = (TEXT / f"{doc_id}.md").read_text(encoding="utf-8")

        assert text.count("<!-- table fixed by hand") == tables
