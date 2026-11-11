"""Scarica i documenti tecnici elencati in manuals/manifest.toml.

Solo libreria standard (Python 3.11+): gira ovunque, senza installare nulla.

    python scripts/download_manuals.py            # scarica i mancanti
    python scripts/download_manuals.py --force    # riscarica tutto

Risultato in data/manuals/:
- <id>.pdf / <id>.md   i documenti (NON vanno nel repo: sono del produttore)
- index.json           cosa c'è, da dove viene, hash sha256: è l'input del RAG
"""

import argparse
import hashlib
import json
import sys
import tomllib
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "manuals" / "manifest.toml"
OUT = ROOT / "data" / "manuals"
USER_AGENT = "Mozilla/5.0 (neuralbrewery-manuals-downloader)"


def detect_kind(data: bytes) -> str | None:
    """Controlla il contenuto, non l'estensione.

    Molti siti rispondono con una pagina HTML al posto del documento.
    """
    if data.startswith(b"%PDF"):
        return "pdf"
    head = data[:512].lstrip().lower()
    if head.startswith((b"<!doctype html", b"<html")):
        return None
    try:
        data.decode("utf-8")
        return "md"
    except UnicodeDecodeError:
        return None


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def existing_file(doc_id: str) -> Path | None:
    for ext in ("pdf", "md"):
        path = OUT / f"{doc_id}.{ext}"
        if path.exists():
            return path
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force", action="store_true", help="riscarica anche i file presenti"
    )
    args = parser.parse_args()

    docs = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))["doc"]
    OUT.mkdir(parents=True, exist_ok=True)
    index: list[dict] = []
    todo_by_hand: list[dict] = []
    failed: list[tuple[str, str]] = []

    for doc in docs:
        path = existing_file(doc["id"])

        if doc["auto"] and (path is None or args.force):
            try:
                data = download(doc["url"])
                kind = detect_kind(data)
                if kind is None:
                    raise ValueError("il server non ha restituito un PDF o un testo")
                path = OUT / f"{doc['id']}.{kind}"
                path.write_bytes(data)
                print(f"OK      {doc['id']}  ({len(data) // 1024} KB)")
            except (urllib.error.URLError, TimeoutError, ValueError) as exc:
                failed.append((doc["id"], str(exc)))
                print(f"ERRORE  {doc['id']}: {exc}")
                continue
        elif path is not None:
            print(f"GIÀ OK  {doc['id']}")

        if path is None:
            todo_by_hand.append(doc)
            continue

        data = path.read_bytes()
        index.append(
            {
                "id": doc["id"],
                "file": path.name,
                "sha256": hashlib.sha256(data).hexdigest(),
                "size_bytes": len(data),
                "indexed_at": datetime.now(UTC).isoformat(timespec="seconds"),
                **{
                    k: doc[k]
                    for k in ("component", "product", "tags", "doc_type", "source")
                },
                "origin": doc.get("url") or doc.get("page"),
            }
        )

    (OUT / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"\n{len(index)}/{len(docs)} documenti pronti in {OUT.relative_to(ROOT)}/")
    for doc in todo_by_hand:
        print(f"  A MANO  {doc['id']}.pdf  <-  {doc['page']}")
        if note := doc.get("note"):
            print(f"          {note}")
    for doc_id, reason in failed:
        print(f"  RIPROVA {doc_id}: {reason}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
