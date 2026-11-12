# Impianto

Piccolo impianto pilota per cotte da 20 L: tre recipienti sul lato caldo e un fermentatore.
Componenti scelti tra prodotti reali con documentazione pubblica: il simulatore ne imita il
comportamento descritto nei manuali. Elenco documenti e link: `manuals/manifest.toml`.

Cosa è rimasto fuori è elencato in fondo, in "Semplificazioni volute".

## Il principio

L'impianto è già governato da un **controllore** (un PLC compatto: marca e protocollo non
contano, e non li simuliamo). Il birraio fa la cotta dal suo pannello. Agenti, sorvegliante
ed esecutore passano dalla stessa porta: non toccano mai sonde e attuatori.

1. **L'AI parla solo con il controllore.** Legge ciò che lui sa e comanda con i suoi
   pulsanti, gli stessi del birraio.
2. **Il controllore sa solo ciò che i dispositivi gli dicono.** Ogni dispositivo dice solo
   quello che il suo manuale prevede: un inverter dà un codice di guasto, una pompa niente.
3. **Il controllore agisce su ciò che crede; la sicurezza cablata agisce sulla realtà.**
   I termostati che aprono K1 sono fili, non programma.

```
Birraio, agenti, sorvegliante ──leggono──▶ ┌────────────────────────────────┐
Esecutore ──────────────────────comanda──▶ │ CONTROLLORE                    │
                                           │ misure, regolazione, comandi,  │
                                           │ interlock, programma, allarmi  │
                                           └──────▲──────────────┬──────────┘
                                          segnali │              │ uscite
                                           ┌──────┴──────────────▼──────────┐
                                           │ DISPOSITIVI                    │──▶ termostati ─▶ K1
                                           │ sonde, livelli, pompe, valvole │    (cablato)
                                           └──────▲──────────────┬──────────┘
                                           misura │              │ agisce
                                           ┌──────┴──────────────▼──────────┐
                                           │ PROCESSO (valori veri)         │
                                           └────────────────────────────────┘
```

| Strato | Cosa contiene | Chi lo vede |
|---|---|---|
| Processo | Liquidi, temperature, fermentazione: i valori veri | Nessuno. Solo test ed eval, per dare il voto |
| Dispositivi | Sonde, livelli, pompe, valvole, relè, inverter, con i loro guasti | Il controllore, attraverso i loro segnali |
| Controllore | Misure, regolazione, comandi, interlock, programma, allarmi, storico | Birraio, agenti, sorvegliante, esecutore |
| Sicurezza cablata | Termostati in serie che aprono K1 | Il controllore ne vede solo il contatto |

Esempio di cosa ne segue: un livello bloccato su "pieno" inganna il controllore, che lascia
accesa la resistenza a secco; la temperatura vera sale e K1 scatta. L'agente deve risalire
la catena partendo da ciò che il controllore mostra.

## La cotta di riferimento

Le taglie dei recipienti vengono da qui. Si parte dal fermentatore, che è un prodotto vero.

| Voce | Quantità |
|---|---|
| Grani | 4,5 kg |
| Acqua di impasto (3 L/kg) | 13,5 L |
| Acqua trattenuta dai grani (1 L/kg) | 4,5 L |
| Primo mosto | 9 L |
| Acqua di lavaggio dei grani | 17 L |
| Nel bollitore prima della bollitura | 26 L |
| Evaporata in 60 minuti | circa 3,4 L |
| Nel fermentatore | 20 L |
| Resta sul fondo del bollitore | circa 2,6 L |
| Acqua usata, su 35 L nella HLT | 30,5 L |

Il lavaggio dei grani si fa in due riprese (prima si svuota il tino, poi lo si riempie di
nuovo): è un metodo vero, e richiede un solo percorso alla volta.

## Recipienti

| Recipiente | Id | Capacità | Riscaldamento | Altro |
|---|---|---|---|---|
| Vasca acqua calda | HLT | 40 L | R1, 3 kW | Parte con 35 L |
| Tino | MASH | 30 L | R2, 2 kW | Agitatore M1, fondo filtrante, grani |
| Bollitore | BOIL | 40 L | R3, 3,5 kW | |
| Fermentatore | FERM | 26,5 L | R4, fascia 100 W | Blichmann G4 da 7 galloni. Serpentina a glicole, EV9 (~300 W di raffreddamento) |

