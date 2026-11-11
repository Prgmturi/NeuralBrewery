# Decisioni di progetto

## In una frase

Un sistema multi-agente per un impianto di birrificazione simulato: monitora i sensori,
diagnostica i problemi usando RAG sui manuali e la memoria delle cotte passate, e propone
azioni che vengono eseguite solo con l'approvazione del birraio, con guardrail e audit trail
su ogni passaggio.

## Requisiti del corso e dove li copriamo

| Requisito | Dove |
|---|---|
| Tool calling | Lettura impianto, calcoli, proposta azioni |
| Client multi-provider | Modello economico per orchestratore e spiegazioni, modello forte per l'analista |
| Memory persistente | Lezioni strutturate dalle cotte passate |
| Architettura giustificata | Multi-agente per privilegio minimo, confrontato con una baseline ad agente singolo |
| Flusso fisso (DagPipeline o equivalente) | Diagnosi su allarme: dati → memory → manuali → ipotesi → proposta |
| Guardrail | Ingresso, parametri dei tool, uscita |
| Audit trail | Tracing di ogni passo + tabella di audit append-only (proposte, approvazioni, esecuzioni) |
| Eval pass/fail | Scenari di guasto con seed fisso (trajectory) + RAGAS sui manuali |
| README, deve girare | docker compose; al tester serve solo una chiave API |
| RAG (facoltativo) | Manuali dei componenti, ricerca ibrida + rerank |

## Scelte fatte

- **Agenti**: orchestratore (parla con l'utente), agente impianto (unico che propone azioni),
  agente analista (dati, calcoli, diagnosi). *Perché*: privilegi separati; chi legge testo non
  fidato non deve poter proporre azioni.
- **Codice, non LLM**: approvazione ed esecuzione, allarmi (sorvegliante a regole fisse),
  interlock. *Perché*: devono funzionare anche se l'LLM sbaglia, è lento o viene manipolato.
- **Diagnosi su allarme come flusso fisso**. *Perché*: prevedibile, economico, facile da valutare.
  L'agente libero resta per la chat.
- **Memory**: lezioni strutturate (evento, causa, intervento, esito), scritte solo a caso chiuso.
  I numeri restano nel database e si leggono con i tool. *Perché*: evita di avvelenare la memory.
- **RAG classico** (ibrido + rerank) con metadati per componente e sigla. *Perché*: le relazioni
  tra componenti sono già note dalla configurazione dell'impianto, non serve estrarle con un LLM.
  Tabelle dei codici di errore spezzate una riga per chunk.
- **Impianto**: vedi `docs/impianto.md`. Componenti reali con manuali pubblici.
- **Simulatore**: servizio separato, un solo worker, modalità a passi per test ed eval.
- **Confine AI–impianto**: porte e adattatori (vedi `AGENTS.md`).
- **Base del codice**: template `fastapi_starter` (FastAPI, PostgreSQL, Alembic, structlog,
  SQLAlchemy async, Keycloak, uv, import-linter, CI, release-please).
- **Nome**: il progetto si chiama NeuralBrewery. Repo `NeuralBrewery`; package Python, immagine
  Docker e nomi tecnici (realm e client Keycloak) `neuralbrewery`, una sola forma minuscola
  senza trattini né underscore, come richiedono package e immagini. La versione riparte da 0.1.0
  con un CHANGELOG vuoto: la storia del template non è la storia di questo progetto.

## Come si innesta nel template

- **Un solo package, una sola immagine, due servizi nel compose**: `api` (il backend del
  template) e `plant-sim` (stessa immagine, comando diverso, un solo worker).
- **Il simulatore vive in `adapters/plant_sim/`.** Per il backend l'impianto è un servizio
  esterno, e il template vieta già alle feature di importare gli adapter: per toccare
  l'impianto devono passare dalle porte, e la CI lo controlla.
- **Porte e vocabolario in `core/plant/`**, come `core/auth/` per il login.
- **Errori**: l'adapter REST traduce gli errori di httpx nelle eccezioni del template (ADR 0006).
  Al posto del `PlantUnavailableError` del prototipo si usa `ServiceUnavailableError`.
- **Impostazioni** in `core/config/plant.py`. `production_problems()` rifiuta i token di
  sviluppo e il controllo della simulazione fuori dallo sviluppo (ADR 0007).
- **I processi restano separati**: nel compose il backend parla con `plant-sim` solo via REST,
  con il token dell'esecutore per i comandi.
- **Alternativa scartata**: workspace uv con due package. Separazione più netta, ma va
  adattato tutto il tooling del template (Dockerfile, CI, test su lockfile e package).
- **L'esempio `features/notes` resta** finché non c'è una nostra feature a tre strati: su di
  lui poggiano due contract, il test e2e e lo smoke test della CI.

## Ancora aperte

- Framework agenti: LangChain/LangGraph o datapizza-ai.
- Modelli e provider concreti.
- Tracing: Langfuse o Phoenix.
- Keycloak: utile per l'identità di chi approva; da valutare il peso nel compose per il tester.
- MQTT: solo se serve, dopo.
- UI e notifiche.

## Roadmap

| # | Milestone | Fatto quando |
|---|---|---|
| M0 | Rinomina del package, posti vuoti per l'impianto, contract, script manuali | Controlli della CI verdi |
| M1 | Vocabolario, porte e modello dell'impianto (Python puro) | Test di plausibilità, interlock e guasti verdi |
| M2 | Servizio plant-sim, adapter REST, impostazioni, compose | Test di contratto in-process e REST verdi |
| M3 | Storico su Postgres + Grafana | Grafici di una cotta simulata |
| M4 | Server MCP (lettura + proposta) + coda approvazioni ed esecutore; via l'esempio notes | Proposta → approvazione → esecuzione da Claude Desktop |
| M5 | Primo agente (impianto) + tracing + primo eval | Eval pass/fail su 3 scenari |
| M6 | RAG sui manuali + RAGAS | RAGAS sopra soglia |
| M7 | Multi-agente + baseline, guardrail, red teaming, eval in CI, UI | Requisiti del corso coperti |
