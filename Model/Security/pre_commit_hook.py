import sys
import subprocess

def check_security():
    # Lista de arquivos sensíveis que NUNCA devem entrar no Git
    forbidden_files = [".env", "config.json", "credentials.json"]
    
    # Execução segura do comando git (sem shell=True)
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True, 
            text=True, 
            check=True
        )
        staging_files = result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao verificar arquivos no Git: {e}")
        sys.exit(1)

    found_danger = False
    
    for file in staging_files:
        # Bloqueio total de arquivos de ambiente
        if any(forbidden in file for forbidden in forbidden_files):
            print(f"❌ ERRO: O arquivo sensível '{file}' foi detectado no staging!")
            found_danger = True
        
        # Verificação de conteúdo em arquivos Python
        if file.endswith(".py"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Padrões comuns de chaves (Gemini, AWS, etc)
                    if "AIzaSy" in content or "client_secret" in content:
                        print(f"⚠️ AVISO: Possível credencial exposta em '{file}'!")
                        found_danger = True
            except FileNotFoundError:
                continue

    if found_danger:
        print("\nCommit abortado. Remova os dados sensíveis ou use o .gitignore.")
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    check_security()