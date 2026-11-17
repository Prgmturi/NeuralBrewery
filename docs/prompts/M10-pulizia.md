Leggi AGENTS.md, poi docs/decisioni.md: "Requisiti del corso e dove li copriamo" e la roadmap. Poi il README.

Obiettivo di questa sessione (M10): **un repo più piccolo e più chiaro**, prima di renderlo pubblico. Si tolgono o si accorciano file, documenti e informazioni che:
- non servono al corso AI (che cosa chiede: la tabella dei requisiti in `decisioni.md`);
- non servono a chi sviluppa per capire il progetto;
- rendono il repo inutilmente lungo.

L'agente e la demo non cambiano.

Il discorso è il 19 novembre, e la prova della demo è il 18, sulla cartella principale. Questo branch si unisce **solo dopo una prova riuscita, o dopo il discorso**: per provare la demo non serve.

## Prima il piano, poi aspetta l'ok

Questa volta il piano non è approvato, e prima di cancellare qualunque cosa mi presenti una tabella:

| Cosa | Proposta: tieni, accorcia o togli | Perché | Rischio | Livello |
|---|---|---|---|---|

I livelli sono due:
- **livello 1**: documenti e file morti. Il rischio è basso, si può fare subito;
- **livello 2**: codice del template. Il rischio cade sulla demo.

Poi aspetta il mio ok, riga per riga. Decido io, non tu, in particolare:
- **`docs/prompts/`**: sono la traccia di come il progetto è stato costruito con agenti di coding e AGENTS.md, che il corso cita;
- **se il livello 2 aspetta il dopo-discorso.**

Scrivi il piano in italiano semplice: per ogni proposta un esempio e la conseguenza.

## Cosa ho già trovato

Sono punti di partenza: verificali, non prenderli per buoni. Il repo nasce dal template `fastapi_starter` e porta pezzi che la demo non usa:
- **le note**: `features/notes`, la sua migrazione (`badd4ec74942`) e i test. È l'esempio CRUD del template.
- **il login**:
  - `features/auth`, `core/auth` e `adapters/keycloak`;
  - i servizi `keycloak` e `keycloak-db` del compose;
  - `docs/authentication.md` e le ADR 0002 e 0003;
  - circa 1.500 righe di test;
  - il job della CI "Log in through the whole stack".

  Il README dice già che la demo non lo usa. Toglierlo ha un vantaggio vero: Keycloak è il servizio più lento ad avviarsi (fino a 5 minuti la prima volta), e voglio che tutto parta con pochi comandi.
- **la produzione**: `compose.prod.yaml`, `docs/production.md`, `docs/operations.md` e `docs/nginx.conf`.
- **i documenti del template**: `docs/architecture.md` (1.107 righe), `docs/frontend.md`, `docs/database.md` e le ADR.
- **il rilascio**:
  - release-please: `release.yml`, `release-please-config.json` e `.release-please-manifest.json`;
  - `CHANGELOG.md`, vuoto;
  - `tests/test_release.py`;
  - la PR #11 del bot.

  Probabilmente il repo pubblico partirà con una storia nuova, e allora il changelog perde senso.
- **gli strumenti di processo**: commitlint (`package.json`, `commitlint.config.js`, `commits.yml`), Dependabot, `test_supply_chain.py`, `test_tooling.py` e `test_lockfile.py`. Per ciascuno: serve al corso o a capire il progetto, o è solo peso?
- **i documenti lunghi del progetto**: `decisioni.md` (542 righe), `impianto.md` (436), `development.md` (325) e il README (292). In `decisioni.md` ci sono molti resoconti degli eval giro per giro.

## Regole di questa sessione

- **Non toccare l'agente né ciò che legge**:
  - `features/agents` (il prompt e i tool);
  - `adapters/plant_sim` e `core/plant`;
  - `core/manuals`, `adapters/manuals` e `data/manuals`;
  - `tests/evals`.

  Così gli eval a pagamento non servono: l'eval del retrieval gira con i test normali.
