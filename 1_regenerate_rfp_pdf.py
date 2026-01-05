"""
RFP PDF GENERATOR
=================
Ten skrypt pobiera dane z pliku data/RFP/rfps.json i generuje świeże pliki PDF.
Uwzględnia liczbę wakatów ("Open Positions") w tekście dokumentu.
"""
import json
import os
from importlib.machinery import SourceFileLoader

# Konfiguracja ścieżek
DATA_DIR = "data"
RFPS_DIR = os.path.join(DATA_DIR, "RFP")
RFPS_JSON = os.path.join(RFPS_DIR, "rfps.json")

# Ładujemy klasę generatora (potrzebna tylko do funkcji zapisu PDF - WeasyPrint)
try:
    gen_module = SourceFileLoader("gen_mod", "1_generate_data.py").load_module()
    GraphRAGDataGenerator = gen_module.GraphRAGDataGenerator
except FileNotFoundError:
    print("❌ Błąd: Nie znaleziono pliku 1_generate_data.py (potrzebny do generowania PDF)")
    exit(1)

def main():
    print("🚀 Rozpoczynam generowanie świeżych PDF-ów dla RFP...")
    
    # 1. Sprawdź czy mamy dane źródłowe
    if not os.path.exists(RFPS_JSON):
        print(f"❌ Błąd: Brak pliku {RFPS_JSON}. Nie mam z czego generować.")
        return

    # 2. Wczytaj JSON
    with open(RFPS_JSON, 'r', encoding='utf-8') as f:
        rfps = json.load(f)
    print(f"📂 Wczytano {len(rfps)} definicji RFP.")

    generator = GraphRAGDataGenerator()

    # 3. Pętla generująca PDF
    for rfp in rfps:
        safe_title = rfp['title'].replace(" ", "_").replace("/", "")
        filename = f"rfp_{rfp['id']}_{safe_title}"
        
        print(f"   📄 Przetwarzanie: {rfp['title']}...")

        # Budowanie listy wymagań z LICZBĄ WAKATÓW
        req_rows = []
        for req in rfp['requirements']:
            count = req.get('required_count', 1) # Domyślnie 1, jeśli brak w JSON
            # Format: Skill: Level (Open Positions: X)
            row = f"- **{req['skill_name']}**: {req['min_proficiency']} (Open Positions: {count})"
            req_rows.append(row)
            
        req_list_text = "\n".join(req_rows)

        # Profesjonalny szablon Markdown
        md_content = f"""
# Request for Proposal: {rfp['title']}

**Client:** {rfp['client']}  
**Budget:** {rfp['budget_range']}  
**Project Duration:** {rfp.get('duration_months', 6)} months  
**Deadline:** {rfp.get('deadline', 'TBD')}

## 1. Executive Summary
This document outlines the requirements for the **{rfp['title']}** project. 
We are seeking a qualified vendor to assemble a team of **{rfp['team_size']} specialists** to deliver this strategic initiative.

## 2. Project Scope & Description
{rfp['description']}

The selected team will be responsible for the full development lifecycle, ensuring scalability, security, and performance.

## 3. Technical Requirements & Capacity
To ensure successful delivery, the following skills and capacity are required:

{req_list_text}

## 4. Submission Guidelines
Proposals must be submitted by **{rfp['start_date']}**. 
Please include a detailed timeline and cost breakdown.

**Contact:** rfp@{rfp['client'].lower().replace(' ', '')}.com
"""

        # Zapisz jako PDF
        pdf_path = generator.save_cv_as_pdf(md_content, filename, RFPS_DIR)
    
    print("\n✅ SUKCES! Wygenerowano wszystkie PDF-y w folderze data/RFP.")

if __name__ == "__main__":
    main()