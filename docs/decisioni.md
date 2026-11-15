# Decisioni di progetto

## In una frase

Un agente AI per un impianto di birrificazione simulato: monitora i sensori, diagnostica i
problemi con la memoria delle cotte passate, e propone azioni che vengono eseguite solo con
l'approvazione del birraio, con guardrail e audit trail su ogni passaggio. Dopo il corso: RAG
sui manuali e più agenti.

## Requisiti del corso e dove li copriamo

| Requisito | Dove |
|---|---|
| Tool calling | Lettura impianto, calcoli, proposta azioni |
| Client multi-provider | Lo stesso agente su Claude o su Gemini (via client compatibile OpenAI), scelto da un'impostazione; gli eval li confrontano (M6) |
| Memory persistente | Le decisioni del birraio sulle proposte passate, che l'agente legge dalla coda (M7) |
| Architettura giustificata | Agente singolo con privilegio minimo: legge e propone. Comanda solo l'esecutore, dopo il guardrail, la coda e l'approvazione del birraio |
| Flusso fisso (DagPipeline, se il caso lo richiede) | Non serve per ora: un agente con i tool. Dopo il corso, con memoria e manuali |
| Guardrail | Parametri del tool che propone, prima della coda (M4) |
| Audit trail | Tracing di ogni passo + tabella di audit append-only (proposte, approvazioni, esecuzioni) |
| Eval pass/fail | Scenari di guasto con seed fisso (trajectory), su Claude e su Gemini |
| README, deve girare | docker compose; al tester serve solo una chiave API (M8) |
| RAG (facoltativo) | Dopo il corso: manuali dei componenti, ricerca ibrida + rerank |

## Scelte fatte

- **Agenti** (15 novembre): per il corso un agente solo, l'agente impianto, che legge e propone;
  comanda solo l'esecutore, dopo l'approvazione. *Perché*: il corso accetta un agente singolo
  con una riga di motivazione, e al discorso mancano 4 giorni. Dopo il corso: orchestratore
  (parla con l'utente), agente impianto (unico che propone azioni), agente analista (dati,
  calcoli, diagnosi), perché chi legge testo non fidato non deve poter proporre azioni.
- **Codice, non LLM**: approvazione ed esecuzione, allarmi, interlock. *Perché*: devono
  funzionare anche se l'LLM sbaglia, è lento o viene manipolato. Gli allarmi hanno due
  fonti: il controllore dell'impianto riporta fatti ("sonda guasta", "K1 aperto"), il
  sorvegliante a regole fisse giudica il processo ("le due sonde non concordano").
- **Diagnosi su allarme come flusso fisso**, dopo il corso: per ora un agente con i tool.
  *Perché*: prevedibile, economico, facile da valutare. L'agente libero resta per la chat.
- **Memory**, dopo il corso: lezioni strutturate (evento, causa, intervento, esito), scritte solo a caso chiuso.
  I numeri restano nel database e si leggono con i tool. *Perché*: evita di avvelenare la memory.
