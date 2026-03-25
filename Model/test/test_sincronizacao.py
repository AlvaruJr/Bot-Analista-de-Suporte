import os
import pytest

from dotenv import load_dotenv


def test_env_vars_carregadas():
    """Verifica se as variáveis críticas de ambiente existem."""
    load_dotenv(override=True)
    assert os.getenv('API_KEY_IA202601') is not None
    assert os.getenv('OUTLOOK_CLIENT_ID') is not None

def test_diretorio_log_escrita():
    """Verifica se o caminho do contexto é gravável."""
    path = os.getenv('CAMINHO_CONTEXTO')
    try:
        with open(path, "a") as f:
            f.write("")
        assert True
    except Exception as e:
        pytest.fail(f"Não foi possível escrever no log: {e}")