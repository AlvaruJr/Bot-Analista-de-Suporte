import os
from google import genai
from google.genai import types

class BotConectaRS:
    def __init__(self, api_key, caminho_contexto):
        # Inicializa o cliente oficial do Gemini 2.5
        self.client = genai.Client(api_key=api_key)
        self.caminho_contexto = caminho_contexto
        self.contexto_texto = self._carregar_contexto()

    def _carregar_contexto(self):
        """Busca as informações no seu log.txt.txt"""
        try:
            if os.path.exists(self.caminho_contexto):
                with open(self.caminho_contexto, 'r', encoding='utf-8') as f:
                    return f.read()
            return "Aviso: Base de conhecimento (log) não localizada."
        except Exception as e:
            return f"Erro ao ler banco de dados: {e}"

    def responder(self, mensagem_usuario, imagem=None):
        """Lógica de resposta para Suporte e Inventário"""
        
        # O 'Prompt de Sistema' que define as regras do projeto Claro/Seduc
        instrucao_sistema = f"""
        Você é o Especialista de Ativação do Projeto Conecta RS.
        Analista Responsável: AlvaruJr.

        BASE DE CONHECIMENTO:
        {self.contexto_texto}

        REGRAS DE OURO:
        1. Se receber foto de etiqueta: Extraia MAC;Serial;Nome.
        2. Regra 55AXE: Equipamentos 55AXE devem ser nomeados como 'AP Outdoor XX'.
        3. Formatação: Responda apenas em texto puro. Proibido usar asteriscos (*), negritos ou tabelas.
        """

        conteudo = [mensagem_usuario]
        if imagem:
            conteudo.append(imagem)

        config = types.GenerateContentConfig(
            system_instruction=instrucao_sistema,
            temperature=0  # Mantém a resposta técnica e precisa
        )

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=conteudo,
                config=config
            )
            return response.text
        except Exception as e:
            return f"Erro técnico na IA: {e}"