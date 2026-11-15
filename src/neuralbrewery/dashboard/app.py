"""The brewer's dashboard: the plant, the simulation, the diagnosis, the queue.

    uv run streamlit run src/neuralbrewery/dashboard/app.py

or the dashboard service of compose.yaml, on http://localhost:8501. The
page talks to the API at DASHBOARD_API_URL, as curl would, and approves
with DASHBOARD_APPROVAL_TOKEN, which it never shows.

Nothing runs in the background: the page runs again when the brewer
presses or types something, and the plant moves only through the commands
of the simulation. Each action is a callback, so it runs before the page
is drawn again, and the page shows the plant after it.
"""

from collections.abc import Callable
from functools import partial
from typing import Any

import streamlit as st

from neuralbrewery.dashboard import client
from neuralbrewery.dashboard.client import Api, ApiError
from neuralbrewery.dashboard.labels import (
    EVENT,
    FAULT_KINDS,
    FAULT_TYPE,
    PROGRAM,
    PROPOSABLE,
    STATUS,
    clock,
)

JSON = dict[str, Any]
Notice = tuple[str, str] | None  # kind (success, warning, error) and text

NAME_FIRST = "Scrivi il tuo nome nella barra a sinistra: l'audit registra chi decide."
SHOW = {"success": st.success, "warning": st.warning, "error": st.error}


# ---------------------------------------------------------------------------
# What the brewer does: each action runs as a callback, before the page
# ---------------------------------------------------------------------------


def act(action: Callable[[], Notice]) -> None:
    """Run an action of the brewer, and keep what came of it, in words."""
    try:
        st.session_state.notice = action()
    except ApiError as error:
        st.session_state.notice = ("error", str(error))


def signed() -> str:
    return str(st.session_state.get("brewer") or "").strip()


def propose(api: Api) -> Notice:
    by = signed()
    if not by:
        return ("error", NAME_FIRST)
    command = st.session_state.propose_command
    proposal = api.propose(command, st.session_state.get("propose_why") or "", by)
    if proposal["status"] == "blocked":
        return ("warning", f"Bloccata dal guardrail: {proposal['blocked_reason']}")
    return ("success", f"In coda: {command}. Aspetta la tua approvazione, qui sotto.")


def approve(api: Api, proposal_id: str) -> Notice:
    by = signed()
    if not by:
        return ("error", NAME_FIRST)
    proposal = api.approve(proposal_id, by)
    command = proposal["action"]["command"]
    outcome = proposal["events"][-1]["data"]
    if proposal["status"] == "execution_failed":
        return ("error", f"L'impianto non ha risposto a {command}: {outcome['error']}")
    if not outcome["accepted"]:
        return (
            "warning",
            f"Il controllore ha rifiutato {command}: {outcome['code']}, "
            f"{outcome['reason']}",
        )
    return ("success", f"Eseguita: il controllore ha accettato {command}.")


def reject(api: Api, proposal_id: str) -> Notice:
    by = signed()
    if not by:
        return ("error", NAME_FIRST)
    reason = str(st.session_state.get(f"reason-{proposal_id}") or "").strip()
    proposal = api.reject(proposal_id, by, reason)
    return ("success", f"Rifiutata: {proposal['action']['command']}.")


def diagnose(api: Api) -> Notice:
    st.session_state.diagnosis = None  # an old diagnosis is not this one
    with st.spinner("L'agente legge l'impianto e le decisioni passate…"):
        st.session_state.diagnosis = api.diagnose()
    return None


def advance(api: Api) -> Notice:
    moved = api.advance(st.session_state.advance_s)
    st.session_state.judgements = moved["judgements"]
    return ("success", f"Tempo simulato: {clock(moved['sim_time_s'])}.")


def inject(api: Api) -> Notice:
    kind = st.session_state.fault_kind
    target = str(st.session_state.fault_target).strip()
    api.inject_fault(kind, target, st.session_state.get("fault_value"))
    return ("success", f"Guasto iniettato: {kind} su {target}. Avanza il tempo.")


def clear(api: Api) -> Notice:
    api.clear_faults()
    return (
        "success",
        "Guasti tolti. Il controllore non riarma da solo: ciò che ha fermato "
        "resta fermo.",
    )


# ---------------------------------------------------------------------------
# What the page shows
# ---------------------------------------------------------------------------


def connection() -> Api:
    """One client for the session of this browser tab."""
    if "api" not in st.session_state:
        st.session_state.api = client.connect()
    api: Api = st.session_state.api
    return api