- **Memoria di M7: le decisioni del birraio** (15 novembre). La coda conserva già ogni proposta
  dell'agente, l'approvazione o il rifiuto con il suo motivo, e l'esito; un tool in più le fa
  leggere all'agente. Niente tabella nuova. *Perché*: è la strada più corta, e la memoria che
  serve è proprio ciò che il birraio ha deciso. Limite: ricorda solo le diagnosi che hanno
  proposto un pulsante. Fatta così (M7, 15 novembre):
  - una porta di sola lettura, `DecisionReader` in `core/approvals/`, accanto a
    `ProposalInbox`. La implementa `features/approvals/`, e `bootstrap.py` la passa all'agente
    insieme al lettore dell'impianto: niente che proponga, approvi o comandi;
  - il tool `read_decisions` dà le ultime 10 proposte dell'agente, dalla più recente. Per
    ognuna: pulsante e argomenti, la spiegazione di allora, lo stato finale, il motivo del
    rifiuto o del blocco, la risposta del controllore. 10 bastano per una giornata di demo, e
    costano poche migliaia di token;
  - solo le proposte dell'agente, filtrate nella query prima del limite: con 8 proposte MCP
    recenti, l'agente vede lo stesso le sue ultime 10. Le proposte MCP restano fuori perché il
    loro `why` lo scrive chiunque raggiunga `/mcp`;
  - nessun tempo: né il momento reale né il `sim_time_s`, che un riavvio rimette a zero;
  - con la coda irraggiungibile la porta alza `ServiceUnavailableError`, e il tool lo dice
    all'agente a parole: la diagnosi continua con i tool dell'impianto;
  - il prompt ha una riga in più: prima di proporre un pulsante l'agente legge le decisioni, e
    non ripropone un pulsante rifiutato per la stessa causa;
  - il server MCP non ha il tool.

  Un difetto che la memoria ha fatto emergere, nel testo degli allarmi (15 novembre). Con il
  tool nuovo Gemini Flash-Lite sbagliava S4: al posto di `reset` proponeva `resume_program`,
  che il controllore rifiuta finché il blocco c'è. 0 volte su 4, contro 3 su 3 con il codice
  di M6. Non dipendeva da che cosa dice il tool: con la regola nella sua descrizione 0 su 3,
  con una descrizione di una riga, mai chiamata, 1 su 3. La causa stava nell'impianto: con TT1
  riparata il blocco diceva ancora "sonda TT1 non valida: regolazione sospesa", senza una parola
  sul riarmo. Claude lo deduceva dal prompt; Gemini ci arrivava per poco, e un tool in più
  bastava a farlo cadere. Ora il testo di un blocco che si riarma con `reset` finisce con
  "(bloccato: serve reset)", come sul pannello di un impianto vero (`docs/impianto.md`). Con
  questo S4 su Gemini passa 3 volte su 3, e `resume_program` non compare più.

  Eval sul codice finale: Claude passa tutti e cinque, S5 3 volte su 3; S3 una volta su 4 ha
  proposto di spegnere l'agitatore, un comando prudente che lo scenario non ammette. Gemini
  passa tutti e cinque; S2 una volta su 4 ha indicato la valvola EV2a invece della pompa, senza
  proporre niente. Nessuno dei due errori si ripete su tre giri: si tengono così.

  Limite: se la causa è "la stessa" lo giudica il modello. Il guardrail non ferma una proposta
  già rifiutata: la memoria è un consiglio all'agente, non una regola in codice. L'eval S5 lo
  verifica.
- **RAG classico**, dopo il corso (ibrido + rerank) con metadati per componente e sigla. *Perché*: le relazioni
  tra componenti sono già note dalla configurazione dell'impianto, non serve estrarle con un LLM.
  Tabelle dei codici di errore spezzate una riga per chunk.
- **Impianto**: vedi `docs/impianto.md`. Componenti reali con manuali pubblici, tenuti nel repo
  in `data/manuals/`. Cotta da 20 L: le taglie dei recipienti vengono dal fermentatore reale e
  dai conti dell'acqua. Un percorso alla volta; niente riempimento della HLT, sonda TT4,
  deriva, chimica. *Perché*: i requisiti del corso stanno tutti nella parte AI. Un dettaglio
  si simula solo se crea un sintomo che l'agente può vedere, o la conseguenza di un'azione
  che può proporre.
- **Controllore tra AI e impianto**: l'impianto è governato da un controllore simulato (un PLC
  generico). Agenti, sorvegliante ed esecutore vedono e comandano solo attraverso di lui; lui
  conosce solo i segnali dei dispositivi, e ogni dispositivo dice solo ciò che il suo manuale
  prevede. Fuori dal controllore resta la sicurezza cablata (K1), l'unica che agisce sui valori
  veri. *Perché*: è come sono fatti gli impianti veri, e fissa con precisione che cosa un
  agente può osservare. Le tre porte sono l'interfaccia del controllore: con un impianto vero
  cambierebbe solo l'adattatore.
- **Programma della cotta nel controllore**: una ricetta a passi, con conferme del birraio e un
  tempo massimo per passo. *Perché*: dà alla diagnosi il contesto ("siamo nella sosta, minuto
  25 di 60") e un allarme tipico degli impianti veri, il passo in ritardo.
- **Il programma è un birraio fatto di codice**: preme i pulsanti del pannello, quindi gli
  rispondono gli stessi interlock, e non riarma mai un blocco. Quando qualcosa è bloccato va
  in pausa da solo; riprende solo con `reset` e `resume_program`. *Perché*: è la regola del
  controllore che non riparte da solo, e dà alla parte AI un flusso completo: programma in
  pausa, diagnosi, proposta di riarmo e ripresa, approvazione.
- **Comandi con una fine certa**: un travaso è a quantità e si ferma da solo. *Perché*: tra la
  proposta e l'esecuzione c'è un'approvazione umana; uno stop che dipende da una seconda
  approvazione arriverebbe tardi.
- **Il controllore non riparte da solo**: ciò che un interlock ferma resta fermo, con il suo
  allarme, finché il birraio o l'esecutore non riarma (`reset`, o un nuovo comando sulla
  stessa cosa). *Perché*: proseguire dopo un allarme è una decisione di chi ne risponde, e
  dà alla parte AI un flusso completo: allarme, diagnosi, proposta di riarmo, approvazione.
