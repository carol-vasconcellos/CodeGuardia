# CodeGuardia: Plataforma de Aprendizado Interativo (Django/Python)

O CodeGuardia é uma plataforma de aprendizado interativo focada em Python, desenvolvimento web e princípios de cibersegurança. O objetivo é fornecer uma trilha de conhecimento prática, permitindo que os usuários aprendam assistindo a vídeos e, crucialmente, executando código Python em um editor integrado.

A aplicação é construída com **Django** e está configurada para ser robusta e segura, utilizando boas práticas para implantação em produção (Render).

-----

## 2\. Funcionalidades Implementadas

Abaixo está um resumo das principais funcionalidades já entregues no projeto:

### 2.1. Autenticação e Usuário

  * **Fluxo Completo de Auth**: Implementação padrão e segura de Cadastro (`/signup`), Login (`/login`) e Logout.
  * **Recuperação de Senha**: Fluxo completo de redefinição de senha em 4 etapas (`PasswordResetView`, `Confirm`, `Done`), usando templates customizados e a configuração SMTP segura do Django (necessita variáveis de ambiente).

### 2.2. Core do Aprendizado (App `lessons`)

  * **Modelo Flexível de Lições**: Suporte a dois tipos principais de conteúdo: **Vídeo** (para aulas teóricas) e **Código** (para desafios práticos).
  * **Editor de Código Interativo**: Nas lições do tipo código, o usuário pode escrever e submeter código Python.
  * **Execução Controlada (MITIGADA)**: A função de execução de código foi **desativada** no servidor principal por segurança, e o usuário recebe feedback de que a lição foi salva.
  * **Validação**: A saída gerada era comparada com a **Saída Esperada** (função agora movida para um ambiente seguro/isolado no futuro).
  * **Controle de Progresso**: Uso do modelo `Progresso` no banco de dados para rastrear quais lições cada usuário concluiu, exibido no Painel do Aluno.

### 2.3. Configurações de Produção e Segurança

**[ESTA SEÇÃO FOI ATUALIZADA PARA REFLETIR AS MUDANÇAS DE DEVOSECOPS]**

  * **Render Deployment**: Configurado para implantação contínua na plataforma Render.
  * **Banco de Dados**: Uso de `dj-database-url` para suportar PostgreSQL em produção e SQLite localmente.
  * **Arquivos Estáticos**: Uso de **WhiteNoise** (`whitenoise.middleware.WhiteNoiseMiddleware`) para servir arquivos estáticos de forma eficiente e segura em produção.
  * **PROTEÇÃO CONTRA RCE (CRÍTICA):** A função `exec()` que rodava código do usuário no servidor foi **removida**. O servidor está agora protegido contra ataques de Execução de Código Remoto.
  * **Endurecimento da Conexão (HSTS):** Configurado para forçar o navegador a se conectar **APENAS via HTTPS** por um ano (`SECURE_HSTS_PRELOAD`), mitigando ataques de *downgrade*.
  * **Controle de Sessão e Senha:**
      * **Tempo Limite de Inatividade:** Sessões são encerradas automaticamente após **10 minutos** de inatividade (`SESSION_COOKIE_AGE = 600`), prevenindo sequestro de sessão.
      * **Força da Senha:** O Django agora exige um **mínimo de 12 caracteres** nas senhas.
  * **Segurança de Configuração:** A `SECRET_KEY` foi removida do código-fonte, garantindo que o deploy **falhe** se a chave não for definida de forma segura via variável de ambiente.
  * **Headers de Segurança:** Ativação de headers de segurança (`SECURE_PROXY_SSL_HEADER`, `SECURE_SSL_REDIRECT`) e segurança de cookies (`CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`, `SECURE_CONTENT_TYPE_NOSNIFF`).

-----

## 3\. Configuração e Instalação (Para Iniciantes)

Siga este guia para colocar o projeto rodando em seu ambiente local.

### 3.1. Pré-requisitos

  * **Python**: Versão 3.8 ou superior.
  * **Git**: Para clonar o repositório.

### 3.2. Passos de Instalação

1.  **Clone o Repositório e Navegue até a Pasta:**

    ```bash
    git clone [[https://github.com/seu-usuario/CodeGuardia.git](https://github.com/seu-usuario/CodeGuardia.git)] # Substitua pelo URL real
    cd CodeGuardia
    ```

2.  **Crie e Ative o Ambiente Virtual (`venv`):**
    É uma boa prática isolar as dependências do projeto.

    ```bash
    python -m venv venv
    # No Linux/macOS:
    source venv/bin/activate
    # No Windows (PowerShell):
    .\venv\Scripts\Activate
    ```

3.  **Instale as Dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Crie o Arquivo de Variáveis de Ambiente (`.env`):**
    Na raiz do projeto (onde está o `manage.py`), crie um arquivo chamado **`.env`** e preencha-o. Este arquivo é crucial para a segurança\!

    ```ini
    # --- Configurações Essenciais ---
    SECRET_KEY='sua-chave-secreta-aleatoria-aqui' # Mude a chave a cada novo deploy!

    # Banco de Dados Local (SQLite)
    DATABASE_URL='sqlite:///db.sqlite3'

    # --- Configurações de E-mail (Para testar o Reset de Senha) ---
    # Opção 1 (Recomendada para dev local): Imprime o link de reset no terminal
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend' 

    # Opção 2 (Para testar envio real - NÃO USE CREDENCIAIS REAIS AQUI):
    # EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend' 
    # EMAIL_HOST='smtp.exemplo.com' 
    # EMAIL_PORT=587 
    # EMAIL_HOST_USER='seu_email@exemplo.com'
    # EMAIL_HOST_PASSWORD='senha_ou_token_de_app'
    # DEFAULT_FROM_EMAIL='no-reply@codeguardia.com'
    ```

