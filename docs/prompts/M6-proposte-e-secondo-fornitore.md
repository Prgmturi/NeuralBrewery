Leggi AGENTS.md, poi docs/decisioni.md:
- "Requisiti del corso";
- in "Scelte fatte", le voci "Agenti", "datapizza con Claude", "Secondo fornitore", "Cache dei prompt" ed "Eval degli agenti";
- "Ancora aperte" e la roadmap.

Poi docs/impianto.md: "Il controllore non riparte da solo" e la tabella sotto il programma della cotta (pausa, `reset`, `resume_program`).

L'agente è in `features/agents/` e `adapters/claude/`, gli eval in `tests/evals/`. Come un adapter traduce gli errori di un servizio esterno: ADR 0006 e `adapters/claude/client.py`.

Obiettivo di questa sessione (M6), in due parti:
- **A.** L'agente propone `reset` quando la causa è chiara e già risolta. La sua proposta arriva dal vivo in coda, viene approvata ed eseguita: è il passo che M4 non ha raggiunto dal vivo.
- **B.** Lo stesso agente gira anche su Gemini (piano gratuito), attraverso il client compatibile OpenAI di datapizza, scelto da un'impostazione. Gli eval confrontano i due fornitori. È il "client multi-provider" che chiede il corso.

Al discorso (19 novembre) mancano 4 giorni: serve la soluzione più semplice che rispetta le regole. Prima A, che non ha bisogno di chiavi nuove. B comincia dal suo cancello.

Prerequisiti, da controllare prima di tutto:
- **Il branch.** La PR #13 (M4) è unita a `master`. Lavora su un branch nuovo, `feat/m6-proposte-e-secondo-fornitore`, creato da `master` aggiornato. Aggiorna `master` senza cambiare branch (`git fetch origin master:master`), poi crea il branch da lì: così le modifiche non committate vengono con te.
- **Il primo commit.** `docs/decisioni.md` ha modifiche non committate, con le decisioni di questa fase e di M7. Committale per prime, da sole, con un commit `docs:`; questo prompt va nello stesso commit.
- **I manuali.** `data/manuals/` ha file non tracciati: non vanno nei commit.
- **Le chiavi.** `ANTHROPIC_API_KEY` e `OPENAI_COMPAT_API_KEY`, la chiave di Gemini, stanno solo in `.env` o nell'ambiente, mai nel repo. Se `OPENAI_COMPAT_API_KEY` manca, fai A, poi fermati prima di B e dimmelo.

## Parte A: l'agente che propone

Fatti già verificati attraverso le porte (15 novembre, `brew_day`, seed 42):
- **Sonda TT1 rotta durante il riscaldamento, poi riparata:** resta `control_probe_fault` su HLT, e `resume_program` è rifiutato ("serve prima reset"). Dopo `reset` il blocco sparisce e `resume_program` fa ripartire il programma.
- **Inverter M1 in guasto, poi riparato:** gli allarmi spariscono da soli. `reset` è accettato ma non cambia niente, e basta `resume_program`.

Quindi un pulsante sblocca e un altro riprende. Nella demo sono due proposte: il `reset` dall'agente, la ripresa da Claude Code via MCP.

1. **Prima l'eval, poi il prompt.** Aggiungi uno scenario, S4 "sonda riparata, blocco attivo", che passa solo se l'agente propone `reset`. Oggi l'agente non propone niente, quindi S4 deve fallire: eseguilo prima di cambiare il prompt e riportami il risultato. S2 (pompa bloccata) resta com'è, e vieta di far ripartire.
2. **Cambia il prompt dell'agente il meno possibile.** La regola nuova: quando la causa è chiara e già risolta, e resta solo il blocco del controllore, proponi `reset`. Per tutto il resto la prudenza resta.
3. **Riesegui tutti gli eval**, S4 almeno tre volte: il modello non è deterministico. Riportami verdetti e costo. Se S1–S3 peggiorano, fermati e dimmelo prima di insistere.
4. **La prova dal vivo**, sullo stack del compose:
   1. guasto e riparazione con `/simulation`;
   2. la diagnosi dall'endpoint dell'agente, e la proposta che entra in coda;
   3. l'approvazione con il token, e l'esecuzione;
   4. la ripresa.

   Aggiorna con questo giro la demo in `docs/development.md` (passo 4).

## Parte B: lo stesso agente su Gemini

