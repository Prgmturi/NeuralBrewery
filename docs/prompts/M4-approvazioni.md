Leggi AGENTS.md, docs/decisioni.md (soprattutto "Scelte fatte", con le cinque voci di M4, e "Ancora aperte") e docs/impianto.md: "In breve", "Il principio", i comandi e "Il controllore non riparte da solo". Poi docs/architecture.md, livello 1 e i capitoli "Add a setting" e "Add an external service", e docs/adr/0007-development-values.md. Il modello di una feature a tre strati è `features/notes`; l'agente di M5 è in `features/agents/` e `adapters/claude/`.

Obiettivo di questa sessione (M4): una proposta che diventa un'azione sull'impianto, solo dopo l'approvazione del birraio. L'impianto vive nel processo dell'API; un server MCP dentro l'API legge e propone; la coda delle proposte tiene l'audit; il birraio approva con il token di approvazione; l'esecutore esegue; anche l'agente di M5 mette in coda le sue proposte. Al discorso (19 novembre) mancano pochi giorni: la soluzione più semplice che rispetta le regole. Niente servizio plant-sim (M2), niente interfaccia.

Prerequisiti, da controllare prima di tutto:
- La PR #12 (M5) è unita a `master`. Se non lo è, fermati e dimmelo.
- Lavora su un branch nuovo, `feat/m4-approvazioni`, creato da `master` aggiornato: aggiorna `master` senza cambiare branch (`git fetch origin master:master`), poi crea il branch da lì, così le modifiche non committate vengono con te. `docs/decisioni.md` ha modifiche non committate con le decisioni di questa fase: portale sul branch nuovo e committale per prime, da sole, con un commit `docs:`. `docs/prompts/M4-approvazioni.md`, questo prompt, va nello stesso commit.
- Lo stack del compose deve partire: Postgres serve ai test di integrazione, e l'API all'avvio cerca ancora Keycloak, anche se la demo non lo usa. Se non parte, fermati e dimmelo.
- `ANTHROPIC_API_KEY` serve solo alla prova finale dell'agente. La chiave non entra mai nel repo.

Passo 1, un cancello e non una formalità: il server MCP dentro l'API, collegato a Claude Desktop. Prima di costruire il resto, prova davvero:
- un server MCP minimo montato nell'app di `create_app`, su HTTP, con un solo tool di lettura (la fotografia dell'impianto in-process), che parte e si ferma con il lifespan dell'app;
- il pacchetto `mcp` è già installato perché lo porta `datapizza-ai-core` (2.3.0): verifica quale API offre per un server HTTP montato in un'app ASGI, e dichiaralo come dipendenza diretta, con un vincolo compatibile con quello di datapizza;
- il collegamento da Claude Desktop su questa macchina (Windows), e che cosa richiede; Claude Code, che parla HTTP direttamente, è l'alternativa.
Se a Claude Desktop serve qualcosa che chiede il mio ok (un programma da installare, un tunnel pubblico), fermati e dimmelo prima di installarlo.