Scambiatore a piastre tra bollitore e fermentatore: passivo, senza sonda. Il mosto ne esce a 20 °C.

## Dispositivi: cosa dicono al controllore

### Misure

| Sigla | Dove | Prodotto | Segnale | Cosa ne sa il controllore |
|---|---|---|---|---|
| TT1, TT2, TT3 | HLT, MASH, BOIL | PT100 E+H iTHERM TM411 + trasmettitore iTEMP TMT80 | 4–20 mA su 0–150 °C | Valore, corrente, stato del segnale |
| TT5a, TT5b | FERM | come sopra | come sopra | Come sopra. TT5a regola, TT5b è di confronto e di riserva |
| LT1–LT4 | HLT, MASH, BOIL, FERM | SICK LFP Cubic | 4–20 mA sul campo del recipiente | Valore, corrente, stato del segnale |
| DT1 | FERM | iSpindel (WiFi, ogni 15 min) | Un messaggio | Densità, temperatura, batteria, forza del segnale WiFi, età del messaggio |

**Stato di un segnale 4–20 mA.** Lo decide il controllore dalla corrente (NAMUR NE43; per il
TMT80 è a pagina 2 del suo foglio tecnico):

| Corrente | Significato | Qualità |
|---|---|---|
| da 3,8 a 20,5 mA | Misura valida | `GOOD` |
| fino a 3,6 mA, oppure da 21 mA in su | Lo strumento segnala un suo guasto | `BAD`, "strumento guasto" |
| circa 0 mA | Cavo interrotto o strumento senza alimentazione | `BAD`, "segnale assente" |

Il controllore sa *che* lo strumento è guasto, non *perché*.

- **PT100 classe A**: tolleranza ±(0,15 + 0,002·|t|) °C (IEC 60751; TM411, pagina 16).
  Ogni sonda ha un suo errore fisso entro tolleranza, estratto dal seed, più un rumore piccolo.
- **TMT80**: con la sonda rotta o in corto porta la corrente ad almeno 21,5 mA (impostazione
  "alta"). Si configura da PC: in esercizio non dà altre informazioni.
- **Livello SICK**: precisione ±5 mm (scheda tecnica, pagina 2), circa ±0,5 L. Come per le
  sonde: errore fisso per sensore più un rumore piccolo. In errore porta le uscite in stato
  sicuro; il messaggio preciso (`!InvEc`, `!Cable`...) compare solo sul suo display, quindi
  lo può leggere il birraio, non il controllore. Ha anche un collegamento digitale IO-Link,
  che qui non usiamo.
- **Nel tino** il livello vede il liquido più il volume dei grani.
- **iSpindel**: nessun messaggio da più di 30 minuti → qualità `STALE`.
- Ogni lettura porta il tempo simulato dell'ultima misura.

### Attuatori

| Sigla | Cosa | Prodotto | Comando | Ritorno al controllore |
|---|---|---|---|---|
| P1 | Pompa acqua calda (dalla HLT) | Blichmann RipTide | Accesa / spenta | Nessuno |
| P2 | Pompa mosto (comune) | Blichmann RipTide | Accesa / spenta | Nessuno |
| EV2a, EV2b | Mandata P1 → tino / → bollitore | U.S. Solid, valvola a sfera motorizzata inox, versione a 5 fili | Apri / chiudi | Due contatti di fine corsa: aperta, chiusa |
| EV3, EV4 | Aspirazione P2 ← tino / ← bollitore | come sopra | come sopra | come sopra |
| EV5, EV6, EV7 | Mandata P2 → ricircolo tino / → bollitore / → scambiatore e fermentatore | come sopra | come sopra | come sopra |
| EV9 | Glicole al fermentatore | come sopra | come sopra | come sopra |
| R1–R4 | Resistenze, comandate da relè statici | Crydom D2425 | Potenza da 0 a 100 % | Nessuno |
| K1 | Contattore di sicurezza a monte di tutte le resistenze | generico | Nessuno: lo aprono i termostati | Un contatto: chiuso / aperto |
| M1 | Agitatore del tino | motoriduttore + inverter Siemens SINAMICS V20 | Marcia / arresto, su linea seriale (Modbus) | In marcia o no, frequenza, corrente, codice di guasto |
| — | Chiller del glicole | Blichmann Glycol Chiller | Nessuno: è una macchina a sé | Nessuno |

