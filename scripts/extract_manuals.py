"""Estrae il testo dei manuali in data/manuals/text/, una volta, per il RAG.

Solo libreria standard, più pdfinfo e pdftotext di poppler:

    python scripts/extract_manuals.py            # estrae i mancanti
    python scripts/extract_manuals.py --force    # riestrae tutto

Un file per documento, data/manuals/text/<id>.md:
- in testa id, prodotto, componente e sigle, presi da manuals/manifest.toml;
- un segno per pagina, <!-- page N -->, con N l'indice della pagina nel PDF
  (quello di pdftotext -f N);
- il testo di pdftotext in modalità normale, una pagina alla volta. Con
  -layout le colonne di una tabella si sfasano: sul V20 F11 diventava
  "DC ripple too high", che è F20.

Un Markdown (l'iSpindel) si copia così com'è, tutto come pagina 1.

Senza --force un file che esiste non si tocca: dentro ci sono le tabelle
sistemate a mano (docs/development.md). L'app legge solo questi .md.
"""

import argparse
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "manuals" / "manifest.toml"
MANUALS = ROOT / "data" / "manuals"
OUT = MANUALS / "text"


def header(doc: dict) -> str:
    """Id, prodotto, componente e sigle del manifest, in testa al file."""
    return (
        "---\n"
        f"id: {doc['id']}\n"
        f"product: {doc['product']}\n"
        f"component: {doc['component']}\n"
        f"tags: {', '.join(doc['tags'])}\n"
        "---\n"
    )


def page(number: int, text: str) -> str:
    return f"\n<!-- page {number} -->\n\n{text.strip()}\n"


def poppler(*args: str) -> str:
    result = subprocess.run(args, capture_output=True, check=True)
    return result.stdout.decode("utf-8")


def pages_of(pdf: Path) -> int:
    """Quante pagine ha il PDF, secondo pdfinfo."""
    for line in poppler("pdfinfo", str(pdf)).splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":")[1])
    raise ValueError(f"pdfinfo non dice quante pagine ha {pdf.name}")


def pdf_page(pdf: Path, number: int) -> str:
    """Il testo di una pagina, senza il form feed che la chiude."""
    text = poppler(
        "pdftotext",
        "-enc",
        "UTF-8",
        "-eol",
        "unix",
        "-f",
        str(number),
        "-l",
        str(number),
        str(pdf),
        "-",
    )
    return text.replace("\f", "")


def pdf_text(pdf: Path) -> str:
    return "".join(
        page(number, pdf_page(pdf, number)) for number in range(1, pages_of(pdf) + 1)
    )


def is_poppler() -> bool:
    """xpdf ha un pdftotext con lo stesso nome, e legge le tabelle in un altro modo."""
    if shutil.which("pdftotext") is None or shutil.which("pdfinfo") is None:
        return False
    result = subprocess.run(["pdftotext", "-v"], capture_output=True, check=False)
    return b"Poppler" in result.stdout + result.stderr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        action="store_true",
        help="riestrae anche i file presenti: le tabelle sistemate a mano si perdono",
    )
    args = parser.parse_args()

    if not is_poppler():
        print(
            "ERRORE  servono pdfinfo e pdftotext di poppler (poppler-utils), "
            "primi nel PATH: quello di xpdf legge le tabelle in un altro modo"
        )
        return 1

    docs = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))["doc"]
    OUT.mkdir(parents=True, exist_ok=True)
    for doc in docs:
        target = OUT / f"{doc['id']}.md"
        pdf = MANUALS / f"{doc['id']}.pdf"
        markdown = MANUALS / f"{doc['id']}.md"
        if target.exists() and not args.force:
            print(f"GIÀ C'È {doc['id']}")
            continue
        if pdf.exists():
            body = pdf_text(pdf)
        elif markdown.exists():
            body = page(1, markdown.read_text(encoding="utf-8"))
        else:
            print(f"MANCA   {doc['id']}: nessun documento in data/manuals/")
            continue
        target.write_text(header(doc) + body, encoding="utf-8", newline="\n")
        print(f"OK      {doc['id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
