Leggi AGENTS.md e docs/impianto.md. In _reference/gateway-demo/ c'è un prototipo funzionante (modello, strumenti, porte, adattatori, 23 test): usalo come base, adattandolo alle convenzioni di questo repo.

Obiettivo di questa sessione (M1): vocabolario, porte e modello dell'impianto. Python puro, niente FastAPI.
- `core/plant/schemas.py`: il vocabolario (Reading, PlantState, Vessel, Route, CommandResult, Fault...).
- `core/plant/protocols.py`: PlantReader, PlantCommander, SimulationControl.
- `adapters/plant_sim/`: modello fisico, strumenti, interlock, guasti, e l'adattatore in-process che implementa le tre porte.
- Test in `tests/adapters/plant_sim/` e, per le porte, in `tests/core/plant/`.

Rispetto al prototipo cambia questo (dettagli in docs/impianto.md):
- sonde PT100 classe A con trasmettitore 4–20 mA, errore fisso per sonda entro tolleranza, guasto segnalato in corrente (NE43); la lettura espone anche i mA;
- valvole esplicite per ogni percorso e un percorso attivo per pompa (lo sparge usa P1 e P2 insieme);
- nuovi componenti: TT4, agitatore M1 con inverter, contattore di sicurezza K1, riempimento HLT con EV1;
- bollitura con evaporazione e plateau a 100 °C;
- tutti i guasti elencati in docs/impianto.md.

Come procedere:
1. Proponi l'elenco dei moduli e dei test prima di scrivere codice, e aspetta il mio ok.
2. Scrivi prima i test della sezione "Controlli di plausibilità" e quelli degli interlock, poi il codice che li fa passare.
3. Seed fisso, tempo simulato ovunque, nessun accesso all'orologio reale nel modello.

Fine sessione: tutti i controlli della CI verdi, commit in Conventional Commits. Se hai dovuto cambiare qualcosa rispetto a docs/impianto.md, aggiornalo nello stesso commit e dimmelo.
