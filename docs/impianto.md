# Impianto

Impianto pilota simulato per cotte da 20 L: tre recipienti sul lato caldo e un fermentatore.
I componenti sono prodotti reali con manuali pubblici (`manuals/manifest.toml`), e il
simulatore si comporta come dicono i manuali. I codici esatti sono in `core/plant/schemas.py`.

## In breve

- Tra l'AI e l'impianto c'è un **controllore** simulato (un PLC generico). Agenti,
  sorvegliante ed esecutore vedono e comandano solo lui.
- Il controllore conosce i **segnali** dei dispositivi, non i valori veri: un sensore guasto
  lo inganna.
- La **sicurezza cablata** (termostati che aprono K1) sta fuori dal controllore e guarda i
  valori veri.
- I comandi sono **pulsanti ad alto livello**: percorsi predefiniti, setpoint, programma. Un
  travaso è a quantità e si ferma da solo.
- Gli **interlock** rifiutano o fermano ciò che è pericoloso. Ciò che fermano resta fermo
  fino al riarmo.
- Il **programma della cotta** fa tutta la cotta in 15 passi (circa 3 h 40 min simulati),
  premendo gli stessi pulsanti del birraio.
- Si possono **iniettare guasti** di misura e di processo: sono la base degli eval.

## Il principio

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

1. **L'AI parla solo con il controllore**: legge ciò che lui sa e preme i suoi pulsanti.
2. **Il controllore sa solo ciò che i dispositivi gli dicono**, e ogni dispositivo dice solo
   ciò che prevede il suo manuale: un inverter dà un codice di guasto, una pompa niente.
3. **Il controllore agisce su ciò che crede; la sicurezza cablata agisce sulla realtà.**

I valori veri li vedono solo test ed eval, per dare il voto.

**Esempio.** Un livello bloccato su "pieno" inganna il controllore, che tiene accesa la
resistenza a secco; la temperatura vera sale e K1 scatta. L'agente deve risalire la catena
partendo da ciò che il controllore mostra.

## La cotta di riferimento

Da qui vengono le taglie dei recipienti, a partire dal fermentatore, che è un prodotto vero.

| Voce | Quantità |
|---|---|
| Acqua nella HLT | 35 L, ne servono 31,5 |
| Grani | 4,5 kg, trattengono 1 L/kg |
| Acqua di impasto (3 L/kg) | 13,5 L |
| Primo mosto | 9 L |
| Lavaggio dei grani | 18 L, in una seconda ripresa: si svuota il tino, lo si riempie, lo si svuota ancora |
| Nel bollitore | 27 L |
| Evaporata in 60 min di bollitura | circa 3,4 L |
| Al fermentatore | 20 L |
| Resta nel bollitore | circa 3,6 L, lontano dal minimo di 2 L che ferma un travaso |

## Recipienti

| Recipiente | Id | Capacità | Resistenza | Setpoint massimo | Termostato scatta a |
|---|---|---|---|---|---|
| Vasca acqua calda | HLT | 40 L | R1, 3 kW | 85 °C | 90 °C |
| Tino (agitatore M1, fondo filtrante) | MASH | 30 L | R2, 2 kW | 80 °C | 85 °C |
| Bollitore | BOIL | 40 L | R3, 3,5 kW | 100 °C | 105 °C |
| Fermentatore Blichmann G4 da 7 galloni | FERM | 26,5 L | R4, fascia 100 W | 30 °C | 35 °C |

Il fermentatore si raffredda con una serpentina a glicole (EV9, ~300 W). Tra bollitore e
fermentatore c'è uno scambiatore a piastre passivo, senza sonda: il mosto ne esce a 20 °C.

## Dispositivi

### Misure

| Sigla | Dove | Prodotto | Segnale |
|---|---|---|---|
| TT1, TT2, TT3 | HLT, MASH, BOIL | PT100 E+H iTHERM TM411 + trasmettitore iTEMP TMT80 | 4–20 mA su 0–150 °C |
| TT5a, TT5b | FERM | come sopra. TT5a regola, TT5b è di confronto e di riserva | come sopra |
| LT1–LT4 | HLT, MASH, BOIL, FERM | SICK LFP Cubic | 4–20 mA sul campo del recipiente |
| DT1 | FERM | iSpindel | Un messaggio WiFi ogni 15 min |

