Leggi AGENTS.md, poi docs/decisioni.md:
- "Requisiti del corso";
- in "Scelte fatte", le voci "La demo si fa da una dashboard del birraio in Streamlit" e "In sviluppo l'API risponde solo su 127.0.0.1";
- "Ancora aperte", in particolare le voci sulla CI, sull'immagine della dashboard e su Postgres e Keycloak;
- la roadmap.

Poi, in docs/development.md, "What CI runs" e "Supply chain". Infine `.github/workflows/ci.yml` (il job "Build container image"), `.github/dependabot.yml`, `docker/Dockerfile` e `docker/dashboard.Dockerfile`, con i loro test: `tests/test_dockerfile.py`, `tests/test_dashboard_image.py`, `tests/test_supply_chain.py`, `tests/test_lockfile.py`.

Obiettivo di questa sessione (M8, parte A): **la CI tutta verde, badge compreso**, e le immagini in ordine prima del discorso. In parallelo un'altra sessione fa la parte B (il README), in un'altra cartella: tu non tocchi `README.md` né `docs/guida.md`.

Lo stato vero, misurato il 15 novembre sulla PR #17:
- "Build container image" è rosso, anche su `master`. Due passi falliscono:
  - **"Scan the image"**: Grype trova due High con correzione, CVE-2026-76844 e CVE-2026-85091, in `zlib1g` dell'immagine base `python:3.13-slim@sha256:09a17ca…`. La versione corretta è `1:1.3.dfsg+really1.3.1-1+deb13u1`. È l'unica cosa che trova, anche ripetuta in locale con Grype 0.118.0 (l'immagine `anchore/grype:v0.118.0` c'è già in locale);
  - **"Upload the scan report"**: il repo è privato, e senza Code scanning il caricamento del rapporto SARIF fallisce. Anche con la scansione verde, il job resterebbe rosso.
- La PR #9 di Dependabot sposta l'immagine base da `09a17ca` a `e48f59c`, ma solo in `docker/Dockerfile`. È di prima della dashboard: con lei `test_the_same_base_image_as_the_api` diventerebbe rosso.
- L'immagine della dashboard la CI la costruisce nello stack di e2e, ma non la scansiona. Ha la stessa base dell'API.
- Nel compose di sviluppo, Postgres (5433) e Keycloak (8080) sono pubblicati su tutte le interfacce; l'API e la dashboard solo su 127.0.0.1.

Prerequisiti, da controllare prima di tutto:
- **La cartella.** Lavori in `../NeuralBrewery-m8a`, un worktree su `chore/m8a-immagini-e-ci`, creato da `master` dopo il merge della PR #17. Non lavorare nella cartella `NeuralBrewery`, né nel worktree della parte B (`../NeuralBrewery-m8b`).
- **Il primo commit.** Questo prompt, da solo, con un commit `docs:`.
- **Lo stack della demo.** Nella cartella `NeuralBrewery` gira lo stack con il database rifatto da zero per la prova del 18: non accenderlo, non fermarlo, non scriverci. Le sue porte (8000, 8501, 5433, 8080) sono occupate.
  - Se ti serve uno stack tuo, nel tuo `.env` usa 28000, 28501, 25433 e 28080 (`SERVER_PORT`, `DASHBOARD_PORT`, `DATABASE_PORT`, `KEYCLOAK_PORT`, più `TEST_DATABASE_PORT` ed `E2E_API_URL`). La parte B usa le 18000.
  - Il `.env` non è in git: copialo da `../NeuralBrewery/.env`, poi cambia le porte.
- **Le chiavi.** Per questa parte non servono: niente diagnosi, niente eval.

## Decisioni già prese

1. **Una sola immagine base per le due immagini**, per tag e per digest, come oggi. Il digest nuovo deve avere `zlib1g` corretto.
2. **La soglia della scansione non si abbassa**: High e Critical con una correzione fanno fallire la build, come oggi. Niente `ignore` di CVE.
3. **Nessuna nuova dipendenza.** Le altre PR di Dependabot (fastapi, pydantic, import-linter, keycloak, codeql-action) restano fuori: aggiornare a tre giorni dal discorso non vale il rischio. La #9 la sostituisci tu; chiudere PR altrui chiedimelo prima.

## Decisioni da proporre nel piano

Per ognuna: il problema, un esempio, le opzioni con che cosa cambia in pratica, la tua raccomandazione.

1. **Il caricamento del rapporto su un repo privato.** Le strade che vedo:
   - caricarlo solo se il repo è pubblico;
   - lasciarlo provare senza che fermi il job;
   - toglierlo e tenere il rapporto come artefatto del job.

   Guarda che cosa difende oggi `tests/test_supply_chain.py`. C'è anche una domanda da farmi: il valutatore del corso deve poter clonare il repo, e oggi il repo è privato. Se lo rendo pubblico, il caricamento torna a funzionare. Dimmi che cosa cambia nei due casi, e non cambiare la visibilità tu.
2. **La scansione dell'immagine della dashboard**: nella CI, nello stesso job o in uno suo, oppure no. Ricorda che la CI non la pubblica.
3. **Dependabot e le due immagini.** Verifica, dalla documentazione di Dependabot e non a memoria, se aggiorna anche `docker/dashboard.Dockerfile`, e se lo fa nella stessa PR. Da qui: tenere o cambiare il test che lega le due immagini alla stessa base.
4. **Postgres e Keycloak su 127.0.0.1** nel compose di sviluppo. Che cosa si rompe: il test e2e, il login dal browser, `KC_HOSTNAME`.

## Come procedere

1. **Proponi il piano** (file, le quattro decisioni, i test) e aspetta il mio ok.
2. **Prima i test, poi il codice.**
3. **Verifica in locale con Grype 0.118.0**, sulle due immagini costruite dal tuo branch, prima di spingere.
4. **La CI vera.** Spingi e apri la PR solo quando te lo dico. Poi guarda il risultato su GitHub, non solo i controlli locali.

## Le regole che i test devono difendere

- le due immagini partono dalla stessa base, per tag e per digest;
- ogni installazione controlla il lock (`--locked`), anche quella della dashboard;
- la scansione fallisce su High e Critical con correzione, e non ignora nessuna CVE;
- nessun caricamento di rapporto senza un rapporto;
- le porte del compose di sviluppo che decidiamo di chiudere restano su 127.0.0.1.

Fuori scope, anche se sembrano facili:
- `README.md` e `docs/guida.md` (parte B);
- l'agente, il suo prompt, gli eval, la dashboard;
- aggiornare dipendenze che non siano l'immagine base;
- il login su `/mcp`;
- M2.

File che puoi toccare: `docker/`, `.github/`, `compose.yaml` (solo le porte), i test elencati sopra più `tests/test_compose.py`, `docs/development.md` (solo "What CI runs" e "Supply chain"), `docs/decisioni.md` (solo le voci di "Ancora aperte" su CI, immagini e porte). Anche la parte B tocca `docs/decisioni.md`: resta nelle tue voci, e chi unisce per secondo risolve il conflitto.

Fine sessione:
- tutti i controlli della CI verdi, su GitHub, "Build container image" compreso;
- commit in Conventional Commits, con il solo nome di chi sviluppa;
- `docs/decisioni.md` aggiornato, se una decisione cambia;
- lo stack della demo intatto.

Poi dimmi cosa devo controllare io e quali dubbi restano.
