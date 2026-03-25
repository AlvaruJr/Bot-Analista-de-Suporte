import os
from msal import ConfidentialClientApplication
import requests
from dotenv import load_dotenv

def testar_conexao_outlook():
    load_dotenv()
    
    print("--- 🔍 INICIANDO SMOKE TEST: OUTLOOK NEXXT DIGITAL ---")
    
    client_id = os.getenv('OUTLOOK_CLIENT_ID')
    tenant_id = os.getenv('OUTLOOK_TENANT_ID')
    client_secret = os.getenv('OUTLOOK_CLIENT_SECRET')
    
    if not all([client_id, tenant_id, client_secret]) or "SUA_SECRET" in client_secret:
        print("❌ ERRO: Chaves do Outlook incompletas no .env!")
        return

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scopes = ["https://graph.microsoft.com/.default"]

    try:
        # 1. Tenta autenticar no Azure
        app = ConfidentialClientApplication(
            client_id, 
            authority=authority, 
            client_credential=client_secret
        )
        
        print("[1/2] Solicitando Token de Acesso...")
        result = app.acquire_token_for_client(scopes=scopes)
        
        if "access_token" in result:
            token = result['access_token']
            print("✅ Token obtido com sucesso!")
            
            # 2. Tenta uma chamada simples (Verificar Perfil do Suporte)
            print("[2/2] Testando chamada à Graph API...")
            headers = {'Authorization': f'Bearer {token}'}
            # Vamos apenas tentar listar o endpoint de mensagens (sem ler o conteúdo ainda)
            res = requests.get("https://graph.microsoft.com/v1.0/users", headers=headers)
            
            if res.status_code == 200:
                print("🚀 CONEXÃO ESTABELECIDA! O Bot já consegue enxergar a Nexxt Cloud.")
            else:
                print(f"⚠️ Quase lá! Token válido, mas erro de permissão (HTTP {res.status_code}).")
                print("DICA: Verifique se você deu 'Consentimento do Administrador' no Azure.")
        else:
            print(f"❌ FALHA NA AUTENTICAÇÃO: {result.get('error_description')}")

    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {e}")

if __name__ == "__main__":
    testar_conexao_outlook()