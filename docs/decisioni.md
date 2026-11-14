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
- **Codice, non LLM**: approvazione ed esecuzione, allarmi, interlock. *Perché*: devono
  funzionare anche se l'LLM sbaglia, è lento o viene manipolato. Gli allarmi hanno due
  fonti: il controllore dell'impianto riporta fatti ("sonda guasta", "K1 aperto"), il
  sorvegliante a regole fisse giudica il processo ("le due sonde non concordano").
- **Diagnosi su allarme come flusso fisso**. *Perché*: prevedibile, economico, facile da valutare.
  L'agente libero resta per la chat.
- **Memory**: lezioni strutturate (evento, causa, intervento, esito), scritte solo a caso chiuso.
  I numeri restano nel database e si leggono con i tool. *Perché*: evita di avvelenare la memory.
- **RAG classico** (ibrido + rerank) con metadati per componente e sigla. *Perché*: le relazioni
  tra componenti sono già note dalla configurazione dell'impianto, non serve estrarle con un LLM.
  Tabelle dei codici di errore spezzate una riga per chunk.
- **Impianto**: vedi `docs/impianto.md`. Componenti reali con manuali pubblici, tenuti nel repo
  in `data/manuals/`. Cotta da 20 L: le taglie dei recipienti vengono dal fermentatore reale e
  dai conti dell'acqua. Un percorso alla volta; niente riempimento della HLT, sonda TT4,
  deriva, chimica. *Perché*: i requisiti del corso stanno tutti nella parte AI. Un dettaglio
  si simula solo se crea un sintomo che l'agente può vedere, o la conseguenza di un'azione
  che può proporre.
- **Controllore tra AI e impianto**: l'impianto è governato da un controllore simulato (un PLC
  generico). Agenti, sorvegliante ed esecutore vedono e comandano solo attraverso di lui; lui
  conosce solo i segnali dei dispositivi, e ogni dispositivo dice solo ciò che il suo manuale
  prevede. Fuori dal controllore resta la sicurezza cablata (K1), l'unica che agisce sui valori
  veri. *Perché*: è come sono fatti gli impianti veri, e fissa con precisione che cosa un
  agente può osservare. Le tre porte sono l'interfaccia del controllore: con un impianto vero
  cambierebbe solo l'adattatore.
- **Programma della cotta nel controllore**: una ricetta a passi, con conferme del birraio e un
  tempo massimo per passo. *Perché*: dà alla diagnosi il contesto ("siamo nella sosta, minuto
  25 di 60") e un allarme tipico degli impianti veri, il passo in ritardo.
- **Il programma è un birraio fatto di codice**: preme i pulsanti del pannello, quindi gli
  rispondono gli stessi interlock, e non riarma mai un blocco. Quando qualcosa è bloccato va
  in pausa da solo; riprende solo con `reset` e `resume_program`. *Perché*: è la regola del
  controllore che non riparte da solo, e dà alla parte AI un flusso completo: programma in
  pausa, diagnosi, proposta di riarmo e ripresa, approvazione.
- **Comandi con una fine certa**: un travaso è a quantità e si ferma da solo. *Perché*: tra la
  proposta e l'esecuzione c'è un'approvazione umana; uno stop che dipende da una seconda
  approvazione arriverebbe tardi.
- **Il controllore non riparte da solo**: ciò che un interlock ferma resta fermo, con il suo
  allarme, finché il birraio o l'esecutore non riarma (`reset`, o un nuovo comando sulla
  stessa cosa). *Perché*: proseguire dopo un allarme è una decisione di chi ne risponde, e
  dà alla parte AI un flusso completo: allarme, diagnosi, proposta di riarmo, approvazione.
- **Test dell'impianto**: solo scenari sull'impianto intero, attraverso le porte (un test per
  guasto, per interlock e per K1, più i conti della cotta e il determinismo). Niente test
  strato per strato. *Perché*: sono i comportamenti su cui poggiano gli eval; il resto
  toglierebbe tempo alla parte AI. La soglia di copertura della CI non cambia.
- **Simulatore**: servizio separato, un solo worker, modalità a passi per test ed eval, con un
  passo di calcolo fisso. Tiene uno storico breve delle letture e dei comandi, che si legge
  dalla porta `PlantReader`. *Perché*: diagnosi ed eval girano senza database, e lo stesso
  scenario dà sempre lo stesso risultato.
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
- Ordine dopo M1b: il servizio plant-sim subito (M2), oppure dopo il primo agente, gli eval e
  la memory, che girano anche senza il servizio.
- Adattatore verso un controllore vero (per esempio OPC UA): le letture hanno già la sua forma
  (valore, qualità, tempo). Non serve al corso: solo se avanza tempo.
- CI su GitHub: il controllo "Build container image" è rosso anche su `master`. La scansione
  trova due vulnerabilità in `zlib1g` dell'immagine base, e il rapporto non si carica da un
  repo privato. Rimandato: non è un errore della sessione in corso.

## Roadmap

| # | Milestone | Fatto quando |
|---|---|---|
| M0 | Rinomina del package, posti vuoti per l'impianto, contract, script manuali | Controlli della CI verdi |
| M1 | Vocabolario, porte, processo, dispositivi e controllore con comandi manuali, interlock, allarmi e storico breve (Python puro) | Test di plausibilità, interlock e guasti verdi |
| M1b | Programma della cotta nel controllore | Una cotta intera simulata, con 20 L nel fermentatore |
| M2 | Servizio plant-sim, adapter REST, impostazioni, compose, sorvegliante | Test di contratto in-process e REST verdi |
| M3 | Storico su Postgres + Grafana (facoltativo, solo se avanza tempo) | Grafici di una cotta simulata |
| M4 | Server MCP (lettura + proposta) + coda approvazioni ed esecutore; via l'esempio notes | Proposta → approvazione → esecuzione da Claude Desktop |
| M5 | Primo agente (impianto) + tracing + primo eval | Eval pass/fail su 3 scenari |
| M6 | RAG sui manuali + RAGAS | RAGAS sopra soglia |
| M7 | Multi-agente + baseline, guardrail, red teaming, eval in CI, UI | Requisiti del corso coperti |
