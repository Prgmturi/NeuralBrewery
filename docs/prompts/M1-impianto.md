Leggi AGENTS.md e docs/impianto.md. In _reference/gateway-demo/ c'è un prototipo funzionante (modello, strumenti, porte, adattatori, 23 test): usalo come base, adattandolo alle convenzioni di questo repo.

Obiettivo di questa sessione (M1): vocabolario, porte e modello dell'impianto. Python puro, niente FastAPI. Servizio, adapter REST, impostazioni e compose sono M2: non toccarli.
- `core/plant/schemas.py`: il vocabolario (Reading, PlantState, Vessel, Route, CommandResult, Fault, Event...).
- `core/plant/protocols.py`: PlantReader, PlantCommander, SimulationControl.
- `adapters/plant_sim/`: modello fisico, strumenti, interlock, guasti, storico breve, e l'adattatore in-process che implementa le tre porte.
- Test in `tests/adapters/plant_sim/` e, per le porte, in `tests/core/plant/`.

Rispetto al prototipo cambia questo (dettagli in docs/impianto.md):
- sonde PT100 classe A con trasmettitore 4–20 mA al posto delle DS18B20: errore fisso per sonda entro tolleranza, guasto segnalato in corrente (NE43), la lettura espone anche i mA. Il guasto `power_reset` del prototipo sparisce;
- valvole nello stato (posizione comandata) e guasto "valvola bloccata chiusa";
- contattore di sicurezza K1: sovratemperatura, relè statico in corto, comando `reset_safety`;
- agitatore M1 con inverter: comando `set_agitator`, interlock sul livello, guasto con un codice di allarme. Il codice è un parametro del guasto: quello vero va preso dal manuale V20, che non è ancora in data/manuals/, quindi segnalalo come da verificare;
- iSpindel con tensione di batteria e guasto "batteria scarica";
- eventi strutturati (tempo simulato, codice, motivo) leggibili da PlantReader, al posto della lista di stringhe del prototipo;
- storico breve delle letture nel simulatore, leggibile da PlantReader.

Resta come nel prototipo: un solo percorso attivo alla volta.

Fuori scope, anche se sembrano facili: sparge con due pompe insieme, evaporazione, riempimento della HLT, sonda TT4, deriva delle sonde.

Tieni conto da subito delle regole del template: mypy strict, copertura minima 99,5 % con i rami, import contract su `adapters/plant_sim/`.

Come procedere:
1. Proponi l'elenco dei moduli e dei test prima di scrivere codice, e aspetta il mio ok.
2. Scrivi prima i test della sezione "Controlli di plausibilità" e quelli degli interlock, poi il codice che li fa passare.
3. Seed fisso, tempo simulato ovunque, nessun accesso all'orologio reale nel modello.

Fine sessione: tutti i controlli della CI verdi, commit in Conventional Commits con il solo nome di chi sviluppa. Se hai dovuto cambiare qualcosa rispetto a docs/impianto.md, aggiornalo nello stesso commit. Poi dimmi cosa devo controllare io e quali dubbi restano: il prompt di M2 lo scriviamo dopo.
