Leggi AGENTS.md, poi docs/decisioni.md:
- "Requisiti del corso";
- in "Scelte fatte", le voci "La demo si fa da un pannello del birraio in Streamlit", "Il server MCP si mostra con un video, non dal vivo", "Chi approva: chi ha il token di approvazione", "Il controllo della simulazione è spento se non lo si chiede", "Memoria di M7: le decisioni del birraio" e "Coda delle proposte e audit";
- "Ancora aperte" e la roadmap.

Poi, in docs/development.md, "The demo: from a proposal to the plant": è il giro che oggi si fa con `curl`, e che il pannello deve sostituire.

L'API che il pannello usa, e che c'è già:
- `GET /plant`: letture, dispositivi, programma, allarmi (`features/plant/router.py`);
- `/simulation/advance`, `POST` e `DELETE /simulation/faults`: solo con `PLANT_SIMULATION_CONTROL` acceso;
- `POST /agents/plant/diagnose`: la diagnosi, con i passi e i token, e la proposta in coda se c'è (`features/agents/router.py`);
- `GET /approvals`, `POST /approvals/{id}/approve` e `/reject`: gli ultimi due chiedono `X-Approval-Token` e il nome di chi decide (`features/approvals/api/router.py`);
- `/mcp`, con `propose_action` (`features/agents/mcp_server.py`).

Obiettivo di questa sessione (M7b): **il pannello del birraio in Streamlit**, una pagina sola sopra l'API. La demo del discorso si fa tutta da lì, senza `curl` né Claude Code. Il pannello ha:
- lo stato dell'impianto e gli allarmi;
- i comandi della simulazione (avanza il tempo, inietta un guasto, toglili), solo quando l'API li espone;
- il pulsante della diagnosi, con la spiegazione dell'agente, le verifiche e la proposta;
- la coda: ogni proposta con la sua storia, e approva o rifiuta con il motivo.

Il discorso è il 19 novembre, e il 18 è per M8 (README, scan, prova della demo): serve la soluzione più semplice che rispetta le regole.

Prerequisiti, da controllare prima di tutto:
- **Il branch.** La PR #16 (M7) è unita a `master`. Lavora su un branch nuovo, `feat/m7b-pannello`, creato da `master` aggiornato: `git fetch origin master:master`, poi crea il branch da lì.
- **Il primo commit.** Questo prompt, da solo, con un commit `docs:`.
- **I manuali.** `data/manuals/` ha file non tracciati: non vanno nei commit.
- **Le chiavi.** `ANTHROPIC_API_KEY` e `OPENAI_COMPAT_API_KEY` stanno solo in `.env`. `AGENT_PROVIDER` non va nel `.env`: la demo resta su Claude.
- **Il database dello stack.** Il 15 novembre è stato rifatto da zero, e la coda era vuota. Ogni prova di questa sessione ci scrive: va bene, ma prima della prova del 18 si rifà da zero (vedi "Fine sessione").

## Decisioni già prese

1. **Streamlit è una dipendenza approvata.** Nessun'altra senza chiedere.
2. **Il pannello è un client dell'API, e basta.** Parla con l'API via HTTP, come un frontend. Non importa niente dell'app: né porte, né adapter, né feature. L'approvazione resta codice dell'API (regola 1): il pannello preme "approva" come farebbe `curl`, con il token.
3. **Il token di approvazione** il pannello lo legge da un'impostazione, mai scritto nel codice. Il nome di chi approva lo scrive il birraio nel pannello, e l'audit lo registra come dichiarato, come oggi.
4. **Niente chat, niente orchestratore, niente aggiornamento automatico in background.** Il tempo dell'impianto si muove solo con i comandi della simulazione, come oggi: la pagina si aggiorna quando il birraio preme qualcosa.
5. **La storia della demo**, decisa il 15 novembre, su un database nuovo:
   1. TT1 si rompe mentre l'acqua scalda, poi torna a posto. L'agente propone `reset`, il birraio approva, il programma riparte;
   2. TT1 si rompe di nuovo. L'agente ripropone `reset`, perché l'ultima volta era stato approvato. Questa volta il birraio rifiuta: "TT1 ha un contatto intermittente: va sostituita prima di riarmare";
   3. nuova diagnosi: l'agente cita il rifiuto e non insiste.

   Il secondo guasto può arrivare nella stessa cotta, senza riavviare l'API: verificalo dal vivo. Il riavvio, che dimostra la memoria persistente, è facoltativo nel discorso.
