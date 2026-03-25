import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from Model.Security.seguranca import GerenciadorDados

# Escopo estrito para leitura
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def obter_servico_gmail():
    """Gerencia autenticação OAuth2 de forma segura."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def extrair_corpo_email(payload):
    """Extrai o texto puro do e-mail de forma recursiva."""
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
            elif 'parts' in part:
                body = extrair_corpo_email(part)
    else:
        data = payload.get('body', {}).get('data')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8')
    return body

def sincronizar_gmail_para_log(path_log):
    """
    Busca e-mails de ativação e salva no log criptografado.
    Implementa camadas independentes de segurança.
    """
    try:
        service = obter_servico_gmail()
        gerenciador = GerenciadorDados()

        # Query específica para evitar processar e-mails irrelevantes (reduz superfície de ataque)
        query = "subject:Ativação"
        results = service.users().messages().list(userId='me', q=query, maxResults=15).execute()
        messages = results.get('messages', [])

        if not messages:
            print("[INFO] Nenhum novo e-mail de ativação encontrado.")
            return

        for msg in messages:
            m_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = m_data.get('payload')
            snippet = m_data.get('snippet', '')
            
            # 1. Extração do conteúdo bruto
            corpo_bruto = extrair_corpo_email(payload)
            conteudo_final = corpo_bruto if corpo_bruto else snippet

            # 2. Formatação do Registro
            log_entry = (
                f"--- REGISTRO GMAIL {msg['id']} ---\n"
                f"ASSUNTO: Ativação Conecta RS\n"
                f"CONTEÚDO: {conteudo_final}\n"
                f"------------------------------------"
            )

            # 3. SEGURANÇA ATIVA: 
            # O método 'criptografar_e_salvar' deve internamente:
            # - Sanitizar PII (CPFs/Senhas)
            # - Sanitizar Injeções (SQL/Markdown)
            # - Criptografar com Fernet (AES-128)
            gerenciador.criptografar_e_salvar(log_entry, path_log)
            
            print(f"[SUCCESS] E-mail {msg['id']} processado e protegido em disco.")

    except Exception as e:
        # Log de erro genérico para não expor detalhes do sistema em produção
        print(f"[ERROR] Falha na sincronização segura: {type(e).__name__}")

if __name__ == "__main__":
    # Carrega o caminho do .env ou usa padrão seguro
    from dotenv import load_dotenv
    load_dotenv()
    PATH = os.getenv('CAMINHO_CONTEXTO', 'contexto_protegido.log')
    sincronizar_gmail_para_log(PATH)