- Lo stato riporta sempre il **comando**. Dove c'è un ritorno, riporta anche quello: sono
  due informazioni distinte, e un guasto si vede quando non concordano.
- Pompe, resistenze e chiller non hanno ritorno: un loro guasto si vede solo dagli effetti.
- Un guasto dell'inverter resta finché non viene confermato con `reset`.

## Sicurezza cablata

Un termostato per ogni recipiente riscaldato, in serie, fuori dal controllore. Se la
temperatura **vera** supera il limite, K1 si apre e toglie corrente a tutte le resistenze.

| Recipiente | Setpoint massimo | Scatto del termostato |
|---|---|---|
| HLT | 85 °C | 90 °C |
| MASH | 80 °C | 85 °C |
| BOIL | 100 °C | 105 °C |
| FERM | 30 °C | 35 °C |

- Il controllore vede solo "K1 aperto": non sa quale termostato è scattato.
- K1 si richiude solo con `reset`, e solo se tutti i termostati sono tornati sotto il limite.
- Nel bollitore l'acqua non supera i 100 °C: il termostato scatta solo se la resistenza
  lavora a secco.

## Controllore

### Regolazione

- Una sonda di regolazione per recipiente: TT1, TT2, TT3, TT5a.
- Acceso / spento con una banda di 0,5 °C. Nel fermentatore R4 scalda sotto il setpoint ed
  EV9 raffredda sopra.
- **Bollitura**: con setpoint a 100 °C, arrivata a 99,5 °C la resistenza R3 passa alla
  potenza di bollitura (75 %).
- **Sonda di regolazione non valida**: uscita a zero e allarme. Il fermentatore passa a
  TT5b e lo segnala.

### Comandi (porta `PlantCommander`)

Sono i pulsanti del pannello. Ogni comando risponde accettato o rifiutato, con un codice e
un motivo. Un comando rifiutato non è un errore.

| Comando | Cosa fa |
|---|---|
| `activate_route(percorso, litri)` | Travasa quella quantità e si ferma da solo. Il ricircolo non ha litri: gira finché non viene fermato |
| `stop_route()` | Ferma il travaso in corso |
| `set_temperature(recipiente, °C o spento)` | Imposta o toglie il setpoint |
| `set_agitator(acceso/spento)` | Avvia o ferma M1 |
| `start_program()` | Avvia la cotta automatica |
| `confirm_step()` | Conferma del birraio a un passo manuale |
| `pause_program()`, `resume_program()` | Mette in pausa e riprende |
| `abort_program()` | Chiude il programma e spegne il lato caldo |
| `stop_all()` | Ferma il lato caldo: travaso, R1–R3, agitatore; programma in pausa. **Non tocca il fermentatore** |
| `reset()` | Riarmo: richiude K1, conferma il guasto dell'inverter |

Ogni comando approvato ha una fine certa: per questo il travaso è a quantità.

### Percorsi

Gli unici percorsi ammessi. Il controllore apre e chiude le valvole da solo.

| Percorso | Pompa | Valvole |
|---|---|---|
| `hlt_to_mash` | P1 | EV2a |
| `hlt_to_boil` | P1 | EV2b |
| `mash_recirc` | P2 | EV3, EV5 |
| `mash_to_boil` | P2 | EV3, EV6 |
| `boil_to_ferm` | P2 | EV4, EV7 |

Un travaso procede così: apre le valvole, aspetta i contatti di fine corsa (al massimo
10 s), avvia la pompa, conta i litri sul livello misurato della sorgente, ferma la pompa
alla quantità chiesta, richiude le valvole. Portata delle pompe: 10 L/min.

### Interlock (sulle misure del controllore)

1. Resistenza accesa solo se il livello misurato copre l'elemento (HLT 8 L, MASH 6 L,
   BOIL 6 L, FERM 4 L).
2. R2 accesa solo se il mosto si muove: agitatore in marcia o ricircolo attivo.
3. Agitatore acceso solo se il livello misurato copre le pale (MASH 8 L).
4. Travaso solo se la sorgente ha almeno 2 L e la quantità chiesta entra nella destinazione.
   Durante il travaso: si ferma se la sorgente scende sotto 2 L o la destinazione è piena.
