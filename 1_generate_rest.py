"""
Uzupełniacz Danych: Generuje Projekty i RFP dla istniejących profili.
Uruchom to RAZ, mając już wygenerowane CV w data/programmers.
"""
import os
import json
from importlib.machinery import SourceFileLoader

# Ładujemy główną klasę
try:
    gen_module = SourceFileLoader("gen_mod", "1_generate_data.py").load_module()
    GraphRAGDataGenerator = gen_module.GraphRAGDataGenerator
except FileNotFoundError:
    print("❌ Nie znaleziono 1_generate_data.py")
    exit(1)

def generate_missing_pieces():
    generator = GraphRAGDataGenerator()
    config = generator.config
    
    # Ścieżki
    progs_dir = config['output']['programmers_dir']
    projs_dir = config['output']['projects_dir']
    rfps_dir = config['output']['rfps_dir']
    
    profiles_path = os.path.join(progs_dir, "programmer_profiles.json")
    
    # 1. Wczytaj Twoich 500 programistów
    if not os.path.exists(profiles_path):
        print("❌ Błąd: Nie znaleziono programmer_profiles.json!")
        return

    print(f"📂 Wczytuję istniejących programistów z {profiles_path}...")
    with open(profiles_path, 'r', encoding='utf-8') as f:
        profiles = json.load(f)
    
    print(f"✅ Załadowano {len(profiles)} profili.")

    # 2. Generuj Projekty (powiązane z tymi ludźmi)
    # Pobieramy liczbę z configu (powinno być 150 wg Twoich ustawień)
    num_projects = config['generation']['num_projects']
    print(f"🔨 Generuję {num_projects} projektów (Historyczne + Aktywne)...")
    
    # Ta metoda automatycznie przydzieli Twoich 500 ludzi do tych projektów
    projects = generator.generate_projects(num_projects, profiles)
    
    # Zapisz projekty
    os.makedirs(projs_dir, exist_ok=True)
    with open(os.path.join(projs_dir, "projects.json"), 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, default=str)
    print(f"💾 Zapisano projekty w {projs_dir}/projects.json")

    # 3. Generuj RFP
    num_rfps = config['generation']['num_rfps']
    print(f"📄 Generuję {num_rfps} dokumentów RFP...")
    
    rfps = generator.generate_rfps(num_rfps)
    os.makedirs(rfps_dir, exist_ok=True)
    
    # Zapisz JSON RFP
    with open(os.path.join(rfps_dir, "rfps.json"), 'w', encoding='utf-8') as f:
        json.dump(rfps, f, indent=2, default=str)
        
    # Wygeneruj PDFy dla RFP
    for i, rfp in enumerate(rfps, 1):
        print(f"   Generowanie PDF dla RFP {i}/{num_rfps}...")
        md = generator.generate_rfp_markdown(rfp)
        safe_title = rfp['title'].replace(" ", "_").replace("/", "")
        generator.save_cv_as_pdf(md, f"rfp_{rfp['id']}_{safe_title}", rfps_dir)

    print("\n✅ ZAKOŃCZONO!")
    print("   Masz teraz komplet danych:")
    print(f"   - {len(profiles)} Programistów (z CV)")
    print(f"   - {len(projects)} Projektów (z przypisanymi ludźmi)")
    print(f"   - {len(rfps)} RFP (do matchowania)")

if __name__ == "__main__":
    generate_missing_pieces()