Per un segnale 4–20 mA il controllore conosce valore, corrente e stato, che ricava dalla
corrente (NAMUR NE43; TMT80, pagina 2). Sa *che* lo strumento è guasto, non *perché*.

| Corrente | Significato | Qualità |
|---|---|---|
| da 3,8 a 20,5 mA | Misura valida | `GOOD` |
| fino a 3,6 mA, o da 21 mA in su | Lo strumento segnala un suo guasto | `BAD`, "strumento guasto" |
| circa 0 mA | Cavo interrotto o strumento senza alimentazione | `BAD`, "segnale assente" |

- **Errore**: ogni strumento ha un errore fisso entro tolleranza, estratto dal seed, più un
  rumore piccolo. PT100 classe A: ±(0,15 + 0,002·|t|) °C (IEC 60751; TM411, pagina 16).
  Livello SICK: ±5 mm (scheda tecnica, pagina 2), circa ±0,5 L.
- **TMT80**: con la sonda rotta o in corto va ad almeno 21,5 mA, e non dice altro.
- **SICK**: in errore porta l'uscita in stato sicuro; il messaggio preciso (`!InvEc`,
  `!Cable`...) è solo sul suo display, per il birraio (niente IO-Link). Nel tino misura il
  liquido più il volume dei grani.
- **iSpindel**: quattro letture per messaggio: `DT1` (densità), `DT1.temperature`,
  `DT1.battery`, `DT1.rssi`, più l'età del messaggio. Muto da più di 30 min → `STALE` con
  l'ultimo valore. Nel giorno di cotta è spento: letture vuote, nessun allarme.
- **Una lettura `BAD` non ha valore**, solo corrente e motivo: 21,5 mA convertiti sarebbero
  164 °C e ingannerebbero chi legge. Ogni lettura porta il tempo simulato della misura.

### Attuatori

| Sigla | Cosa | Prodotto | Comando | Ritorno al controllore |
|---|---|---|---|---|
| P1, P2 | Pompa acqua calda (dalla HLT); pompa mosto (comune) | Blichmann RipTide | Accesa / spenta | Nessuno |
| EV2a, EV2b | Mandata P1 → tino / → bollitore | U.S. Solid, valvola a sfera motorizzata inox, 5 fili | Apri / chiudi | Fine corsa aperta e chiusa |
| EV3, EV4 | Aspirazione P2 ← tino / ← bollitore | come sopra | come sopra | come sopra |
| EV5, EV6, EV7 | Mandata P2 → ricircolo tino / → bollitore / → scambiatore e fermentatore | come sopra | come sopra | come sopra |
| EV9 | Glicole al fermentatore | come sopra | come sopra | come sopra |
| R1–R4 | Resistenze, con relè statici | Crydom D2425 | Potenza 0–100 % | Nessuno |
| K1 | Contattore di sicurezza a monte di tutte le resistenze | generico | Nessuno: lo aprono i termostati | Chiuso / aperto |
| M1 | Agitatore del tino | motoriduttore + inverter Siemens SINAMICS V20 | Marcia / arresto, via Modbus | In marcia, frequenza, corrente, codice di guasto |
| — | Chiller del glicole | Blichmann Glycol Chiller | Nessuno: è una macchina a sé | Nessuno |

- Lo stato riporta il **comando** e, dove esiste, il **ritorno**: un guasto si vede quando
  non concordano. Dove non c'è ritorno (pompe, resistenze, chiller) si vede solo dagli effetti.
- Un guasto dell'inverter resta finché non arriva `reset`.

## Sicurezza cablata

Un termostato per recipiente riscaldato, in serie, fuori dal controllore (soglie nella tabella
dei recipienti). Se la temperatura **vera** supera la soglia, K1 si apre e toglie corrente a
tutte le resistenze.

- Il controllore vede solo "K1 aperto", non quale termostato è scattato.
- K1 si richiude solo con `reset`, e solo se tutti i termostati sono sotto la soglia.
- Nel bollitore l'acqua non supera i 100 °C: il termostato scatta solo con la resistenza a secco.

## Controllore

### Regolazione

- Una sonda per recipiente (TT1, TT2, TT3, TT5a), acceso / spento con una banda di 0,5 °C.
  Nel fermentatore R4 scalda sotto il setpoint ed EV9 raffredda sopra.
- **Bollitura**: con setpoint a 100 °C, da 99,5 °C R3 passa alla potenza di bollitura (75 %).
- **Sonda di regolazione non valida**: uscita a zero e allarme. Il fermentatore passa a TT5b e
  lo segnala. Resta così fino al riarmo, anche se la sonda torna valida.