5. Un solo percorso attivo alla volta.
6. Travaso senza avanzamento: livello della sorgente fermo per 60 s → pompa ferma e allarme.
7. Valvola che non raggiunge la posizione in 10 s → travaso annullato e allarme.
8. Setpoint entro i limiti del recipiente (tabella della sicurezza cablata; FERM da 0 a 30 °C).
9. Livello non valido: vale come "livello sconosciuto", quindi resistenza spenta e travaso rifiutato.
10. Ogni intervento automatico produce un evento, con tempo simulato, codice e motivo.

### Programma della cotta

Una sola ricetta, quella dei conti qui sopra. Ogni passo ha un tempo massimo: oltre, il
controllore dà l'allarme `step_late` e prosegue.

| # | Passo | Cosa fa il controllore | Finisce quando | Tempo massimo |
|---|---|---|---|---|
| 1 | Scalda l'acqua | HLT a 72 °C | TT1 arriva a 72 °C | 60 min |
| 2 | Impasto | `hlt_to_mash` 13,5 L; agitatore acceso | Travaso finito | 5 min |
| 3 | Porta il tino a 66 °C | MASH a 66 °C; HLT a 78 °C | TT2 arriva a 66 °C | 15 min |
| 4 | Sosta | Mantiene | Passati 60 min | — |
| 5 | Fine sosta | MASH a 76 °C | TT2 arriva a 76 °C | 15 min |
| 6 | Ricircolo | Agitatore spento; `mash_recirc` | Passati 10 min | — |
| 7 | Primo mosto | MASH spento; `mash_to_boil` 9 L | Travaso finito | 5 min |
| 8 | Lavaggio | HLT spenta; `hlt_to_mash` 17 L | Travaso finito | 5 min |
| 9 | Ricircolo | `mash_recirc` | Passati 10 min | — |
| 10 | Secondo mosto | `mash_to_boil` 17 L | Travaso finito | 5 min |
| 11 | Porta a bollore | BOIL a 100 °C | TT3 arriva a 99,5 °C | 30 min |
| 12 | Bollitura | Potenza di bollitura | Passati 60 min | — |
| 13 | Pronto al travaso | BOIL spento; aspetta il birraio | `confirm_step` | — |
| 14 | Al fermentatore | `boil_to_ferm` 20 L | Travaso finito | 5 min |
| 15 | Lievito | Aspetta il birraio; poi FERM a 19 °C | `confirm_step` | — |

- **Stati**: fermo, in corso, in attesa di conferma, in pausa, finito, annullato.
- **Pausa automatica**: se un allarme impedisce il passo (travaso annullato, K1 aperto,
  sonda di regolazione guasta, inverter in guasto) il programma va in pausa e dice perché.
- **In pausa** le temperature restano, i travasi e il conteggio del tempo si fermano.
  `resume_program` riprende il passo; un travaso riparte dai litri che mancano.
- **Con il programma in corso** i comandi manuali del lato caldo sono rifiutati; in pausa
  sono ammessi.
- Una cotta intera dura circa 3 ore e 40 minuti simulati.

### Allarmi ed eventi

Il controllore riporta **fatti**. Un allarme resta attivo finché la causa c'è.

| Codice | Quando | Su cosa |
|---|---|---|
| `signal_fault` | Segnale 4–20 mA guasto o assente | TT, LT |
| `hydrometer_silent` | Nessun messaggio dall'iSpindel da più di 30 min | DT1 |
| `control_probe_fault` | Regolazione sospesa, o passata alla sonda di riserva | Recipiente |
| `valve_not_reached` | Valvola non arrivata in 10 s | EV |
| `transfer_no_progress` | Livello fermo per 60 s durante un travaso | Percorso |
| `transfer_stopped` | Travaso fermato: sorgente bassa o destinazione piena | Percorso |
| `heater_blocked` | Resistenza bloccata: livello basso o mosto fermo | R |
| `agitator_blocked` | Agitatore bloccato: livello basso | M1 |
| `drive_fault` | L'inverter segnala un guasto, con il suo codice | M1 |
| `safety_open` | K1 aperto | K1 |
| `step_late` | Passo oltre il tempo massimo | Programma |
| `program_paused` | Programma in pausa per un allarme | Programma |