5.  **Aplique as Migrações:**
    Crie as tabelas no banco de dados local.

    ```bash
    python manage.py migrate
    ```

6.  **Crie um Superusuário (Admin):**
    Isso é necessário para cadastrar as lições antes de testar.

    ```bash
    python manage.py createsuperuser
    ```

7.  **Execute o Servidor Local:**

    ```bash
    python manage.py runserver
    ```

    Acesse a aplicação em [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

-----

## 4\. Guia de Testes Manuais

Para garantir que todas as funcionalidades estejam operando corretamente, siga estes testes:

### Teste 1: Configuração Inicial e Conteúdo

1.  Acesse o Painel Admin em [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).
2.  Navegue até **Lições (Lessons)** e clique em **Adicionar Lição**.
3.  Crie pelo menos três lições:
      * **Lição 1 (Vídeo)**: Tipo **Vídeo de Conteúdo**. Preencha Título, Ordem e URL do Vídeo.
      * **Lição 2 (Código - Simulação de Sucesso)**: Tipo **Desafio de Código**. Preencha Título, Ordem, Conselho, Código Padrão e Esperado (ambos não serão executados no servidor, mas são necessários para o modelo).
      * **Lição 3 (Código - Simulação de Erro)**: Tipo **Desafio de Código**. Preencha Título, Ordem, etc.

### Teste 2: Fluxo do Usuário

1.  Acesse [http://127.0.0.1:8000/signup/](http://127.0.0.1:8000/signup/) e crie um novo usuário. A senha deve ter no mínimo **12 caracteres**.
2.  Após o cadastro, verifique se você é redirecionado para o Painel do Aluno (`/bem-vindo/`).
3.  Clique em "Acessar Todas as Lições".

### Teste 3: Execução de Lições e Progresso

  * **Teste de Lição de Vídeo:**
      * Acesse a Lição 1.
      * Clique em "Marcar como concluída".
      * Volte ao Painel. O progresso deve ter aumentado e a lição deve estar como **CONCLUÍDA**.
      * Clique em "Refazer Lição" e verifique se o status volta para **PENDENTE**.
  * **Teste de Lição de Código (Simulação de Conclusão Segura):**
      * Acesse a Lição 2.
      * Mantenha o código no editor e clique em "Rodar Código e Testar".
      * **Resultado Esperado:** O Modal de Sucesso deve aparecer, e o Console Output deve exibir a **mensagem de segurança** informando que o teste foi desativado no servidor, mas a lição foi marcada como concluída.
  * **Teste de Session Timeout:**
      * Logado, **fique inativo (sem clicar ou navegar)** por mais de 10 minutos.
      * Após o tempo, tente clicar em qualquer link (ex: Painel do Aluno).
      * **Resultado Esperado:** Você deve ser redirecionado automaticamente para a página de Login.

### Teste 4: Recuperação de Senha

1.  Na tela de Login, clique em "Esqueceu sua senha?".
2.  Digite o e-mail do usuário criado no Teste 2.
3.  A tela de **Instruções Enviadas** deve aparecer.
4.  O link de redefinição de senha aparecerá no seu terminal (console) onde o servidor Django está rodando.
5.  Copie o link (`/reset/<uidb64>/<token>/`) e cole no navegador.
6.  Defina a nova senha, que deve ter no mínimo **12 caracteres**. A tela de **"Senha Redefinida com Sucesso"** deve aparecer.
7.  Use a nova senha para logar.

-----

## 5\. Implementações de Segurança DevSecOps (Próximos Passos)

Continuamos aprimorando o CodeGuardia para ser um modelo de aplicação web segura por padrão. As próximas implementações têm alto impacto na proteção do sistema.

### 5.1. Missão Crítica: Isolamento de Código (Sandboxing)

O ponto de maior risco de segurança (`exec()`) foi removido, mas a funcionalidade de execução precisa retornar de forma segura.

  * **A Implementar**: Refatorar a execução de código para usar um ambiente isolado (sandboxing).
  * **Como**: Investigar e implementar soluções baseadas em **Docker** ou em **WebAssembly (WASM)**, que executam o código em um contêiner separado ou em uma máquina virtual leve, isolando-o completamente do servidor Django e dos recursos do sistema operacional.

### 5.2. Defesa contra Força Bruta (Rate Limiting)

Para proteger as rotas de autenticação contra tentativas incessantes de ataques de dicionário ou de força bruta.

  * **A Implementar**: Adicionar a biblioteca `django-ratelimit` e configurar limites de taxa específicos.
  * **Onde**:
      * **Login** (`/login/`): Permitir, por exemplo, 5 tentativas por minuto por IP.
      * **Recuperação de Senha** (`/password_reset/`): Limitar o número de e-mails de redefinição enviados por IP e por e-mail.

### 5.3. Endurecimento de Headers Adicionais (CSP)

Garantir que os navegadores sigam rigorosas políticas de segurança ao interagir com o site.

  * **A Implementar**: Configurar o Content Security Policy (CSP) usando `django-csp` para definir fontes confiáveis para scripts e estilos, mitigando ataques de Cross-Site Scripting (XSS).

### 5.4. Segurança Automatizada (Shift-Left com Bandit)

Integrar a segurança no fluxo de trabalho do desenvolvedor (o conceito de "shift left" do DevSecOps).

  * **A Implementar**: Adicionar a ferramenta de SAST (Static Application Security Testing), como o **Bandit**, ao ambiente de desenvolvimento e aos hooks de pré-commit do Git, para escanear código Python automaticamente em busca de vulnerabilidades.

-----

## Domínio em Produção

Você pode acessar a versão mais recente da aplicação aqui:

🔗 **URL**: [https://codeguardia.onrender.com](https://codeguardia.onrender.com)
