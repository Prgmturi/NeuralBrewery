# Guida rapida a NeuralBrewery

Questa guida spiega cosa fa il progetto oggi, dove cercare il codice e come seguire una
diagnosi fino all'impianto. Non serve conoscere prima l'intelligenza artificiale o la
birrificazione.

## In breve

NeuralBrewery è un'API FastAPI collegata a un birrificio simulato. Un agente AI può leggere
lo stato dell'impianto, cercare indizi e consegnare una diagnosi. Se suggerisce un comando,
questo resta in attesa: soltanto il birraio può approvarlo e farlo eseguire.

Il progetto usa **un solo agente impianto**, non un gruppo di agenti. Oggi l'agente usa
strumenti per leggere lo stato e lo storico; **non consulta ancora i manuali con RAG** e
non legge le decisioni passate come memoria. RAG e un sistema multi-agente sono sviluppi
futuri, descritti in [decisioni di progetto](decisioni.md).

## Da dove iniziare

Per provare il progetto con Docker:

```bash
docker compose up --build --wait
```

Apri <http://localhost:8000/docs> per esplorare le API. Compose usa valori di sviluppo e
accende i comandi di simulazione; per chiedere una diagnosi serve anche la chiave del modello
scelto (`ANTHROPIC_API_KEY` per Claude, oppure `OPENAI_COMPAT_API_KEY` per il provider
compatibile con OpenAI). La chiave resta nell'ambiente o nel file `.env`, mai nel codice.

