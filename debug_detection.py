# debug_connection.py
from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI

# Ładujemy zmienne
load_dotenv(override=True)

print("🔍 DIAGNOSTYKA POŁĄCZENIA AZURE OPENAI")
print("-" * 30)

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
version = os.getenv("OPENAI_API_VERSION")

# 1. Sprawdzamy czy zmienne istnieją
print(f"Endpoint:   {endpoint}")
print(f"Deployment: {deployment}")
print(f"Version:    {version}")
if api_key:
    print(f"API Key:    {'*' * 5}{api_key[-4:]} (Znaleziono)")
else:
    print(f"API Key:    ❌ BRAK")

if not all([endpoint, api_key, deployment]):
    print("\n❌ BŁĄD: Brakuje zmiennych w pliku .env!")
    exit(1)

# 2. Próba połączenia
print("\n📡 Próba wysłania prostego zapytania 'Hello'...")

try:
    llm = AzureChatOpenAI(
        azure_deployment=deployment,
        openai_api_version=version,
        azure_endpoint=endpoint,
        api_key=api_key,
        temperature=0
    )
    
    response = llm.invoke("Hello, are you working?")
    print(f"\n✅ SUKCES! Odpowiedź modelu:\n{response.content}")

except Exception as e:
    print(f"\n❌ BŁĄD KRYTYCZNY POŁĄCZENIA:\n{e}")