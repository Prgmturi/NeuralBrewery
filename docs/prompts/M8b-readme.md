Leggi AGENTS.md, poi docs/decisioni.md:
- "In una frase" e "Requisiti del corso";
- in "Scelte fatte", le voci "Agenti", "Memoria di M7: le decisioni del birraio", "La demo si fa da una dashboard del birraio in Streamlit", "Il birraio propone dalla dashboard con il suo token", "Il server MCP si mostra con un video, non dal vivo", "Chi approva: chi ha il token di approvazione", "Secondo fornitore" e "Eval degli agenti a mano";
- "Ancora aperte" e la roadmap.

Poi docs/development.md, tutta la sezione "The demo: from a proposal to the plant", ed "Eval of the agents". Infine il `README.md` di oggi e la PR #15 (`docs/guida.md`, una bozza di Copilot).

Obiettivo di questa sessione (M8, parte B): **il README di NeuralBrewery**, quello che il corso chiede ("README che spiega install e run: completato solo se gira"), e la prova che la demo gira da zero seguendolo. In parallelo un'altra sessione fa la parte A (immagini e CI), in un'altra cartella: tu non tocchi `docker/`, `.github/`, `compose.yaml`, `src/` né i test.

Lo stato vero, il 15 novembre:
- il `README.md` è ancora quello del template `fastapi_starter`. Parla di login Keycloak, delle note di esempio, di come aggiungere una feature. La sua prima frase promette un sistema multi-agente con RAG sui manuali, che per il corso non c'è: un agente solo, RAG e multi-agente dopo il corso;
- la PR #15 è una bozza di Copilot con una guida in italiano (`docs/guida.md`), scritta prima della dashboard;
- la demo si fa dalla dashboard, su http://localhost:8501, e `docs/development.md` ne ha i passi. Il badge della CI in cima al README è rosso: lo sistema la parte A.

Prerequisiti, da controllare prima di tutto:
- **La cartella.** Lavori in `../NeuralBrewery-m8b`, un worktree su `docs/m8b-readme`, creato da `master` dopo il merge della PR #17. Non lavorare nella cartella `NeuralBrewery`, né nel worktree della parte A (`../NeuralBrewery-m8a`).
- **Il primo commit.** Questo prompt, da solo, con un commit `docs:`.
- **Lo stack della demo.** Nella cartella `NeuralBrewery` gira lo stack con il database rifatto da zero per la prova del 18: non accenderlo, non fermarlo, non scriverci. Le sue porte (8000, 8501, 5433, 8080) sono occupate.
- **Il tuo stack.** La prova da zero la fai nel tuo worktree, che per il compose è un altro progetto, con volumi suoi.
  - Nel tuo `.env` usa 18000, 18501, 15433 e 18080 (`SERVER_PORT`, `DASHBOARD_PORT`, `DATABASE_PORT`, `KEYCLOAK_PORT`, più `TEST_DATABASE_PORT` ed `E2E_API_URL`). La parte A usa le 28000.
  - A fine sessione spegni il tuo stack e cancella i suoi volumi; ti dico io quando.
- **Le chiavi.** Il `.env` non è in git: copialo da `../NeuralBrewery/.env`, poi cambia le porte. `ANTHROPIC_API_KEY` e `OPENAI_COMPAT_API_KEY` stanno solo lì. `AGENT_PROVIDER` non va nel `.env`: la demo resta su Claude.

## Decisioni già prese

1. **Per chi è il README: per chi valuta il progetto**, che ha Docker e una chiave, e non conosce il codice. Deve potere, in quest'ordine: capire che cos'è in un minuto; accenderlo; fare la demo dalla dashboard; trovare dove il progetto copre ogni requisito del corso.
2. **Al tester servono solo Docker e una chiave API**, come dice `decisioni.md`. uv serve solo per i test e gli eval, ed è facoltativo.
3. **Il README dice il vero.** Un agente solo, con privilegio minimo: legge e propone, e l'approvazione è codice. La memoria sono le decisioni del birraio. Due fornitori, Claude e Gemini. RAG e multi-agente stanno fra le cose "dopo il corso", non fra quelle fatte. I limiti noti ci sono.
4. **Niente duplicati.** Il README racconta e rimanda: i passi completi della demo, il video MCP e i comandi dell'API restano in `docs/development.md`, le scelte in `docs/decisioni.md`, l'impianto in `docs/impianto.md`.
5. **Nessuna nuova dipendenza.**

## Decisioni da proporre nel piano

Per ognuna: il problema, un esempio, le opzioni con che cosa cambia in pratica, la tua raccomandazione.

1. **La lingua del README.** Gli altri documenti tecnici sono in inglese, `decisioni.md` e il corso in italiano, e chi valuta è italiano.
2. **Che cosa resta del README del template**: la guida per chi sviluppa (aggiungere una feature, proteggere una rotta, i comandi di ogni giorno). Restare, spostarsi in un documento in `docs/`, o andare via.
3. **La PR #15** (`docs/guida.md`): tenerla e aggiornarla, assorbirla nel README, o chiuderla. Chiudere una PR chiedimelo prima.
4. **Come si mostra la dashboard nel README**: a parole, o con uno screenshot. Uno screenshot lo farei io, perché tu non hai un browser: dimmi dove andrebbe e che cosa deve inquadrare.

## Come procedere

1. **Proponi il piano**: l'indice del README con una riga per sezione, le quattro decisioni, che cosa cambia negli altri documenti. Aspetta il mio ok.
2. **Scrivi il README.**
3. **La prova da zero, seguendo il README alla lettera**, nel tuo worktree e con le tue porte, su Claude: accendi lo stack, fai dalla dashboard la storia della demo descritta in `docs/development.md`, "The round of the speech". Non hai un browser: guida la pagina con `streamlit.testing`, come nella prova di M7b. Riportami che cosa hai visto a ogni passo, e ogni punto in cui il README non bastava o sbagliava. Correggilo, e rifai la prova di quel punto. Costa circa 10 centesimi.
4. **La CI vera.** Spingi e apri la PR solo quando te lo dico. Poi guarda il risultato su GitHub.

## Che cosa deve reggere

- ogni comando del README, copiato così com'è, funziona su una cartella nuova;
- ogni link del README porta a un file o a una sezione che esiste;
- niente nel README promette ciò che il codice non fa;
- il badge della CI resta, perché lo sistema la parte A.

Fuori scope, anche se sembrano facili:
- `docker/`, `.github/`, `compose.yaml`, `src/` e i test (parte A, o già fatti);
- l'agente, il suo prompt, gli eval, la dashboard;
- le slide del discorso;
- M2.

File che puoi toccare: `README.md`, `docs/guida.md` (se lo decidiamo), `docs/development.md` (solo le correzioni trovate seguendo il README), `docs/decisioni.md` (solo la riga del README nei requisiti, e M8 nella roadmap). Anche la parte A tocca `docs/decisioni.md`: resta nelle tue righe, e chi unisce per secondo risolve il conflitto.

Fine sessione:
- tutti i controlli della CI verdi su GitHub, a parte "Build container image" se la parte A non è ancora unita;
- commit in Conventional Commits, con il solo nome di chi sviluppa;
- `docs/decisioni.md` aggiornato, se una decisione cambia;
- il tuo stack spento e i suoi volumi cancellati, dopo avermelo chiesto. Lo stack della demo intatto.

Poi dimmi cosa devo controllare io e quali dubbi restano.
