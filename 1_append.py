import os
import json
import time
from importlib.machinery import SourceFileLoader

# Ładujemy klasę z oryginalnego pliku
try:
    gen_module = SourceFileLoader("gen_mod", "1_generate_data.py").load_module()
    GraphRAGDataGenerator = gen_module.GraphRAGDataGenerator
except FileNotFoundError:
    print("❌ Błąd: Nie znaleziono pliku 1_generate_data.py")
    exit(1)

def append_data():
    print("🚀 Rozpoczynam dolewanie danych (Append Mode)...")
    
    # Inicjalizacja generatora (wczytuje config.toml)
    generator = GraphRAGDataGenerator()
    
    # 1. Pobierz ścieżki dynamicznie z konfiguracji (POPRAWKA)
    try:
        PROG_DIR = generator.config['output']['programmers_dir']
    except KeyError:
        PROG_DIR = "data/programmers" # Fallback
        
    PROFILES_FILE = os.path.join(PROG_DIR, "programmer_profiles.json")
    
    # Upewnij się, że katalog istnieje
    os.makedirs(PROG_DIR, exist_ok=True)

    # 2. Wczytaj istniejące dane
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, 'r', encoding='utf-8') as f:
            existing_profiles = json.load(f)
        last_id = existing_profiles[-1]['id'] if existing_profiles else 0
        print(f"📂 Znaleziono {len(existing_profiles)} istniejących profili w {PROG_DIR}. Ostatnie ID: {last_id}")
    else:
        existing_profiles = []
        last_id = 0
        print(f"⚠️ Nie znaleziono pliku JSON w {PROG_DIR}. Zaczynam od zera.")

    # 3. Pobierz liczbę do wygenerowania z configu
    # Możesz tu zmienić ręcznie na np. 5, jeśli chcesz dolać tylko kilku
    num_to_generate = generator.config['generation']['num_programmers']
    print(f"🔨 Będę generować {num_to_generate} nowych profili (od ID {last_id + 1}).")

    new_profiles = []
    
    # 4. Pętla generująca
    for i in range(num_to_generate):
        current_id = last_id + i + 1
        
        # Używamy nowej metody z 1_generate_data.py - ona już generuje GPA, Rates, Soft Skills!
        temp_list = generator.generate_programmer_profiles(1)
        profile = temp_list[0]
        profile['id'] = current_id 
        
        print(f"[{i+1}/{num_to_generate}] Generowanie CV: {profile['name']} (${profile['hourly_rate']}/hr)")

        try:
            # Generuj treść CV przez LLM (użyje nowego promptu z bogatymi danymi)
            cv_markdown = generator.generate_cv_markdown(profile)
            
            # Zapisz plik (MD/PDF)
            safe_name = profile['name'].replace(" ", "_").replace(".", "")
            filename = f"cv_{current_id:03d}_{safe_name}"
            generator.save_cv_as_pdf(cv_markdown, filename, PROG_DIR)
            
            new_profiles.append(profile)

            # --- BEZPIECZNIK: Zapis co 5 osób ---
            if (i + 1) % 5 == 0:
                print(f"   💾 Checkpoint...")
                combined_profiles = existing_profiles + new_profiles
                with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(combined_profiles, f, indent=2, default=str)
            
            # --- AZURE SLEEP ---
            # Jeśli masz wysoki limit, możesz zmniejszyć sleep
            time.sleep(2) 
            
        except Exception as e:
            print(f"❌ Błąd przy generowaniu {profile['name']}: {e}")
            time.sleep(5) 

    # 5. Zapis końcowy
    print("🏁 Kończenie i zapisywanie całości...")
    final_profiles = existing_profiles + new_profiles
    with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_profiles, f, indent=2, default=str)

    print(f"✅ Sukces! Baza powiększona do {len(final_profiles)} profili.")
    print("ℹ️ Uwaga: Nowi programiści nie są przypisani do istniejących projektów w projects.json (to są 'wolni strzelcy').")

if __name__ == "__main__":
    append_data()