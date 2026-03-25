🌐 Especialista Conecta RS v2.6
O Especialista Conecta RS é uma solução de Inteligência Artificial baseada em Agentes (IA Generativa) projetada para auxiliar analistas de suporte na ativação de infraestrutura de rede para o projeto Claro/SEDUC. O sistema utiliza a arquitetura MVC (Model-View-Controller) e implementa rigorosas camadas de segurança cibernética (Pentest-Ready).

🚀 Funcionalidades Principais
🤖 IA Especialista: Processamento de linguagem natural via Google Gemini 2.5 Flash para suporte técnico em ativações.

📧 Sincronização Multicanal: "Colheita" automática de e-mails de ativação de contas Gmail e Outlook (Nexxt Digital).

📸 Visão Computacional: Leitura automática de etiquetas Zyxel para extração de MAC e Serial.

🔐 Segurança de Dados: Criptografia AES-128 (Fernet) para armazenamento de logs e sanitização de dados sensíveis (PII).

🛡️ Resiliência a Ataques: Proteção nativa contra Prompt Injection, Path Traversal e Remote File Inclusion (RFI).

🏗️ Arquitetura do Sistema (MVC)
O projeto está organizado para garantir manutenibilidade e escalabilidade:

View/: Interface de usuário desenvolvida em Streamlit. Cuida da apresentação e sanitização de saída visual.

Controller/: O "Cérebro" do bot (BotController). Orquestra a lógica entre a IA, o contexto de rede e o usuário.

Model/:

Collector/: Módulos de integração com Graph API (Outlook) e Gmail API.

Security/: Motor de criptografia, sanitização de logs e gerenciamento de chaves.

test/: Bateria de testes automatizados com Pytest para validação de segurança e lógica.

🛠️ Configuração e Instalação
1. Pré-requisitos
Python 3.10 ou superior.

Ambiente Virtual (venv).

2. Instalação
PowerShell
# Clonar o repositório
git clone https://github.com/AlvaruJr/Bot-Analista-de-Suporte.git

# Instalar dependências
pip install -r requirements.txt
3. Variáveis de Ambiente (.env)
Crie um arquivo .env na raiz com as seguintes chaves:

Bash
API_KEY_IA202601=Sua_Chave_Gemini
CHAVE_CRIPTOGRAFIA_LOG=Sua_Chave_Fernet_Gerada
CAMINHO_CONTEXTO="contexto/log.txt"
OUTLOOK_CLIENT_ID=Seu_ID_Azure
OUTLOOK_TENANT_ID=Seu_ID_Locatario
OUTLOOK_CLIENT_SECRET=Sua_Secret_Azure
🧪 Qualidade e Segurança
O projeto utiliza Test-Driven Development (TDD) para garantir que as travas de segurança nunca sejam quebradas durante atualizações.

Para rodar a bateria de testes de Pentest:

PowerShell
$env:PYTHONPATH = "."
python -m pytest Model/test/
Nota de Segurança: O sistema foi validado contra injeção de prompt, garantindo que as regras de negócio (MAC;Serial;Nome) sejam mantidas em 100% das interações.

👨‍💻 Autor
Alvaro Carvalho (AlvaruJr) Analista de Suporte N1 - Nexxt Digital

Estudante de ADS - Fatec