- **Test dell'impianto**: solo scenari sull'impianto intero, attraverso le porte (un test per
  guasto, per interlock e per K1, più i conti della cotta e il determinismo). Niente test
  strato per strato. *Perché*: sono i comportamenti su cui poggiano gli eval; il resto
  toglierebbe tempo alla parte AI. La soglia di copertura della CI non cambia.
- **Simulatore**: servizio separato, un solo worker, modalità a passi per test ed eval, con un
  passo di calcolo fisso. Tiene uno storico breve delle letture e dei comandi, che si legge
  dalla porta `PlantReader`. *Perché*: diagnosi ed eval girano senza database, e lo stesso
  scenario dà sempre lo stesso risultato.
- **Confine AI–impianto**: porte e adattatori (vedi `AGENTS.md`).
- **Ordine dopo M1b** (13 novembre): prima la parte AI, con l'impianto in-process: primo agente,
  sorvegliante e primo eval (M5). Il servizio plant-sim (M2) viene dopo, ridotto, solo se serve
  alla demo. *Perché*: tutti i requisiti obbligatori del corso stanno nella parte AI e girano
  senza il servizio; al discorso (19 novembre) mancano 6 giorni.
- **Framework agenti: datapizza-ai.** Solo `datapizza-ai-core`, `datapizza-ai-clients-anthropic`
  e, da M6, `datapizza-ai-clients-openai-like`: il pacchetto `datapizza-ai` installa anche
  Qdrant e altri client, che non usiamo. *Perché*: è il
  framework di riferimento del corso, e i requisiti ne nominano i pezzi (`DagPipeline`,
  `ContextTracing`).
- **datapizza con Claude, provato con chiamate vere** (14 novembre: `datapizza-ai-core` 0.1.3,
  client Anthropic 0.0.8, `claude-sonnet-5-5`). Funzionano il ciclo con più tool, `max_tokens`,
  `effort` e il fallback lato server sui rifiuti, che passano come argomenti della chiamata.
  I limiti, aggirati senza un nostro client:
  - la risposta strutturata (`output_cls`) non regge i tool: la diagnosi arriva come argomenti
    di un tool finale, `submit_diagnosis`. Li controlliamo noi con pydantic, perché datapizza
    non chiede all'API di garantire lo schema;
  - i blocchi di ragionamento non tornano a Claude tra un tool e l'altro: l'API lo accetta, e si
    perde solo il ragionamento di quel turno. Sui passi semplici Sonnet non ragiona affatto.
    Accettato per M5;
  - il ciclo ignora lo `stop_reason`: su un rifiuto senza testo richiamerebbe il modello fino a
    `max_steps`. Un hook ferma i passi vuoti, e lo `stop_reason` si legge dal tracing;
  - un `tool_choice` forzato dà 400 su questo modello: sempre `auto`;
  - per un parametro enum facoltativo, lo schema che datapizza ricava dalla firma non si
    serializza in JSON: lo schema di `submit_diagnosis` lo scriviamo da un modello pydantic;
  - datapizza stampa ogni passo sulla console: l'agente gli dà un logger che scrive con
    structlog. Resta il riepilogo dei token che `ContextTracing` stampa a fine diagnosi.

  *Perché*: il resto del framework serve ai requisiti del corso, e un nostro client sarebbe
  codice in più da mantenere.
- **Modello: Claude (Anthropic)**, primo agente su `claude-sonnet-5-5` (14 novembre), con il
  fallback lato server sui rifiuti. *Perché*: costa la metà di `claude-opus-5-5` (2 $ e 10 $
  per milione di token in entrata e in uscita, contro 4 $ e 20 $).
- **Secondo fornitore: Gemini Flash-Lite, piano gratuito, con un client compatibile OpenAI**
  (15 novembre). Lo stesso agente, scelto da un'impostazione; Claude resta il default e la demo
  dal vivo resta su Claude. Gli eval girano su tutti e due e li confrontano. Il client è
  `OpenAILikeClient` di datapizza: indirizzo, modello e chiave sono impostazioni, quindi lo
  stesso codice raggiunge anche Groq o un modello locale. *Perché*: non abbiamo altre chiavi a
  pagamento, e Mistral non dà più chiavi API senza il piano a pagamento. Per Gemini basta un
  account Google: secondo fonti di ottobre 2026, Flash-Lite dà circa 15 richieste al minuto e
  500 al giorno, mentre Flash ne dà 20 al giorno. Un giro di eval ne chiede 30–40. Groq, il
  ripiego, limita i token al minuto (8 mila) e renderebbe lenta ogni diagnosi; un modello locale
  su questo portatile, senza scheda grafica, lo sarebbe ancora di più. I limiti veri si leggono
  in Google AI Studio. Sul piano gratuito Google può usare le richieste per migliorare i suoi
  prodotti: qui è innocuo, perché i dati dell'impianto sono finti.
