import sys
import os

def check_env_files():
    # Lista de arquivos que NUNCA devem ser commitados
    forbidden_files = [".env", "config.json", "credentials.json"]
    
    # Simula uma verificação simples no diretório (ou via git status)
    # No hook real, o Git passa a lista de arquivos alterados
    staging_files = os.popen('git diff --cached --name-only').read().splitlines()
    
    found_danger = False
    for file in staging_files:
        if file in forbidden_files:
            print(f"❌ ERRO DE SEGURANÇA: O arquivo '{file}' não pode ser enviado ao repositório!")
            found_danger = True
        
        # Opcional: Verifica se há chaves de API expostas em arquivos .py
        if file.endswith(".py"):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "AIzaSy" in content: # Padrão de chave Google Gemini
                    print(f"⚠️ AVISO: Detectada possível chave de API no arquivo '{file}'!")
                    found_danger = True

    if found_danger:
        print("\nCommit abortado. Remova os arquivos sensíveis ou use .gitignore.")
        sys.exit(1) # Retorno 1 interrompe o commit
    sys.exit(0)

if __name__ == "__main__":
    check_env_files()