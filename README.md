# Progetto "Sunny": Agente AI Sicuro con Verifica di Sicurezza via Red Teaming

Questo repository contiene il codice e i risultati del mio progetto di tesi di laurea in Ingegneria Informatica, focalizzato sulla creazione e la verifica di sicurezza di "Sunny", un agente conversazionale per il supporto psicologico infantile.

## 🎯 Obiettivo del Progetto

L'obiettivo principale era esplorare le sfide pratiche nella creazione di un'AI per un'applicazione ad alto rischio e applicare una metodologia strutturata di **Red Teaming** per validarne la sicurezza, l'etica e l'affidabilità.

## 🛠️ Tecnologie Utilizzate

* **Linguaggio:** Python
* **Piattaforma AI:** Aisuru
* **Modelli LLM Testati:** OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet
* **Framework di Test:** Promptfoo
* **Concetti Chiave:** AI Safety, Red Teaming, Prompt Engineering, Jailbreaking, Guardrail Models

## 🛡️ Metodologia di Red Teaming

Ho implementato una campagna di test automatizzati usando **Promptfoo** per orchestrare l'invio di prompt malevoli, simulando attacchi avversari per identificare le vulnerabilità del sistema. I test si sono concentrati su:

* **Jailbreaking:** Tentativi di aggirare i filtri di sicurezza etici del modello.
* **Prompt Injection:** Inserimento di istruzioni nascoste per manipolare il comportamento dell'agente.
* **Fuga di Dati Sensibili:** Tentativi di forzare il modello a rivelare informazioni riservate.

## 📈 Risultati

I risultati dei test hanno permesso di misurare la robustezza dell'agente tramite specifici KPI, identificando le vulnerabilità residue e fornendo una valutazione oggettiva dell'efficacia delle misure di sicurezza implementate.

*(Consiglio: Inserisci qui uno screenshot dei risultati di Promptfoo, come quello che hai nella tesi! Puoi trascinare l'immagine direttamente nell'editor del README su GitHub).*