- **Gemini, provato con chiamate vere** (15 novembre, cancello di M6: client openai-like
  0.0.11, `openai` 2.54):
  - il modello è `gemini-3.5-flash-lite`, fissato. `gemini-flash-lite-latest` è un altro nome
    che punta già a un 3.x, e cambierebbe modello sotto gli eval; `gemini-2.5-flash-lite`
    risponde 404, "non più disponibile per i nuovi utenti";
  - tool e schema di `submit_diagnosis` reggono. Una chiamata dura da 0,6 a 2,2 s, una diagnosi
    da 4 a 7 s. Gemini legge un tool per chiamata, Claude ne chiede più insieme: in entrata
    Gemini usa da 1,3 a 2,3 volte i token di Claude, in uscita da 4 a 6 volte meno;
  - il piano gratuito dà, per progetto e per modello, 15 richieste al minuto, 250 mila token
    al minuto e 500 richieste al giorno (Google AI Studio, 15 novembre). Le richieste al giorno
    si azzerano a mezzanotte del Pacifico, le 9 in Italia (pagina dei limiti di Google). Oltre
    il limite risponde 429 `RESOURCE_EXHAUSTED`, "riprova tra 14 s". Un giro di eval chiede
    circa 21 richieste. Uno scenario fa fino a 12 chiamate, e le due riprove dell'SDK non
    aspettano 14 s: sul piano gratuito gli eval partono a un minuto l'uno dall'altro;
  - due cose che datapizza sbaglia con Gemini 3, sistemate nell'adapter
    (`adapters/openai_compat/`), che ridefinisce due metodi del client di datapizza:
    - la firma del ragionamento (`thought_signature`) che Gemini mette sulla prima chiamata a
      un tool di ogni risposta: datapizza non la rimanda, e Gemini risponde 400 alla seconda
      chiamata della diagnosi. L'adapter la tiene per id della chiamata e la rimette;
    - due chiamate parallele della stessa risposta: datapizza le rimanda in due messaggi, e
      Gemini rifiuta la seconda come un turno senza firma (400). L'adapter le rimette in un
      messaggio solo, come vuole anche OpenAI. `parallel_tool_calls=False` viene accettato ma
      ignorato.

  *Perché*: è la strada più corta per avere il secondo fornitore con lo stesso agente; Groq,
  il ripiego, non regge diagnosi da 13–30 mila token in entrata con 8 mila token al minuto.
  Limite: se datapizza cambia quei due metodi interni, l'adapter si rompe. I test della CI
  rifanno la conversazione con le risposte di Gemini, senza rete, e se ne accorgono. Gli altri
  modelli gratuiti non convengono: Gemini 2.5 Flash dà 20 richieste al giorno, un giro di
  eval appena.
- **Cache dei prompt su ogni chiamata**: datapizza non la attiva, e l'adapter passa
  `cache_control` come argomento della chiamata. Provata nell'eval di M5: in S2, 6,6 mila token
  scritti nella cache e 15,6 mila letti. *Perché*: in un ciclo con i tool ogni chiamata rimanda
  tutta la conversazione, e su `claude-sonnet-5-5` una lettura dalla cache costa un ventesimo
  dell'input.
- **Tracing in locale** con `ContextTracing` di datapizza: ogni passo dell'agente (chiamata al
  modello con il suo `stop_reason` e i token, tool con gli argomenti) resta in memoria, e l'eval
  lo scrive su file. *Perché*: basta per l'audit trail e per gli eval, senza un servizio in più
  nel compose.
- **Eval degli agenti a mano**, fuori dalla CI (`uv run pytest -m eval`): scenari di guasto con
  seed fisso, verdetto passa / non passa con controlli in codice sulla risposta strutturata e
  sulla traiettoria, niente LLM come giudice. *Perché*: costa, e la CI non ha la chiave; un
  giudice LLM sarebbe un'altra fonte di errore da valutare. Da M6 girano sul fornitore di
  `AGENT_PROVIDER`, e una tabella confronta l'ultimo giro di ciascuno.