### Comandi (porta `PlantCommander`)

I pulsanti del pannello, gli stessi per birraio, esecutore e programma.

| Comando | Cosa fa |
|---|---|
| `activate_route(percorso, litri)` | Travasa quella quantità e si ferma da solo. Il ricircolo non ha litri: gira finché non viene fermato |
| `stop_route()` | Ferma il travaso in corso |
| `set_temperature(recipiente, °C o spento)` | Imposta o toglie il setpoint |
| `set_agitator(acceso/spento)` | Avvia o ferma M1 |
| `start_program()`, `confirm_step()` | Avvia la cotta automatica; conferma del birraio a un passo manuale |
| `pause_program()`, `resume_program()`, `abort_program()` | Pausa, ripresa; chiusura del programma con il lato caldo spento |
| `stop_all()` | Ferma il lato caldo (travaso, R1–R3, agitatore) e mette in pausa il programma. **Non tocca il fermentatore** |
| `reset()` | Riarmo: richiude K1, conferma il guasto dell'inverter, sblocca ciò che il controllore aveva fermato |

- Ogni comando risponde **accettato o rifiutato**, con un codice e un motivo. Un rifiuto non
  è un errore. È rifiutato ciò che un interlock fermerebbe subito: i codici sono accanto agli
  interlock, più `invalid_quantity` (travaso senza litri o con zero litri, ricircolo con i
  litri), `probe_fault` (nessuna sonda valida per regolare) e `drive_fault` (inverter in
  guasto: prima `reset`). I codici del programma sono nella sua sezione.
- **Fermare è sempre accettato**: `stop_route`, `stop_all`, setpoint tolto, agitatore spento,
  `pause_program`, `abort_program`. Anche `reset`: il controllore manda l'impulso e poi
  guarda; se K1 resta aperto lo dice l'allarme.

### Percorsi

Gli unici ammessi. Le valvole le apre e chiude il controllore.

| Percorso | Pompa | Valvole |
|---|---|---|
| `hlt_to_mash` | P1 | EV2a |
| `hlt_to_boil` | P1 | EV2b |
| `mash_recirc` | P2 | EV3, EV5 |
| `mash_to_boil` | P2 | EV3, EV6 |
| `boil_to_ferm` | P2 | EV4, EV7 |

Un travaso apre le valvole, aspetta i fine corsa (al massimo 10 s), avvia la pompa
(10 L/min), conta i litri sul livello misurato della sorgente, si ferma alla quantità chiesta
e richiude le valvole.

- Se il livello si ferma quando mancano meno di 0,5 L (la sua precisione), il travaso è
  **finito**, senza allarme: così si può chiedere al tino tutto il liquido che ha.
- La pompa si ferma un passo dopo la misura: fino a 0,2 L in più.

### Interlock

Agiscono sulle misure del controllore, non sui valori veri. Tra parentesi il codice del
rifiuto e l'allarme quando l'interlock ferma qualcosa in corsa.

1. Resistenza accesa solo se il livello copre l'elemento: HLT 8 L, MASH 6 L, BOIL 6 L,
   FERM 4 L (`level_low`; `heater_blocked`).
2. R2 accesa solo se il mosto si muove: agitatore comandato e inverter senza guasto, oppure
   ricircolo attivo (`wort_not_moving`; `heater_blocked`). Conta il comando, non il ritorno di
   marcia che arriva un ciclo dopo: "accendi l'agitatore" e subito "scalda il tino" funziona.
3. Agitatore acceso solo se il livello copre le pale: MASH 8 L (`level_low`; `agitator_blocked`).
4. Travaso solo se la sorgente ha almeno 2 L e la quantità entra nella destinazione
   (`source_low`, `no_room`). In corsa si ferma se la sorgente scende sotto 2 L o la
   destinazione è piena (`transfer_stopped`).
5. Un solo percorso attivo alla volta (`route_busy`).
6. Travaso senza avanzamento: livello della sorgente fermo per 60 s (meno di 0,5 L) quando
   mancano almeno 0,5 L → pompa ferma (`transfer_no_progress`). Con il rumore del livello,
   l'allarme arriva 1–2 minuti dopo che il liquido si è fermato.
