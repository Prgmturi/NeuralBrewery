"""A passage of a manual: where it comes from, and what it says.

Plain Python, like the other vocabularies the agent reads.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ManualPassage:
    """A piece of a page of a manual, with what says where it comes from.

    The document, the product and the tags come from manuals/manifest.toml,
    through the header of the text (scripts/extract_manuals.py). The page
    is the index of the page in the PDF, as pdftotext -f counts it: the
    number a reader types to open it.
    """

    document: str  # the id in the manifest
    product: str
    tags: tuple[str, ...]  # the components it is the manual of: M1, TT1...
    page: int
    text: str
