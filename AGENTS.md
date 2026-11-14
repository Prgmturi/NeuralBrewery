# AGENTS.md

Istruzioni per gli agenti di coding (Claude Code, GitHub Copilot) che lavorano su questo repo.

## Il progetto

**NeuralBrewery**, progetto finale del corso AI: un assistente multi-agente per un impianto di birrificazione
simulato. Monitora l'impianto, diagnostica i problemi usando i manuali tecnici dei componenti
(RAG) e la memoria delle cotte passate, e propone azioni che vengono eseguite solo dopo
l'approvazione del birraio.

Il repo nasce dal template `fastapi_starter`: le sue regole valgono anche qui.

## Leggi prima di iniziare

- `docs/decisioni.md`: cosa è deciso, come si innesta nel template, cosa è aperto, roadmap.
- `docs/impianto.md`: il controllore e cosa espone, componenti, sigle, percorsi, interlock,
  programma della cotta, guasti, controlli di plausibilità.
- `docs/architecture.md`, almeno il livello 1: dove va il codice e perché.
- `docs/development.md`: strumenti, test, CI.
- `docs/adr/`: le decisioni del template. Una decisione architetturale nuova diventa un ADR
  con il numero successivo, nello stesso formato.
- `_reference/gateway-demo/`: prototipo funzionante del confine AI–impianto. È un riferimento
  da adattare alle convenzioni di questo repo, non da copiare. Non va modificato.

## Dove vive l'impianto

```
src/neuralbrewery/
  core/plant/schemas.py      vocabolario: Reading, PlantState, Route, CommandResult, Fault...
  core/plant/protocols.py    porte: PlantReader, PlantCommander, SimulationControl
  core/plant/watcher.py      il sorvegliante: regole fisse sul processo, solo PlantReader
  core/config/plant.py       impostazioni: adattatore, URL, token
  adapters/plant_sim/        l'impianto simulato: processo, dispositivi, controllore
                             (interlock, programma, allarmi), guasti, adattatore
                             in-process (test ed eval)
  adapters/plant_rest/       client httpx verso il servizio plant-sim
  plant_service.py           entry point del servizio plant-sim (FastAPI, un solo worker)
  bootstrap.py               sceglie l'adattatore e lo mette in app.state
  features/                  (dopo) plant, approvals, agents...
```

- Un solo package e una sola immagine; nel compose due servizi: `api` e `plant-sim`.
- Le tre porte sono l'interfaccia del controllore dell'impianto, non dei singoli dispositivi:
  - `PlantReader`: lettura. La usano agenti, server MCP, sorvegliante.
  - `PlantCommander`: comandi ad alto livello. La usa **solo** l'esecutore delle azioni approvate.
  - `SimulationControl`: tempo e guasti. La usano **solo** test, eval e demo; mai in produzione.

## Regole non negoziabili

1. **Nessun agente riceve `PlantCommander`.** Gli agenti leggono e propongono; l'esecutore
   esegue solo proposte approvate. L'approvazione è codice, mai una decisione dell'LLM.
2. **La sicurezza dell'impianto sta nel simulatore**: negli interlock del controllore e nella
   sicurezza cablata (K1). Il guardrail dell'agente è un secondo livello, non l'unico.
   Il controllore non riparte mai da solo dopo un intervento: riarma solo il birraio, o
   l'esecutore con un'azione approvata.
3. **Comandi ad alto livello.** Percorsi predefiniti, quantità e setpoint, mai "apri la
   valvola X". Ogni comando ha una fine certa.
4. **Valore vero e valore misurato sono separati.** Il processo non sa come viene misurato;
   rumore, tolleranze e guasti di misura vivono nei dispositivi. Il controllore legge solo i
   segnali dei dispositivi, mai i valori veri; l'app vede solo ciò che vede il controllore.
   L'unica eccezione è la sicurezza cablata.
5. **Tempo simulato ovunque.** Ogni dato porta il tempo simulato. Il modello non legge mai
   l'orologio reale.
