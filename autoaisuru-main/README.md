# autoAisuru — Istruzioni d’Uso

Questo script serve per **inviare automaticamente domande verso un agente di aisuru** e salvare le risposte in un file CSV.

---

## Cosa ti serve prima di iniziare

### 1. Un file `config.txt`

Deve trovarsi nella stessa cartella dello script e avere questa struttura:

```
csv_file=nomefile.csv
agent_id=tuo_agent_id
agent_password=password_agente
url=https://...
thinking=true
save_tempo_risposta=true
```

#### Campo per campo:

* **csv\_file** → Il nome del file CSV che contiene le domande.
* **agent\_id** → L’ID dell’agente da contattare.
* **agent\_password** → La password dell’agente se privato
* **url** → L’URL base per le chiamate API. **Non** deve finire con `/` finale. Esempio `https://api.endpoint.com`
* **thinking** → `true` se vuoi estrarre dal modello anche il "pensiero interno" (se disponibile). `false` se ti basta solo la risposta finale.
* **save\_tempo\_risposta** → `true` se vuoi salvare i tempi di risposta alle domande. `false` altrimenti.

##### thinking e save\_tempo\_risposta
Sono campi che possono anche essere omessi, il loro valore default sarà
* `false` per thinking
* `true` per save_tempo_risposta


##### Password
Se l'agente ha la password, bisogna inserirla nel campo apposito del file. Se non è presente una password perché l'agente è pubblico, si **deve** eliminare la riga corrispondente alla password.

---

## 2. Un file CSV

Il file CSV da usare deve contenere almeno queste colonne:

```
conversazione,domanda,risposta
```

Facoltativamente puoi aggiungere:

```
valutazione,note,thinking
```

Quando viene eseguito lo script viene **aggiunta una colonna** nel csv dove viene riempita con il **tempo** che ha impiegato il modello a rispondere.

### Esempio di CSV corretto:

```csv
conversazione,domanda,risposta,valutazione,note,thinking
1,"Qual è la capitale d’Italia?",,,,
1,"E perché è importante?",,,,
```

* La colonna `conversazione` serve per raggruppare le domande che fanno parte dello stesso dialogo.
* Se nel `config.txt` hai messo `thinking=true`, la colonna `thinking` deve esserci.

---

## Come si usa

1. Metti il file `config.txt` e il file `.csv` nella stessa cartella dello script.

2. Lancia lo script con:

   ```
   python main.py
   ```

3. Se nel CSV ci sono già delle risposte, il programma ti chiederà se vuoi **sovrascriverle tutte**. Se rispondi “n”, si ferma.

4. Il programma controllerà che il modello risponda correttamente. Se non lo fa, si fermerà da solo. In questo caso ci dovrebbe essere qualche problema lato agente che non riesce a comunicare con le API del LLM.

5. Le domande vengono inviate una alla volta. Alla fine, il file CSV verrà aggiornato con le risposte e il tempo di risposta (e, se richiesto, anche con il “thinking”).

---

## Note utili

* Lo script crea una nuova sessione per ogni conversazione, così il contesto viene mantenuto.
* Se hai impostato `thinking=true`, lo script si aspetta che il modello usi questo formato:

  ```text
  <think>qui il ragionamento del modello</think>qui la risposta finale
  ```

  Il ragionamento sarà salvato nella colonna `thinking`, il resto nella colonna `risposta`.
* Le risposte vengono salvate direttamente **nel file CSV di partenza** (sovrascrivendo il file).

---

## In sintesi

| Cosa                     | Serve per                                                               |
| ------------------------ | ----------------------------------------------------------------------- |
| `config.txt`             | Dire al programma dove trovare le domande e come parlare con il modello |
| `csv`                    | Contenere domande e ricevere le risposte                                |
| `thinking=true`          | Se vuoi dividere “ragionamento” e “risposta” in due colonne             |
| `save_tempo_risposta=false`| Se non vuoi salvare il tempo di risposta dell'agente        |
| `python main.py` | Per far partire tutto                                                   |

---
