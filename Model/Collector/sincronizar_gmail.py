import os
import base64
from googleapiclient.discovery import build
from Model.Security.seguranca import GerenciadorDados
from google.oauth2.credentials import Credentials

def sincronizar_gmail_para_log(path_log):
    try:
        # Assume-se que o token.json já existe via OAuth flow
        creds = Credentials.from_authorized_user_file('token.json')
        service = build('gmail', 'v1', credentials=creds)
        gerenciador = GerenciadorDados()

        # Busca e-mails de ativação
        query = "subject:Ativação"
        results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
        messages = results.get('messages', [])

        for msg in messages:
            m_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            # Pega o snippet (resumo) ou body
            conteudo = m_data.get('snippet', '')
            
            log_entry = f"ID: {msg['id']} | DADO: {conteudo}"
            # Salva usando a camada de segurança (Sanitiza + Criptografa)
            gerenciador.criptografar_e_salvar(log_entry, path_log)
            
        return True
    except Exception as e:
        print(f"Erro sincronização: {e}")
        return False