- **Sorvegliante su richiesta**: una funzione a regole fisse che riceve solo `PlantReader`,
  chiamata dopo ogni avanzamento del tempo o da un tool dell'agente; nessun ciclo in background.
  Si costruisce con il primo agente (M5), non in M2. *Perché*: con il tempo a passi l'impianto è
  fermo tra un avanzamento e l'altro, quindi il controllo resta deterministico; ed è lui che fa
  partire la diagnosi.
- **Fino a M2 l'impianto vive nel processo dell'API** (14 novembre, per M4): `bootstrap.py` lo
  costruisce da una partenza con nome e lo mette in `app.state`, con uno `StateKey` per porta. Il
  tempo avanza solo con un comando di `SimulationControl` esposto dall'API in sviluppo, e dopo
  ogni avanzamento si chiama il sorvegliante; nessun ciclo in background. Un solo worker: con più
  worker ci sarebbero più impianti, ognuno diverso: `SERVER_WORKERS` diverso da 1 ferma l'avvio.
  Un riavvio costruisce un impianto nuovo dalla stessa partenza; la coda resta in Postgres. Il
  timeout dell'esecutore c'è, ma con l'impianto nel processo un comando risponde subito: conta
  dal servizio di M2. *Perché*: un processo solo e deterministico, e la demo si guida a passi;
  il tempo che scorre da solo è il lavoro di M2.
- **Server MCP dentro l'API**, su HTTP: i tool di lettura e uno per proporre un'azione, che mette
  la proposta in coda. Non approva e non comanda. *Perché*: vede lo stesso impianto e la stessa
  coda, senza un secondo processo. `mcp` è una dipendenza diretta (`>=2.3.0,<3`, dentro i
  limiti di datapizza); la sua protezione degli host prende `SERVER_TRUSTED_HOSTS`, che
  altrimenti rifiuterebbe ogni host fuori da localhost con 421.
- **La demo si fa da una dashboard del birraio in Streamlit** (15 novembre, a fine M6). È una
  pagina sola sopra l'API, con un solo endpoint in più (sotto):
  - stato dell'impianto e allarmi;
  - comandi della simulazione, solo in sviluppo;
  - il pulsante della diagnosi, con la spiegazione dell'agente;
  - la coda, con approva e rifiuta.

  `streamlit` è una dipendenza approvata. Niente chat e niente orchestratore: restano dopo il
  corso, con il multi-agente. *Perché*: con i `curl` in un terminale, in un discorso di 10
  minuti si capisce poco. Claude Code in demo sembrava parte del prodotto, ed era un punto in
  più in cui incepparsi. La dashboard viene dopo la memoria (M7), che il corso chiede, e prima
  del README (M8). Fatta così (M7b, 15 novembre):
  - **un client dell'API, e basta**: `src/neuralbrewery/dashboard/` parla HTTP con l'API, come
    `curl`, e non importa niente dell'app. Due contract di import-linter lo verificano, uno per
    verso: la dashboard non importa l'app, l'app non importa né la dashboard né Streamlit;
  - **un'immagine sua** (`docker/dashboard.Dockerfile`), servizio `dashboard` del compose, su
    http://localhost:8501. Installa solo il gruppo `dashboard` di `pyproject.toml` (Streamlit,
    httpx, pydantic-settings); `dev` lo include, per mypy e i test. *Perché*: Streamlit porta
    13 pacchetti che l'API non usa, misurati il 15 novembre: pyarrow 165 MB, pandas 45, numpy
    30, pydeck 23 e altri. Nell'immagine dell'API sarebbero passati da 276 a circa 590 MB, e
    sarebbero stati pacchetti in più per la sua scansione. Quel giorno Grype, con la versione
    della CI, non vi trovava nessuna High o Critical con una correzione: il motivo è il peso,
    e le vulnerabilità che verranno. Così l'immagine dell'API resta com'era, e al tester di
    M8 basta ancora `docker compose`. In produzione la dashboard parte solo con
    `--profile dashboard`;
  - **il token** lo legge da `DASHBOARD_APPROVAL_TOKEN`, che il compose imposta; il nome di chi
    decide lo scrive il birraio nella pagina. Il token non compare mai nella pagina né nei log;
  - **solo su 127.0.0.1**, anche in sviluppo: la pagina tiene il token, e nessuno sul Wi-Fi
    della sala deve poter approvare. Streamlit non manda le statistiche d'uso, e non chiede a
    un servizio esterno l'indirizzo pubblico della macchina, che altrimenti cerca per
    stamparlo all'avvio (visto nella prova del container);
  - **niente in background**: la pagina si ridisegna quando il birraio preme o scrive. Ogni
    azione è un callback, quindi la pagina mostra l'impianto dopo l'azione. L'ultima diagnosi
    resta sulla pagina, e scrivere un nome non richiama l'agente;
  - **i comandi della simulazione** compaiono solo se la descrizione dell'API (`/openapi.json`)
    elenca `/simulation/advance`. Fuori dallo sviluppo la descrizione non c'è, e la simulazione
    è comunque rifiutata;
  - **test senza rete**: `streamlit.testing` esegue la pagina sopra l'API vera in memoria (un
    `TestClient`, che è un client httpx), con la coda in memoria e un agente finto. I 401, i
    409 e i 503 vengono dall'app, non da JSON scritto a mano. Una fixture fa fallire ogni
    chiamata che uscirebbe dal processo. Per misurare la pagina, che gira come script
    (`__main__`), la copertura legge la cartella `src/neuralbrewery` invece del nome del
    package.