Per la demo completa, compresi esempi di approvazione, iniezione guasti e uso di MCP, segui
la [guida allo sviluppo](development.md#the-demo-from-a-proposal-to-the-plant). Le
impostazioni di produzione non devono esporre le rotte di simulazione: MCP e diagnosi non
richiedono login nella configurazione attuale, quindi non esporre un'istanza di sviluppo su
Internet.

## Il flusso completo

```text
impianto simulato
       │ letture, eventi, storico
       ▼
PlantReader ──▶ agente AI ──▶ diagnosi strutturata
                                  │ se contiene un comando
                                  ▼
                          guardrail ──▶ coda + audit
                                           │
                                decisione del birraio
                                  ┌────────┴────────┐
                               rifiuta          approva
                                                  │
                                                  ▼
                                          esecutore unico
                                                  │
                                                  ▼
                                         PlantCommander
                                                  │
                                                  ▼
                                             controllore
```

1. **Il controllore mostra lo stato.** Agenti e API leggono misure, qualità dei sensori,
   allarmi, eventi e storico attraverso `PlantReader`.
2. **L'agente cerca indizi.** Riceve gli allarmi del controllore e i giudizi del sorvegliante,
   poi usa i suoi strumenti di lettura. Distingue un guasto di misura (il sensore mente) da
   uno di processo (l'impianto è guasto).
3. **L'agente consegna una risposta strutturata.** Indica componente, tipo di guasto, quanto
   è sicuro, spiegazione e verifiche manuali. Può non proporre alcun comando se servono prima
   controlli sul posto.
4. **Il guardrail controlla la proposta.** Accetta solo i pulsanti del pannello e gli
   argomenti previsti, entro i limiti impostati. Una proposta fuori limite viene bloccata e
   ne viene registrato il motivo.
5. **Il birraio decide.** Approva o rifiuta una proposta in attesa. L'approvazione richiede
   il token; una proposta approvata viene eseguita subito.
6. **L'esecutore preme il pulsante.** È l'unico componente applicativo con accesso a
   `PlantCommander`. Il controllore verifica comunque i propri interlock e può rifiutare
   l'azione: guardrail e approvazione non li sostituiscono.

Le decisioni e gli esiti sono salvati come eventi di audit append-only. L'approvazione è
gestita dal codice, mai delegata al modello.

## Concetti AI, senza gergo

- **Agente:** un modello a cui il progetto dà un compito e strumenti limitati. Qui il compito
  è trovare una causa plausibile e, se sicuro, proporre un pulsante.
- **Tool calling:** il modello sceglie quando chiamare funzioni messe a disposizione
  dall'app. Può leggere stato, eventi, storico e giudizi del sorvegliante; `submit_diagnosis`
  consegna il risultato. Gli strumenti di lettura non possono comandare l'impianto.
- **Diagnosi strutturata:** la risposta ha campi e valori controllati, non è solo testo
  libero. Questo consente all'app e agli eval di verificare componente, tipo di guasto e
  comando proposto.
- **Provider:** il servizio che esegue il modello. `AGENT_PROVIDER` seleziona Claude
  (predefinito) o un servizio compatibile con l'API OpenAI, configurabile per esempio con
  Gemini.
- **RAG:** cercare informazioni in documenti e mostrarle al modello prima della risposta.
  I manuali pubblici sono previsti nel progetto, ma la ricerca RAG non è parte dell'agente
  attuale.
- **Memoria:** usare informazioni di sessioni o decisioni precedenti. La coda conserva le
  proposte e le decisioni per l'audit, ma oggi l'agente non le interroga come memoria.
- **Eval:** prove ripetibili in scenari di guasto. Il codice valuta la diagnosi e i passaggi
  dell'agente; non si chiede a un altro modello se la risposta è giusta.

## Come è organizzato il codice

Il codice segue una regola semplice: le dipendenze vanno verso le parti più generali.

| Percorso | Cosa contiene |
|---|---|
| `src/neuralbrewery/main.py` | Crea l'app, registra rotte e avvio/arresto |
| `src/neuralbrewery/bootstrap.py` | Costruisce i servizi e assegna a ciascuno solo le porte necessarie |
| `src/neuralbrewery/features/agents/` | Agente, strumenti di lettura, diagnosi, endpoint e server MCP |
| `src/neuralbrewery/features/approvals/` | Guardrail, coda, audit, API ed esecutore |
| `src/neuralbrewery/features/plant/` | Lettura dell'impianto e controllo della simulazione |
| `src/neuralbrewery/core/plant/` | Vocabolario, porte, pannello, accessi limitati e sorvegliante |
| `src/neuralbrewery/adapters/plant_sim/` | Processo, dispositivi, controllore e simulatore |
| `src/neuralbrewery/adapters/claude/` e `openai_compat/` | Collegamento ai provider AI e traduzione dei loro errori |
| `tests/evals/` | Scenari e criteri automatici per valutare l'agente |

Una **porta** descrive cosa si può fare senza dire come. `PlantReader` legge,
`PlantCommander` invia i comandi e `SimulationControl` fa avanzare il tempo o inserisce
guasti. Le porte sono separate per dare a ogni parte solo i permessi necessari. Il simulatore
è Python puro; non dipende da FastAPI o dal database.

L'API parla anche con PostgreSQL: la coda delle approvazioni e il suo audit sono persistenti.
L'impianto, invece, è attualmente nello stesso processo dell'API: al riavvio riparte da
zero. Il servizio separato `plant-sim` è previsto per una fase futura.

## Impianto e sicurezza

Il simulatore rappresenta quattro recipienti e un controllore che funziona come un PLC.
Il modello distingue i valori reali del processo da ciò che leggono i sensori: un sensore
guasto può ingannare il controllore. La protezione cablata K1 guarda invece la temperatura
reale. Le azioni disponibili sono pulsanti ad alto livello (per esempio impostare una
temperatura o avviare un percorso), non comandi diretti a valvole o fili.

Gli **interlock** sono controlli del controllore: fermano o rifiutano azioni pericolose, per
esempio una resistenza senza liquido sufficiente. Un blocco non si risolve da solo quando la
causa sparisce: può servire un reset approvato. Il tempo è simulato e avanza solo su richiesta;
seed e azioni uguali producono lo stesso scenario.

## Provare i flussi principali

- `GET /plant`: stato visto dal controllore.
- `POST /agents/plant/diagnose`: avvia la diagnosi; se l'agente propone un comando, lo mette
  in coda.
- `GET /approvals`: elenca le proposte e gli eventi associati.
- `POST /approvals/{id}/approve` o `/reject`: registra la decisione del birraio. Serve
  `X-Approval-Token`; approvare esegue subito il comando.
- `POST /simulation/advance` e `/simulation/faults`: avanzano la simulazione e inseriscono o
  rimuovono guasti. Sono rotte per sviluppo e prove, non per la produzione.
- `/mcp`: offre a un client MCP gli stessi strumenti di lettura e la possibilità di proporre
  un comando; non permette di approvare o comandare direttamente.

## Verifiche e letture successive

```bash
uv run pytest                 # test unitari
uv run pytest -m integration  # test con PostgreSQL
uv run pytest -m e2e          # prova login e API attraverso lo stack
uv run pytest -m eval         # scenari AI; usa il provider e la sua chiave
```

Per i dettagli pratici: [sviluppo e demo](development.md), [impianto e guasti](impianto.md),
[architettura](architecture.md), [decisioni e roadmap](decisioni.md) e
[manuali dei componenti](../manuals/manifest.toml).