6. **Determinismo.** Stesso seed e stesse azioni devono dare lo stesso stato: gli eval ci contano.
7. **`adapters/plant_sim/` è Python puro**: niente FastAPI, httpx, SQLAlchemy (import contract).
8. **I manuali dei produttori stanno nel repo**, in `data/manuals/`: chi usa il progetto li
   trova già pronti. Solo documenti pubblici, ognuno con la sua fonte in `manuals/manifest.toml`.

## Convenzioni del codice (dal template)

- **Gli import scendono.** Entry point (`main.py`, `serve.py`, `healthcheck.py`; da M2 anche
  `plant_service.py`) → `bootstrap.py` | `exception_handlers.py` → `features/` | `adapters/` →
  `core/`. Feature e adapter non si importano mai a vicenda. `uv run lint-imports` lo verifica; un confine nuovo merita
  un contract nuovo in `pyproject.toml`.
- **Porte** = classi `Protocol`, in `core/.../protocols.py` se condivise o in
  `features/<x>/domain/protocols.py` se di una sola feature. I tipi che servono a una porta
  stanno in un modulo `schemas`, mai in un adapter.
- **Adapter** in `adapters/<servizio>/`. Traducono ogni errore della loro libreria nelle
  eccezioni di `core/exceptions.py` (ADR 0006): servizio irraggiungibile → `ServiceUnavailableError`
  (503), risposta inutilizzabile → `ExternalServiceError` (502). Un comando rifiutato da un
  interlock non è un errore: è un `CommandResult` con il motivo.
- **Wiring solo in `bootstrap.py`**, con uno `StateKey` per porta (`core/state.py`).
- **Una feature** copia la forma di `features/notes`: `api/` → `persistence/` → `domain/`, con il
  dominio in Python puro. Senza regole proprie può restare piatta, come `features/auth`.
- **Impostazioni** in `core/config/`, una sezione per argomento. Un valore di sviluppo
  pericoloso va aggiunto a `production_problems()` (ADR 0007).
- **App factory**: `create_app(settings)`; i test costruiscono le impostazioni, non leggono `.env`.
- **Errori dell'API** in formato RFC 9457; **log** con structlog, mai `print`.
- **Test** async, con fake o `AsyncMock` fuori da `tests/integration/`; marker `integration`
  (Postgres vero) ed `e2e` (stack completo). La copertura ha una soglia minima.
- **mypy strict, ruff**, Python 3.13.
- **Commit** in Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`, `refactor:`...):
  commitlint li controlla.
- **I commit portano solo il nome di chi sviluppa.** Un agente non si firma mai: niente
  `Co-Authored-By`, niente riga "Generated with", né nei commit né nelle pull request.

## Comandi

```bash
uv sync
uv run pre-commit install
uv run ruff check . && uv run ruff format --check .
uv run mypy src/
uv run lint-imports
uv run pytest                 # unit test
uv run pytest --cov           # come la CI
uv run pytest -m integration  # serve Postgres, vedi docs/development.md
uv run pytest -m e2e          # serve lo stack: docker compose up --build --wait
python scripts/download_manuals.py   # scarica in data/manuals/ i manuali che mancano
```

## Come lavorare

- Una milestone per sessione (roadmap in `docs/decisioni.md`). Niente lavoro fuori scope.
- Prima proponi il piano (file e test), aspetta l'ok, poi scrivi.
- Prima i test, poi il codice: plausibilità fisica, interlock, contratto delle porte.
  Per l'impianto solo scenari attraverso le porte, non test strato per strato
  (`docs/decisioni.md`).
- Nessuna nuova dipendenza senza chiedere.
- KISS: la soluzione più semplice che rispetta le regole sopra.
- Se una decisione cambia, aggiorna `docs/decisioni.md` o `docs/impianto.md` nello stesso commit
  e segnalalo.
- Fine sessione: tutti i controlli della CI verdi, commit, elenco breve di cosa è cambiato.
- Fine fase: di' a chi sviluppa cosa deve controllare e quali dubbi restano, guardando lo stato
  vero (PR e CI su GitHub, non solo i controlli locali). Il prompt della fase successiva, in
  `docs/prompts/`, si scrive solo quando quei punti sono risolti.
