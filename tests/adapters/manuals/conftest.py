"""The table of the eval of the retrieval, printed at the end of the run.

test_retrieval.py fills RETRIEVAL: one row per question of the golden set,
with the place of the first passage that answers (None: not in the first
three). A plain pytest captures print: the table goes to the summary.
"""

from typing import Any

RETRIEVAL: list[tuple[str, str, str, int | None]] = []


def pytest_terminal_summary(terminalreporter: Any) -> None:
    if not RETRIEVAL:
        return
    write = terminalreporter.write_line
    terminalreporter.section("retrieval: the manuals, golden set")
    write(f"{'fault':<24}{'tag':<6}{'place':>6}  question")
    for fault, tag, question, place in RETRIEVAL:
        write(f"{fault:<24}{tag:<6}{place or '-':>6}  {question}")
    total = len(RETRIEVAL)
    at_1 = sum(place == 1 for *_, place in RETRIEVAL)
    at_3 = sum(place is not None for *_, place in RETRIEVAL)
    write(f"hit@1 {at_1}/{total} = {at_1 / total:.0%}")
    write(f"hit@3 {at_3}/{total} = {at_3 / total:.0%}")
