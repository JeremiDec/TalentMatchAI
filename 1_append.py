import os
import json
import time
from importlib.machinery import SourceFileLoader

# Konfiguracja
PROG_DIR = "data/programmers"
PROFILES_FILE = os.path.join(PROG_DIR, "programmer_profiles.json")

# Ładujemy klasę z oryginalnego pliku
try:
    gen_module = SourceFileLoader("gen_mod", "1_generate_data.py").load_module()
    GraphRAGDataGenerator = gen_module.GraphRAGDataGenerator
except FileNotFoundError:
    print("❌ Błąd: Nie znaleziono pliku 1_generate_data.py")
    exit(1)

def append_data():
    print("🚀 Rozpoczynam dolewanie danych (Append Mode)...")
    
    generator = GraphRAGDataGenerator()
    
    # 1. Wczytaj istniejące dane
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, 'r', encoding='utf-8') as f:
            existing_profiles = json.load(f)
        last_id = existing_profiles[-1]['id'] if existing_profiles else 0
        print(f"📂 Znaleziono {len(existing_profiles)} istniejących profili. Ostatnie ID: {last_id}")
    else:
        existing_profiles = []
        last_id = 0
        print("⚠️ Nie znaleziono pliku JSON. Zaczynam od zera.")

    # 2. Pobierz liczbę do wygenerowania z configu
    num_to_generate = generator.config['generation']['num_programmers']
    print(f"🔨 Będę generować {num_to_generate} nowych profili (od ID {last_id + 1}).")

    new_profiles = []
    
    # 3. Pętla generująca
    for i in range(num_to_generate):
        current_id = last_id + i + 1
        
        # Generujemy sam profil (dane w pamięci) - generujemy po 1 sztuce
        # Używamy metody generate_programmer_profiles dla 1 osoby
        temp_list = generator.generate_programmer_profiles(1)
        profile = temp_list[0]
        profile['id'] = current_id # Nadpisujemy ID, żeby zachować ciągłość
        
        print(f"[{i+1}/{num_to_generate}] Generowanie CV dla: {profile['name']} (ID: {current_id})")

        try:
            # Generuj treść CV przez LLM
            cv_markdown = generator.generate_cv_markdown(profile)
            
            # Zapisz plik (MD/PDF)
            safe_name = profile['name'].replace(" ", "_").replace(".", "")
            filename = f"cv_{current_id:03d}_{safe_name}"
            generator.save_cv_as_pdf(cv_markdown, filename, PROG_DIR)
            
            new_profiles.append(profile)

            # --- BEZPIECZNIK: Zapis co 10 osób ---
            if (i + 1) % 10 == 0:
                print(f"   💾 Checkpoint: Zapisywanie stanu...")
                combined_profiles = existing_profiles + new_profiles
                with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(combined_profiles, f, indent=2, default=str)
            
            # --- AZURE SLEEP ---
            time.sleep(3) # 3 sekundy przerwy dla Azure
            
        except Exception as e:
            print(f"❌ Błąd przy generowaniu {profile['name']}: {e}")
            time.sleep(5) # Dłuższa przerwa po błędzie

    # 4. Zapis końcowy
    print("🏁 Kończenie i zapisywanie całości...")
    final_profiles = existing_profiles + new_profiles
    with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_profiles, f, indent=2, default=str)

    print(f"✅ Sukces! Masz teraz łącznie {len(final_profiles)} profili.")
    print(f"   Projekty i RFP zostały nietknięte (zgodnie z planem).")

if __name__ == "__main__":
    append_data()