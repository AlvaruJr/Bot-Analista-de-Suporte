import os
from google import genai
from google.genai import types

class BotConectaRS:
    def __init__(self, api_key, caminho_contexto):
        self.client = genai.Client(api_key=api_key)
        self.caminho_contexto = caminho_contexto
        self.contexto_texto = self._carregar_contexto()

    def _carregar_contexto(self):
        try:
            if os.path.exists(self.caminho_contexto):
                with open(self.caminho_contexto, 'r', encoding='utf-8') as f:
                    return f.read()
            return "Base de conhecimento não encontrada."
        except Exception as e:
            return f"Erro ao carregar log: {e}"

    def responder(self, mensagem_usuario, imagem=None):
        instrucao = f"""
        Você é o Especialista de Ativação do Projeto Conecta RS.
        Analista responsável: AlvaruJr.
        Base de dados: {self.contexto_texto}

        REGRAS:
        1. Imagens: Extraia MAC;Serial;Nome.
        2. Regra 55AXE: Nomear como 'AP Outdoor XX'.
        3. Texto puro, sem asteriscos ou negrito.
        4 ."mac": "70:49:A2:06:52:A1",
      "sn": "S242L26003598",
      "name": "Switch"
        """
        
        conteudo = [mensagem_usuario]
        if imagem:
            conteudo.append(imagem)

        config = types.GenerateContentConfig(system_instruction=instrucao, temperature=0)

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=conteudo,
                config=config
            )
            return response.text
        except Exception as e:
            return f"Erro: {e}"