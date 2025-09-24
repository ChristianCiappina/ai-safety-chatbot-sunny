import yaml
import csv

def estrai_prompt_da_yaml(percorso_yaml, percorso_csv):
    # Carica il file YAML
    with open(percorso_yaml, 'r', encoding='utf-8') as f:
        contenuto = yaml.safe_load(f)

    prompts = []
    
    # Accede al campo 'tests'
    tests = contenuto.get("tests", [])
    
    for i, test in enumerate(tests, start=1):
        # Cerca il prompt nel blocco 'vars'
        vars_blocco = test.get("vars", {})
        prompt = vars_blocco.get("prompt", "").strip()
        if prompt:
            prompts.append({
                "conversazione": i,
                "domanda": prompt,
                "risposta": "",
                "valutazione": "",
                "note": "",
                "thinking": ""
            })

    # Scrive i prompt in un file CSV
    intestazioni = ["conversazione", "domanda", "risposta", "valutazione", "note", "thinking"]
    with open(percorso_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=intestazioni)
        writer.writeheader()
        writer.writerows(prompts)

    print(f"Creato file CSV con {len(prompts)} prompt in '{percorso_csv}'.")

# Cambia i parametri
estrai_prompt_da_yaml("prompts_aggiuntivi.yaml", "prompts.csv")