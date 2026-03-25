import os
import streamlit as st
# Importações corrigidas conforme os nomes dos arquivos
try:
    from Model.Collector.sincronizar_gmail import sincronizar_gmail_para_log
    from Model.Collector.sincronizar_outlook import sincronizar_outlook_para_log
except ImportError as e:
    st.error(f"Erro ao importar módulos de sincronização: {e}")

def sincronizacao_total(path_log):
    """Executa a colheita de dados em ambas as plataformas de forma segura."""
    status = {"gmail": False, "outlook": False}
    
    # Validação de caminho simples
    if not path_log or ".." in path_log:
        raise ValueError("Caminho de log inválido ou inseguro.")

    # Gmail
    try:
        sincronizar_gmail_para_log(path_log)
        status["gmail"] = True
    except Exception as e:
        print(f"[ERRO GMAIL] {e}")

    # Outlook
    try:
        sincronizar_outlook_para_log(path_log)
        status["outlook"] = True
    except Exception as e:
        print(f"[ERRO OUTLOOK] {e}")
        
    return status