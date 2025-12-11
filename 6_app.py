import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components
import os
import tempfile

# Importujemy Twój istniejący system
# Upewnij się, że plik 3_query_knowledge_graph.py jest w tym samym folderze
from importlib.machinery import SourceFileLoader
graph_rag_module = SourceFileLoader("graph_rag", "3_query_knowledge_graph.py").load_module()
CVGraphRAGSystem = graph_rag_module.CVGraphRAGSystem

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="TalentMatch AI - GraphRAG",
    page_icon="🔍",
    layout="wide"
)

# --- INICJALIZACJA SYSTEMU (Cache, żeby nie łączyć się z Neo4j przy każdym kliknięciu) ---
@st.cache_resource
def get_system():
    try:
        system = CVGraphRAGSystem()
        return system
    except Exception as e:
        st.error(f"Błąd połączenia z Neo4j: {e}")
        return None

system = get_system()

# --- FUNKCJA DO WIZUALIZACJI GRAFU (PYVIS) ---
def visualize_graph(driver, query):
    """Generuje interaktywny graf HTML z zapytania Cypher."""
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
    
    # Pobieramy dane bezpośrednio z drivera Neo4j (dostępny w system.graph._driver)
    # Ale bezpieczniej użyć metody graph.query z LangChain
    try:
        results = system.graph.query(query)
        
        # Budujemy sieć
        for record in results:
            # Zakładamy, że zapytanie zwraca ścieżki lub węzły source/target
            # Dostosujmy logikę do prostego schematu: source -> rel -> target
            
            # Obsługa różnych typów wyników wymagałaby skomplikowanego parsowania
            # Dla uproszczenia wizualizujemy konkretne relacje Person -> Skill/Company
            
            if 'p' in record and 's' in record: # Person -> Skill
                src_id = record['p']['id']
                src_label = record['p'].get('name', src_id)
                dst_id = record['s']['id']
                dst_label = record['s'].get('name', dst_id)
                
                net.add_node(src_id, label=src_label, title=src_label, color="#4CAF50") # Zielony dla ludzi
                net.add_node(dst_id, label=dst_label, title=dst_label, color="#2196F3") # Niebieski dla skilli
                net.add_edge(src_id, dst_id, color="#ffffff")
            
            elif 'p' in record and 'c' in record: # Person -> Company
                src_id = record['p']['id']
                src_label = record['p'].get('name', src_id)
                dst_id = record['c']['id']
                dst_label = record['c'].get('name', dst_id)
                
                net.add_node(src_id, label=src_label, title=src_label, color="#4CAF50")
                net.add_node(dst_id, label=dst_label, title=dst_label, color="#FFC107") # Żółty dla firm
                net.add_edge(src_id, dst_id, color="#ffffff")

    except Exception as e:
        st.warning(f"Nie udało się wygenerować wizualizacji: {e}")
        return None

    # Opcje fizyki grafu
    net.force_atlas_2based()
    
    # Zapis do pliku tymczasowego
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        net.save_graph(tmp.name)
        return tmp.name

# --- INTERFEJS UŻYTKOWNIKA ---

st.title("🔍 TalentMatch AI: CV Knowledge Graph")
st.markdown("System RAG oparty na grafie wiedzy (Neo4j + Azure OpenAI)")

# Pasek boczny
with st.sidebar:
    st.header("Status Systemu")
    if system:
        st.success("✅ Neo4j Połączone")
        
        # Statystyki
        try:
            stats = system.graph.query("MATCH (n) RETURN count(n) as count")
            st.metric("Liczba węzłów", stats[0]['count'])
            stats_rel = system.graph.query("MATCH ()-[r]->() RETURN count(r) as count")
            st.metric("Liczba relacji", stats_rel[0]['count'])
        except:
            pass
    else:
        st.error("❌ Brak połączenia")

    st.markdown("---")
    st.markdown("### Przykładowe pytania:")
    examples = [
        "Who has Python skills?",
        "How many people worked at Google?",
        "Find people with both React and Node.js skills.",
        "Who studied at Stanford University?",
        "Find senior-level professionals with leadership experience."
    ]
    
    for ex in examples:
        if st.button(ex):
            st.session_state['query_input'] = ex

# Zakładki główne
tab1, tab2 = st.tabs(["💬 Czat / Zapytania", "🕸️ Eksplorator Grafu"])

with tab1:
    st.subheader("Zapytaj o Kandydatów")
    
    # Input użytkownika (pobiera z session state jeśli kliknięto przycisk)
    user_query = st.text_input("Wpisz swoje pytanie:", key='query_input')

    if user_query and system:
        with st.spinner("Analizuję graf wiedzy..."):
            # Wywołujemy metodę z Twojego systemu
            response = system.query_graph(user_query)
            
            # Główna odpowiedź
            st.markdown("### 💡 Odpowiedź:")
            st.success(response['answer'])
            
            # Szczegóły techniczne (Expandery)
            with st.expander("🛠️ Zobacz wygenerowane zapytanie Cypher"):
                st.code(response['cypher_query'], language="cypher")
                st.caption("To zapytanie zostało wygenerowane przez LLM i wykonane na Neo4j.")

            # Próba wizualizacji wyników w tabeli (jeśli zapytanie zwraca listę)
            # To jest "bajer" - próbujemy zgadnąć czy wynik to lista ludzi
            if "RETURN" in response['cypher_query'].upper():
                try:
                    # Uruchamiamy to samo zapytanie Cypher, żeby dostać surowe dane do tabelki
                    raw_data = system.graph.query(response['cypher_query'])
                    if raw_data:
                        st.markdown("#### 📊 Znalezione dane:")
                        df = pd.DataFrame(raw_data)
                        st.dataframe(df, use_container_width=True)
                except:
                    pass

with tab2:
    st.subheader("Interaktywna Wizualizacja Grafu")
    st.markdown("Przeglądaj powiązania między ludźmi a umiejętnościami (próbka 100 relacji).")
    
    viz_option = st.selectbox(
        "Wybierz widok:",
        ["Ludzie i ich Umiejętności", "Ludzie i ich Firmy", "Ludzie i Uniwersytety"]
    )
    
    cypher_viz = ""
    if viz_option == "Ludzie i ich Umiejętności":
        cypher_viz = "MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) RETURN p, s LIMIT 100"
    elif viz_option == "Ludzie i ich Firmy":
        cypher_viz = "MATCH (p:Person)-[:WORKED_AT]->(c:Company) RETURN p, c LIMIT 100"
    elif viz_option == "Ludzie i Uniwersytety":
        # Uwaga: zakładam relację STUDIED_AT na podstawie Twojego schematu
        cypher_viz = "MATCH (p:Person)-[:STUDIED_AT]->(u:University) RETURN p, u as c LIMIT 100" # alias u as c dla uproszczenia kodu wizualizacji

    if st.button("Generuj Graf 🕸️"):
        with st.spinner("Rysuję graf..."):
            html_path = visualize_graph(None, cypher_viz)
            if html_path:
                components.html(open(html_path, 'r').read(), height=600, scrolling=True)
                os.remove(html_path) # sprzątanie

st.markdown("---")
st.caption("Projekt GraphRAG | Powered by Neo4j & Azure OpenAI")