Decisioni già prese:
1. **Impianto nel processo dell'API, fino a M2.** Impostazioni in `core/config/plant.py`: partenza con nome, seed, controllo della simulazione acceso solo in sviluppo (`production_problems()` lo rifiuta altrove, ADR 0007). `bootstrap.py` costruisce l'adattatore in-process e lo mette in `app.state` con uno `StateKey` per porta: `PlantReader` per tutti, `PlantCommander` solo per l'esecutore, `SimulationControl` solo in sviluppo. Il tempo avanza solo con un endpoint di sviluppo, che restituisce gli allarmi del controllore e i giudizi del sorvegliante; con lo stesso spirito, iniettare e togliere un guasto per la demo. Nessun ciclo in background. Un solo worker: con l'impianto in-process, l'avvio rifiuta `SERVER_WORKERS` diverso da 1. Un riavvio dell'API riparte da un impianto nuovo: va detto nella documentazione.
2. **Server MCP dentro l'API**, su HTTP: i tool di lettura (riusa ciò che fa `features/agents/tools.py`, senza copiarne la logica) e `propose_action`, che mette la proposta in coda con origine "mcp". Riceve un `ReadOnlyPlant` e la sola funzione che propone: mai l'approvazione, mai `PlantCommander`.
3. **Chi approva**: chi ha il token di approvazione, non Keycloak. Approvare e rifiutare chiedono `APPROVAL_TOKEN` in un'intestazione e il nome di chi approva, che l'audit registra come dichiarato. `APPROVAL_TOKEN` è un'impostazione nuova in `core/config/`, un segreto (`SecretStr`) con un valore di sviluppo in `.env.example`; `production_problems()` rifiuta quel valore (ADR 0007). Il confronto è a tempo costante (`secrets.compare_digest`). Il token non arriva mai ai tool MCP, all'agente o ai loro prompt. Keycloak e il login del template restano come sono: la demo non li usa.
4. **Coda e audit**: `features/approvals/` a tre strati, come `notes`. Una tabella Postgres a cui si aggiunge e basta, con la sua migrazione Alembic: lo stato di una proposta è il suo ultimo evento. Ogni evento ha la proposta, il tipo (proposta, approvazione, rifiuto, esecuzione, esecuzione fallita), chi (un utente, l'agente, MCP), i dati, il tempo simulato e l'ora reale. L'esecutore è l'unico codice che riceve `PlantCommander`: esegue solo proposte approvate, una volta sola, con un timeout, e registra la risposta del controllore (un rifiuto di un interlock è una risposta, non un errore).
5. **Guardrail prima della coda**: il comando è un pulsante del pannello, ha gli argomenti che gli servono, ed è nei limiti (setpoint tra 0 e il massimo del recipiente, litri positivi). Una proposta fuori dai limiti non entra in coda, chi l'ha mandata riceve il motivo, e il rifiuto resta nell'audit. È il guardrail su un tool che chiede il corso; gli interlock del controllore restano il primo livello.
6. **L'agente mette in coda**: un endpoint diagnostica l'impianto adesso, con `PlantAgent`, e mette in coda la proposta della diagnosi, se c'è, con origine "agente". Esposto dall'API, deve tradurre gli errori di Anthropic (ADR 0006): una sottoclasse minima del client Anthropic di datapizza, in `adapters/claude/`, che traduce solo gli errori (servizio irraggiungibile → `ServiceUnavailableError`, risposta inutilizzabile → `ExternalServiceError`). Se serve cambiare altro del client, fermati e chiedimelo.
7. **Dove va il vocabolario**: `Proposal` e `Command` passano da `features/agents/diagnosis.py` a `core/plant/schemas.py`, perché due feature non si importano. Attenzione alla lezione di M5: un `domain/` non può caricare pydantic, nemmeno passando da `core/plant/schemas.py`: le regole della coda in dataclass, come `Note`, e la conversione ai bordi.
8. **L'esempio `notes` resta**: toglierlo è fuori scope.

Le regole che i test devono difendere:
- solo l'esecutore riceve `PlantCommander`: non il server MCP, non l'agente, non le rotte di lettura. Verificato a run time, come in M5, e nel codice per nome;
- niente si esegue senza approvazione; una proposta approvata si esegue una volta sola; una rifiutata mai;
- l'audit si aggiunge e basta: nessun UPDATE né DELETE sulla tabella, verificato anche su Postgres vero;
- senza il token giusto non si approva né si rifiuta (401), e l'audit registra il nome dichiarato; il token non compare in nessun tool, prompt, log o risposta;
- il guardrail ferma i parametri fuori dai limiti prima della coda;
- fuori dallo sviluppo il controllo della simulazione non esiste: `production_problems()` lo rifiuta e le sue rotte non ci sono;
- con l'impianto in-process, più di un worker è rifiutato all'avvio;
- Anthropic irraggiungibile: l'endpoint dell'agente risponde 503 in formato RFC 9457;
- i test della CI non chiamano mai la rete (l'agente con il client finto di M5). La soglia di copertura (99,5 % con i rami) resta.

Fuori scope, anche se sembrano facili: servizio plant-sim e tempo che scorre da solo (M2), interfaccia e notifiche, RAG e manuali, multi-agente, memory, secondo fornitore, togliere `notes`, Grafana.

Come procedere:
1. Fai la prova del passo 1 e riportami l'esito.
2. Proponi i moduli, la tabella e la sua migrazione, gli endpoint e i test, e aspetta il mio ok.
3. Prima i test (le regole della coda, l'esecutore, il guardrail, gli endpoint con i fake), poi il codice, poi i test di integrazione su Postgres. Per ultimo la prova vera: da Claude Desktop una proposta via MCP, l'approvazione con il token, l'esecuzione sull'impianto; e una diagnosi dell'agente che finisce in coda. Riportami com'è andata e quanto è costato.
4. In `docs/development.md` (o nel README) la demo passo per passo: avviare, far avanzare il tempo, iniettare un guasto, proporre, approvare, vedere l'esecuzione.

Fine sessione: tutti i controlli della CI verdi, commit in Conventional Commits con il solo nome di chi sviluppa, docs/decisioni.md aggiornato se una decisione cambia. Poi dimmi cosa devo controllare io e quali dubbi restano: il prompt della fase dopo lo scriviamo dopo.
