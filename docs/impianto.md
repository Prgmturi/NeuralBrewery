# Impianto

Piccolo impianto pilota a recipienti separati. Componenti scelti tra prodotti reali con
documentazione pubblica: il simulatore ne imita il comportamento descritto nei manuali.
Elenco documenti e link: `manuals/manifest.toml`.

Questa è la versione ridotta: basta per la diagnosi e per gli eval. Cosa è rimasto fuori è
elencato in fondo, in "Semplificazioni volute".

## Recipienti

| Recipiente | Id | Capacità | Riscaldamento | Altro |
|---|---|---|---|---|
| Vasca acqua calda | HLT | 60 L | R1, 3 kW | Parte già piena |
| Tino | MASH | 50 L | R2, 2 kW | Agitatore M1, fondo filtrante |
| Bollitore | BOIL | 50 L | R3, 3,5 kW | |
| Fermentatore | FERM | 30 L | R4, fascia 100 W | Serpentina a glicole, EV9 (~300 W di raffreddamento) |

Scambiatore a piastre tra bollitore e fermentatore: passivo, senza sonda. Il mosto ne esce a 20 °C.

## Strumenti

| Sigla | Dove | Prodotto | Segnale |
|---|---|---|---|
| TT1, TT2, TT3 | HLT, MASH, BOIL | PT100 E+H iTHERM TM411 + trasmettitore iTEMP TMT80 | 4–20 mA su 0–150 °C |
| TT5a, TT5b | FERM (due sonde, per confronto) | come sopra | come sopra |
| LT1–LT4 | HLT, MASH, BOIL, FERM | SICK LFP Cubic | 4–20 mA sul campo del recipiente |
| DT1 | FERM | iSpindel (WiFi, ogni 15 min) | Densità, tensione batteria |

- **PT100 classe A**: tolleranza ±(0,15 + 0,002·|t|) °C (IEC 60751), cioè ±0,35 °C a 100 °C.
  Ogni sonda ha un suo errore fisso entro tolleranza (estratto dal seed) più un rumore piccolo.
- **Guasto segnalato in corrente** (NAMUR NE43): misura valida tra 3,8 e 20,5 mA; sotto 3,6 o
  sopra 21 mA il trasmettitore segnala guasto → qualità `BAD`. *Da verificare sul manuale TMT80.*
- La lettura espone sia il valore convertito sia la corrente grezza, utile per la diagnosi.

## Attuatori

| Sigla | Cosa | Prodotto |
|---|---|---|
| P1 | Pompa acqua calda (dalla HLT) | Blichmann RipTide |
| P2 | Pompa mosto (comune) | Blichmann RipTide |
| EV2a, EV2b | Mandata P1 → tino / → bollitore | U.S. Solid, valvola a sfera motorizzata inox |
| EV3, EV4 | Aspirazione P2 ← tino / ← bollitore | come sopra |
| EV5, EV6, EV7 | Mandata P2 → ricircolo tino / → bollitore / → scambiatore e fermentatore | come sopra |
| EV9 | Glicole al fermentatore | come sopra |
| R1–R4 | Resistenze, comandate da relè statici | Crydom D2425 |
| K1 | Contattore di sicurezza a monte di tutte le resistenze | generico |
| M1 | Agitatore del tino | motoriduttore + inverter Siemens SINAMICS V20 |

Le valvole non hanno un segnale di posizione: lo stato riporta la posizione comandata, e una
valvola bloccata si vede solo dai livelli.

## Percorsi

Gli unici percorsi ammessi. Il controllore apre e chiude le valvole da solo.

| Percorso | Pompa | Valvole |
|---|---|---|
| `hlt_to_mash` | P1 | EV2a |
| `hlt_to_boil` | P1 | EV2b |
| `mash_recirc` | P2 | EV3, EV5 |
| `mash_to_boil` | P2 | EV3, EV6 |
| `boil_to_ferm` | P2 | EV4, EV7 |

