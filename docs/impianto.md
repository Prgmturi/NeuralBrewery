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
| Acqua di lavaggio dei grani | 18 L |
| Nel bollitore prima della bollitura | 27 L |
| Evaporata in 60 minuti | circa 3,4 L |
| Nel fermentatore | 20 L |
| Resta sul fondo del bollitore | circa 3,6 L |
| Acqua usata, su 35 L nella HLT | 31,5 L |

Il lavaggio dei grani si fa in due riprese (prima si svuota il tino, poi lo si riempie di
nuovo): è un metodo vero, e richiede un solo percorso alla volta.

Il fondo del bollitore è di 3,6 L per restare lontani dal minimo di 2 L sotto cui un travaso
si ferma. Con 17 L di lavaggio ne restavano 2,4–2,9: provando la cotta su 50 seed, in un caso
l'ultimo travaso finiva in allarme. Con 18 L arrivano in fondo 200 seed su 200.

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
- **iSpindel**: quattro letture per messaggio (`DT1` la densità, poi `DT1.temperature`,
  `DT1.battery`, `DT1.rssi`). Nessun messaggio da più di 30 minuti → qualità `STALE`, con
  l'ultimo valore ricevuto. Nel giorno di cotta è spento, perché non è ancora nel
  fermentatore: le sue letture sono vuote, senza allarme.
- Una lettura guasta (`BAD`) non ha valore: restano la corrente e il motivo. Un numero
  ricavato da una corrente di guasto (21,5 mA sarebbero 164 °C) ingannerebbe chi legge.
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
  TT5b e lo segnala. Resta così fino al riarmo, anche se la sonda torna valida.

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
| `reset()` | Riarmo: richiude K1, conferma il guasto dell'inverter, sblocca ciò che il controllore aveva fermato |

- Ogni comando approvato ha una fine certa: per questo il travaso è a quantità.
- **Un comando è rifiutato se un interlock lo fermerebbe subito**: scaldare un recipiente
  vuoto, o il tino con il mosto fermo. Il motivo è nella risposta.
- I comandi che fermano (`stop_route`, `stop_all`, un setpoint tolto, agitatore spento,
  `pause_program`, `abort_program`) sono sempre accettati. Con il programma in corso, un
  comando manuale che ferma lo mette in pausa.
- `reset` è sempre accettato: il controllore manda l'impulso e poi guarda. Se K1 resta
  aperto lo dice l'allarme; il controllore non sa quale termostato lo tiene aperto.

| Codice del rifiuto | Quando |
|---|---|
| `route_busy` | C'è già un travaso in corso |
| `invalid_quantity` | Travaso senza litri o con zero litri; ricircolo con i litri |
| `source_low` | Sorgente sotto 2 L |
| `no_room` | La quantità non entra nella destinazione |
| `level_unknown` | Il livello che serve non è valido |
| `level_low` | Livello sotto il minimo della resistenza o dell'agitatore |
| `setpoint_out_of_range` | Setpoint fuori dai limiti del recipiente |
| `wort_not_moving` | Tino: né agitatore in marcia né ricircolo |
| `probe_fault` | Nessuna sonda valida con cui regolare |
| `drive_fault` | Inverter in guasto: serve prima `reset` |
| `program_running` | Comando manuale che avvia qualcosa sul lato caldo, con il programma in corso |
| `program_state` | Il programma non è nello stato che il comando chiede: avvio con un programma già aperto, ripresa senza pausa, conferma senza un passo in attesa |
| `alarm_active` | Avvio o ripresa del programma con un blocco attivo, K1 aperto o inverter in guasto: serve prima `reset` |

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

- I litri si contano sul livello, che è preciso a mezzo litro. Se il livello si ferma
  quando mancano meno di 0,5 L, il travaso è **finito**, senza allarme: i due scarichi del
  tino chiedono tutto il liquido che il tino può dare.
- La pompa si ferma un passo dopo la misura: un travaso può dare fino a 0,2 L in più.

### Interlock (sulle misure del controllore)

1. Resistenza accesa solo se il livello misurato copre l'elemento (HLT 8 L, MASH 6 L,
   BOIL 6 L, FERM 4 L).
