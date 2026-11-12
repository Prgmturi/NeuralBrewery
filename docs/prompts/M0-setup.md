Questo repo nasce dal mio template fastapi_starter. Stiamo costruendo NeuralBrewery, il progetto finale del corso AI: un assistente multi-agente per un impianto di birrificazione simulato. Leggi AGENTS.md, docs/decisioni.md e docs/impianto.md, poi il livello 1 di docs/architecture.md.

Obiettivo di questa sessione (M0): solo setup, niente logica dell'impianto.

1. Il progetto si chiama NeuralBrewery. Rinomina entrambe le forme del vecchio nome, `fastapi_starter` e `fastapi-starter`, nell'unica forma tecnica `neuralbrewery`; `NeuralBrewery` solo dove è un nome da leggere (titoli, testi). Vale per src/, test, pyproject (anche `root_package` e i contract di import-linter), uv.lock (rigeneralo con `uv lock`), alembic, Dockerfile, compose, realm Keycloak di sviluppo, .env.example, workflow della CI, release-please, README e guide. Prima mostrami l'elenco dei file da toccare (`git grep -il "fastapi.starter"`) e aspetta il mio ok.
2. Riparti da zero con la versione: 0.1.0 in pyproject, uv.lock, `.release-please-manifest.json` e nelle righe `image:` di `compose.prod.yaml`; CHANGELOG.md con la sola intestazione. Nel README cambia solo titolo e prima descrizione (prendila da docs/decisioni.md): il README vero lo scriviamo alla fine.
3. Verifica che le sezioni "Convenzioni del codice" e "Comandi" di AGENTS.md corrispondano al repo; correggi solo ciò che è sbagliato.
4. Prepara i posti vuoti dell'impianto descritti in docs/decisioni.md ("Come si innesta nel template"): i package `core/plant/` e `adapters/plant_sim/` con solo `__init__.py` e docstring, e un import contract che vieta ad `adapters/plant_sim` di importare fastapi, httpx e sqlalchemy.
5. Porta nel repo `manuals/manifest.toml` e `scripts/download_manuals.py` da `_reference/gateway-demo/`; aggiungi a .gitignore `_reference/` e `data/manuals/*` (tenendo `data/manuals/.gitkeep`).
6. Non toccare l'esempio `features/notes`: lo togliamo quando avremo una feature nostra.

Vincoli: nessuna nuova dipendenza senza chiedermelo; non cambiare il comportamento del template.

Fine sessione: ruff, mypy, lint-imports e pytest verdi (gli stessi comandi della CI). Poi ricordami di provare lo stack da zero (`docker compose down -v`, poi `docker compose up --build --wait` e `uv run pytest -m e2e`), perché la rinomina tocca Keycloak e il Dockerfile. Commit in Conventional Commits, elenco breve di cosa hai cambiato.
