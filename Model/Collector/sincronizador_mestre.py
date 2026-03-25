import streamlit as st
from Model.Collector.sincronizar_gmail import sincronizar_gmail_para_log
from Model.Collector.sincronizar_outlook import sincronizar_outlook_para_log

def sincronizacao_total(path_log):
    """
    Executa a colheita de dados em ambas as plataformas.
    Retorna um dicionário com o status de cada operação.
    """
    status = {"gmail": False, "outlook": False}
    
    print(f"\n[SINC] Iniciando varredura total em: {path_log}")

    # 1. Tenta extrair dados do Gmail
    try:
        sincronizar_gmail_para_log(path_log)
        status["gmail"] = True
        print("[SINC] Gmail: Sucesso")
    except Exception as e:
        print(f"[SINC] Gmail: Falha -> {e}")

    # 2. Tenta extrair dados do Outlook
    try:
        sincronizar_outlook_para_log(path_log)
        status["outlook"] = True
        print("[SINC] Outlook: Sucesso")
    except Exception as e:
        print(f"[SINC] Outlook: Falha -> {e}")
        
    return status