2. R2 accesa solo se il mosto si muove: agitatore comandato e inverter senza guasto, oppure
   ricircolo attivo. Vale il comando, non il ritorno di marcia, che arriva un ciclo dopo:
   così "accendi l'agitatore" e subito dopo "scalda il tino" funzionano.
3. Agitatore acceso solo se il livello misurato copre le pale (MASH 8 L).
4. Travaso solo se la sorgente ha almeno 2 L e la quantità chiesta entra nella destinazione.
   Durante il travaso: si ferma se la sorgente scende sotto 2 L o la destinazione è piena.
5. Un solo percorso attivo alla volta.
6. Travaso senza avanzamento: livello della sorgente fermo per 60 s (meno di 0,5 L) quando
   mancano ancora almeno 0,5 L → pompa ferma e allarme. Con il rumore del livello
   l'allarme arriva da uno a due minuti dopo che il liquido si è fermato.
7. Valvola i cui contatti non concordano con il comando da 10 s → allarme; se è di un
   travaso che sta partendo, il travaso è annullato. Vale per tutte le valvole, anche EV9,
   e anche in chiusura.
8. Setpoint entro i limiti del recipiente (tabella della sicurezza cablata; FERM da 0 a 30 °C).
9. Livello non valido: vale come "livello sconosciuto", quindi resistenza spenta e travaso rifiutato.
10. Ogni intervento automatico produce un evento, con tempo simulato, codice e motivo.

