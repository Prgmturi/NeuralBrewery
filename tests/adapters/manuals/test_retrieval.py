"""The eval of the retrieval: does the search find the page that answers?

Under test: src/neuralbrewery/adapters/manuals/index.py, on the real text
of the manuals (data/manuals/text/).

WHY this eval exists: the agent cites what the search gives it. Free,
deterministic and with no network, it runs with the other tests, in CI.

The golden set: one question for each injectable fault of docs/impianto.md
that has a manual saying something about it, written as the agent would
write it (in English, with the tag of the component). The pages that
answer were checked by hand on the PDF; a fact stated on two pages counts
on either. Left out, and why:
- pump_blocked (P1, P2), glycol_failed (CHILLER), fermentation_stuck
  (FERM): their manuals did not download (pump, chiller, fermenter);
- ssr_shorted and heater_open (R1-R4): the datasheet of the Crydom D2425
  has ratings and wiring, and no word on a relay that fails closed or on
  an open heater;
- level_stuck (LT1-LT4): the SICK manuals say nothing of a value that
  freezes with a good signal.

hit@k: the share of questions with an answering page among the first k
passages. The table is printed at the end of the run (conftest.py).
"""

from pathlib import Path

import pytest

from neuralbrewery.adapters.manuals.index import ManualIndex
from tests.adapters.manuals.conftest import RETRIEVAL

TEXT = Path(__file__).parents[3] / "data" / "manuals" / "text"

V20 = "vfd-siemens-v20-getting-started"
TMT80 = "transmitter-itemp-tmt80"
TM411 = "pt100-itherm-tm411"
SICK = "level-sick-lfp-cubic-instructions"
ISPINDEL = "hydrometer-ispindel"
VALVE = "valve-ussolid-motorized"

# fault, question, tag, the pages that answer
GOLDEN = [
    ("drive_fault", "F11 fault code", "M1", {(V20, 55)}),
    (
        "probe_broken",
        "transmitter output current 21.5 mA sensor breakage",
        "TT1",
        {(TMT80, 2), (TMT80, 6)},
    ),
    (
        "probe_offset",
        "PT100 maximum measurement error tolerance class A",
        "TT5a",
        {(TM411, 16), (TM411, 18)},
    ),
    (
        "signal_cable_broken",
        "analog output current lost cable break",
        "LT1",
        {(SICK, 54), (SICK, 29)},
    ),
    (
        "level_foam",
        "level occasionally jumps to a higher value foam",
        "LT2",
        {(SICK, 54)},
    ),
    ("hydrometer_battery_low", "battery voltage low", "DT1", {(ISPINDEL, 1)}),
    (
        "hydrometer_wifi_lost",
        "WiFi connection lost data not sent",
        "DT1",
        {(ISPINDEL, 1)},
    ),
    (
        "valve_stuck",
        "valve stuck does not open or close",
        "EV5",
        {(VALVE, 7), (VALVE, 8)},
    ),
]

HIT_AT_1 = 0.8  # at least, over the golden set
K = 3


@pytest.fixture(scope="module")
def manuals() -> ManualIndex:
    return ManualIndex.from_folder(TEXT)


def rank(manuals: ManualIndex, question: str, tag: str, answers: set) -> int | None:
    """Where the first answering passage is, from 1; None if not in the first K."""
    found = manuals.search(question, tag=tag, limit=K)
    for place, passage in enumerate(found, start=1):
        if (passage.document, passage.page) in answers:
            return place
    return None


def test_hit_at_3_on_every_question_and_hit_at_1_on_most(manuals):
    """[HP] Every fault finds its page in the first three; most, first."""
    places = {
        fault: rank(manuals, question, tag, answers)
        for fault, question, tag, answers in GOLDEN
    }
    RETRIEVAL.extend(
        (fault, tag, question, places[fault]) for fault, question, tag, _ in GOLDEN
    )

    missed = [fault for fault, place in places.items() if place is None]
    first = sum(place == 1 for place in places.values())
    assert missed == []
    assert first / len(GOLDEN) >= HIT_AT_1, places


@pytest.mark.parametrize(
    ("code", "meaning", "next_row"),
    [
        ("F11", "Motor overtemperature", "DC ripple"),
        ("F20", "DC ripple too high", "Motor overtemperature"),
    ],
)
def test_a_code_of_the_v20_gives_its_own_meaning(manuals, code, meaning, next_row):
    """[SEC] The trap: with pdftotext -layout F11 read "DC ripple too high".

    That is F20, two rows below. The agent would have cited the wrong
    meaning with the right page.
    """
    [first, *_] = manuals.search(code, tag="M1")

    assert (first.document, first.page) == (V20, 55)
    assert meaning in first.text
    assert next_row not in first.text


@pytest.mark.parametrize(
    ("query", "parameter", "meaning", "other"),
    [
        ("actual motor temperature", "r0035", "Actual motor temperature", "r0039"),
        ("r0039", "r0039", "Energy consumpt. meter", "r0035"),
    ],
)
def test_a_parameter_of_the_v20_gives_its_own_meaning(
    manuals, query, parameter, meaning, other
):
    """[SEC] The same trap on the parameter list (pp. 45-53).

    The plain text put the codes of p.46 apart from their descriptions,
    r0035 and r0039 first, then what they mean: live, the agent wrote
    "r0039 = motor temperature", which is r0035. Each parameter is now a
    row of its own, checked on the PDF.
    """
    [first, *_] = manuals.search(query, tag="M1")
    row = first.text.splitlines()[-1]

    assert (first.document, first.page) == (V20, 46)
    assert parameter in row
    assert meaning in row
    assert other not in row
