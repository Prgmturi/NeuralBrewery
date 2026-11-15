# Development

The tools, the tests, the checks of CI, the releases, and the care taken with what the project takes from others.

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

## Run the app on the machine

With Postgres and Keycloak from the stack:

```bash
docker compose stop api           # if the whole stack is up: its container holds port 8000
docker compose up --wait db keycloak
uv run alembic upgrade head
uv run uvicorn neuralbrewery.main:create_app --factory --reload
```

Then open http://localhost:8000/docs. `docker compose up --wait api` starts the container again.

## The demo: from a proposal to the plant

An action reaches the plant only after the brewer approves it. Until M2 the simulated plant lives in the API process.

The demo runs from the brewer's dashboard, one Streamlit page over the API: no `curl` and no Claude Code. The `curl` commands at the end stay as a reference of the API.

- **A restart builds a new plant.** It starts from `PLANT_START` (`brew_day` or `fermentation`) with `PLANT_SEED`, and what happened to the old plant is gone. The queue stays in Postgres.
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
- **the simulation**: move the time, inject a fault, clear the faults. Only when the API exposes these routes, that is in development with `PLANT_SIMULATION_CONTROL` on.

In the page, from the top:
- **the outcome of the last action**, in words: what the controller answered, or what the API refused and why, a 401 or a 409 included;
- **the plant**: simulated time, program and step, the controller's alarms, the watcher's judgements after the last advance, the readings, and the devices in a box that opens;
- **the diagnosis**: a button that calls the agent, then its explanation, the checks by hand, the proposal and what the queue made of it. A box shows each step of the agent and its tokens. The diagnosis stays on the page until the next one: typing or pressing anything else does not call the agent again;
- **the queue**, the newest first. Each proposal shows who proposed it (`agent`, `mcp` or `user`), why, and each event since. The waiting ones have *Approva* and *Rifiuta*, with the reason of a rejection.

What to know about it:
- **It is a client of the API**, as `curl` is. It reads `DASHBOARD_API_URL` and `DASHBOARD_APPROVAL_TOKEN`, which compose sets. It imports nothing of the app, and approving stays code of the API: with a wrong token, approve and reject show the API's 401.
- **It answers on 127.0.0.1 only.** The page holds the token, and nobody on the Wi-Fi of the room must reach it.
- **Nothing runs in the background.** The page runs again when you press or type something. To see a proposal that came from elsewhere, from MCP for one, press `R` in the page, or any button.
- **Its image is its own** (`docker/dashboard.Dockerfile`), with Streamlit and nothing of the API. The image of the API stays without Streamlit, about 300 MB less.
- **The tokens it shows are those the API reports**: outside the prompt cache, and read from it. What is written into the cache is not counted, so the cost of a diagnosis comes from the evals. On Claude it is 2 or 3 cents.
- **It runs on the host too**, while you change it: `docker compose stop dashboard`, put `DASHBOARD_APPROVAL_TOKEN` in `.env` (`.env.example`), then `uv run streamlit run src/neuralbrewery/dashboard/app.py`. `.streamlit/config.toml` keeps it on localhost and turns off the usage statistics that Streamlit sends by default.

### The round of the speech

