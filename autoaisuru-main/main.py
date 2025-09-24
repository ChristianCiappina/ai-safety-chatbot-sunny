import time
import pandas as pd
import requests
import json
import os
import re

MESSAGGIO_ERRORE = "Mi dispiace, le mie risposte sono limitate. Devi farmi le domande giuste. C'è altro che vuoi sapere?"

def validate_csv_structure(df, has_thinking=False):
    """
    Valida la struttura del CSV controllando le colonne necessarie
    
    Args:
        df: DataFrame da validare
        has_thinking: Se True, controlla anche la presenza della colonna thinking
    
    Returns:
        bool: True se tutto ok, False se ci sono errori (e stampa i problemi)
    """
    required_columns = ['conversazione', 'domanda', 'risposta']
    missing_columns = []
    
    # Controlla colonne obbligatorie
    for col in required_columns:
        if col not in df.columns:
            missing_columns.append(col)
    
    # Controlla colonna thinking se richiesta
    if has_thinking and 'thinking' not in df.columns:
        missing_columns.append('thinking')
    
    # Se manca colonna del tempo, aggiungila
    if 'tempo_risposta' not in df.columns:
        print("Aggiungo colonna per contare il tempo risposta")
    
    # Se mancano colonne, mostra errori e soluzioni
    if missing_columns:
        print("❌ ERRORE: Colonne mancanti nel CSV:")
        for col in missing_columns:
            print(f"   - {col}")
        
        print("\n🔧 COME RISOLVERE:")
        print("Aggiungi le colonne mancanti al tuo file CSV.")
        
        if has_thinking and 'thinking' in missing_columns:
            print("Dato che 'thinking=true' nella config, serve anche la colonna: thinking")
        else:
            print("Le colonne obbligatorie sono: conversazione, domanda, risposta")
        
        print("\nEsempio di header corretto:")
        if has_thinking:
            print("conversazione,domanda,risposta,valutazione,note,thinking")
        else:
            print("conversazione,domanda,risposta,valutazione,note")
        
        return False
    
    print("✅ Struttura CSV validata correttamente")
    return True


def load_csv_data(file_path):
    """Carica i dati dal file CSV"""
    df = pd.read_csv(file_path)
    return df

def get_conversations(df):
    """Raggruppa le domande per conversazione"""
    conversations = {}
    
    for _, row in df.iterrows():
        conv_id = row['conversazione']
        question = row['domanda']
        
        if conv_id not in conversations:
            conversations[conv_id] = []
        
        conversations[conv_id].append(question)
    
    return conversations

def save_answers_to_csv(df, conversations_answers, output_path, has_thinking=False, save_tempo_risposta=True):
    """Salva le risposte nel DataFrame originale"""
    
    df['risposta'] = df['risposta'].astype(str).replace('nan', '')
    if has_thinking and 'thinking' in df.columns:
        df['thinking'] = df['thinking'].astype(str).replace('nan', '')
    
    # Aggiungi colonna tempo_risposta se non esiste
    if save_tempo_risposta and ('tempo_risposta' not in df.columns):
        df['tempo_risposta'] = 0.0
        
    # Aggiorna le risposte nel DataFrame
    for index, row in df.iterrows():
        conv_id = row['conversazione']
        question = row['domanda']
        
        # Trova la risposta corrispondente
        if conv_id in conversations_answers:
            for entry in conversations_answers[conv_id]:
                if len(entry) == 3:
                    q, answer, response_time = entry
                elif len(entry) == 2:
                    q, answer = entry
                    response_time = None
                if q == question:
                    
                    # Tempo della risposta
                    if save_tempo_risposta:
                        df.at[index, 'tempo_risposta'] = response_time
                    
                    if has_thinking:
                        # Estrae il thinking tra i tag <think></think>
                        thinking_pattern = r'<think>(.*?)</think>'
                        thinking_matches = re.findall(thinking_pattern, answer, re.DOTALL)
                        
                        if thinking_matches:
                            # Prende tutto il thinking
                            thinking_text = '\n'.join(thinking_matches).strip()
                            # Rimuove i tag thinking dalla risposta
                            clean_answer = re.sub(thinking_pattern, '', answer, flags=re.DOTALL).strip()
                            
                            df.at[index, 'thinking'] = thinking_text
                            df.at[index, 'risposta'] = clean_answer
                        else:
                            # Nessun thinking trovato
                            df.at[index, 'thinking'] = ''
                            df.at[index, 'risposta'] = answer
                    else:
                        # Salva la risposta completa senza separare il thinking
                        df.at[index, 'risposta'] = answer
                    break
    # Salva il CSV
    df.to_csv(output_path, index=False)
    return df

def load_config(config_path):
    """Carica la configurazione dal file .config"""
    config = {}
    
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    return config

def create_session(session_url, agent_id, agent_password="undefined"):
    """Crea una nuova sessione e restituisce il session ID"""
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        "memoriId": agent_id,
        "password": agent_password,
        "birthDate": "1986-04-24T13:38:07.728Z"
    })
    
    response = requests.post(session_url, headers=headers, data=payload)
    response.raise_for_status()
    
    session_id = response.json()["sessionID"]
    return session_id

