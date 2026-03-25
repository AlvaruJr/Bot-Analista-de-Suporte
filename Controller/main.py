import streamlit as st
import os
import PIL.Image
from dotenv import load_dotenv
from Controller.BotConectaRS import BotConectaRS

# 1. Configurações Iniciais e Segurança
load_dotenv(override=True)
KEY = os.getenv('API_KEY_IA202601')
PATH = os.getenv('CAMINHO_CONTEXTO')

st.set_page_config(page_title="Bot Conecta RS", layout="centered", page_icon="🌐")

# 2. Inicialização Segura por Sessão (Isolamento de Usuários)
if "bot" not in st.session_state:
    try:
        # Cada aba de navegador aberta terá sua própria instância
        st.session_state.bot = BotConectaRS(KEY, PATH)
        st.session_state.messages = []
    except Exception as e:
        st.error("Erro crítico na inicialização do Analista.")

# 3. Sidebar e Upload
with st.sidebar:
    st.header("⚙️ Painel")
    foto = st.file_uploader("Etiqueta Zyxel", type=['png', 'jpg', 'jpeg'])
    
    # Limitação de tamanho de imagem (Segurança básica)
    if foto and foto.size > 5 * 1024 * 1024:
        st.error("Imagem muito grande! Máximo 5MB.")
        foto = None

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 4. Chat Interface
st.title("🌐 Especialista Conecta RS")

# Exibir histórico da sessão atual
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Como posso ajudar?"):
    # Adiciona pergunta ao estado
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando Nebula..."):
            try:
                img_input = PIL.Image.open(foto) if foto else None
                
                # Passamos o histórico para a classe decidir o comportamento
                resposta = st.session_state.bot.responder(
                    pergunta=prompt, 
                    historico=st.session_state.messages, 
                   imagem=img_input
                )
                
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error(f"Erro no processamento: {e}")