Sono eventi: ogni allarme che nasce o finisce, ogni comando accettato, ogni cambio di passo.

I **giudizi sul processo** non sono del controllore ma del sorvegliante (M2): due sonde che
non concordano, temperatura lontana dal setpoint, livelli che cambiano senza un travaso,
densità ferma.

### Lettura (porta `PlantReader`)

| Chiamata | Cosa restituisce |
|---|---|
| `snapshot()` | La fotografia del controllore in questo istante (tabella sotto) |
| `events(da quando)` | Gli eventi, dal più vecchio |
| `history(sigla, da quando)` | Lo storico breve di una sigla |

| Nella fotografia | Contenuto |
|---|---|
| Tempo | Tempo simulato |
| Letture | Per sigla: valore, unità, qualità e motivo, corrente in mA (se 4–20 mA), tempo dell'ultima misura. Per l'iSpindel quattro letture: densità, temperatura, batteria, segnale |
| Dispositivi | Per sigla: comando e, dove esiste, ritorno. Per M1 anche frequenza, corrente e codice di guasto |
| Regolazione | Per recipiente: setpoint, sonda in uso |
| Travaso | Percorso attivo, litri chiesti, litri fatti |
| Programma | Stato, numero e nome del passo, tempo trascorso e tempo massimo |
| Allarmi | Quelli attivi: codice, sigla, testo, da quando |

**Storico breve**: letture e comandi di resistenze, pompe ed EV9, con finestra e passo
configurabili (24 ore e 60 s). Basta per la diagnosi e per gli eval, senza database.

### Simulazione (porta `SimulationControl`)

Non fa parte del controllore: è la mano di chi prova. Solo test, eval e demo.

- **Tempo**: `advance(secondi)`. Il passo di calcolo è fisso, scelto alla creazione del
  simulatore (1 s; 10 s per le fermentazioni lunghe), e il tempo si conta in passi interi.
- **Guasti**: `inject_fault`, `clear_faults`. Un guasto su una sigla che non lo ammette è
  un errore, non viene ignorato.
- **Partenze con nome**:
  - *giorno di cotta*: HLT con 35 L, tino con 4,5 kg di grani asciutti, bollitore e
    fermentatore vuoti;
  - *fermentazione*: lato caldo vuoto e spento, fermentatore con 20 L a 19 °C in
    fermentazione, con l'avanzamento come parametro.
- La temperatura della stanza è un parametro della partenza (20 °C se non detto).

## Processo (valori veri)

| Cosa | Come |
|---|---|
| Temperatura | Sale con la potenza, scende con la dispersione verso la stanza |
| Dispersione | Fissa per recipiente: HLT 6, MASH 5, BOIL 6, FERM 2 W/°C (valori di partenza, da tarare) |
| Grani | Calore specifico 1,7 kJ/kg·°C; trattengono 1 L/kg; occupano 0,67 L/kg |
| Bollitura | A 100 °C la potenza che avanza fa evaporare l'acqua (2257 kJ/kg) |
| Travaso | 10 L/min; le temperature si mescolano; il mosto esce dallo scambiatore a 20 °C |
| Troppo pieno | Ciò che supera la capacità trabocca ed è perso |
| Fermentazione | Da 1.050 a 1.010 in circa 5 giorni a 19 °C, curva a S, più veloce al caldo. Parte all'inoculo |
| Calore del lievito | Circa 50 kJ per litro in tutto, con un picco di circa 0,25 W/L |
| Agitatore | Non cambia la fisica: il suo effetto passa dall'interlock 2 |

## Guasti iniettabili

**Di misura** (lo strumento mente; il controllore agisce sulla misura, quindi il processo ne risente)

| Guasto | Su | Cosa vede il controllore |
|---|---|---|
| PT100 filo rotto | TT | Corrente ad almeno 21,5 mA, `signal_fault`. Se è la sonda di regolazione: `control_probe_fault` |
| PT100 starata (offset fisso) | TT | Niente di anomalo. Il recipiente va alla temperatura sbagliata; nel fermentatore le due sonde non concordano |
| Cavo del segnale interrotto | TT, LT | 0 mA, `signal_fault` con "segnale assente" |
| Livello bloccato su un valore | LT | Valore fermo con qualità buona. Gli interlock sono ingannati |
| Livello disturbato dalla schiuma | LT | Salti ogni tanto verso un valore più alto (manuale SICK, 11.4) |
| iSpindel batteria scarica | DT1 | Tensione che cala, poi silenzio: `hydrometer_silent` |
| iSpindel WiFi perso | DT1 | Silenzio di colpo, con batteria buona |

