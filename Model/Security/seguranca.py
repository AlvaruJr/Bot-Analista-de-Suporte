import os
import re
import html
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

class GerenciadorDados:
    def __init__(self):
        self.chave = os.getenv('CHAVE_CRIPTOGRAFIA_LOG')
        if not self.chave:
            raise ValueError("CHAVE_CRIPTOGRAFIA_LOG crítica não encontrada no .env")
        self.cipher_suite = Fernet(self.chave.encode())

    def sanitizar_saida_ui(self, texto):
        """Impede RFI/SSRF e XSS na interface Streamlit."""
        if not texto: return ""
        # Escapa HTML para evitar scripts injetados
        texto_seguro = html.escape(texto)
        # Remove links de imagem Markdown maliciosos ![alt](url)
        texto_seguro = re.sub(r'!\[.*?\]\(.*?\)', '[CONTEÚDO_BLOQUEADO_POR_SEGURANCA]', texto_seguro)
        return texto_seguro

    def sanitizar_entrada_log(self, texto):
        """Remove PII e caracteres de injeção antes de salvar no log."""
        # Remove CPFs e E-mails
        texto = re.sub(r'\d{3}\.\d{3}\.\d{3}-\d{2}', '[CPF_REMOVIDO]', texto)
        texto = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL_REMOVIDO]', texto)
        # Remove tentativas de escape de shell/SQL
        texto = re.sub(r'[;\\|`]', '', texto)
        return texto

    def criptografar_e_salvar(self, texto, caminho_arquivo):
        """Criptografa e anexa ao log em modo binário."""
        limpo = self.sanitizar_entrada_log(texto)
        texto_cifrado = self.cipher_suite.encrypt(limpo.encode())
        with open(caminho_arquivo, "ab") as f:
            f.write(texto_cifrado + b"\n")

    def ler_e_descriptografar(self, caminho_arquivo):
        """Lê do disco e decifra apenas em memória (RAM)."""
        if not os.path.exists(caminho_arquivo): return "Aviso: Base de dados vazia."
        linhas = []
        with open(caminho_arquivo, "rb") as f:
            for linha in f:
                if linha.strip():
                    try:
                        dec = self.cipher_suite.decrypt(linha.strip())
                        linhas.append(dec.decode())
                    except: continue
        return "\n".join(linhas)