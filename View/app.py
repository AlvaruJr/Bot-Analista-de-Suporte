import streamlit as st
import os
import PIL.Image
from dotenv import load_dotenv

# Imports seguindo a estrutura MVC
from Controller.BotConectaRS import BotController
from Model.Security.seguranca import GerenciadorDados
from Model.Collector.sincronizacao import sincronizacao_total

# Inicialização Dinâmica do Ambiente
base_path = os.path.dirname(os.path.dirname(__file__)) # Sobe uma pasta (Raiz)
dotenv_path = os.path.join(base_path, '.env')
load_dotenv(dotenv_path, override=True)

KEY = os.getenv('API_KEY_IA202601')
PATH = os.path.join(base_path, os.getenv('CAMINHO_CONTEXTO', '')) # Garante o caminho relativo correto

st.set_page_config(page_title="Bot Conecta RS v2.6", layout="centered", page_icon="🌐")

# CSS Customizado
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1 { color: #ee2e24; font-family: 'Arial Black'; }
    .stButton>button { background-color: #ee2e24; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização do Bot na Sessão
if "bot" not in st.session_state:
    try:
        st.session_state.bot = BotController(KEY, PATH)
        st.session_state.messages = []
    except Exception as e:
        st.error(f"Erro na inicialização: {e}")

# Interface
st.title("🌐 Especialista Conecta ")
st.write("Analista de Suporte: **AlvaruJr**")

with st.sidebar:
    st.header("⚙️ Painel de Controle")
    
    # Sincronização
    if st.button("🔄 Sincronizar Tudo (Gmail/Outlook)"):
        with st.spinner("Atualizando base de dados..."):
            sincronizacao_total(PATH)
            st.session_state.bot = BotController(KEY, PATH) # Recarrega contexto
            st.toast("Base de dados atualizada!")

    st.divider()
    
    # Inventário
    foto = st.file_uploader("Etiqueta Zyxel", type=['png', 'jpg', 'jpeg'])
    if foto and foto.size > 5 * 1024 * 1024:
        st.error("Imagem muito grande (Máx 5MB).")
        foto = None
    if foto:
        st.image(foto, caption="Etiqueta carregada", use_container_width=True)

# Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(set.sanitizar_saida_ui(message["content"]))

if prompt := st.chat_input("Como posso ajudar hoje?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(set.sanitizar_saida_ui(prompt))

    with st.chat_message("assistant"):
        with st.spinner("Analisando..."):
            img_input = PIL.Image.open(foto) if foto else None
            # Resposta via Controller
            resposta = st.session_state.bot.responder(prompt, st.session_state.messages, img_input)
            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})