- **Il birraio propone dalla dashboard con il suo token** (M7b, 15 novembre). Nella demo di M6
  la ripresa della cotta (`resume_program`) e l'avvio (`start_program`) li proponeva Claude
  Code, via MCP. Ora li propone il birraio: `POST /approvals`, con `X-Approval-Token` e il nome
  dichiarato, mette in coda la proposta come `user`, attraverso lo stesso guardrail. Non preme
  niente: la proposta aspetta l'approvazione come ogni altra, e sono due eventi nell'audit.
  *Perché*: la strada senza backend nuovo era `propose_action` su `/mcp`, che scrive sempre
  `mcp`. Nella coda la ripresa chiesta dal birraio sarebbe stata identica a una proposta di
  Claude Code: l'audit avrebbe detto il falso, e il video del server MCP ("la proposta compare
  come `mcp`") non avrebbe più distinto niente. La memoria dell'agente non cambia: legge solo
  le proposte `agent`.
- **Il server MCP si mostra con un video, non dal vivo** (15 novembre). Claude Code esce dalla
  demo dal vivo. Durante M7b o la prova di M8 si registra un video breve: Claude Code legge
  l'impianto e propone, e la proposta compare nella coda del pannello con mittente `mcp`. Il
  video va in una slide; se avanza tempo, dal vivo si rifà in 30 secondi. *Perché*: il corso
  mette fra ciò che alza il livello "un MCP server custom usato anche da un altro host", e va
  dimostrato, non solo raccontato.
- **L'agente non passa dal server MCP** (15 novembre). Agente e server MCP usano gli stessi
  strumenti: l'agente li chiama da dentro l'app, il server MCP li apre agli assistenti
  esterni. Il corso consiglia, senza obbligarlo, di collegare un server MCP all'agente (S12).
  *Perché*: farlo costerebbe circa un giorno, e gli eval, che oggi girano con l'impianto in
  memoria, dovrebbero accendere l'app intera. Con memoria e README ancora da fare, non vale il
  rischio.
- **Chi approva: chi ha il token di approvazione** (14 novembre). Approvare e rifiutare chiedono
  un token dal `.env` (`APPROVAL_TOKEN`) e il nome di chi approva, che l'audit registra come
  dichiarato, non verificato. Il token non arriva mai ai tool MCP né all'agente, e
  `production_problems()` rifiuta il valore di sviluppo. Keycloak resta nel compose e il login del
  template funziona, ma la demo non lo usa. *Perché*: senza un segreto niente distinguerebbe il
  birraio da un modello che chiama da solo l'endpoint; con Keycloak la demo avrebbe chiesto un
  login senza frontend e un realm da reimportare. Passare a Keycloak cambia solo la dipendenza
  dell'endpoint, non la coda né l'audit.
- **Coda delle proposte e audit**: una feature a tre strati, `features/approvals/`, con una tabella
  Postgres a cui si aggiunge e basta: proposta, approvazione o rifiuto, esecuzione con la risposta
  del controllore. L'esecutore è l'unico codice che riceve `PlantCommander`: esegue solo proposte
  approvate, con un timeout. Prima di entrare in coda i parametri di ogni proposta si
  controllano: è il guardrail su un tool che chiede il corso, un secondo livello dopo gli
  interlock. *Perché*: l'approvazione è codice, mai una decisione dell'LLM, e ogni passaggio resta
  scritto.