def simulation_on(api: Api) -> bool:
    """Asked once per session: the API does not change it while it runs."""
    if "simulation" not in st.session_state:
        st.session_state.simulation = api.simulation_on()
    return bool(st.session_state.simulation)


def sidebar(api: Api, simulation: bool) -> None:
    with st.sidebar:
        st.text_input("Il tuo nome, per l'audit", key="brewer")

        st.subheader("Proponi un pulsante")
        st.selectbox("Pulsante", PROPOSABLE, key="propose_command")
        st.text_input("Perché", key="propose_why")
        st.button("Proponi", key="propose", on_click=act, args=(partial(propose, api),))

        if not simulation:
            return
        st.subheader("Simulazione")
        st.number_input(
            "Secondi da avanzare",
            min_value=1,
            max_value=86400,
            value=300,
            step=60,
            key="advance_s",
        )
        st.button(
            "Avanza il tempo",
            key="advance",
            on_click=act,
            args=(partial(advance, api),),
        )
        st.selectbox("Guasto", FAULT_KINDS, key="fault_kind")
        st.text_input("Sigla", value="TT1", key="fault_target")
        st.number_input(
            "Valore, per i guasti che lo chiedono", value=None, key="fault_value"
        )
        st.button(
            "Inietta il guasto",
            key="inject",
            on_click=act,
            args=(partial(inject, api),),
        )
        st.button(
            "Togli i guasti", key="clear", on_click=act, args=(partial(clear, api),)
        )


def notice() -> None:
    """What came of the last action, until the next one."""
    shown = st.session_state.get("notice")
    if shown:
        kind, text = shown
        SHOW[kind](text)


def plant_section(plant: JSON) -> None:
    st.header("Impianto")
    program = plant["program"]
    now, status, step = st.columns(3)
    now.metric("Tempo simulato", clock(plant["sim_time_s"]))
    status.metric("Programma", PROGRAM.get(program["status"], program["status"]))
    if program["step"] is None:
        step.metric("Passo", "—")
    else:
        step.metric("Passo", f"{program['step']} · {program['step_name']}")
        limit = f" su {clock(program['max_s'])}" if program["max_s"] else ""
        step.caption(f"Da {clock(program['elapsed_s'])}{limit}")
    if program["reason"]:
        st.caption(f"In pausa: {program['reason']}")

    if not plant["alarms"]:
        st.success("Nessun allarme")
    for alarm in plant["alarms"]:
        st.error(f"**{alarm['tag']}** · {alarm['text']} · `{alarm['code']}`")
    for judgement in st.session_state.get("judgements") or []:
        st.warning(f"Sorvegliante · **{judgement['tag']}** · {judgement['text']}")

    st.dataframe(
        [
            {
                "Sigla": tag,
                "Valore": reading["value"],
                "Unità": reading["unit"],
                "Qualità": reading["quality"],
                "Motivo": reading["reason"],
            }
            for tag, reading in plant["readings"].items()
        ],
        hide_index=True,
    )
    with st.expander("Regolazione, travaso e dispositivi"):
        st.json(
            {
                "regolazione": plant["regulation"],
                "travaso": plant["transfer"],
                "dispositivi": plant["devices"],
            },
            expanded=False,
        )


def diagnosis_section(api: Api) -> None:
    st.header("Diagnosi")
    st.button(
        "Diagnostica adesso",
        key="diagnose",
        type="primary",
        on_click=act,
        args=(partial(diagnose, api),),
    )
    st.caption(
        "L'agente legge l'impianto e le tue decisioni sulle sue ultime proposte. "
        "Su Claude costa qualche centesimo."
    )
    answer = st.session_state.get("diagnosis")
    if not answer:
        return
    run = answer["run"]
    diagnosis = run["diagnosis"]
    if diagnosis is None:
        st.warning(f"Nessuna diagnosi ({run['outcome']}): {run['detail']}")
    else:
        sure = "confermata" if diagnosis["confirmed"] else "da confermare"
        kind = FAULT_TYPE.get(diagnosis["fault_type"], diagnosis["fault_type"])
        st.markdown(f"**{diagnosis['component']}** · {kind} · {sure}")
        st.info(diagnosis["explanation"])
        if diagnosis["checks"]:
            checks = "\n".join(f"- {check}" for check in diagnosis["checks"])
            st.markdown(f"**Verifiche a mano**\n\n{checks}")
        proposal_of(diagnosis["proposal"], answer["queued"])
    with st.expander(
        f"Passi dell'agente · token: {run['input_tokens']} in entrata fuori dalla "
        f"cache, {run['cached_tokens']} letti dalla cache, {run['output_tokens']} "
        "in uscita"
    ):
        # The API does not report what is written into the cache: the cost of a
        # diagnosis is measured by the evals, on the answers of the provider
        st.caption("Le scritture nella cache non sono contate.")
        for step in run["steps"]:
            if step["kind"] == "tool":
                st.markdown(f"tool `{step['name']}` {step['arguments']}")
            else:
                st.markdown(
                    f"modello {step['name']} · {step['input_tokens']} token in "
                    f"entrata fuori dalla cache, {step['cached_tokens']} letti dalla "
                    f"cache, {step['output_tokens']} in uscita"
                )