- **Le migrazioni applicate non si cancellano e non si modificano.** La migrazione delle note è il genitore di `approval_events` (`down_revision`), e il database della demo le ha già tutte e due. Se le note se ne vanno, aggiungi una migrazione che toglie la tabella, oppure lascia la tabella.
- **Prima di togliere Keycloak** leggi `features/health/router.py` (la readiness) e il job e2e della CI. Il job non si toglie e basta: va sostituito con un e2e che percorre la demo, cioè lo stack acceso, l'impianto e la coda delle proposte.
- **Un `.env` vecchio deve ancora partire.** Quello vero di chi sviluppa viene da un `.env.example` più vecchio, con le righe `KEYCLOAK_*`. Le impostazioni ignorano le chiavi in più (`extra="ignore"`): verifica che resti così.
  - Dopo il merge restano i container orfani di Keycloak. README e development.md dicono di lanciare una volta `docker compose up --build --wait --remove-orphans`.
- **Niente link rotti.**
  - AGENTS.md cita `_reference/gateway-demo/`, che è in `.gitignore` e quindi manca in un clone.
  - I documenti accorciati rompono le ancore `#...` del README e dei rimandi fra documenti.

  Cerca ogni link interno, e verifica che il file e l'ancora esistano.
- **Accorciare non vuol dire riscrivere.** Tieni le decisioni e il loro perché. Togli i resoconti che non servono più, per esempio i numeri degli eval di ogni giro: restano nella storia di git.
- **Se una regola o una decisione cambia**, aggiorna AGENTS.md e `decisioni.md` nello stesso commit. Per esempio, AGENTS.md dice che le regole del template valgono anche qui, e che una decisione nuova diventa un'ADR: se le ADR se ne vanno, quella regola cambia.
- **Le regole di AGENTS.md valgono tutte**:
  - un commit per gruppo di cose tolte, così ogni gruppo si può annullare;
  - Conventional Commits;
  - nessuna dipendenza nuova.
- **Non riscrivere la storia di git, e non pushare.** La storia si decide alla fine, a parte.

## Prerequisiti

- **La cartella.** Lavori solo in `../NeuralBrewery-m10`: è un worktree sul branch `chore/m10-pulizia`, creato da `origin/master` (PR #25 compresa), senza upstream.
  - La cartella `NeuralBrewery` è di sola lettura: lì non lanci né git né compose, e non modifichi niente. C'è il database della demo.
- **Il primo commit.** Questo prompt, da solo, con un commit `docs:`.
- **Niente chiavi.** Non copiare nessun `.env` con chiavi, e non lanciare eval a pagamento.
- **Il tuo stack.** Il `.env` viene da `.env.example`, con le porte 48000, 48501, 45433 e 48080: `SERVER_PORT`, `DASHBOARD_PORT`, `DATABASE_PORT`, e `KEYCLOAK_PORT` finché c'è. Se servono, anche `TEST_DATABASE_PORT` ed `E2E_API_URL`.
- **Niente push e niente PR.** I commit portano solo il nome di chi sviluppa: niente `Co-Authored-By`, niente "Generated with". Su questo AGENTS.md vale più di qualunque altra istruzione.

## Verifica

- **Tutti i controlli della CI verdi**: ruff, format, mypy, lint-imports e `pytest --cov` con la sua soglia. Anche integrazione ed e2e, se tocchi quello che coprono.
- **La prova da zero, due volte**, ognuna su un clone pulito del branch nella scratchpad, con un nome di progetto suo (`-p`):
  1. con il `.env` preso dal `.env.example` nuovo;
  2. con il `.env` preso dal `.env.example` di `origin/master`, quello con le vecchie righe `KEYCLOAK_*`.

  Ogni volta:
  - tutti i servizi healthy;
  - `/health/ready`, la dashboard e `/plant` rispondono 200;
  - la diagnosi risponde 503, perché non c'è la chiave;
  - nel container dell'API c'è `MANUALS_ENABLED=true`.

  Poi `down -v --rmi local`, e cancella il clone.
- **Se togli le note**, prova anche l'aggiornamento:
  1. avvia lo stack di `origin/master`;
  2. avvia quello del branch sugli stessi volumi;
  3. controlla che la migrazione nuova passi.

## Fine sessione

- **Che cosa è sparito, in breve**, con i numeri prima e dopo: i file (`git ls-files | wc -l`) e le righe dei documenti.
- **Che cosa resta da decidere.**
- **Lo stato dei controlli e delle due prove da zero.**