- **Una proposta fuori dai limiti è "bloccata"** (15 novembre): un tipo di evento in più, oltre a
  proposta, approvata, rifiutata, eseguita, esecuzione fallita. Il guardrail la ferma prima della
  coda, chi l'ha mandata riceve il motivo, e il blocco resta nell'audit. *Perché*: nell'audit si
  distingue chi ha detto no, il guardrail o il birraio. Il passo di ogni evento è il suo `seq`
  (0 la nascita, 1 la decisione, 2 l'esito): un vincolo unico su (proposta, `seq`) e un controllo
  che lega il tipo al passo danno a ogni proposta una sola decisione e un solo esito, anche con
  due approvazioni nello stesso istante. Ogni evento si salva nella sua transazione, prima del
  passo dopo.
- **Il controllo della simulazione è spento se non lo si chiede** (15 novembre):
  `PLANT_SIMULATION_CONTROL` vale false per default, il compose di sviluppo e `.env.example` lo
  accendono, staging e produzione lo rifiutano. *Perché*: chiunque raggiunga quelle rotte
  muove il tempo dell'impianto e lo guasta.
- **Anche l'agente mette in coda**: un endpoint diagnostica l'impianto adesso e mette in coda la
  proposta della diagnosi, se c'è. Esposto dall'API, l'agente deve tradurre gli errori di
  Anthropic (ADR 0006): lo fa una sottoclasse minima del client di datapizza, nell'adapter, che
  non fa altro. *Perché*: è il flusso completo della demo: allarme, diagnosi, proposta,
  approvazione, esecuzione.
- **Base del codice**: template `fastapi_starter` (FastAPI, PostgreSQL, Alembic, structlog,
  SQLAlchemy async, Keycloak, uv, import-linter, CI, release-please).
- **Nome**: il progetto si chiama NeuralBrewery. Repo `NeuralBrewery`; package Python, immagine
  Docker e nomi tecnici (realm e client Keycloak) `neuralbrewery`, una sola forma minuscola
  senza trattini né underscore, come richiedono package e immagini. La versione riparte da 0.1.0
  con un CHANGELOG vuoto: la storia del template non è la storia di questo progetto.

## Come si innesta nel template

- **Un solo package, un'immagine per l'app, due servizi nel compose**: `api` (il backend del
  template) e `plant-sim` (stessa immagine, comando diverso, un solo worker). Fino a M2 c'è solo
  `api`, con l'impianto nel suo processo. Da M7b la dashboard del birraio ha un'immagine sua,
  con il solo gruppo `dashboard`: è un client dell'API, non una parte dell'app (sopra).
- **Il simulatore vive in `adapters/plant_sim/`.** Per il backend l'impianto è un servizio
  esterno, e il template vieta già alle feature di importare gli adapter: per toccare
  l'impianto devono passare dalle porte, e la CI lo controlla.
- **Porte e vocabolario in `core/plant/`**, come `core/auth/` per il login.
- **Errori**: l'adapter REST traduce gli errori di httpx nelle eccezioni del template (ADR 0006).
  Al posto del `PlantUnavailableError` del prototipo si usa `ServiceUnavailableError`.
- **Impostazioni** in `core/config/plant.py`. `production_problems()` rifiuta i token di
  sviluppo e il controllo della simulazione fuori dallo sviluppo (ADR 0007).
- **I processi restano separati**: nel compose il backend parla con `plant-sim` solo via REST,
  con il token dell'esecutore per i comandi.
- **Alternativa scartata**: workspace uv con due package. Separazione più netta, ma va
  adattato tutto il tooling del template (Dockerfile, CI, test su lockfile e package).
- **L'esempio `features/notes` resta**, anche dopo M4 e la sua prima feature nostra a tre strati
  (14 novembre): su di lui poggiano due contract, il test e2e e lo smoke test della CI. Si toglie
  solo se avanza tempo.

## Ancora aperte

- Un'interfaccia per leggere i trace (Langfuse o Phoenix): solo se serve alla demo.
- Approvazione con identità verificata (Keycloak, un ruolo `brewer`): solo se avanza tempo.
- Claude Desktop come client MCP: i suoi connettori partono dal cloud di Anthropic e non
  raggiungono `localhost`; la configurazione locale lancia programmi, quindi servirebbe un ponte
  (`npx mcp-remote http://localhost:8000/mcp`). La demo di M4 usava Claude Code, che parla HTTP;
  da M7b la demo dal vivo non usa nessun client MCP.
- `/mcp` e `/agents/plant/diagnose` non chiedono login: in sviluppo va bene, fuori no. Chi
  raggiunge l'API legge l'impianto, mette proposte in coda e spende diagnosi; approvare no, serve
  il token. Deciso il 15 novembre: per il corso resta così, ed è un limite noto. Proteggerli
  chiederebbe un secondo token, perché quello del birraio non arriva mai all'AI.
- Limite noto (15 novembre): se l'API cade tra il pulsante premuto e la scrittura dell'esito, la
  proposta resta approvata senza esito e non si riesegue. Il pulsante non viene mai premuto due
  volte, e l'impianto in-process riparte comunque da zero.
- Limiti noti finché l'impianto vive nell'API (15 novembre): il timeout dell'esecutore c'è ed è
  testato, ma dal vivo non scatta, perché l'impianto risponde nello stesso processo; far
  avanzare il tempo blocca l'API per circa 0,16 s per ora simulata. M2 non si fa per il corso.
- MQTT: solo se serve, dopo.
- Notifiche, e un'interfaccia completa: dopo il corso. Per il corso c'è la dashboard di M7b.
- Limiti noti della dashboard (15 novembre, dalla prova dal vivo):
  - i token che mostra sono quelli che l'API riporta: fuori dalla cache e letti dalla cache.
    Quelli scritti nella cache datapizza non li passa, quindi il costo di una diagnosi lo
    misurano gli eval, sulle risposte del fornitore: 2 o 3 centesimi su Claude;
  - dopo un `reset` approvato l'allarme resta sulla pagina fino al prossimo avanzamento del
    tempo: il controllore lo toglie al suo giro successivo. Nella demo si avanza il tempo
    subito dopo.
- L'immagine della dashboard la CI la costruisce nello stack di e2e, ma non la scansiona, come
  non scansiona quella di Keycloak. Ha la stessa immagine base dell'API: le vulnerabilità di
  `zlib1g` sono anche sue. Da decidere in M8, con la scansione.
- M2, dopo il corso: tempo a passi e un comando di `SimulationControl` per ripartire da una
  partenza con nome, invece di riavviare il container (preferenze, da confermare).
- Adattatore verso un controllore vero (per esempio OPC UA): le letture hanno già la sua forma
  (valore, qualità, tempo). Non serve al corso: solo se avanza tempo.
- CI su GitHub: il controllo "Build container image" è rosso anche su `master`. La scansione
  trova due vulnerabilità in `zlib1g` dell'immagine base, e il rapporto non si carica da un
  repo privato. Si sistema in M8, dopo i requisiti obbligatori (15 novembre): il badge della CI
  in cima al README è rosso.

## Roadmap

| # | Milestone | Fatto quando |
|---|---|---|
| M0 | Rinomina del package, posti vuoti per l'impianto, contract, script manuali | Controlli della CI verdi |
| M1 | Vocabolario, porte, processo, dispositivi e controllore con comandi manuali, interlock, allarmi e storico breve (Python puro) | Test di plausibilità, interlock e guasti verdi |
| M1b | Programma della cotta nel controllore | Una cotta intera simulata, con 20 L nel fermentatore |
| M2 | Servizio plant-sim, adapter REST, impostazioni, compose (dopo il corso) | Test di contratto in-process e REST verdi |
| M3 | Storico su Postgres + Grafana (dopo il corso) | Grafici di una cotta simulata |
| M4 | Impianto nel processo dell'API, server MCP (lettura + proposta), coda approvazioni con audit ed esecutore, l'agente che mette in coda | Proposta → approvazione → esecuzione da Claude Code (15 novembre: Claude Desktop non è installato e vorrebbe un ponte, vedi sotto) |
| M5 | Primo agente (impianto) + sorvegliante + tracing + primo eval | Eval pass/fail su 3 scenari |
| M6 | L'agente propone `reset` quando la causa è risolta; lo stesso agente anche su Gemini | Una proposta dell'agente in coda, approvata ed eseguita dal vivo; eval su tutti e due i fornitori, confrontati |
| M7 | Memoria persistente: le decisioni del birraio, lette dalla coda | Un eval in cui l'agente usa una decisione passata |
| M7b | Dashboard del birraio in Streamlit, sopra l'API: impianto, simulazione, diagnosi, coda con proponi, approva e rifiuta | La demo si fa tutta dalla dashboard, senza `curl` né Claude Code; una proposta di Claude Code via MCP compare nella coda della dashboard (il video per la slide) |
| M8 | README dell'impianto e della demo, scan dell'immagine, prova della demo | La demo gira da zero seguendo il README |

Ordine: dopo M1b viene M5, con l'impianto in-process; dopo M5 viene M4 (deciso il 14 novembre,
a fine M5). A fine M4 (15 novembre): M6, M7 e M8 prima del discorso, con il 18 novembre tenuto
per M8 e la prova della demo. A fine M6 (15 novembre): M7 il 16, il pannello (M7b) il 17, M8 il
18. Dopo il corso: M2, M3, RAG sui manuali con RAGAS, multi-agente con l'orchestratore e la
baseline, red teaming, eval in CI, interfaccia completa.