On a clean queue ([below](#a-clean-queue-before-a-demo)), `brew_day` with seed 42. TT1 breaks twice in the same brew, with no restart.

1. Write your name. Propose `start_program`, with *cotta di riferimento* as why, and approve it: the program runs, step 1, *Scalda l'acqua*.
2. Advance 600 s. Inject `probe_broken` on `TT1`, then advance 300 s. Three alarms:
   - `signal_fault` on TT1;
   - `control_probe_fault` on HLT;
   - `program_paused`.
3. Clear the faults and advance 300 s. `signal_fault` goes. The block stays, and its text ends with *(bloccato: serve reset)*: the controller does not restart by itself.
4. Press *Diagnostica adesso*. The agent names TT1, a fault of measure, and proposes `reset`: it is in the queue, from `agent`. Approve it. The alarm goes at the controller's next turn, the next time you move the time.
5. The program still waits. Propose `resume_program` and approve it, then advance 300 s: the program runs, and TT1 climbs towards 72 °C.
6. TT1 breaks again: inject the fault, advance 300 s, clear the faults, advance 300 s. Diagnose: the agent proposes `reset` again, because the brewer approved it last time, and it notes that the fault came back.
7. Reject that `reset`, with the reason *TT1 ha un contatto intermittente: va sostituita prima di riarmare*.
8. Diagnose again. The agent proposes nothing. Its explanation cites the rejection and its reason, and its checks include replacing TT1 before re-arming.
9. If there is time: `docker compose restart api`. The plant starts over from zero, and the queue stays in Postgres. Repeat steps 1 to 3, then diagnose: the agent still recalls the rejection, and proposes no `reset`. The memory outlives the process.

How the round went on 15 November, live on Claude:
- the three diagnoses took 17, 11 and 10 s;
- in the third the agent wrote *Il birraio ha già rifiutato il reset (…), quindi non lo ripropongo*;
- the three cost about 8 cents together, measured as the evals measure S4 and S5.

### A clean queue before a demo

Every round writes into the queue, and the agent reads its own past proposals. Before the speech, start from an empty database:

```bash
docker compose down
docker volume rm neuralbrewery_db_data
docker compose up --build --wait
docker compose exec db createdb -U appbase appbase_test   # the integration tests' database
```

The volume takes its name from the folder of the clone: `docker volume ls` lists it.

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
uv run pytest tests/core/auth/             # one folder
uv run pytest tests/core/auth/test_service.py::TestValidateToken  # one class
uv run pytest --cov                        # with coverage, as CI runs it
uv run pytest -m integration               # only the integration tests, on a real Postgres
uv run pytest -m e2e                       # a login through the running stack
uv run pytest -m eval                      # the plant agent on a real model (AGENT_PROVIDER), by hand
```

- **Unit tests** are async, and outside `tests/integration/` they use stubs (`AsyncMock`): no database and no Keycloak. The root `conftest.py` provides the app, an HTTP client, mock services, and users with different roles.
- **They ignore the machine.** Tests never read the local `.env`, nor the exported `APP_*`, `KEYCLOAK_*` and other variables: an autouse fixture in `tests/conftest.py` switches both off. A test that needs some settings builds them and passes them to `create_app(settings)`.
- **CI runs the suite twice**, the second time with a `.env` and variables of a production server, and fails when coverage drops below `fail_under` in `pyproject.toml`.

### Integration tests

The tests in `tests/integration/` run on a real Postgres, for what a mock cannot show, such as a commit that the database refuses.

- `uv run pytest` leaves them out, even with their file named on the command line; `-m integration` runs only them.
- They read `TEST_DATABASE_*`, exported or in `.env` (see `.env.example`), and no other setting.
- They refuse a database whose name does not end in `_test`, because they create and drop tables in it. [Prepare the machine](#prepare-the-machine) creates it, once.
- Before the first test, a fixture brings that database to the last migration (`alembic upgrade head`), as CI does: no command is needed.
- CI runs them in a job of its own, with its own Postgres. They do not count towards the coverage threshold.

### End-to-end test

`uv run pytest -m e2e` logs the test user in through Keycloak, then calls the API with the token, as a frontend would. CI does it on every push, on the stack it starts.

The stack takes its ports from `SERVER_PORT`, `KEYCLOAK_PORT` and `DATABASE_PORT`, exported or in `.env`. The test calls the API at `E2E_API_URL`, `http://localhost:8000` by default: with the stack on another port, export it too (`E2E_API_URL=http://localhost:18000`), or the test calls whatever answers on 8000.

### Eval of the agents

`uv run pytest -m eval` runs the plant agent on a real model, on five fault scenarios with a fixed seed (`tests/evals/scenarios.py`):
- S1, an offset probe in the fermenter;
- S2, a blocked pump at the mash-in;
- S3, the drive of the agitator in fault;
- S4, a probe repaired while the block of the controller is still on, where only `reset` passes;
- S5, the plant of S4 with a memory: the brewer already rejected that `reset`, and said why. It passes only if the agent read its past decisions and proposes nothing that re-arms.

The memory of the agent is an object in memory, no database: empty, but for S5. The verdict is pass or fail, by code, on the diagnosis the agent hands in and on its trajectory: no LLM is the judge.

The model is the one of `AGENT_PROVIDER`, as for the app. Export it for the run rather than writing it in `.env`, where compose would read it too and move the demo to Gemini:

```bash
uv run pytest -m eval                                # Claude, the default
AGENT_PROVIDER=openai_compat uv run pytest -m eval   # Gemini Flash-Lite, free tier
```

On PowerShell, `$env:AGENT_PROVIDER = 'openai_compat'` before the command.

- **On Claude** it costs about 15 cents for the five, and needs `ANTHROPIC_API_KEY`.
- **On Gemini** it costs nothing, and needs `OPENAI_COMPAT_API_KEY`, from Google AI Studio. The free tier allows 15 requests a minute and a scenario makes up to 12, so the scenarios start a minute apart: about 4 minutes for the five.
- A plain `uv run pytest` leaves the evals out, and CI does not run them.
- Before the agent is called, each scenario checks that the plant shows its fault: a scenario that went wrong costs nothing.
- At the end a table gives the verdict, the tokens and the cost of each scenario. A second table compares the last run of each provider, once both have run.
- `.evals/<provider>/`, ignored by git, keeps one JSON per scenario, with the diagnosis and every step of the trace.
- The model is not deterministic: a scenario that passed may fail on the next run. Read its JSON before changing the prompt.

## What CI runs

| Job | What it does |
|---|---|
| `ci` | ruff, the format, mypy, the import contracts ([What checks each rule](architecture.md#what-checks-each-rule)), the unit tests with coverage, then the tests again in a production-like environment |
| Integration tests | The migrations up, checked against the models, down and up again; then the integration tests, on a Postgres of their own |
| Build container image | The image of `docker/Dockerfile`, a smoke test of the app inside it, the check that the app cannot change its own code, and the Grype scan |
| Log in through the whole stack | `docker compose up` of the stack, then the end-to-end test |
| Lint commit messages | Every commit of a pull request, and its title, through commitlint |

## Releases

Commits follow [Conventional Commits](https://www.conventionalcommits.org/). commitlint checks every commit of a pull request, and its title, which becomes the commit on `master` when the pull request is squashed.

[release-please](https://github.com/googleapis/release-please) keeps a release pull request open, with the next version and the changelog. Merging it:

- tags `vX.Y.Z` and publishes the GitHub release;
- publishes the image `ghcr.io/prgmturi/neuralbrewery:X.Y.Z`, and `:latest`;
- has already raised the version in `pyproject.toml`, `uv.lock` and the `image:` lines of `compose.prod.yaml`.

Under 1.0, `feat` and `fix` raise the patch number, and a breaking change (`!`) the minor one.

Only a change to what runs makes a release: `feat`, `fix`, `perf`, `deps` and `revert`, and a breaking change of any type. `docs`, `refactor`, `test`, `build`, `ci` and `chore` wait for the next release, with no line in the changelog (`changelog-sections` in `release-please-config.json`).

## Supply chain

What the project takes from others, and how it is checked:

- **Actions pinned to a commit.** Every GitHub Action is pinned to a commit, with its version in a comment. A tag can be moved to other code: it happened to `aquasecurity/trivy-action` in March 2026.
- **Dependabot** proposes updates once a week (`.github/dependabot.yml`): the actions, the base image of `docker/Dockerfile`, Postgres and Keycloak in the compose files, and `uv.lock`. What the image runs comes as `fix(deps)`, so it leads to a release; the tools of development come as `build(deps-dev)` or `ci`. New majors of Python, Postgres and Keycloak, and new versions of uv, are upgrades done by hand.
- **Grype** scans the image in CI ([Grype](https://github.com/anchore/grype)), and fails on a High or Critical vulnerability that has a fix. The report goes to the Security tab of the repository.
- **gitleaks** runs in the pre-commit hook ([gitleaks](https://github.com/gitleaks/gitleaks)) on the staged changes, and stops a commit that holds a secret. When it takes for a secret a value that is not one, end that line with `# gitleaks:allow`, as `KC_DB_URL` does in `compose.yaml`.
- **On GitHub**, turn on secret scanning and push protection (*Settings*, *Advanced Security*): they check every push.