7. Valvola con i contatti diversi dal comando da 10 s → allarme (`valve_not_reached`); se il
   travaso stava partendo, è annullato. Vale per tutte le valvole, EV9 compresa, anche in
   chiusura.
8. Setpoint da 0 °C al setpoint massimo del recipiente, nella tabella dei recipienti
   (`setpoint_out_of_range`).
9. Livello non valido = livello sconosciuto: resistenza e agitatore fermi, travaso rifiutato o
   fermato (`level_unknown`; `heater_blocked`, `agitator_blocked`, `transfer_stopped`).
10. Ogni intervento automatico produce un evento, con tempo simulato, codice e motivo.

### Il controllore non riparte da solo

Ciò che un interlock ferma (resistenza, agitatore, regolazione, travaso) resta fermo con il
suo allarme anche se la causa sparisce. Lo sblocca il birraio, o l'esecutore con un'azione
approvata:

- con `reset`: riparte ciò che non ha più la sua causa, il resto resta bloccato;
- con un nuovo comando sulla stessa cosa: un setpoint, l'agitatore, un altro travaso.

Un setpoint bloccato resta visibile nella regolazione.

### Programma della cotta

Una sola ricetta, quella della cotta di riferimento. Il programma è un birraio fatto di
codice: preme gli stessi pulsanti, gli rispondono gli stessi interlock, ogni suo comando è un
evento.

