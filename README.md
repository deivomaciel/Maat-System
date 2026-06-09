# Maat-System (MaatS)

<p align="center">
  <img width="1892" height="860" alt="image" src="https://github.com/user-attachments/assets/f0ce7467-bcf1-467b-a9f5-8e72d5cbb359" />
</p>

<!--
  📸 Para adicionar a capa:
  1. Tire um print da tela do projeto (ex: a Home ou o Dashboard).
  2. Salve a imagem numa pasta "docs/" na raiz do repositório, com o nome "cover.png".
     (Pode usar outro nome/formato — só ajuste o caminho acima, ex: docs/capa.jpg)
  3. Faça o commit da imagem junto com o README.
  Dica: dá pra arrastar a imagem direto na caixa de edição do README no GitHub —
  ele gera um link automático que você cola no lugar de "docs/cover.png".
-->

Sistema web para **coleta e medição de avaliações de serviços**. O usuário cria links de avaliação para o seu serviço, compartilha esses links com seus clientes e acompanha as métricas das respostas (ruim / bom / ótimo) em um painel.

🔗 **Aplicação online:** https://maat-system.vercel.app/

> Projeto acadêmico desenvolvido como exercício de construção de uma aplicação web completa, com autenticação, banco de dados e arquitetura em camadas.

---

## Funcionalidades

- Cadastro e login de usuários
- Criação de links de avaliação para um serviço
- Exclusão dos próprios links
- Visualização das métricas de cada link

Cada avaliação registra uma de três notas: **ruim**, **bom** ou **ótimo**.

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python |
| Framework web | FastAPI |
| Servidor ASGI | Uvicorn |
| Templates HTML | Jinja2 |
| ORM | Tortoise ORM |
| Banco de dados | PostgreSQL |
| Hash de senha | pwdlib (Argon2) |
| Validação | Pydantic + email-validator |
| Deploy | Vercel |

O front-end é renderizado no servidor com templates Jinja2 e arquivos estáticos (HTML/CSS).

---

## Estrutura do projeto

```
Maat-System/
├── Controller/      # Rotas e lógica de entrada (UserController, LinkController)
├── Model/           # Modelos do ORM (UserModel, LinkModel, RatingModel)
├── Repository/      # Acesso e persistência de dados
├── Schemas/         # Schemas Pydantic (validação de entrada/saída)
├── View/            # Templates Jinja2 (Home, Login, Register, Dashboard)
├── Static/          # Arquivos estáticos (CSS, imagens, etc.)
├── DB/              # Configuração do banco de dados
├── api/             # Ponto de entrada para deploy na Vercel
├── server.py        # Aplicação principal (FastAPI)
├── requirements.txt # Dependências do projeto
├── vercel.json      # Configuração de deploy
└── .env.example     # Exemplo de variáveis de ambiente
```

O projeto segue uma organização em camadas no estilo **MVC** (Model, View, Controller), com o `Repository` isolando o acesso aos dados.

---

## Como rodar localmente

### Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

### 1. Clone o repositório

```bash
git clone https://github.com/deivomaciel/Maat-System.git
cd Maat-System
```

### 2. Crie e ative um ambiente virtual

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Edite o `.env` e defina a `DATABASE_URL`. Você tem duas opções:

**Opção A — SQLite (mais simples para testar localmente):**
```env
DATABASE_URL=sqlite://db.sqlite3
```
Não exige instalar nenhum banco; o arquivo `db.sqlite3` é criado automaticamente.

**Opção B — PostgreSQL (igual ao ambiente de produção):**
```env
DATABASE_URL=postgres://usuario:senha@host/nome_do_banco
```

> As tabelas são criadas automaticamente na inicialização (`generate_schemas=True`), então não é necessário rodar migrações manualmente.

### 5. Inicie o servidor

```bash
uvicorn server:app --reload
```

A aplicação ficará disponível em **http://127.0.0.1:8000**.

---

## Rotas principais

| Rota | Descrição |
|---|---|
| `/` | Página inicial |
| `/register` | Cadastro de usuário |
| `/login` | Login |
| `/dashboard` | Painel com os links e métricas |

A documentação interativa da API (gerada automaticamente pelo FastAPI) fica em **http://127.0.0.1:8000/docs**.

---

## Autor

Desenvolvido por [@deivomaciel](https://github.com/deivomaciel).