**Passo 1, un cancello e non una formalità.** Fai una chiamata vera da questa macchina, con un tool, usando la chiave di Gemini e `OpenAILikeClient` di datapizza. L'endpoint compatibile OpenAI di Gemini è `https://generativelanguage.googleapis.com/v1beta/openai/`. Il client sta in `datapizza-ai-clients-openai-like`, dipendenza approvata il 15 novembre, che si risolve con il `datapizza-ai-core` installato e porta `openai` 2.x.

La chiamata deve rispondere a tre domande:
- **Il modello.** Quale modello Flash-Lite usare: con questa chiave, il 15 novembre, l'elenco dei modelli dava `gemini-3.5-flash-lite` e `gemini-flash-lite-latest`. Verifica se regge i tool e lo schema di `submit_diagnosis`, che scriviamo da un modello pydantic (vedi la voce su datapizza in decisioni). Il README del client dice che i tool funzionano "dove supportati": verificalo.
- **Tempi e limiti.** Quanto dura una chiamata, e che cosa risponde il piano gratuito quando si superano i limiti. I limiti veri sono in Google AI Studio, non nei blog.
- **Le impostazioni solo di Claude.** Quali oggi valgono solo per Claude (effort, cache dei prompt, 16000 token, fallback sui rifiuti), e dove stanno.

Se con Gemini i tool non reggono, prova lo stesso codice su Groq, cambiando solo indirizzo, modello e chiave. Se non va nemmeno lì, fermati e dimmelo: il ripiego è un secondo modello per un compito piccolo, da decidere insieme. Una chiave Groq la crea chi sviluppa: chiedimela.

Decisioni già prese:
1. **Il fornitore è un'impostazione.**
   - `AGENT_PROVIDER` vale `claude`, il default, oppure `openai_compat`.
   - Il secondo fornitore ha la sua sezione in `core/config/`: `OPENAI_COMPAT_BASE_URL`, `OPENAI_COMPAT_MODEL` e `OPENAI_COMPAT_API_KEY`. La chiave è un segreto (`SecretStr`).
   - Claude resta il default, e la demo dal vivo resta su Claude.
2. **Un adapter** in `adapters/openai_compat/`, come `adapters/claude/`. Traduce gli errori dell'SDK `openai` nelle eccezioni di `core/exceptions.py` (ADR 0006): limiti superati e servizio irraggiungibile diventano `ServiceUnavailableError`, una risposta inutilizzabile `ExternalServiceError`. Se serve cambiare altro del client di datapizza, fermati e chiedimelo.
3. **L'agente non conosce il fornitore.** Un contract vieta agli agenti l'SDK `openai`, come quello di Anthropic. Le impostazioni solo di Claude restano fuori dal codice condiviso.
4. **Gli eval girano sul fornitore scelto.** La tabella finale dà verdetto, token e costo per scenario e per fornitore. Il piano gratuito costa zero: la tabella lo dice.
5. **Fatto quando** gli eval girano su tutti e due i fornitori e la tabella li confronta. Se Gemini fallisce qualche scenario, è un risultato da raccontare nel discorso, non un blocco.

## Le regole che i test devono difendere

- con qualunque fornitore, l'agente riceve solo `PlantReader`, e mette in coda solo attraverso la casella delle proposte;
- con `AGENT_PROVIDER=openai_compat` e la chiave vuota, l'endpoint dell'agente risponde 503 in formato RFC 9457, come con Claude;
- il secondo fornitore irraggiungibile o oltre i limiti: 503; risposta inutilizzabile: 502;
- la chiave non compare in log, risposte, prompt o trace;
- i test della CI non chiamano mai la rete. La soglia di copertura resta.

Fuori scope, anche se sembrano facili:
- memoria (M7: il metodo è deciso, vedi decisioni);
- README e scan dell'immagine (M8);
- RAG e multi-agente;
- M2;
- login su `/mcp`;
- interfaccia.

## Come procedere

1. Parte A, punto 1: lo scenario S4 e il suo risultato di oggi.
2. Proponi il cambio del prompt e aspetta il mio ok. Poi porta A fino alla prova dal vivo.
3. Parte B: fai il cancello e riportami l'esito. Poi proponi file, impostazioni e test, e aspetta il mio ok.
4. Prima i test, poi il codice. Per ultimi gli eval su tutti e due i fornitori: riportami com'è andata e quanto è costato.

Fine sessione:
- tutti i controlli della CI verdi;
- commit in Conventional Commits, con il solo nome di chi sviluppa;
- `docs/decisioni.md` aggiornato, se una decisione cambia.

Poi dimmi cosa devo controllare io e quali dubbi restano. Il prompt della fase dopo lo scriviamo dopo.
