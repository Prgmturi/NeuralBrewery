# Development

The tools, the tests, the checks of CI, the commits, and the care taken with what the project takes from others.

## Tools

- **Docker**, for the stack of `compose.yaml`.
- **[uv](https://docs.astral.sh/uv/) 0.13 or later.** An older uv stops with an error in this project: run `uv self update`. uv installs the Python of `.python-version`, 3.13, when the machine does not have it.

## Prepare the machine

The stack of `compose.yaml` needs no `.env`, but every command that runs on the machine does. Without it Alembic and the app look for Postgres on port 5432 with the user `postgres`, while the stack publishes it on 5433 with the user `appbase`. `.env.example` holds the values of the stack, as the host sees them, and the `TEST_DATABASE_*` of the integration tests:

```bash
uv sync
uv run pre-commit install         # ruff, gitleaks and commitlint on every commit, as CI runs them
cp .env.example .env
docker compose up --wait db
uv run alembic upgrade head       # a new migration starts from the last one
docker compose exec db createdb -U appbase appbase_test   # once: -U is DATABASE_USER
```

The stack publishes every port on `127.0.0.1` only, so `.env.example` calls the database at `127.0.0.1`. On Windows `localhost` tries `::1` first, and waits about 2 s for each new connection before it falls back. A `.env` copied before 16 November says `localhost`: set `DATABASE_HOST` and `TEST_DATABASE_HOST` to `127.0.0.1`.

## Run the app on the machine

With Postgres from the stack:

```bash
docker compose stop api           # if the whole stack is up: its container holds port 8000
docker compose up --wait db
uv run alembic upgrade head
uv run uvicorn neuralbrewery.main:create_app --factory --reload
```

Then open http://localhost:8000/docs. `docker compose up --wait api` starts the container again.

## The demo: from a proposal to the plant

An action reaches the plant only after the brewer approves it. Until M2 the simulated plant lives in the API process.

The demo runs from the brewer's dashboard, one Streamlit page over the API: no `curl` and no Claude Code. The `curl` commands at the end stay as a reference of the API.

- **Riparti da zero builds a new plant**, and so does a restart of the API. It starts from `PLANT_START` (`brew_day` or `fermentation`) with `PLANT_SEED`, at simulated time 0, and what happened to the old plant is gone. The queue and its audit stay in Postgres.
- **Time moves only when you move it**, from the dashboard or with `/simulation/advance`.

The stack of `compose.yaml` has everything the demo needs:
- the simulation routes are on;
- the approval token is `brewer-dev-token`, for the API and for the dashboard;
- `ANTHROPIC_API_KEY` comes from `.env`, for the agent endpoint only.

Compose also reads `AGENT_PROVIDER` and `OPENAI_COMPAT_API_KEY` from `.env`: with `AGENT_PROVIDER=openai_compat` there, the agent of the stack runs on Gemini. The demo stays on Claude, so keep `AGENT_PROVIDER` out of `.env`, or at `claude`.

```bash
docker compose up --build --wait
```

Then open http://localhost:8501.

### The brewer's dashboard

On the left, the brewer's own controls:
- **their name**, which the audit records as declared, for every proposal, approval and rejection;
- **a button to propose**, among those that take no argument, such as `start_program` and `resume_program`. It goes into the queue as from `user`, and waits for an approval like any other;
- **the simulation**: move the time, inject a fault, clear the faults, and **Riparti da zero**, which waits for a tick in *Sì, cancella lo stato dell'impianto*. It takes the plant back to its start and seed, and clears the watcher's judgements and the diagnosis on the page; the queue stays. Only when the API exposes these routes, that is in development with `PLANT_SIMULATION_CONTROL` on.

In the page, from the top:
- **the outcome of the last action**, in words: what the controller answered, or what the API refused and why, a 401 or a 409 included;
- **the plant**: simulated time, program and step, the controller's alarms, the watcher's judgements after the last advance, the readings, and the devices in a box that opens;
- **the diagnosis**: a button that calls the agent, then its explanation, the checks by hand, the proposal and what the queue made of it. A box shows each step of the agent and its tokens. The diagnosis stays on the page until the next one: typing or pressing anything else does not call the agent again;
- **the queue**, the newest first. Each proposal shows who proposed it (`agent`, `mcp` or `user`), why, and each event since. The waiting ones have *Approva* and *Rifiuta*, with the reason of a rejection.

What to know about it:
- **It is a client of the API**, as `curl` is. It reads `DASHBOARD_API_URL` and `DASHBOARD_APPROVAL_TOKEN`, which compose sets. It imports nothing of the app, and approving stays code of the API: with a wrong token, approve and reject show the API's 401.
- **The page answers on 127.0.0.1 only**, since it holds the token, and so does every port of the development stack: the API's simulation is open, `/mcp` and the agent ask for no login, and the token and the passwords of `compose.yaml` are public. Nobody on the Wi-Fi of the room reaches the page, the API or Postgres.
- **Nothing runs in the background.** The page runs again when you press or type something. To see a proposal that came from elsewhere, from MCP for one, press `R` in the page, or any button.
- **Its image is its own** (`docker/dashboard.Dockerfile`), with Streamlit and nothing of the API. The image of the API stays without Streamlit, about 300 MB less.
- **The tokens it shows are those the API reports**: outside the prompt cache, and read from it. What is written into the cache is not counted, so the cost of a diagnosis comes from the evals: on Claude, 1 to 3 cents for S4 and S5.
- **It runs on the host too**, while you change it: `docker compose stop dashboard`, put `DASHBOARD_APPROVAL_TOKEN` in `.env` (`.env.example`), then `uv run streamlit run src/neuralbrewery/dashboard/app.py`. `.streamlit/config.toml` keeps it on localhost and turns off the usage statistics that Streamlit sends by default.

### The round of the speech

On a clean queue ([below](#a-clean-queue-before-a-demo)), `brew_day` with seed 42. TT1 breaks once in each of two brews, with **Riparti da zero** between them.

Brew 1:

1. Write your name. Propose `start_program`, with *cotta di riferimento* as why, and approve it: the program runs, step 1, *Scalda l'acqua*.
2. Advance 600 s. Inject `probe_broken` on `TT1`, then advance 300 s. Three alarms:
   - `signal_fault` on TT1;
   - `control_probe_fault` on HLT;
   - `program_paused`.
3. Clear the faults and advance 300 s. `signal_fault` goes. The block stays, and its text ends with *(bloccato: serve reset)*: the controller does not restart by itself.
4. Press *Diagnostica adesso*. The agent names TT1, a fault of measure, and proposes `reset`: it is in the queue, from `agent`. Approve it. The alarm goes at the controller's next turn, the next time you move the time.
5. The program still waits. Propose `resume_program` and approve it, then advance 300 s: the program runs, and TT1 climbs towards 72 °C.

Brew 2:

6. Tick the confirm and press **Riparti da zero**. The plant starts over from zero, and the queue stays in Postgres. Repeat steps 1 to 3.
7. Diagnose: the agent proposes `reset` again, and writes that a reset like it was executed before. Reject it, with the reason *TT1 ha un contatto intermittente: va sostituita prima di riarmare*. Type the reason and press Enter before *Rifiuta*: a text box of Streamlit takes its value on Enter.
8. Diagnose again. The agent proposes nothing. Its explanation cites the rejection and its reason, and its checks include replacing TT1 before re-arming.
9. If there is time: **Riparti da zero** again, steps 1 to 3, then diagnose: the agent still recalls the rejection, and proposes no `reset`. The memory outlives the plant. `docker compose restart api` does the same, and shows that it outlives the process too.

Why two brews: until 19 November the round broke TT1 twice in the same brew, and the agent had to propose `reset` again at the second fault. On 22 November it read in the history that the fault had come back, and proposed nothing: prudent, but it left nothing to reject. No eval covers two faults in one brew. Each diagnosis of this round is the case of S4 or S5: one fault, gone, with the block still on.

A proposal left waiting from before **Riparti da zero** stays in the queue: approved later, it is pressed on the new plant, behind the guardrail and the interlocks like any other. Decide it, or reject it, before you start over.

How the round went on 22 November, on Claude with the manuals on, twice on a clean queue, through the calls the dashboard makes:
- every diagnosis went as above, 8 of 8: `reset` in brew 1, `reset` again in brew 2, nothing after the rejection, nothing in brew 3;
- each took 7 to 10 s;
- in brew 2 the agent wrote *Un reset simile era già stato eseguito con esito ok*, and after the rejection *Il birraio aveva già rifiutato un reset per questa causa*;
- the four diagnoses of a round cost about 8 cents together. That is an estimate from what the evals measured on S4 and S5, since the API does not report the tokens written into the cache.

### A clean queue before a demo

Every round writes into the queue, and the agent reads its own past proposals. **Riparti da zero** starts the plant over but keeps the queue, on purpose: it is the agent's memory. Only to empty the queue, before the speech, start from an empty database:

```bash
docker compose down
docker volume rm neuralbrewery_db_data
docker compose up --build --wait
docker compose exec db createdb -U appbase appbase_test   # the integration tests' database
```

The volume takes its name from the folder of the clone: `docker volume ls` lists it.

A stack started before 17 November also ran Keycloak: the first time, `docker compose up --build --wait --remove-orphans` removes its containers. A `.env` copied from that `.env.example` still works: the settings ignore the `KEYCLOAK_*` and `AUTH_COOKIE_*` lines.

### The MCP server, for the video

The API serves MCP at `/mcp`, over HTTP. It has four tools that read the plant, and `propose_action`, which only puts a proposal in the queue, as from `mcp`. The live demo uses no MCP client: a short video shows one.

1. Start the stack and open the dashboard. Write your name.
2. Connect Claude Code once. `claude mcp list` shows whether it is there already:
   ```bash
   claude mcp add --transport http neuralbrewery http://localhost:8000/mcp
   ```
   In Claude Code, `/mcp` shows `neuralbrewery` connected, with five tools.
3. Put the browser and the terminal side by side, and start recording.
4. Ask Claude Code: *Leggi l'impianto di NeuralBrewery e proponi al birraio di avviare il programma della cotta*. It calls `read_plant`, then `propose_action` with `start_program`. The answer holds the id of the proposal and `"status": "proposed"`.
5. In the dashboard press `R`. The queue shows `start_program`, *in attesa*, *da mcp · mcp*.
6. Approve it from the dashboard: *Eseguita*, and the program runs. Claude Code proposed; only the brewer pressed.
7. If there is time, the guardrail: ask *proponi di portare il fermentatore a 45 °C*. The answer says `blocked`, with the maximum of 30 °C. In the dashboard the proposal shows as *bloccata dal guardrail*, with the reason, and with no button.

About 40 seconds of video.

Claude Desktop is not connected. Its custom connectors call from Anthropic's cloud and cannot reach `localhost`. Its local configuration starts programs, not addresses, so it needs a bridge such as `npx mcp-remote http://localhost:8000/mcp`.

### The API by hand, as a reference

What the dashboard calls. Reading needs no token. Proposing, approving and rejecting need the `X-Approval-Token` header and the name of the person who decides, which the audit writes as declared, and nobody checks.

The queue:

```bash
APPROVAL_TOKEN=brewer-dev-token                        # the one of compose.yaml and .env.example
curl -s localhost:8000/approvals                       # newest first, each with every event
curl -s -X POST localhost:8000/approvals \
  -H "X-Approval-Token: $APPROVAL_TOKEN" -H "Content-Type: application/json" \
  -d '{"command": "resume_program", "why": "TT1 a posto", "by": "Salvatore"}'
curl -s -X POST localhost:8000/approvals/<id>/approve \
  -H "X-Approval-Token: $APPROVAL_TOKEN" -H "Content-Type: application/json" \
  -d '{"by": "Salvatore"}'
curl -s -X POST localhost:8000/approvals/<id>/reject \
  -H "X-Approval-Token: $APPROVAL_TOKEN" -H "Content-Type: application/json" \
  -d '{"by": "Salvatore", "reason": "first I check TT5a"}'
```

`POST /approvals` puts a button in the queue as from `user`, through the same guardrail as the agent's and MCP's proposals. It answers 201:
- `proposed`: it waits for an approval;
- `blocked`: it is out of limits, and `blocked_reason` says why.

`approve` executes at once and answers with the outcome:
- `executed`, with the controller's answer. A refusal by an interlock counts as an answer: `accepted` is false, and `code` and `reason` say why.
- `execution_failed`, if the plant did not answer.

The responses for other cases:
- without the right token: 401;
- a proposal that is not waiting, because it was already approved, rejected or blocked: 409.

The status of a proposal is its last event, and `approval_events` keeps them all. Rows are only added: a trigger refuses UPDATE, DELETE and TRUNCATE.

The plant and the simulation:

```bash
curl -s localhost:8000/plant                           # what the controller shows now
curl -s -X POST localhost:8000/simulation/advance \
  -H "Content-Type: application/json" -d '{"seconds": 3600}'
curl -s -X POST localhost:8000/simulation/faults \
  -H "Content-Type: application/json" -d '{"kind": "drive_fault", "target": "M1", "value": 11}'
curl -s -X DELETE localhost:8000/simulation/faults
curl -s -X POST localhost:8000/simulation/restart     # Riparti da zero: 204, the queue stays
```

`advance` answers with the new simulated time, the controller's alarms, and the watcher's judgements.
- It takes at most a day per call.
- On a brew day it blocks the API for about 0.16 s per simulated hour.

The faults and their targets are in `docs/impianto.md`. Scenario S3 of the evals, for example: start the program, advance until step 4, then inject `drive_fault` on M1 with 11.

The plant agent:

```bash
curl -s -X POST localhost:8000/agents/plant/diagnose
```

The agent reads the plant now and hands in its diagnosis. If the diagnosis has a command, it goes into the queue as from `agent`, through the same guardrail.

What this endpoint costs and needs:
- One diagnosis costs a few cents on Claude, nothing on the free tier of Gemini.
- Without the key of the chosen provider it answers 503, and 503 again when the provider cannot be reached or is over its limits. An answer that cannot be used is a 502.
- The agent proposes the most prudent action. When manual checks come first, it proposes nothing. When the cause gives no more signs and only a block of the controller is left, it proposes `reset`.
- Before it proposes a button, the agent reads the brewer's decisions on its last 10 proposals, with the tool `read_decisions`. If the brewer rejected the same button for the same cause, it does not propose it again, and says so. It reads only its own proposals: those from MCP and from the brewer stay out. It reads no time either, real or simulated.

Each button is a proposal of its own, with its own approval:
- `reset` re-arms what no longer has its cause;
- `resume_program` takes the step up again, and is refused while a block is on.

When a fault goes and leaves no block, as when a drive is repaired, `resume_program` alone is enough.

## Tests

```bash
uv run pytest                              # every test but the integration and end-to-end ones
uv run pytest tests/core/plant/            # one folder
uv run pytest tests/core/plant/test_watcher.py::TestProbesDisagree  # one class
uv run pytest --cov                        # with coverage, as CI runs it
uv run pytest -m integration               # only the integration tests, on a real Postgres
uv run pytest -m e2e                       # the demo through the running stack
uv run pytest -m eval                      # the plant agent on a real model (AGENT_PROVIDER), by hand
```

- **Unit tests** are async, and outside `tests/integration/` they use stubs (`AsyncMock`): no database. The root `conftest.py` provides the app, an HTTP client and a mock database.
- **They ignore the machine.** Tests never read the local `.env`, nor the exported `APP_*`, `DATABASE_*` and other variables: an autouse fixture in `tests/conftest.py` switches both off. A test that needs some settings builds them and passes them to `create_app(settings)`.
- **CI runs the suite twice**, the second time with a `.env` and variables of a production server, and fails when coverage drops below `fail_under` in `pyproject.toml`.
- **The eval of the retrieval** over the manuals runs with them, and prints its table at the end: [The manuals](#the-manuals-their-text-and-the-eval-of-the-retrieval).

### Integration tests

The tests in `tests/integration/` run on a real Postgres, for what a mock cannot show, such as a commit that the database refuses.

- `uv run pytest` leaves them out, even with their file named on the command line; `-m integration` runs only them.
- They read `TEST_DATABASE_*`, exported or in `.env` (see `.env.example`), and no other setting.
- They refuse a database whose name does not end in `_test`, because they create and drop tables in it. [Prepare the machine](#prepare-the-machine) creates it, once.
- Before the first test, a fixture brings that database to the last migration (`alembic upgrade head`), as CI does: no command is needed.
- CI runs them in a job of its own, with its own Postgres. They do not count towards the coverage threshold.

### End-to-end test

`uv run pytest -m e2e` runs the demo through the running stack: the readiness, the plant, the dashboard, a `reset` proposed and approved with the development token, which the executor presses. CI does it on every push, on the stack it starts, and there also checks that the diagnosis answers 503 without a key (`E2E_NO_AGENT_KEY=true`): with a key that test would call the model, so it is skipped unless asked for.

Run it on a stack you can throw away: the audit keeps every proposal, and the test adds one, by `e2e`.

The stack takes its ports from `SERVER_PORT`, `DASHBOARD_PORT` and `DATABASE_PORT`, exported or in `.env`. The test calls the API at `E2E_API_URL`, `http://localhost:8000` by default, and the dashboard at `E2E_DASHBOARD_URL`, `http://localhost:8501`: with the stack on other ports, export them too, or the test calls whatever answers there.

### Eval of the agents

`uv run pytest -m eval` runs the plant agent on a real model, on six fault scenarios with a fixed seed (`tests/evals/scenarios.py`):
- S1, an offset probe in the fermenter;
- S2, a blocked pump at the mash-in;
- S3, the drive of the agitator in fault;
- S4, a probe repaired while the block of the controller is still on, where only `reset` passes;
- S5, the plant of S4 with a memory: the brewer already rejected that `reset`, and said why. It passes only if the agent read its past decisions and proposes nothing that re-arms;
- S6, the plant of S3 with the manuals on: it passes only if the checks of S3 pass, the agent called `search_manuals`, and its explanation or checks say what F11 means (the motor overheated). Whether it cites manual and page is printed under the row, and not graded.

With `MANUALS_ENABLED=true`, exported for the command or in `.env` as `.env.example` has it, every scenario runs with the manuals, as the stack does: S1–S5 must not get worse. S6 has them in any case.

The memory of the agent is an object in memory, no database: empty, but for S5. The verdict is pass or fail, by code, on the diagnosis the agent hands in and on its trajectory: no LLM is the judge.

The model is the one of `AGENT_PROVIDER`, as for the app. Export it for the run rather than writing it in `.env`, where compose would read it too and move the demo to Gemini:

```bash
uv run pytest -m eval                                # Claude, the default
AGENT_PROVIDER=openai_compat uv run pytest -m eval   # Gemini Flash-Lite, free tier
```

On PowerShell, `$env:AGENT_PROVIDER = 'openai_compat'` before the command.

- **On Claude** it costs about 18 cents for the six, and needs `ANTHROPIC_API_KEY`.
- **On Gemini** it costs nothing, and needs `OPENAI_COMPAT_API_KEY`, from Google AI Studio. The free tier allows 15 requests a minute and a scenario makes up to 12, so the scenarios start a minute apart: about 8 minutes for the six.
- A plain `uv run pytest` leaves the evals out, and CI does not run them.
- Before the agent is called, each scenario checks that the plant shows its fault: a scenario that went wrong costs nothing.
- At the end a table gives the verdict, the tokens and the cost of each scenario. A second table compares the last run of each provider, once both have run.
- `.evals/<provider>/`, ignored by git, keeps one JSON per scenario, with the diagnosis and every step of the trace.
- The model is not deterministic: a scenario that passed may fail on the next run. Read its JSON before changing the prompt.

### The manuals: their text, and the eval of the retrieval

The plant agent searches the manuals of the components when `MANUALS_ENABLED` is on ([decisioni.md](decisioni.md), "RAG sui manuali, leggero"). The app reads only the text in `data/manuals/text/<id>.md`, which is in the repository: no PDF library at run time.

**Regenerate the text** only when a manual changes, or a new one arrives in `data/manuals/`. Every manual is in the repository, with its source in `manuals/manifest.toml`: there is nothing to download.

```bash
python scripts/extract_manuals.py    # the text of each document that has none yet
```

- It needs `pdfinfo` and `pdftotext` of poppler (`poppler-utils`), first in `PATH`. Git for Windows ships the `pdftotext` of xpdf, which reads tables another way: the script refuses it. On Windows, `PATH="/c/poppler/Library/bin:$PATH"` in Git Bash, or wherever poppler is.
- A file that exists is left alone. `--force` writes every file again, and **loses the tables fixed by hand**: each is marked `<!-- table fixed by hand, checked on the PDF -->`. To regenerate one document, delete its file and run the script.
- To replace a manual: put the new file at `data/manuals/<id>.pdf`, with the id of the manifest, and update its entry (`source`, `url` or `page`, `note`). Delete only `data/manuals/text/<id>.md`, then run the script: it extracts that document alone.
- A copy from manualslib carries the header of the site on its first and last page, and a "Downloaded from" line on each page: remove them from the text, as for the pump and the fermenter.
- After a regeneration, fix those tables again on the PDF, one entry per row as a Markdown table under its title. Where its cells fit on one line, `pdftotext -layout` keeps the rows of a table together; `pdftotext -bbox-layout` gives the place of each word, to prove that each row is right (the parameter list of the V20, 218 rows). `tests/test_manuals.py` checks that the marks are still there, that each header says what the manifest says, and that the pages are marked in order.

**The eval of the retrieval** runs with the other tests, in CI too: `tests/adapters/manuals/test_retrieval.py`. The golden set is one question for each injectable fault of [impianto.md](impianto.md) that a manual speaks of, written as the agent would write it, with the pages that answer, checked on the PDF. The docstring lists the faults left out, and why. At the end of `uv run pytest` a table gives, for each question, the place of the first passage that answers (`-`: not in the first three), then hit@1 and hit@3. The test fails below hit@3 = 100% or hit@1 = 80%. More tests check single rows: F11 must give "Motor overtemperature" first and F20 "DC ripple too high"; r0035 the motor temperature and r0039 the energy meter; the valve, one page only, the row of its operating time.

## What CI runs

| Job | What it does |
|---|---|
| `ci` | ruff, the format, mypy, the import contracts (`[tool.importlinter]` in `pyproject.toml`), the unit tests with coverage, then the tests again in a production-like environment |
| Integration tests | The migrations up, checked against the models, down and up again; then the integration tests, on a Postgres of their own |
| Build container image | The image of `docker/Dockerfile`, a smoke test of the app inside it, the check that the app cannot change its own code, and the Grype scan, with what it found in the summary of the run |
| Build dashboard image | The image of `docker/dashboard.Dockerfile` and its Grype scan, with the same thresholds |
| The demo through the whole stack | `docker compose up` of the stack, then the end-to-end test |
| Lint commit messages | Every commit of a pull request, and its title, through commitlint |

## Commits

Commits follow [Conventional Commits](https://www.conventionalcommits.org/). commitlint checks every commit of a pull request, and its title, which becomes the commit on `master` when the pull request is squashed. There are no releases: the project runs from the repository, with `compose.yaml`.

## Supply chain

What the project takes from others, and how it is checked:

- **Actions pinned to a commit.** Every GitHub Action is pinned to a commit, with its version in a comment. A tag can be moved to other code: it happened to `aquasecurity/trivy-action` in March 2026.
- **Grype** scans both images in CI, the API's and the dashboard's ([Grype](https://github.com/anchore/grype)). It fails on a High or Critical vulnerability that has a fix, and ignores none: no `.grype.yaml` in the repository, no `config` or `vex` input. Its log says only that it failed, so what it found goes to the summary of the run. The report goes to the Security tab once the repository is public: a private repository of a personal account has no Code scanning.
- **Debian's security fixes, before the base has them.** On 16 November 2026 no `python:3.13-slim` had the `zlib1g` that fixes two High the scan failed on: the fix was in `trixie-security` only. On 22 November two High in the C library (`libc6`, `libc-bin`) failed the scan again, fixed in Debian's 2.41-12+deb13u5. The runtime stage of both images upgrades what is installed (`apt-get upgrade`), as `fastapi_starter` does since 0.9.3: no list of packages to keep, and the next CVE of the same kind does not fail the scan. The price is that an image is only as reproducible as Debian's archive that day. The base image still moves by hand, in both Dockerfiles.
- **gitleaks** runs in the pre-commit hook ([gitleaks](https://github.com/gitleaks/gitleaks)) on the staged changes, and stops a commit that holds a secret. When it takes for a secret a value that is not one, end that line with `# gitleaks:allow`, as `KC_DB_URL` does in `compose.yaml`.
- **On GitHub**, turn on secret scanning and push protection (*Settings*, *Advanced Security*): they check every push.
