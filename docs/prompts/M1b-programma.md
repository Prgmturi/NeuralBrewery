Leggi AGENTS.md e docs/impianto.md, tutto: soprattutto "La cotta di riferimento" e, sotto "Controllore", i comandi, gli interlock, "Il controllore non riparte da solo", "Programma della cotta" e gli allarmi. Il codice di M1 è in `src/neuralbrewery/adapters/plant_sim/`: leggi `controller/controller.py` e i test in `tests/adapters/plant_sim/` prima di proporre qualcosa.

Obiettivo di questa sessione (M1b): il programma della cotta nel controllore. Python puro, niente FastAPI. Servizio, adapter REST, impostazioni, compose e sorvegliante sono M2: non toccarli.
- `core/plant/schemas.py`: il programma nella fotografia (stato, numero e nome del passo, tempo trascorso e tempo massimo, motivo della pausa); gli allarmi `step_late` e `program_paused`; gli eventi di cambio passo e di fine programma; i codici di rifiuto nuovi.
- `core/plant/protocols.py`: `start_program`, `confirm_step`, `pause_program`, `resume_program`, `abort_program` in `PlantCommander`.
- `adapters/plant_sim/controller/`: la ricetta come tabella di dati e il programma che la esegue dentro il ciclo del controllore.
- simulatore e adattatore in-process: i cinque comandi. Alla conferma del passo "Lievito" il simulatore fa ciò che il birraio fa con le mani: inocula il lievito e accende l'iSpindel. Il controllore non tocca il processo.
- Test in `tests/adapters/plant_sim/test_program.py`.

Decisioni già prese. Alcune cambiano docs/impianto.md: aggiornalo nello stesso commit.
1. **Lavaggio con 18 L, non 17.** Con 17 L il bollitore resta con 2,4–2,9 L dopo il travaso al fermentatore, troppo vicino al minimo di 2 L: su un seed su 50 l'ultimo travaso finisce in allarme. Con 18 L: 200 seed su 200. La tabella della cotta diventa: 27 L nel bollitore, circa 3,6 L sul fondo, 31,5 L di acqua usata.
2. **Agitatore acceso dal passo 3, non dal 2.** Durante l'impasto il livello del tino è sotto le pale: il comando sarebbe rifiutato.
3. **Passo 15**: FERM a 19 °C da quando il passo comincia; la conferma del birraio è l'inoculo e chiude il programma.
4. **Un passo descrive lo stato intero del lato caldo**: setpoint di HLT, MASH e BOIL, agitatore, percorso con i litri. Quando il passo comincia, e a ogni ripresa, il programma porta l'impianto a quello stato dando solo i comandi che mancano, in quest'ordine: setpoint da togliere, percorso, agitatore, setpoint da mettere. Così nessun interlock scatta per l'ordine dei comandi, e la ripresa dopo `stop_all` rimette tutto com'era.
5. **Interlock 2**: "il mosto si muove" vuol dire agitatore comandato e inverter senza guasto, oppure ricircolo attivo. Oggi guarda il ritorno di marcia, che arriva un passo dopo il comando: accendere l'agitatore e subito dopo scaldare il tino viene rifiutato.
6. **Il programma usa i comandi del birraio**: stessi controlli, stessi eventi. Non riarma mai un blocco: un comando già a posto non viene ridato.
7. **`step_late` è un avviso**: il passo continua, non viene saltato. Finisce quando finisce il passo.
8. **Pausa automatica**, con l'allarme `program_paused` e il motivo: un blocco attivo, K1 aperto, inverter in guasto, oppure un comando del programma rifiutato.
9. **In pausa**: i setpoint restano, il tempo del passo si ferma, il travaso a quantità si ferma e i litri fatti restano contati. Il ricircolo resta acceso: è ciò che permette al tino di tenere la temperatura.
10. **`resume_program` è rifiutato finché c'è un blocco attivo**: prima `reset`, poi la ripresa. I due comandi dati uno dopo l'altro, nello stesso istante, devono funzionare. Un travaso riparte dai litri che mancano.
11. **Comandi manuali con il programma in corso**: quelli che avviano qualcosa sul lato caldo sono rifiutati; quelli che fermano (`stop_route`, setpoint tolto, agitatore spento) sono accettati e mettono il programma in pausa, senza allarme. Il fermentatore si comanda sempre. In pausa i comandi manuali sono ammessi.
12. **`start_program`** è rifiutato se c'è già un programma aperto o un blocco attivo.

Le regole che i test devono difendere:
- una cotta intera finisce con 20 L nel fermentatore, entro mezzo litro, in circa 3 ore e 40 minuti simulati, senza allarmi;
- il controllore non riparte da solo: dopo un blocco il programma resta in pausa finché non arrivano `reset` e `resume_program`;
- un travaso ripreso non supera la quantità del passo;
- `stop_all` e `abort_program` non toccano il fermentatore;
- stesso seed e stesse azioni: stessa cotta, fino all'ultima cifra;
- un passo manuale non prosegue senza `confirm_step`.

Fuori scope, anche se sembrano facili: una seconda ricetta o ricette con parametri, il salto di un passo, luppolo e altre azioni a mano, riempimento della HLT, lavaggio dell'impianto, due cotte di fila.

Tieni conto delle regole del template: mypy strict, copertura minima 99,5 % con i rami, import contract. Per l'impianto solo test di scenario attraverso le porte (docs/decisioni.md, "Test dell'impianto"): un ramo che nessuno scenario percorre si toglie, oppure gli manca uno scenario.

Come procedere:
1. Proponi l'elenco dei moduli e dei test prima di scrivere codice, e aspetta il mio ok.
2. Scrivi prima il test della cotta intera (controllo di plausibilità 6) e quelli di pausa e ripresa, poi il codice che li fa passare.
3. Fuori dai test, fai girare la cotta su almeno 50 seed e riporta i numeri: litri nel fermentatore, litri rimasti nel bollitore e nella HLT, durata di ogni passo. Nessun seed deve finire in allarme.

Fine sessione: tutti i controlli della CI verdi, commit in Conventional Commits con il solo nome di chi sviluppa, docs/impianto.md aggiornato nello stesso commit. Poi dimmi cosa devo controllare io e quali dubbi restano: il prompt di M2 lo scriviamo dopo.