6. **Il server MCP si mostra con un video**, non dal vivo. Claude Code legge l'impianto e propone via MCP, e la proposta compare nella coda del pannello come `mcp`. Prepara i passi, e il video lo registro io a fine sessione o nella prova del 18.

## Decisioni da proporre nel piano

Per ognuna: il problema, un esempio della demo, le opzioni con che cosa cambia in pratica, la tua raccomandazione.

1. **Chi propone `start_program` e `resume_program` dal pannello.** Nella demo di M6 li proponeva Claude Code, che ora è fuori. Per esempio: dopo il `reset` approvato, il programma aspetta ancora `resume_program`. Le strade che vedo:
   - il pannello chiama `propose_action` su `/mcp`: niente backend nuovo, ma nell'audit la proposta del birraio risulta `mcp`, come quella di un client esterno;
   - un endpoint nuovo con cui il birraio propone come `user`, con il token: l'audit dice il vero, ma è un cambio del backend, e `decisioni.md` diceva "senza cambiare il backend".
2. **Dove vive il codice del pannello, e come entra nei controlli**: dentro `src/neuralbrewery/` (copertura, mypy, un contract che gli vieti di importare l'app) o fuori. La soglia di copertura non si abbassa.
3. **Come si avvia**: come servizio del compose, nella stessa immagine, o con `uv run streamlit run` sulla macchina. Attenzione alla scansione dell'immagine: Streamlit porta molte dipendenze, e una vulnerabilità "high" nuova renderebbe più difficile M8. Guarda che cosa entrerebbe nell'immagine prima di proporre.
4. **Come si testa senza rete**: per esempio `streamlit.testing` con l'API finta. I test della CI non chiamano mai la rete.

## Come procedere

1. **Proponi il piano** (file, le quattro decisioni, i test) e aspetta il mio ok.
2. **Prima i test, poi il codice.**
3. **La prova dal vivo, sullo stack del compose, tutta dal pannello**: la storia della demo del punto 5, dall'inizio alla fine, su Claude. Riportami che cosa hai visto a ogni passo, e quanto è costato.
4. **I passi del video MCP**, pronti da seguire.
5. Aggiorna la demo in `docs/development.md`: il pannello prende il posto dei `curl`, che restano solo come riferimento dell'API.

## Le regole che i test devono difendere

- il pannello non importa niente dell'app, e passa solo dall'API;
- senza il token giusto, approva e rifiuta non vanno: il pannello mostra il 401, non lo nasconde;
- con il controllo della simulazione spento, il pannello non mostra i suoi comandi e non si rompe;
- gli errori dell'API (503 dell'agente senza chiave, 409 di una proposta già decisa) arrivano al birraio in parole;
- il token non compare mai nella pagina né nei log;
- i test della CI non chiamano mai la rete. La soglia di copertura resta.

Fuori scope, anche se sembrano facili:
- chat, orchestratore, multi-agente, RAG;
- cambiare l'agente, il suo prompt o gli eval;
- il testo "(bloccato: serve reset)" quando la causa c'è ancora (limite noto, deciso il 15 novembre);
- login su `/mcp` e Keycloak per il pannello;
- README e scan dell'immagine (M8);
- M2.

Fine sessione:
- tutti i controlli della CI verdi;
- commit in Conventional Commits, con il solo nome di chi sviluppa;
- `docs/decisioni.md` aggiornato, se una decisione cambia;
- il database dello stack rifatto da zero, pronto per la prova del 18: cancella il volume `neuralbrewery_db_data`, riaccendi lo stack, ricrea `appbase_test`. Prima chiedimelo.

Poi dimmi cosa devo controllare io e quali dubbi restano. Il prompt della fase dopo lo scriviamo dopo.
