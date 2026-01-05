"""
PDF REGENERATOR: Naprawia PDF-y, dodając brakujące "Count" z pliku JSON.
Działa OFFLINE. Nie zmienia danych w JSON, tylko aktualizuje wygląd dokumentów.
"""
import json
import os
from importlib.machinery import SourceFileLoader

# Ścieżki
DATA_DIR = "data"
RFPS_DIR = os.path.join(DATA_DIR, "RFP")
RFPS_JSON = os.path.join(RFPS_DIR, "rfps.json")

# Ładujemy klasę generatora (tylko do zapisu PDF)
try:
    gen_module = SourceFileLoader("gen_mod", "1_generate_data.py").load_module()
    GraphRAGDataGenerator = gen_module.GraphRAGDataGenerator
except FileNotFoundError:
    print("❌ Nie znaleziono 1_generate_data.py")
    exit(1)

def regenerate_pdfs():
    print("🔄 Regeneracja PDF-ów z uwzględnieniem 'Count'...")
    
    if not os.path.exists(RFPS_JSON):
        print(f"❌ Brak pliku: {RFPS_JSON}")
        return

    # 1. Wczytaj istniejące dane (które są już poprawne w JSON)
    with open(RFPS_JSON, 'r', encoding='utf-8') as f:
        rfps = json.load(f)

    generator = GraphRAGDataGenerator()

    # 2. Generuj PDF-y na nowo z lepszym szablonem
    for rfp in rfps:
        safe_title = rfp['title'].replace(" ", "_").replace("/", "")
        
        # --- TU BYŁ BŁĄD: Teraz dodajemy 'required_count' do tekstu ---
        req_rows = []
        for req in rfp['requirements']:
            # Domyślnie 1, jeśli z jakiegoś powodu brakuje w JSON
            count = req.get('required_count', 1)
            # Format: "- Python: Advanced (Open Positions: 2)"
            row = f"- **{req['skill_name']}**: {req['min_proficiency']} (Open Positions: {count})"
            req_rows.append(row)
            
        req_list_text = "\n".join(req_rows)
        
        # Szablon Markdown
        md_content = f"""
# Request for Proposal: {rfp['title']}

**Client:** {rfp['client']}
**Budget:** {rfp['budget_range']}
**Deadline:** {rfp.get('deadline', 'TBD')}

## 1. Executive Summary
Strategic initiative for {rfp['project_type']}. 
We are looking to assemble a team of **{rfp['team_size']} specialists**.

## 2. Technical Requirements & Capacity
The following skills and capacity are required for the successful delivery:

{req_list_text}

## 3. Submission Guidelines
Proposals should be submitted by {rfp['start_date']}.
Contact: rfp@{rfp['client'].lower().replace(' ', '')}.com
"""
        # Zapisz PDF (nadpisuje stary)
        generator.save_cv_as_pdf(md_content, f"rfp_{rfp['id']}_{safe_title}", RFPS_DIR)
        print(f"   ✅ Zaktualizowano PDF: {safe_title}.pdf")

    print("\n🎉 GOTOWE! Sprawdź folder data/RFP - pliki PDF powinny mieć teraz 'Open Positions'.")

if __name__ == "__main__":
    regenerate_pdfs()