def send_question(message_url, question, session_id):
    """Invia una domanda e restituisce la risposta"""
    headers = {'Content-Type': 'application/json'}
    
    # Costruisce l'URL con il session ID
    url = message_url.format(sessionID=session_id)
    
    # Prepara il body della richiesta
    body = json.dumps({"text": question})
    
    # Invia la richiesta
    response = requests.post(url, headers=headers, data=body)
    response.raise_for_status()
    
    # Estrae la risposta
    emission = response.json().get("currentState", {}).get("emission", "")
    return emission

def check_model_health(session_url, message_url, agent_id, agent_password="undefined", test_question="Ciao, puoi rispondere?", error_string="ERRORE_MODELLO"):
    """Verifica se il modello funziona correttamente inviando una domanda di test"""
    try:
        # Crea sessione di test
        test_session_id = create_session(session_url, agent_id, agent_password)
        
        # Invia domanda di test
        test_response = send_question(message_url, test_question, test_session_id)
        
        if not delete_session(session_url, test_session_id):
            print("Non sono riuscito a chiudere la sessione del modello")
            
        # Controlla se la risposta contiene la stringa di errore
        if error_string in test_response:
            return False
        return True
        
    except Exception as e:
        print(f"❌ ERRORE durante il test del modello: {e}")
        return False

def delete_session(session_url, session_id):
    headers = {}
    payload = ""
    try:
        response = requests.request("DELETE", session_url+f"/{session_id}", headers=headers, data=payload)
        response.raise_for_status()
        result = response.json()["resultMessage"]
        if result == "Ok":
            return True
        return False
    except Exception as e:
        print(f"❌ Errore chiusura sessione: {e}")
        return False
        

if __name__ == "__main__":
    
    # Carica configurazione
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.txt")
    config = load_config(config_path)
    
    csv_path = f"{{path}}/{config['csv_file']}".format(path=script_dir)
    
    agent_id = config['agent_id']
    agent_password = config.get('agent_password', 'undefined')
    url = config["url"]       
    has_thinking = config.get('thinking', 'false').lower() == 'true'
    save_tempo_risposta = config.get('save_tempo_risposta', 'true').lower() == 'true'
    session_url = url + "/memori/v2/session"
    message_url = url + "/memori/v2/TextEnteredEvent/{sessionID}"
    
    # Carica dati CSV
    df = load_csv_data(csv_path)
    
    # Controlla se il file csv è valido
    if not validate_csv_structure(df, has_thinking):
        exit("❌ Correggere il CSV prima di continuare")
    
    if not pd.isna(df['risposta'].iloc[0]):
        continua = input("La prima risposta non è vuota! Vuoi continuare sovrascrivendo tutte le risposte? (y/n): ")
        if continua.lower() == 'n':
            exit("Uscito dal programma!")
        else:
            print("Ok, continuiamo!")
            
    # Controlla se il modello su aisuru è settato correttamente e non da il messaggio di errore predefinito
    print("Controllo se il modello è raggiungibile...")
    if not check_model_health(session_url, message_url, agent_id, agent_password, error_string=MESSAGGIO_ERRORE):
        exit("Modello non funzionante, esco dal programma")
    print("Modello raggiunto!")
    
    # Raggruppa per conversazioni
    conversations = get_conversations(df)
    
    # Contenitore per tutte le risposte
    conversations_answers = {}
    
    # Elabora ogni conversazione
    for conv_id, questions in conversations.items():
        print(f"Elaboro conversazione {conv_id}: {len(questions)} domande")
        
        # Crea una sessione per questa conversazione
        session_id = create_session(session_url, agent_id, agent_password)
        print(f"Session ID: {session_id}")
        
        # Lista per salvare domande e risposte di questa conversazione
        conversation_qa = []
        
        # Invia tutte le domande della conversazione
        for question in questions:
            print(f"Invio: {question}")
            if save_tempo_risposta:
                start_time = time.time()
            answer = send_question(message_url, question, session_id)
            if save_tempo_risposta:
                end_time = time.time()
                response_time = end_time - start_time
                response_time = str(f"{response_time:.2f}".replace('.', ','))
            
            print(f"Risposta: {answer[:100]}...")  # Solo i primi 100 caratteri
            if save_tempo_risposta:
                conversation_qa.append((question, answer, response_time))
            else:
                conversation_qa.append((question, answer))
        
        if not delete_session(session_url, session_id):
            print("Non sono riuscito a chiudere la sessione del modello")
        
        conversations_answers[conv_id] = conversation_qa
        print("-" * 50)
    
    # Salva tutte le risposte nel CSV originale
    updated_df = save_answers_to_csv(df, conversations_answers, csv_path, has_thinking, save_tempo_risposta)
    print(f"✅ Risposte salvate in {csv_path}")
