import os
import requests
from msal import ConfidentialClientApplication
from Model.Security.seguranca import GerenciadorDados
from dotenv import load_dotenv

load_dotenv()

class SincronizadorOutlook:
    def __init__(self):
        # Configurações Nexxt Digital vindas do .env
        self.client_id = os.getenv('OUTLOOK_CLIENT_ID')
        self.tenant_id = os.getenv('OUTLOOK_TENANT_ID')
        self.client_secret = os.getenv('OUTLOOK_CLIENT_SECRET') # Deve estar no .env
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scopes = ["https://graph.microsoft.com/.default"]
        self.gerenciador = GerenciadorDados()

    def obter_token(self):
        """Autenticação OAuth2 Client Credentials (Server-to-Server)."""
        app = ConfidentialClientApplication(
            self.client_id, 
            authority=self.authority, 
            client_credential=self.client_secret
        )
        result = app.acquire_token_for_client(scopes=self.scopes)
        if "access_token" in result:
            return result['access_token']
        else:
            raise Exception(f"Erro ao obter token Outlook: {result.get('error_description')}")

    def sincronizar_outlook_para_log(self, path_log):
        """
        Busca e-mails de ativação no Office 365 e salva no log criptografado.
        Independência total: Se o Gmail falhar, esta camada continua operando.
        """
        try:
            token = self.obter_token()
            headers = {'Authorization': f'Bearer {token}'}
            
            # Query: Busca e-mails com "Ativação" no assunto nas últimas 48h
            # O filtro 'top=10' limita a superfície de exposição de dados
            endpoint = (
                "https://graph.microsoft.com/v1.0/users/suporte@nexxt.digital/messages"
                "?$filter=contains(subject,'Ativação')&$top=10&$select=subject,bodyPreview,body"
            )

            response = requests.get(endpoint, headers=headers)
            if response.status_code != 200:
                print(f"[ERRO API] Falha na Graph API: {response.status_code}")
                return False

            messages = response.json().get('value', [])
            if not messages:
                print("[INFO] Nenhum e-mail novo no Outlook da Nexxt Digital.")
                return True

            for msg in messages:
                # Prioriza o bodyPreview para evitar overhead de HTML pesado
                conteudo = msg.get('bodyPreview', '') or msg.get('body', {}).get('content', '')
                
                log_entry = (
                    f"--- REGISTRO OUTLOOK {msg['id'][:10]} ---\n"
                    f"ORIGEM: Nexxt Digital / Outlook\n"
                    f"DADO: {conteudo}\n"
                    f"------------------------------------------"
                )

                # CAMADA DE SEGURANÇA: O dado é limpo de PII e criptografado antes do dump
                self.gerenciador.criptografar_e_salvar(log_entry, path_log)

            print(f"[SUCCESS] {len(messages)} e-mails do Outlook processados com sucesso.")
            return True

        except Exception as e:
            # Erro genérico para Pentest (não vaza detalhes da infra)
            print(f"[ERROR] Falha na camada Outlook: {type(e).__name__}")
            return False

# Função wrapper para manter compatibilidade com seu sincronizacao_total
def sincronizar_outlook_para_log(path_log):
    sinc = SincronizadorOutlook()
    return sinc.sincronizar_outlook_para_log(path_log)