| # | Passo | Cosa fa il controllore | Finisce quando | Tempo massimo |
|---|---|---|---|---|
| 1 | Scalda l'acqua | HLT a 72 °C | TT1 arriva a 72 °C | 60 min |
| 2 | Impasto | `hlt_to_mash` 13,5 L | Travaso finito | 5 min |
| 3 | Porta il tino a 66 °C | Agitatore acceso (non prima: all'impasto il livello è sotto le pale); HLT a 78 °C; MASH a 66 °C | TT2 arriva a 66 °C | 15 min |
| 4 | Sosta | Mantiene | Passati 60 min | — |
| 5 | Fine sosta | MASH a 76 °C | TT2 arriva a 76 °C | 15 min |
| 6 | Ricircolo | `mash_recirc`; agitatore spento | Passati 10 min | — |
| 7 | Primo mosto | MASH spento; `mash_to_boil` 9 L | Travaso finito | 5 min |
| 8 | Lavaggio | HLT spenta; `hlt_to_mash` 18 L | Travaso finito | 5 min |
| 9 | Ricircolo | `mash_recirc` | Passati 10 min | — |
| 10 | Secondo mosto | `mash_to_boil` 18 L | Travaso finito | 5 min |
| 11 | Porta a bollore | BOIL a 100 °C | TT3 arriva a 99,5 °C | 30 min |
| 12 | Bollitura | Potenza di bollitura | Passati 60 min | — |
| 13 | Pronto al travaso | BOIL spento; aspetta il birraio | `confirm_step` | — |
| 14 | Al fermentatore | `boil_to_ferm` 20 L | Travaso finito | 5 min |
| 15 | Lievito | FERM a 19 °C; aspetta il birraio. La conferma è l'inoculo e chiude il programma | `confirm_step` | — |

- **Stati**: fermo, in corso, in attesa di conferma, in pausa, finito, annullato.
- **Un passo descrive tutto il lato caldo** (setpoint di HLT, MASH e BOIL, agitatore,
  percorso con i litri); la tabella mostra solo ciò che cambia. All'inizio del passo, e a ogni
  ripresa, il programma dà solo i comandi che mancano, in quest'ordine: setpoint da togliere,
  percorso, agitatore, setpoint da mettere. Così nessun interlock scatta per l'ordine, e il
  programma non riarma mai ciò che un interlock ha fermato.

| Situazione | Cosa succede |
|---|---|
| Passo oltre il tempo massimo | Avviso `step_late`. Il passo continua; l'avviso finisce con il passo |
| Blocco attivo, K1 aperto, inverter in guasto, o un comando del programma rifiutato | Pausa automatica, con l'allarme `program_paused` e il motivo |
| Comando manuale che ferma | Eseguito; il programma va in pausa, senza allarme |
| Comando manuale che avvia qualcosa sul lato caldo | Rifiutato: `program_running`. Il fermentatore si comanda sempre |
| In pausa | Setpoint e ricircolo restano (il ricircolo tiene la temperatura del tino); il tempo del passo si ferma; un travaso a quantità si ferma, con i litri fatti contati. I comandi manuali sono ammessi |
| `resume_program` | Rifiutato con un blocco attivo, K1 aperto o inverter in guasto (`alarm_active`): prima `reset`, e i due comandi di seguito funzionano. Rimette lo stato del passo, anche dopo `stop_all`; il travaso riparte dai litri mancanti. Se la causa c'è ancora, torna in pausa |
| `start_program` | Rifiutato con un programma già aperto, e negli stessi casi della ripresa. I comandi del primo passo partono al ciclo dopo: se uno è rifiutato (es. HLT vuota) il programma va in pausa e dice perché |

Avvio con un programma aperto, ripresa senza pausa, conferma senza un passo in attesa:
rifiutati con `program_state`.

### Allarmi ed eventi

Il controllore riporta **fatti**. Un **avviso** non ferma niente e finisce da solo con la
causa. Un **blocco** accompagna qualcosa che il controllore ha fermato, e resta fino al riarmo.
Il testo di un blocco che si riarma con `reset` finisce con "(bloccato: serve reset)", come lo
mostra il pannello di un impianto vero: la causa può essere già finita (la sonda legge di
nuovo), il blocco no. `program_paused` non lo dice: riprende con `resume_program`.

| Codice | Tipo | Quando | Su cosa |
|---|---|---|---|
| `signal_fault` | avviso | Segnale 4–20 mA guasto o assente | TT, LT |
| `hydrometer_silent` | avviso | iSpindel muto da più di 30 min | DT1 |
| `drive_fault` | avviso | Guasto dell'inverter, con il suo codice; l'inverter resta in guasto fino a `reset` | M1 |
| `safety_open` | avviso | K1 aperto; resta aperto fino a `reset` | K1 |
| `control_probe_fault` | blocco | Regolazione sospesa, o passata alla sonda di riserva | Recipiente |
| `heater_blocked` | blocco | Resistenza bloccata: livello basso o sconosciuto, mosto fermo | R |
| `agitator_blocked` | blocco | Agitatore bloccato: livello basso o sconosciuto | M1 |
| `valve_not_reached` | blocco | Contatti della valvola diversi dal comando da 10 s | EV |
| `transfer_no_progress` | blocco | Livello fermo per 60 s durante un travaso | Percorso |
| `transfer_stopped` | blocco | Sorgente bassa, destinazione piena, livello non valido | Percorso |
| `step_late` | avviso | Passo oltre il tempo massimo | `PROGRAM` |
| `program_paused` | blocco | Pausa decisa dal controllore, con il motivo; resta fino a `resume_program` o `abort_program` | `PROGRAM` |

**Eventi**: ogni allarme che nasce o finisce, ogni comando accettato (anche del programma),
ogni travaso completato, ogni passo che comincia, la fine del programma. Un numero
progressivo tiene in ordine gli eventi dello stesso istante.

I **giudizi sul processo** (sonde che non concordano, temperatura lontana dal setpoint,
livelli che cambiano senza un travaso, densità ferma) non sono del controllore ma del
**sorvegliante** (`core/plant/watcher.py`): regole fisse, senza LLM, che leggono solo da
`PlantReader`. Si chiama su richiesta, dopo un avanzamento del tempo o da un tool dell'agente, e
non tiene niente tra una chiamata e l'altra. Un giudizio finisce quando l'impianto non lo mostra
più.

| Codice | Quando | Su cosa |
|---|---|---|
| `probes_disagree` | TT5a e TT5b, entrambe valide, distanti più di 1 °C da almeno 10 minuti di storico. Le due tolleranze sommate fanno circa 0,4 °C. Una sonda guasta non si confronta: c'è già `signal_fault` | FERM |

Le altre regole si aggiungono quando uno scenario le chiede.

### Lettura (porta `PlantReader`)

| Chiamata | Cosa restituisce |
|---|---|
| `snapshot()` | La fotografia del controllore: tempo simulato, letture, dispositivi (comando e ritorno), regolazione (setpoint e sonda in uso), travaso (litri chiesti e fatti), programma (passo, tempo nel passo senza le pause, tempo massimo, motivo della pausa), allarmi attivi |
| `events(da quando)` | Gli eventi, dal più vecchio |
| `history(sigla, da quando)` | Lo storico breve di una sigla |

**Storico breve**: letture e comandi di resistenze, pompe ed EV9; 24 ore, un campione ogni
60 s (configurabili). Basta per diagnosi ed eval, senza database. Una lettura è salvata
com'era; un comando come **media dall'ultimo campione**, in percento: una resistenza accesa
24 s su 60 vale 40. Il valore dell'istante perderebbe quasi tutto: a temperatura raggiunta la
resistenza della HLT sta accesa mezzo minuto ogni cinque.

## Simulazione (porta `SimulationControl`)

Non fa parte del controllore: è la mano di chi prova. Solo test, eval e demo, mai in produzione.

- **Tempo**: `advance(secondi)`. Passo di calcolo fisso, scelto alla creazione (1 s; 10 s per
  le fermentazioni lunghe); il tempo si conta in passi interi. Un tempo che non è un numero
  intero di passi è un errore, non viene arrotondato.
- **Ordine di un passo**: i dispositivi eseguono le uscite e la sicurezza cablata guarda le
  temperature vere → il processo avanza → i dispositivi misurano → il controllore legge e
  decide. Un comando ha effetto dal passo successivo.
- **Guasti**: `inject_fault`, `clear_faults`. Un guasto su una sigla che non lo ammette è un
  errore, non viene ignorato.
- **Partenze con nome**, con la temperatura della stanza come parametro (20 °C):
  *giorno di cotta* (HLT con 35 L, tino con 4,5 kg di grani asciutti, bollitore e
  fermentatore vuoti, iSpindel spento) e *fermentazione* (lato caldo vuoto e spento,
  fermentatore con 20 L a 19 °C, avanzamento come parametro).

## Processo (valori veri)

| Cosa | Come |
|---|---|
| Temperatura | Sale con la potenza, scende con la dispersione verso la stanza |
| Dispersione | HLT 6, MASH 5, BOIL 6, FERM 2 W/°C (valori di partenza, da tarare) |
| Grani | Calore specifico 1,7 kJ/kg·°C; trattengono 1 L/kg; occupano 0,67 L/kg |
| Bollitura | A 100 °C la potenza che avanza fa evaporare l'acqua (2257 kJ/kg) |
| Travaso | 10 L/min; le temperature si mescolano; dallo scambiatore il mosto esce a 20 °C |
| Troppo pieno | Ciò che supera la capacità trabocca ed è perso |
| Recipiente vuoto | Capacità termica del suo acciaio (1 kJ/°C): una resistenza a secco lo scalda di gradi al secondo |
| Più vie aperte | La pompa divide la portata tra i percorsi con tutte le valvole aperte (solo con una valvola bloccata aperta) |
| Fermentazione | Da 1.050 a 1.010 in circa 5 giorni a 19 °C, curva a S, più veloce al caldo. Parte all'inoculo |
| Calore del lievito | Circa 50 kJ per litro in tutto, con un picco di circa 0,25 W/L |
| Agitatore | Non cambia la fisica: il suo effetto passa dall'interlock 2 |

## Guasti iniettabili

**Di misura**: lo strumento mente; il controllore agisce sulla misura, quindi il processo ne
risente.

| Guasto | Codice | Su | Cosa vede il controllore |
|---|---|---|---|
| PT100 filo rotto | `probe_broken` | TT | Almeno 21,5 mA, `signal_fault`. Sulla sonda di regolazione anche `control_probe_fault` |
| PT100 starata | `probe_offset`, con i gradi | TT | Niente di anomalo. Il recipiente va alla temperatura sbagliata; nel fermentatore le due sonde non concordano |
| Cavo del segnale interrotto | `signal_cable_broken` | TT, LT | 0 mA, `signal_fault` con "segnale assente" |
| Livello bloccato | `level_stuck`, con il valore o senza (resta dov'è) | LT | Valore fermo con qualità buona. Gli interlock sono ingannati |
| Schiuma sul livello | `level_foam` | LT | Una misura su venti salta in alto di 1–5 L (manuale SICK, 11.4) |
| iSpindel batteria scarica | `hydrometer_battery_low` | DT1 | Tensione che cala (0,1 V l'ora), poi silenzio sotto 3,3 V: `hydrometer_silent` |
| iSpindel WiFi perso | `hydrometer_wifi_lost` | DT1 | Silenzio di colpo, con batteria buona |

**Di processo**: la misura è giusta, l'impianto no.

| Guasto | Codice | Su | Cosa vede il controllore |
|---|---|---|---|
| Pompa bloccata o disinnescata | `pump_blocked` | P1, P2 | Pompa comandata, livelli fermi: `transfer_no_progress` |
| Valvola bloccata dov'è | `valve_stuck` | EV | `valve_not_reached`. Se è rimasta aperta, il travaso dopo va a metà portata |
| Relè statico in corto | `ssr_shorted` | R | Comandata a 0 %, temperatura che sale. HLT e tino: scatta K1. Bollitore: bolle senza comando e il livello cala. Fermentatore: il glicole compensa, EV9 aperta molto più del solito |
| Resistenza interrotta | `heater_open` | R | Comandata al 100 %, temperatura ferma; con il programma, `step_late` |
| Glicole guasto | `glycol_failed` | `CHILLER` | EV9 aperta con contatto regolare, temperatura che sale |
| Inverter in guasto | `drive_fault`, con il codice | M1 | `drive_fault` con il codice (F1 sovracorrente, F11 motore surriscaldato...: V20, pagina 55). Agitatore fermo, R2 bloccata |
| Fermentazione bloccata | `fermentation_stuck` | FERM | Densità ferma sopra 1.010 |

- `clear_faults` non cancella gli effetti: K1 resta aperto e l'inverter in guasto fino a
  `reset`. Una batteria tolta dai guasti è una batteria nuova.
- Pompa bloccata, pompa disinnescata e sorgente che non scarica danno lo stesso allarme:
  l'agente deve proporre verifiche, non tirare a indovinare.

## Controlli di plausibilità

1. HLT, 35 L da 20 a 72 °C con 3 kW: circa 42 minuti senza perdite, poco di più con le perdite.
2. Impasto: 13,5 L a 72 °C su 4,5 kg di grani a 20 °C danno circa 65 °C (66 senza l'acciaio
   del tino). Il passo 3 del programma porta poi il tino a 66 °C.
3. Bollitura: TT3 si ferma a 100 °C e in 60 minuti evaporano tra 3 e 4 L.
4. Fermentazione a 19 °C da 1.050 a 1.010 in circa 5 giorni, con curva a S.
5. Travaso: il volume totale si conserva, tolti evaporazione e traboccamenti.
6. Una cotta intera con il programma finisce con 20 L nel fermentatore, entro la tolleranza
   dei livelli, in circa 3 ore e 40 minuti e senza allarmi.
7. Ogni interlock ha almeno un test che lo fa scattare; lo stesso per K1.
8. Due sonde sane nel fermentatore restano entro la somma delle loro tolleranze.
9. Stesso seed, stessa partenza e stesse azioni → stesso stato.
10. Un guasto su uno strumento non cambia il rumore degli altri.
11. Ogni guasto mostra al controllore ciò che dice la sua riga in "Guasti iniettabili".

I test fanno girare l'impianto intero attraverso le tre porte (`tests/adapters/plant_sim/`):
niente test strato per strato.

## Semplificazioni volute

- Niente chimica, pH, CO₂, pressioni, idraulica: amaro, colore e grado alcolico sono dei tool
  di ricetta. La densità iniziale è configurata.
- Una sola ricetta, un percorso alla volta, regolazione acceso / spento (non PID).
- Scambiatore senza sonda (TT4) e senza guasti. HLT già carica: il riempimento (EV1) non c'è.
- Sonde senza deriva (solo un offset fisso); valvole che si muovono in un passo (la corsa di
  3–5 s non c'è); dell'iSpindel non si simula l'angolo.
- Azioni a mano: i grani sono già nel tino, il luppolo non esiste, e la conferma del passo
  "Lievito" vale come inoculo (lievito e iSpindel entrano nel mosto: lo fa il simulatore).
- Il controllore non si guasta. Se il servizio non risponde, l'app vede "impianto non
  raggiungibile".

## Da verificare

- **Valvole**: il documento in `data/manuals/` traduce la pagina del modello a 3 fili; l'impianto
  usa la variante a 5 fili con i fine corsa, di cui non c'è un manuale pubblico.
- **Valori scelti da noi**, non dai manuali: batteria dell'iSpindel (4,1 V da carica, spento
  sotto 3,3 V, 0,1 V l'ora con il guasto); schiuma sul livello (una misura su venti, da 1 a
  5 L); inverter in marcia (50 Hz, 1,2 A); "nessun ritorno" di pompa e chiller.
- **Dispersioni dei recipienti**: valori di partenza, da tarare con i controlli di plausibilità.
