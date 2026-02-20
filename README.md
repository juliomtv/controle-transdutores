# Aplicação Web de Controle de Transdutores (Flask/Python)

Esta é uma aplicação web simples desenvolvida em Python com o framework Flask para o controle de validade de transdutores, conforme solicitado.

## Funcionalidades

1.  **Cadastro de Transdutores:** Com campos para Descrição, Data de Validade (Mês/Ano), Número de Série (Opcional) e Localização/Célula (Opcional).
2.  **Visualização:** Lista todos os transdutores, calcula os dias restantes para o vencimento e exibe o status (OK, Atenção, VENCIDO).
3.  **Estilização:** Utiliza as cores da TechnipFMC (Roxo e Vermelho) para o design.
4.  **Notificação por E-mail:** Possui uma função para verificar e enviar e-mails de alerta quando um transdutor estiver a **10 ou 5 dias** do vencimento.

## Estrutura do Projeto

```
transducer_app/
├── app.py              # Aplicação principal Flask (rotas, lógica de validade)
├── email_sender.py     # Módulo para envio de e-mails
├── data.csv            # Arquivo de armazenamento dos dados dos transdutores
├── requirements.txt    # Dependências do Python
├── .env                # Arquivo de configuração de variáveis de ambiente (E-mail)
├── templates/
│   ├── index.html      # Template da página de visualização
│   └── register.html   # Template da página de cadastro
└── static/
    └── css/
        └── style.css   # Estilos CSS com as cores da TechnipFMC
```

## Como Rodar Localmente

Siga os passos abaixo para configurar e rodar a aplicação em seu ambiente local.

### 1. Pré-requisitos

Você precisa ter o **Python 3** instalado em seu sistema.

### 2. Instalação das Dependências

Navegue até o diretório `transducer_app` e instale as bibliotecas necessárias:

```bash
# Navegue até o diretório do projeto
cd transducer_app

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configuração do E-mail

A funcionalidade de envio de e-mail requer a configuração de um servidor SMTP.

1.  **Edite o arquivo `.env`:**
    *   Substitua `SUA_CHAVE_SECRETA_AQUI` por uma chave aleatória.
    *   Preencha `SMTP_SERVER` e `SMTP_PORT` (o padrão `smtp.gmail.com` e `587` funciona para Gmail).
    *   Preencha `EMAIL_USER` com o e-mail remetente (`julio.marcostavaresviana@technipfmc.com`).
    *   **IMPORTANTE:** Preencha `EMAIL_PASSWORD` com uma **Senha de Aplicativo** (App Password) gerada pelo seu provedor de e-mail, e **NUNCA** com a sua senha principal.
    *   Preencha `RECIPIENTS` com a lista de e-mails que devem receber as notificações, separados por vírgula.

2.  **Atualize o `app.py`:**
    Para que o arquivo `.env` seja lido, você precisa adicionar as seguintes linhas no topo do seu `app.py`:

    ```python
    from dotenv import load_dotenv
    load_dotenv()
    ```
    *(Eu não adicionei isso no código final para evitar uma dependência extra, mas é a forma mais segura de gerenciar as variáveis de ambiente localmente. Se preferir, você pode exportar as variáveis diretamente no terminal antes de rodar o app).*

### 4. Execução da Aplicação

Execute o arquivo `app.py` no terminal:

```bash
python app.py
```

A aplicação estará disponível em: `http://127.0.0.1:5000/`

### 5. Checagem de Notificações

Para verificar se há transdutores próximos do vencimento e enviar o e-mail de notificação, acesse a rota:

`http://127.0.0.1:5000/check_notifications`

**Nota:** Esta rota deve ser executada manualmente ou pode ser configurada para rodar automaticamente (por exemplo, usando um *cron job* no seu sistema operacional) para que as notificações sejam enviadas no momento certo.