- **Un solo percorso attivo alla volta.** Per attivarne un altro va prima fermato quello attivo.
- Portata delle pompe: 10 L/min (semplificazione).

## Comandi (porta `PlantCommander`)

`activate_route`, `stop_route`, `set_temperature(vessel, °C)`, `set_agitator(on/off)`,
`stop_all`, `reset_safety` (richiude K1 dopo un intervento).

## Lettura (porta `PlantReader`)

- **Stato**: letture con qualità e tempo simulato, attuatori e valvole (stato comandato),
  percorso attivo, setpoint, stato di K1.
- **Eventi**: ogni intervento automatico, con tempo simulato, codice e motivo.
- **Storico breve**: il simulatore tiene le ultime letture di ogni strumento (finestra e passo
  configurabili). Basta per la diagnosi e per gli eval, senza database.

## Interlock (nel simulatore)

1. Resistenza accesa solo se il livello copre l'elemento.
2. Agitatore acceso solo se il livello copre le pale.
3. Pompa accesa solo se la sorgente ha almeno 2 L (niente pompa a secco) e la destinazione non è piena.
4. Un solo percorso attivo alla volta.
5. Setpoint entro i limiti del recipiente (HLT 85 °C, MASH 80 °C, BOIL 100 °C, FERM 30 °C).
6. Sovratemperatura (setpoint massimo + 5 °C) → K1 si apre e stacca tutte le resistenze.
   Si richiude solo con `reset_safety`.
7. Ogni intervento automatico produce un evento con tempo simulato e motivo.

## Guasti iniettabili (porta `SimulationControl`)

**Di misura** (il processo va bene, lo strumento no)
- PT100 filo rotto → corrente fuori scala (NE43) → `BAD`.
- PT100 starata (offset fisso).
- Livello bloccato su un valore.
- iSpindel batteria scarica: la tensione cala, poi smette di trasmettere → `STALE`.
- iSpindel WiFi perso: smette di trasmettere di colpo → `STALE`.

**Di processo** (la misura è giusta, l'impianto no)
- Pompa bloccata o disinnescata: percorso attivo, livelli fermi.
- Valvola bloccata chiusa: stesso sintomo della pompa. L'agente deve proporre verifiche, non tirare a indovinare.
- Relè statico in corto: resistenza sempre accesa anche se comandata spenta → interviene K1.
- Resistenza interrotta: comandata accesa, la temperatura non sale.
- Glicole guasto: il fermentatore si scalda (calore del lievito).
- Inverter in allarme: agitatore fermo con un codice preso dal manuale V20.
- Fermentazione bloccata: la densità si ferma sopra la densità finale.

## Controlli di plausibilità (test)

1. HLT, 40 L da 20 a 65 °C con 3 kW: circa 42 minuti senza perdite, poco di più con le perdite.
2. Bollitura: TT3 si ferma intorno a 100 °C.
3. Fermentazione a 19 °C da 1.050 a 1.010 in circa 5 giorni, con curva a S.
4. Trasferimento: il volume totale si conserva.
5. Ogni interlock ha almeno un test che lo fa scattare.
6. Due sonde sane nel fermentatore restano entro la somma delle loro tolleranze.
7. Stesso seed e stesse azioni → stesso stato.

## Semplificazioni volute

- Niente chimica, pH, CO₂, enzimi, idraulica. Amaro, colore e grado alcolico li calcolano i
  tool di ricetta, non il simulatore.
- La fermentazione parte da una densità iniziale configurata, non calcolata dal bollitore.
- Il mosto esce dallo scambiatore a 20 °C: lo scambiatore non ha sonda (TT4) né guasti.
- Un percorso alla volta: niente sparge con P1 e P2 insieme.
- Niente evaporazione in bollitura: il volume non cala.
- La HLT parte già piena: il riempimento da rete (EV1) non è simulato.
- Le sonde non vanno in deriva: l'unico errore di taratura è un offset fisso.
- Dell'iSpindel si simulano densità e batteria, non angolo e temperatura.