**Di processo** (la misura è giusta, l'impianto no)

| Guasto | Su | Cosa vede il controllore |
|---|---|---|
| Pompa bloccata o disinnescata | P1, P2 | Pompa comandata, livelli fermi: `transfer_no_progress` |
| Valvola bloccata | EV | Contatto non raggiunto: `valve_not_reached` |
| Relè statico in corto | R | Resistenza comandata a 0 % e temperatura che sale. HLT e tino: scatta K1. Bollitore: bolle senza comando e il livello cala. Fermentatore: il glicole compensa, EV9 resta aperta molto più del solito |
| Resistenza interrotta | R | Comandata al 100 %, temperatura ferma; con il programma, `step_late` |
| Glicole guasto | Chiller | EV9 aperta e contatto regolare, temperatura che sale |
| Inverter in guasto | M1 | `drive_fault` con il codice (F1 sovracorrente, F11 motore surriscaldato...: V20, pagina 55). Agitatore fermo, R2 bloccata |
| Fermentazione bloccata | FERM | Densità ferma sopra 1.010 |

Una pompa bloccata, una pompa disinnescata e una sorgente che non scarica danno lo stesso
allarme: l'agente deve proporre verifiche, non tirare a indovinare.

## Controlli di plausibilità (test)

1. HLT, 35 L da 20 a 72 °C con 3 kW: circa 42 minuti senza perdite, poco di più con le perdite.
2. Impasto: 13,5 L a 72 °C su 4,5 kg di grani a 20 °C danno circa 66 °C.
3. Bollitura: TT3 si ferma a 100 °C e in 60 minuti evaporano tra 3 e 4 L.
4. Fermentazione a 19 °C da 1.050 a 1.010 in circa 5 giorni, con curva a S.
5. Travaso: il volume totale si conserva, tolti evaporazione e traboccamenti.
6. Una cotta intera con il programma finisce con 20 L nel fermentatore, entro la
   tolleranza dei livelli.
7. Ogni interlock ha almeno un test che lo fa scattare; lo stesso per K1.
8. Due sonde sane nel fermentatore restano entro la somma delle loro tolleranze.
9. Stesso seed, stessa partenza e stesse azioni → stesso stato.
10. Un guasto su uno strumento non cambia il rumore degli altri.
11. Ogni guasto mostra al controllore ciò che dice la sua riga nelle tabelle qui sopra.

## Semplificazioni volute

- Niente chimica, pH, CO₂, pressioni, idraulica. Amaro, colore e grado alcolico li calcolano
  i tool di ricetta, non il simulatore.
- La densità iniziale è configurata, non calcolata dalla cotta.
- Il mosto esce dallo scambiatore a 20 °C: lo scambiatore non ha sonda (TT4) né guasti.
- Un percorso alla volta: il lavaggio dei grani è in due riprese.
- La HLT parte già carica: il riempimento da rete (EV1) non è simulato.
- Le sonde non vanno in deriva: l'unico errore di taratura è un offset fisso.
- Le valvole si muovono in un passo: il tempo di corsa (3–5 s) non è simulato.
- Regolazione acceso / spento, non PID.
- Le azioni a mano: i grani sono già nel tino, il luppolo non esiste, e la conferma del
  birraio al passo "Lievito" vale come inoculo.
- Una sola ricetta.
- Il controllore non si guasta. Se il servizio non risponde, l'app vede "impianto non
  raggiungibile".
- Dell'iSpindel non si simula l'angolo.

## Da verificare

- **Valvole**: il manuale oggi in `data/manuals/` è del modello a 3 fili, che ha solo un
  indicatore visivo. Per i contatti di fine corsa serve il manuale della versione a 5 fili.
- **iSpindel**: tensione di spegnimento e velocità di scarica della batteria non sono nel
  suo README.
- **Pompa e chiller**: "nessun ritorno" viene dalla conoscenza dei prodotti, non dai manuali.
- **Dispersioni dei recipienti**: valori di partenza, da tarare con i controlli di plausibilità.
