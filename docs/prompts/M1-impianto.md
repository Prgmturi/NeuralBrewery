Leggi AGENTS.md e docs/impianto.md, tutto, a partire da "Il principio". In _reference/gateway-demo/ c'è un prototipo più vecchio: usalo per la forma del codice (porte, adattatore in-process, test di contratto), non per il comportamento. Il prototipo regola e blocca sui valori veri e non ha un controllore: qui è diverso.

Obiettivo di questa sessione (M1): vocabolario, porte, processo, dispositivi e controllore con i comandi manuali. Python puro, niente FastAPI. Il programma della cotta è M1b; servizio, adapter REST, impostazioni, compose e sorvegliante sono M2: non toccarli.
- `core/plant/schemas.py`: il vocabolario. Letture con qualità e motivo, dispositivi con comando e ritorno, fotografia del controllore, allarmi, eventi, CommandResult con codice, Fault.
- `core/plant/protocols.py`: PlantReader, PlantCommander, SimulationControl. I comandi del programma (`start_program`, `confirm_step`, `pause_program`, `resume_program`, `abort_program`) e la parte "Programma" della fotografia arrivano con M1b: non metterli ora.
- `adapters/plant_sim/`, tre strati che non si scavalcano:
  - processo: i valori veri (termica con dispersione per recipiente, grani, evaporazione, travasi, traboccamento, fermentazione);
  - dispositivi: sonde e livelli 4–20 mA, iSpindel, pompe, valvole con fine corsa, resistenze con potenza da 0 a 100 %, K1 con i suoi termostati, inverter;
  - controllore: stato dei segnali, regolazione sulla sonda, comandi, interlock sulle misure, allarmi, eventi, storico breve.
  In più: le partenze con nome, i guasti, e l'adattatore in-process che implementa le tre porte.
- Test in `tests/adapters/plant_sim/` e, per le porte, in `tests/core/plant/`.

Le regole che i test devono difendere:
- il controllore non legge mai un valore vero, solo i segnali dei dispositivi. Aggiungi un import contract (il modulo del controllore non importa quello del processo, e il processo non importa i dispositivi) con la sua riga in docs/architecture.md, "What checks each rule";
- lo stato riporta il comando e, dove esiste, il ritorno: mai l'effetto reale. Una resistenza interrotta resta "comandata al 100 %";
- un comando ha una fine certa: il travaso è a quantità e si ferma da solo;
- la sicurezza cablata (termostati e K1) è l'unica cosa che agisce sui valori veri;
- passo di calcolo fisso scelto alla creazione del simulatore, tempo contato in passi interi, nessun accesso all'orologio reale;
- una sequenza casuale per strumento, derivata da seed e sigla: un guasto su uno strumento non cambia il rumore degli altri;
- un guasto su una sigla che non lo ammette è un errore, non viene ignorato;
- un travaso non supera mai la capacità della destinazione: ciò che eccede trabocca.

Fuori scope, anche se sembrano facili: programma della cotta (M1b), sparge con due pompe insieme, riempimento della HLT, sonda TT4, deriva delle sonde, tempi di corsa delle valvole, PID, IO-Link del livello.

Tieni conto da subito delle regole del template: mypy strict, copertura minima 99,5 % con i rami, import contract su `adapters/plant_sim/`.

Come procedere:
1. Proponi l'elenco dei moduli e dei test prima di scrivere codice, e aspetta il mio ok.
2. Scrivi prima i test dei "Controlli di plausibilità" (tranne il 6, che è di M1b) e quelli degli interlock e di K1, poi il codice che li fa passare.
3. Poi un test per ogni riga delle tabelle "Guasti iniettabili": ciò che vede il controllore deve essere ciò che dice la riga.

Segnala come "da verificare" i punti in fondo a docs/impianto.md: valvole a 5 fili, batteria dell'iSpindel, dispersioni dei recipienti.

Fine sessione: tutti i controlli della CI verdi, commit in Conventional Commits con il solo nome di chi sviluppa. Se hai dovuto cambiare qualcosa rispetto a docs/impianto.md, aggiornalo nello stesso commit. Poi dimmi cosa devo controllare io e quali dubbi restano: il prompt di M1b lo scriviamo dopo.
