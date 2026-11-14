Leggi AGENTS.md, docs/decisioni.md (soprattutto "Scelte fatte" e "Ancora aperte") e docs/impianto.md: "In breve", "Il principio", gli allarmi e "Guasti iniettabili". L'impianto è in `src/neuralbrewery/adapters/plant_sim/`; l'adattatore in-process è `adapter.py`, le partenze con nome sono in `starts.py`. Leggi i test in `tests/adapters/plant_sim/` per vedere come si guida l'impianto.

Obiettivo di questa sessione (M5): il primo agente, il sorvegliante e il primo eval, con l'impianto in-process. Niente servizio plant-sim (M2), niente REST, niente compose.

Prerequisiti, da controllare prima di tutto:
- La chiave Anthropic è in `ANTHROPIC_API_KEY` (ambiente o `.env`), con credito. Se manca, fermati e dimmelo. La chiave non entra mai nel repo.
- La PR #10 (M1 e M1b) è unita a `master`. Se non lo è, fermati e dimmelo.
- Lavora su un branch nuovo, `feat/m5-primo-agente`, creato da `master` aggiornato. `docs/decisioni.md` ha modifiche non committate con le decisioni di questa fase (ordine, datapizza-ai, Claude, sorvegliante): portale sul branch nuovo e committale per prime, da sole, con un commit `docs:`. `docs/prompts/M5-primo-agente.md`, questo prompt, va nello stesso commit.

Passo 1, un cancello e non una formalità: la prova di datapizza con Claude. Il client Anthropic di datapizza (0.0.8) usa l'SDK `anthropic` 0.x e non rimanda a Claude i blocchi di ragionamento tra un tool e l'altro; su `claude-opus-5-5` il ragionamento non si spegne. Prima di costruire qualunque cosa, prova con una chiamata vera esattamente le strade che userai:
- un ciclo con più tool: chiamata, risultato, seconda chiamata, risposta finale;
- la risposta strutturata, se l'eval la legge;
- `max_tokens` esplicito: il client ripiega su 2048, e il ragionamento consuma lo stesso budget;
- `tool_choice` sempre `auto`: "required", "required_first" o una lista di nomi diventano uso forzato dei tool, che su `claude-opus-5-5` dà errore 400;
- `effort` esplicito (`high` per la diagnosi; il default del modello è `medium`).
Se una di queste fallisce, fermati e riportami l'errore. La soluzione prevista (un nostro client Anthropic per datapizza) chiede il mio ok: niente rattoppi silenziosi.

Decisioni già prese:
1. **Dipendenze**: solo `datapizza-ai-core` e `datapizza-ai-clients-anthropic`, non il pacchetto `datapizza-ai`. Il vincolo `anthropic<1.0` viene dal client di datapizza: scrivilo nel commit. datapizza-ai-core non ha `py.typed`: per mypy strict serve un override mirato. Python 3.13 rientra nel suo `<3.14`.
2. **Modello**: `claude-opus-5-5`. Se datapizza lo permette, attiva il fallback lato server sui rifiuti (`fallbacks: "default"` con la beta `server-side-fallback-2026-07-01`); altrimenti tratta `stop_reason == "refusal"` come un esito esplicito, non come un'eccezione qualunque.
3. **Regola 1**: l'agente riceve solo `PlantReader`. Può proporre un'azione, ma la proposta è solo testo strutturato nella risposta: non viene eseguita da nessuno finché non ci sono approvazioni ed esecutore (M4).
4. **Sorvegliante**: regole fisse in Python puro, senza LLM, che ricevono solo `PlantReader` e restituiscono allarmi. Si chiama quando serve (dopo un avanzamento del tempo, o da un tool dell'agente); nessun ciclo in background. Prima regola: le due sonde del fermentatore che non concordano. Le altre di docs/impianto.md ("giudizi sul processo") solo se servono agli scenari.
5. **Tracing**: ogni passo dell'agente tracciato con `ContextTracing` di datapizza, in locale. Niente servizi esterni.
6. **Dove va il codice**: proponilo tu seguendo docs/architecture.md. Le regole del sorvegliante sono dominio puro; datapizza resta fuori dal dominio.

L'eval:
- tre scenari con guasti iniettati e seed fisso. Proposta di partenza, da rivedere nel piano: `probe_offset` su TT5a in fermentazione (il sorvegliante vede le sonde in disaccordo; la temperatura dell'iSpindel fa da terzo testimone), `pump_blocked` durante un travaso (l'agente deve proporre verifiche, non indovinare), `drive_fault` F11 sull'agitatore;
- il verdetto è passa / non passa, con controlli deterministici sulla risposta strutturata dell'agente (componente indicato, guasto di misura o di processo, proposta tra i comandi ammessi). Niente LLM come giudice;
- marker proprio, fuori dalla CI: costa e la CI non ha la chiave. Si lancia a mano.

Le regole che i test devono difendere:
- nessun pezzo dell'agente riceve `PlantCommander` o `SimulationControl`;
- il sorvegliante dà lo stesso allarme con lo stesso seed e le stesse azioni, e nessuno sull'impianto sano;
- il percorso dell'LLM è coperto con un client finto: i test della CI non chiamano mai la rete. La soglia di copertura (99,5 % con i rami) resta.

Fuori scope, anche se sembrano facili: multi-agente, RAG e manuali, memory, server MCP, approvazioni ed esecutore, servizio plant-sim, secondo fornitore, interfaccia.

Come procedere:
1. Fai la prova del passo 1 e riportami l'esito.
2. Proponi l'elenco dei moduli e dei test, e aspetta il mio ok.
3. Prima i test del sorvegliante e dell'agente con il client finto, poi il codice; per ultimo l'eval vero, e riportami i risultati dei tre scenari e quanto è costato.

Fine sessione: tutti i controlli della CI verdi, commit in Conventional Commits con il solo nome di chi sviluppa, docs/decisioni.md aggiornato se una decisione cambia. Poi dimmi cosa devo controllare io e quali dubbi restano: il prompt della fase dopo lo scriviamo dopo.
