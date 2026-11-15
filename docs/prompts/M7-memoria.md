Leggi AGENTS.md, poi docs/decisioni.md:
- "Requisiti del corso";
- in "Scelte fatte", le voci "Agenti", "Memoria di M7: le decisioni del birraio", "Coda delle proposte e audit", "Una proposta fuori dai limiti è bloccata", "Anche l'agente mette in coda", "L'agente non passa dal server MCP" ed "Eval degli agenti";
- "Ancora aperte" e la roadmap.

Il codice da conoscere:
- l'agente: `features/agents/` (`plant_agent.py`, `tools.py`, `router.py`);
- la porta della casella: `core/approvals/` (`protocols.py`, `schemas.py`);
- la coda: `features/approvals/`. Gli eventi stanno in `domain/proposal.py`, e `ProposalLog.page()` legge le proposte a pagine, dalla più recente;
- gli eval: `tests/evals/`.

Obiettivo di questa sessione (M7): **la memoria persistente** che chiede il corso. L'agente impianto legge le decisioni passate del birraio sulle sue proposte, e ne tiene conto. Il metodo è già deciso: niente tabella nuova. La coda conserva già:
- ogni proposta dell'agente;
- l'approvazione o il rifiuto, con il motivo;
- l'esito sull'impianto.

Un tool in più la fa leggere all'agente.

Al discorso (19 novembre) mancano 3 giorni, e il 17 c'è il pannello (M7b): serve la soluzione più semplice che rispetta le regole.

Prerequisiti, da controllare prima di tutto:
- **Il branch.** La PR #14 (M6) è unita a `master`. Lavora su un branch nuovo, `feat/m7-memoria`, creato da `master` aggiornato: `git fetch origin master:master`, poi crea il branch da lì.
- **Il primo commit.** Questo prompt, da solo, con un commit `docs:`.
- **I manuali.** `data/manuals/` ha file non tracciati: non vanno nei commit.
- **Le chiavi.** `ANTHROPIC_API_KEY` e `OPENAI_COMPAT_API_KEY` stanno solo in `.env`. `AGENT_PROVIDER` non va nel `.env`: lo leggerebbe anche il compose, e la demo passerebbe a Gemini. Per gli eval su Gemini esportalo solo per quel comando.

## Il caso che la memoria deve risolvere

S4 di M6: TT1 si è rotta, poi è tornata a leggere bene, e resta solo il blocco del controllore. L'agente propone `reset`, ed è giusto.

Supponiamo ora che, in una cotta precedente, il birraio abbia **rifiutato** lo stesso `reset` con il motivo *"TT1 ha un contatto intermittente: va sostituita prima di riarmare"*. Con la memoria, l'agente:
- non propone di nuovo `reset`;
- dice nella spiegazione che il birraio l'aveva rifiutato, e perché;
- mette fra le verifiche la sostituzione di TT1.

## Decisioni già prese

1. **Una porta di sola lettura in `core/approvals/`**, accanto a `ProposalInbox`:
   - le feature non si importano a vicenda, quindi l'implementazione sta in `features/approvals/` e `bootstrap.py` la passa all'agente;
   - la porta legge e basta: niente approvare, rifiutare, proporre;
   - i tipi che servono alla porta stanno in `core/approvals/schemas.py`, in Python puro.
2. **Che cosa legge l'agente.** Solo le proposte dell'agente, con:
   - comando e argomenti;
   - la spiegazione della diagnosi;
   - lo stato finale: in attesa, bloccata, approvata, rifiutata, eseguita, fallita;
   - il motivo del rifiuto o del blocco;
   - la risposta del controllore.

   Le proposte arrivate da MCP restano fuori. Il loro `why` è testo scritto da chiunque raggiunga `/mcp`, che non chiede login: un agente che propone non deve leggere testo non fidato (decisioni, "Agenti").
3. **Niente tempo reale** (regola 5): né il campo `at` né date. Anche il `sim_time_s` di una cotta passata non si confronta con quello di adesso, perché un riavvio riparte da zero. Le decisioni arrivano in ordine dalla più recente, senza tempi, e al massimo un numero fisso (proponi tu quante).
4. **Il prompt dell'agente cambia il meno possibile.** Prima di proporre un pulsante, l'agente legge le decisioni passate. Se il birraio ha rifiutato lo stesso pulsante per la stessa causa, non lo propone di nuovo, e lo dice nella spiegazione. Per tutto il resto la prudenza resta com'è.
5. **Il server MCP non riceve il tool nuovo.** Resta com'è.
6. **Gli eval:**
   - **S5 "reset già rifiutato"**: l'impianto di S4, più una decisione passata, il `reset` rifiutato con il motivo sopra. Passa solo se l'agente ha letto la memoria e non propone `reset`;
   - **S1–S4** girano con una memoria vuota, e devono restare come prima;
   - negli eval la memoria è un oggetto in memoria che implementa la porta: niente database.

## Come procedere

1. **Prima l'eval, poi il codice.** Aggiungi S5 e la memoria finta degli eval. Oggi l'agente non ha il tool, quindi S5 deve fallire: eseguilo e riportami il risultato.
2. **Proponi file, porta, tool e cambio del prompt, e aspetta il mio ok.** Prima i test, poi il codice.
3. **Riesegui tutti gli eval**, su Claude e su Gemini, S5 almeno tre volte su Claude. Riportami verdetti e costo. Se S1–S4 peggiorano, fermati e dimmelo prima di insistere.
4. **La prova dal vivo**, sullo stack del compose, con `curl`: il pannello arriva in M7b.
   1. Porta l'impianto alla situazione di S4.
   2. Fai diagnosticare l'agente, e **rifiuta** il suo `reset` con il motivo.
   3. Fai diagnosticare di nuovo: la seconda diagnosi deve citare il rifiuto, e non riproporre `reset`.
   4. Riavvia l'API: l'impianto riparte da zero, la coda resta in Postgres. Rifai l'impianto di S4 e diagnostica: l'agente ricorda ancora il rifiuto. È la prova che la memoria è persistente.

   Aggiorna con questo giro la demo in `docs/development.md`.

## Le regole che i test devono difendere

- l'agente riceve solo `PlantReader` e la porta di sola lettura delle decisioni: niente che approvi, rifiuti o comandi;
- il tool non restituisce mai le proposte MCP né il loro `why`;
- nella risposta del tool non compaiono tempi reali;
- con la coda irraggiungibile, il tool risponde all'agente con un errore in parole, come gli altri tool, e la diagnosi continua;
- i test della CI non chiamano mai la rete. La soglia di copertura resta.

Fuori scope, anche se sembrano facili:
- il pannello (M7b);
- README e scan dell'immagine (M8);
- le "lezioni strutturate" della memoria dopo il corso;
- RAG e multi-agente;
- il tool della memoria nel server MCP;
- login su `/mcp`;
- M2.

Fine sessione:
- tutti i controlli della CI verdi;
- commit in Conventional Commits, con il solo nome di chi sviluppa;
- `docs/decisioni.md` aggiornato, se una decisione cambia.

Poi dimmi cosa devo controllare io e quali dubbi restano. Il prompt della fase dopo lo scriviamo dopo.
