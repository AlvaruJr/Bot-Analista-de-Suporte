import streamlit as st
import os
import PIL.Image
from dotenv import load_dotenv
from especialista import BotConectaRS

# Configuração e Carregamento
load_dotenv(override=True)
KEY = os.getenv('API_KEY_IA202601')
PATH = os.getenv('CAMINHO_CONTEXTO')

st.set_page_config(page_title="Bot Conecta RS v2.5", page_icon="🌐")

# Estilo Visual (Vermelho Claro)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1 { color: #ee2e24; font-family: 'Arial Black'; }
    .stButton>button { background-color: #ee2e24; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 Especialista Conecta RS")
st.write("Analista: **AlvaruJr**")

# Inicializar o Bot
if "bot" not in st.session_state:
    st.session_state.bot = BotConectaRS(KEY, PATH)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar para Inventário
with st.sidebar:
    st.header("📸 Inventário")
    foto = st.file_uploader("Upload de Etiqueta", type=['png', 'jpg', 'jpeg'])
    if foto:
        st.image(foto, caption="Etiqueta carregada")
    
    if st.button("Limpar Chat"):
        st.session_state.messages = []
        st.rerun()

# Exibir Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de Mensagem
if prompt := st.chat_input("Dúvida sobre ativação ou inventário?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        img_input = PIL.Image.open(foto) if foto else None
        resposta = st.session_state.bot.responder(prompt, img_input)
        st.markdown(resposta)
        st.session_state.messages.append({"role": "assistant", "content": resposta})