**Il controllore non riparte da solo.** Quando un interlock ferma qualcosa (una resistenza,
l'agitatore, la regolazione, un travaso), resta fermo con il suo allarme anche se la causa
sparisce. Lo sblocca solo il birraio, o l'esecutore con un'azione approvata:

- con `reset`: riparte ciò che non ha più la sua causa, il resto resta bloccato;
- con un nuovo comando sulla stessa cosa (un setpoint, l'agitatore, un altro travaso).

La richiesta del birraio resta: un setpoint bloccato si vede ancora nella regolazione.

### Programma della cotta

Una sola ricetta, quella dei conti qui sopra. Il programma è il controllore che fa il
birraio: a ogni passo preme gli stessi pulsanti. Gli rispondono gli stessi interlock, e
ogni suo comando è un evento.

| # | Passo | Cosa fa il controllore | Finisce quando | Tempo massimo |
|---|---|---|---|---|
| 1 | Scalda l'acqua | HLT a 72 °C | TT1 arriva a 72 °C | 60 min |
| 2 | Impasto | `hlt_to_mash` 13,5 L | Travaso finito | 5 min |
| 3 | Porta il tino a 66 °C | Agitatore acceso; HLT a 78 °C; MASH a 66 °C | TT2 arriva a 66 °C | 15 min |
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
| 15 | Lievito | FERM a 19 °C; aspetta il birraio | `confirm_step` | — |

- **Stati**: fermo, in corso, in attesa di conferma, in pausa, finito, annullato.
- **L'agitatore parte al passo 3**: durante l'impasto il livello del tino è sotto le pale.
- **Passo 15**: il fermentatore è tenuto a 19 °C mentre aspetta il lievito. La conferma
  del birraio è l'inoculo, e chiude il programma.
- **Un passo descrive tutto il lato caldo**: setpoint di HLT, MASH e BOIL, agitatore,
  percorso con i litri. La tabella mostra solo ciò che cambia; la ricetta nel codice ha lo
  stato intero. Quando il passo comincia, e a ogni ripresa, il programma porta l'impianto
  a quello stato:
  - dà solo i comandi che mancano: uno già a posto non viene ridato, quindi il programma
    non riarma mai ciò che un interlock ha fermato;
  - li dà in quest'ordine: setpoint da togliere, percorso, agitatore, setpoint da
    mettere. Così nessun interlock scatta per l'ordine dei comandi.
- **Passo in ritardo**: oltre il tempo massimo il controllore dà l'avviso `step_late`. Il
  passo continua: non viene saltato né fermato. L'avviso finisce con il passo.
- **Pausa automatica**, con l'allarme `program_paused` e il motivo. Scatta con un blocco
  attivo (un allarme di tipo blocco), con K1 aperto, con l'inverter in guasto, o quando
  l'impianto rifiuta un comando del programma.
- **In pausa** i setpoint restano e il tempo del passo si ferma. Un travaso a quantità si
  ferma, e i litri già fatti restano contati. Il ricircolo resta acceso: è ciò che
  permette al tino di tenere la temperatura.
- **Ripresa**: `resume_program` è rifiutato finché c'è un blocco attivo, K1 è aperto o
  l'inverter è in guasto. Prima `reset`, poi la ripresa; i due comandi dati uno dopo
  l'altro funzionano. Se la causa c'è ancora il programma torna in pausa. Un travaso
  riparte dai litri che mancano.
- **Comandi manuali con il programma in corso**:
  - quelli che avviano qualcosa sul lato caldo sono rifiutati (`program_running`);
  - quelli che fermano (`stop_route`, un setpoint tolto, agitatore spento, `stop_all`)
    sono eseguiti e mettono il programma in pausa, senza allarme;
  - il fermentatore si comanda sempre;
  - in pausa i comandi manuali sono ammessi. Alla ripresa il programma rimette lo stato
    del passo, anche dopo uno `stop_all`.
- **Avvio**: `start_program` è rifiutato con un programma già aperto, e negli stessi casi
  della ripresa. I comandi del primo passo arrivano con il ciclo successivo: se l'impianto
  ne rifiuta uno (per esempio la HLT è vuota) il programma va in pausa e dice perché.
- Una cotta intera dura circa 3 ore e 40 minuti simulati.

### Allarmi ed eventi

Il controllore riporta **fatti**. Gli allarmi sono di due tipi:

- **avviso**: non ferma niente, e finisce da solo quando finisce la causa;
- **blocco**: il controllore ha fermato qualcosa. Resta attivo fino al riarmo (vedi sopra,
  "Il controllore non riparte da solo").

| Codice | Tipo | Quando | Su cosa |
|---|---|---|---|
| `signal_fault` | avviso | Segnale 4–20 mA guasto o assente | TT, LT |
| `hydrometer_silent` | avviso | Nessun messaggio dall'iSpindel da più di 30 min | DT1 |
| `drive_fault` | avviso | L'inverter segnala un guasto, con il suo codice. È l'inverter a restare in guasto fino a `reset` | M1 |
| `safety_open` | avviso | K1 aperto. È K1 a restare aperto fino a `reset` | K1 |
| `control_probe_fault` | blocco | Regolazione sospesa, o passata alla sonda di riserva | Recipiente |
| `heater_blocked` | blocco | Resistenza bloccata: livello basso o sconosciuto, mosto fermo | R |
| `agitator_blocked` | blocco | Agitatore bloccato: livello basso o sconosciuto | M1 |
| `valve_not_reached` | blocco | Contatti della valvola diversi dal comando da 10 s | EV |
| `transfer_no_progress` | blocco | Livello fermo per 60 s durante un travaso | Percorso |
| `transfer_stopped` | blocco | Travaso fermato: sorgente bassa, destinazione piena, livello non valido | Percorso |
| `step_late` | avviso | Passo del programma oltre il tempo massimo. Finisce con il passo | `PROGRAM` |
| `program_paused` | blocco | Il controllore ha messo in pausa il programma: il testo dice perché. Resta fino a `resume_program` o `abort_program` | `PROGRAM` |

Sono eventi: ogni allarme che nasce o finisce, ogni comando accettato (anche quelli che dà
il programma), ogni travaso completato, ogni passo che comincia, la fine del programma.
Ogni evento ha un numero progressivo: due eventi dello stesso istante restano in ordine.

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
| Letture | Per sigla: valore (vuoto se la lettura è guasta), unità, qualità e motivo, corrente in mA (se 4–20 mA), tempo dell'ultima misura. Per l'iSpindel quattro letture: densità, temperatura, batteria, segnale |
| Dispositivi | Per sigla: comando e, dove esiste, ritorno. Per M1 anche frequenza, corrente e codice di guasto |
| Regolazione | Per recipiente: setpoint, sonda in uso |
| Travaso | Percorso attivo, litri chiesti, litri fatti |
| Programma | Stato, numero e nome del passo, tempo trascorso nel passo (pause escluse) e tempo massimo, motivo della pausa |
| Allarmi | Quelli attivi: codice, sigla, testo, da quando |

**Storico breve**: letture e comandi di resistenze, pompe ed EV9, con finestra e passo
configurabili (24 ore e 60 s). Basta per la diagnosi e per gli eval, senza database.

- Una lettura è salvata com'era in quell'istante.
- Un comando è salvato come **media dall'ultimo campione**, in percento: una resistenza
  accesa 24 secondi su 60 vale 40. Il valore dell'istante perderebbe quasi tutto: a
  temperatura raggiunta la resistenza della HLT sta accesa mezzo minuto ogni cinque.

### Simulazione (porta `SimulationControl`)

Non fa parte del controllore: è la mano di chi prova. Solo test, eval e demo.

- **Tempo**: `advance(secondi)`. Il passo di calcolo è fisso, scelto alla creazione del
  simulatore (1 s; 10 s per le fermentazioni lunghe), e il tempo si conta in passi interi.
  Un tempo che non è un numero intero di passi è un errore, non viene arrotondato.
- **Ordine di un passo**: i dispositivi eseguono le uscite e la sicurezza cablata guarda
  le temperature vere; il processo avanza; i dispositivi misurano; il controllore legge
  e decide. Un comando ha quindi effetto sull'impianto dal passo successivo.
- **Guasti**: `inject_fault`, `clear_faults`. Un guasto su una sigla che non lo ammette è
  un errore, non viene ignorato.
- **Partenze con nome**:
  - *giorno di cotta*: HLT con 35 L, tino con 4,5 kg di grani asciutti, bollitore e
    fermentatore vuoti, iSpindel spento;
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
| Recipiente vuoto | Ha la capacità termica del suo acciaio (1 kJ/°C): una resistenza a secco lo scalda di gradi al secondo |
| Più vie aperte | La pompa divide la portata tra i percorsi che hanno tutte le valvole aperte. Succede solo con una valvola bloccata aperta |
| Fermentazione | Da 1.050 a 1.010 in circa 5 giorni a 19 °C, curva a S, più veloce al caldo. Parte all'inoculo |
| Calore del lievito | Circa 50 kJ per litro in tutto, con un picco di circa 0,25 W/L |
| Agitatore | Non cambia la fisica: il suo effetto passa dall'interlock 2 |

## Guasti iniettabili

**Di misura** (lo strumento mente; il controllore agisce sulla misura, quindi il processo ne risente)

| Guasto | Codice | Su | Cosa vede il controllore |
|---|---|---|---|
| PT100 filo rotto | `probe_broken` | TT | Corrente ad almeno 21,5 mA, `signal_fault`. Se è la sonda di regolazione: `control_probe_fault` |
| PT100 starata (offset fisso) | `probe_offset`, con i gradi | TT | Niente di anomalo. Il recipiente va alla temperatura sbagliata; nel fermentatore le due sonde non concordano |
| Cavo del segnale interrotto | `signal_cable_broken` | TT, LT | 0 mA, `signal_fault` con "segnale assente" |
| Livello bloccato su un valore | `level_stuck`, con il valore o senza (resta dov'è) | LT | Valore fermo con qualità buona. Gli interlock sono ingannati |
| Livello disturbato dalla schiuma | `level_foam` | LT | Salti ogni tanto verso un valore più alto (manuale SICK, 11.4): una misura su venti, da 1 a 5 L |
| iSpindel batteria scarica | `hydrometer_battery_low` | DT1 | Tensione che cala (0,1 V l'ora), poi silenzio sotto 3,3 V: `hydrometer_silent` |
| iSpindel WiFi perso | `hydrometer_wifi_lost` | DT1 | Silenzio di colpo, con batteria buona |

**Di processo** (la misura è giusta, l'impianto no)

| Guasto | Codice | Su | Cosa vede il controllore |
|---|---|---|---|
| Pompa bloccata o disinnescata | `pump_blocked` | P1, P2 | Pompa comandata, livelli fermi: `transfer_no_progress` |
| Valvola bloccata (ferma dove si trova) | `valve_stuck` | EV | Contatto non raggiunto: `valve_not_reached`. Se è rimasta aperta, il travaso dopo va a metà portata |
| Relè statico in corto | `ssr_shorted` | R | Resistenza comandata a 0 % e temperatura che sale. HLT e tino: scatta K1. Bollitore: bolle senza comando e il livello cala. Fermentatore: il glicole compensa, EV9 resta aperta molto più del solito |
| Resistenza interrotta | `heater_open` | R | Comandata al 100 %, temperatura ferma; con il programma, `step_late` |
| Glicole guasto | `glycol_failed` | `CHILLER` | EV9 aperta e contatto regolare, temperatura che sale |
| Inverter in guasto | `drive_fault`, con il codice | M1 | `drive_fault` con il codice (F1 sovracorrente, F11 motore surriscaldato...: V20, pagina 55). Agitatore fermo, R2 bloccata |
| Fermentazione bloccata | `fermentation_stuck` | FERM | Densità ferma sopra 1.010 |

Togliere i guasti (`clear_faults`) non cancella ciò che hanno già fatto: K1 resta aperto e
l'inverter resta in guasto fino a `reset`. Una batteria tolta dai guasti è una batteria nuova.

Una pompa bloccata, una pompa disinnescata e una sorgente che non scarica danno lo stesso
allarme: l'agente deve proporre verifiche, non tirare a indovinare.

## Controlli di plausibilità (test)

1. HLT, 35 L da 20 a 72 °C con 3 kW: circa 42 minuti senza perdite, poco di più con le perdite.
2. Impasto: 13,5 L a 72 °C su 4,5 kg di grani a 20 °C danno circa 65 °C (66 senza
   contare l'acciaio del tino). Il passo 3 del programma porta poi il tino a 66 °C.
3. Bollitura: TT3 si ferma a 100 °C e in 60 minuti evaporano tra 3 e 4 L.
4. Fermentazione a 19 °C da 1.050 a 1.010 in circa 5 giorni, con curva a S.
5. Travaso: il volume totale si conserva, tolti evaporazione e traboccamenti.
6. Una cotta intera con il programma finisce con 20 L nel fermentatore, entro la
   tolleranza dei livelli, in circa 3 ore e 40 minuti e senza allarmi.
7. Ogni interlock ha almeno un test che lo fa scattare; lo stesso per K1.
8. Due sonde sane nel fermentatore restano entro la somma delle loro tolleranze.
9. Stesso seed, stessa partenza e stesse azioni → stesso stato.
10. Un guasto su uno strumento non cambia il rumore degli altri.
11. Ogni guasto mostra al controllore ciò che dice la sua riga nelle tabelle qui sopra.

I test fanno girare l'impianto intero attraverso le tre porte, in
`tests/adapters/plant_sim/`. Non ci sono test strato per strato: ripeterebbero questi.

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
  birraio al passo "Lievito" vale come inoculo: il lievito entra nel mosto e l'iSpindel
  con lui. Lo fa il simulatore, non il controllore.
- Una sola ricetta.
- Il controllore non si guasta. Se il servizio non risponde, l'app vede "impianto non
  raggiungibile".
- Dell'iSpindel non si simula l'angolo.

## Da verificare

- **Valvole**: il manuale oggi in `data/manuals/` è del modello a 3 fili, che ha solo un
  indicatore visivo. Per i contatti di fine corsa serve il manuale della versione a 5 fili.
- **iSpindel**: tensione di spegnimento e velocità di scarica della batteria non sono nel
  suo README. Valori scelti da noi: 4,1 V da carica, spento sotto 3,3 V, 0,1 V l'ora con
  il guasto.
- **Schiuma sul livello**: il manuale SICK descrive l'effetto, non quanto. Valori scelti da
  noi: una misura su venti, da 1 a 5 L in più.
- **Inverter**: 50 Hz e 1,2 A in marcia sono valori fissi, non presi dal manuale.
- **Pompa e chiller**: "nessun ritorno" viene dalla conoscenza dei prodotti, non dai manuali.
- **Dispersioni dei recipienti**: valori di partenza, da tarare con i controlli di plausibilità.