def proposal_of(proposal: JSON | None, queued: JSON | None) -> None:
    """The button the diagnosis proposes, and what the queue made of it."""
    if proposal is None:
        st.markdown("Nessuna proposta: prima le verifiche.")
        return
    arguments = {k: v for k, v in proposal.items() if k != "command" and v is not None}
    st.markdown(f"**Proposta**: `{proposal['command']}` {arguments or ''}")
    if queued is not None and queued["status"] == "blocked":
        st.warning(f"Bloccata dal guardrail: {queued['reason']}")
    else:
        st.markdown("In coda, in attesa della tua decisione.")


def queue_section(api: Api) -> None:
    st.header("Coda delle proposte")
    try:
        proposals = api.proposals()
    except ApiError as error:
        st.error(str(error))
        return
    if not proposals:
        st.caption("Nessuna proposta.")
    for proposal in proposals:
        proposal_card(api, proposal)


def status_of(proposal: JSON) -> str:
    """Executed means the controller answered: a refusal is an answer too."""
    status: str = proposal["status"]
    if status == "executed" and not proposal["events"][-1]["data"]["accepted"]:
        return "rifiutata dal controllore"
    return STATUS.get(status, status)


def event_line(event: JSON) -> str:
    """One step of a proposal: what, who as declared, when in simulated time."""
    line = (
        f"{EVENT.get(event['kind'], event['kind'])} · {event['actor']} · "
        f"{event['by']} · {clock(event['sim_time_s'])}"
    )
    data = event["data"]
    if event["kind"] == "rejected" and data.get("reason"):
        return f"{line} · «{data['reason']}»"
    if event["kind"] == "executed":
        answer = "accettata" if data["accepted"] else "rifiutata dal controllore"
        return f"{line} · {answer}: {data['code']} {data['reason']}".rstrip()
    if event["kind"] == "execution_failed":
        return f"{line} · {data['error']}"
    return line


def proposal_card(api: Api, proposal: JSON) -> None:
    proposal_id = proposal["id"]
    action = proposal["action"]
    birth = proposal["events"][0]
    with st.container(border=True):
        arguments = f" {action['arguments']}" if action["arguments"] else ""
        st.markdown(
            f"**`{action['command']}`**{arguments} · **{status_of(proposal)}** · "
            f"da {birth['actor']} · {birth['by']}"
        )
        if proposal["why"]:
            st.caption(proposal["why"])
        if proposal["blocked_reason"]:
            st.markdown(f"Motivo del blocco: {proposal['blocked_reason']}")
        for event in proposal["events"][1:]:
            st.caption(event_line(event))
        if proposal["status"] != "proposed":
            return
        st.text_input(
            "Motivo del rifiuto",
            key=f"reason-{proposal_id}",
            placeholder="Facoltativo: finisce nell'audit, e l'agente lo legge",
        )
        left, right = st.columns(2)
        left.button(
            "Approva",
            key=f"approve-{proposal_id}",
            type="primary",
            on_click=act,
            args=(partial(approve, api, proposal_id),),
        )
        right.button(
            "Rifiuta",
            key=f"reject-{proposal_id}",
            on_click=act,
            args=(partial(reject, api, proposal_id),),
        )


def main() -> None:
    st.set_page_config(page_title="NeuralBrewery · birraio", layout="wide")
    st.title("NeuralBrewery · la dashboard del birraio")
    api = connection()
    try:
        plant = api.plant()
        simulation = simulation_on(api)
    except ApiError as error:
        st.error(str(error))
        st.stop()
    sidebar(api, simulation)
    notice()
    plant_section(plant)
    diagnosis_section(api)
    queue_section(api)


# Streamlit runs the page as __main__, and so does streamlit.testing.
# Imported as a module, by a test that imports every module of the app,
# it draws nothing and calls no API.
if __name__ == "__main__":
    main()
