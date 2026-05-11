# 🎉 Lisbon Events Chatbot

Um chatbot conversacional que recomenda eventos locais em Lisboa, especialmente para estudantes.

**Stack:** Python · FastAPI · Agno AgentOS · SQLite · Ticketmaster API

---

## 📋 Pré-requisitos

Antes de começar, garante que tens instalado:

- **Python 3.11 ou superior** → [python.org/downloads](https://python.org/downloads)
- **Git** (opcional) → [git-scm.com](https://git-scm.com)

Para verificar se tens Python, abre o terminal e escreve:
```bash
python --version
```

---

## 🚀 Guia Passo-a-Passo

### Passo 1 – Descarregar o projecto

```bash
# Opção A: com Git
git clone https://github.com/teu-usuario/lisbon-events-chatbot.git
cd lisbon-events-chatbot

# Opção B: sem Git – descarrega o ZIP e abre a pasta no terminal
cd lisbon-events-chatbot
```

---

### Passo 2 – Criar um ambiente virtual

Um ambiente virtual é uma "caixa de areia" isolada para instalar bibliotecas sem baralhar o teu Python global.

```bash
# Criar o ambiente
python -m venv venv

# Activar (Mac/Linux)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate
```

> 💡 Quando o ambiente está activo, vês `(venv)` no início da linha do terminal.

---

### Passo 3 – Instalar as bibliotecas

```bash
pip install -r requirements.txt
```

O que é instalado:
| Biblioteca | Para quê |
|---|---|
| `fastapi` | Framework para criar a API |
| `uvicorn` | Servidor web que corre o FastAPI |
| `sqlalchemy` | Comunicar com a base de dados |
| `agno` | Framework do agente de IA |
| `anthropic` | SDK do Claude (o cérebro do chatbot) |
| `requests` | Fazer pedidos HTTP (para o Ticketmaster) |
| `python-dotenv` | Ler o ficheiro `.env` |

---

### Passo 4 – Configurar as chaves de API

#### 4a. Copiar o ficheiro de configuração

```bash
cp .env.example .env
```

#### 4b. Obter a chave da Anthropic (OBRIGATÓRIO)

1. Vai a [console.anthropic.com](https://console.anthropic.com)
2. Regista-te (é grátis para começar)
3. Clica em **API Keys** → **Create Key**
4. Copia a chave e cola no `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-api03-...
```

#### 4c. Obter a chave do Ticketmaster (OPCIONAL)

Serve para importar eventos reais de Lisboa. Sem ela, o chatbot funciona com dados de exemplo.

1. Vai a [developer.ticketmaster.com](https://developer.ticketmaster.com)
2. Clica em **Sign In** → **Register**
3. Vai a **My Apps** → **Create New App**
4. Copia a **Consumer Key** e cola no `.env`:

```env
TICKETMASTER_API_KEY=abc123...
```

---

### Passo 5 – Popular a base de dados com eventos

#### Opção A: Dados de exemplo (sem API key)

```bash
python etl/seed.py
```

Isto cria automaticamente o ficheiro `events.db` e insere 12 eventos fictícios de Lisboa.

#### Opção B: Eventos reais do Ticketmaster

```bash
python etl/ticketmaster.py
```

*(Precisa de TICKETMASTER_API_KEY no `.env`)*

---

### Passo 6 – Arrancar o servidor

```bash
uvicorn main:app --reload
```

O `--reload` faz com que o servidor reinicie automaticamente quando alteras o código.

Deves ver algo como:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ Agno Playground activo em http://localhost:8000/playground
```

---

### Passo 7 – Usar o chatbot!

Tens 3 formas de interagir:

#### 🤖 Interface de Chat (Agno Playground)
Abre no browser: **http://localhost:8000/playground**

Experimenta perguntar:
- *"Há alguma festa esta noite?"*
- *"Eventos de networking grátis esta semana?"*
- *"Algo barato para estudantes?"*

#### 📖 Documentação interactiva da API
Abre no browser: **http://localhost:8000/docs**

Aqui podes testar todos os endpoints da REST API visualmente.

#### 🔧 API directamente (via terminal)
```bash
# Listar todos os eventos
curl http://localhost:8000/api/events

# Filtrar por categoria
curl "http://localhost:8000/api/events?category=party&price=free"

# Correr seed via API
curl -X POST http://localhost:8000/api/etl/seed
```

---

## 📁 Estrutura do Projecto

```
lisbon-events-chatbot/
│
├── main.py                  # Ponto de entrada – FastAPI + Agno
│
├── database/
│   ├── models.py            # Modelo de dados (tabela de eventos)
│   └── database.py          # Ligação à base de dados SQLite
│
├── etl/
│   ├── seed.py              # Dados de exemplo para testar
│   └── ticketmaster.py      # ETL real da API do Ticketmaster
│
├── agent/
│   └── events_agent.py      # Agente Agno + ferramenta search_events
│
├── api/
│   └── routes.py            # Endpoints REST da API
│
├── logs/
│   └── agent.log            # Log das conversas e chamadas ao agente
│
├── events.db                # Base de dados SQLite (criada automaticamente)
├── requirements.txt         # Bibliotecas necessárias
└── .env                     # As tuas chaves de API (NÃO partilhes!)
```

---

## 🔍 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Página inicial com links |
| `GET` | `/api/events` | Lista eventos (com filtros opcionais) |
| `GET` | `/api/events/{id}` | Detalhes de um evento |
| `POST` | `/api/etl/seed` | Insere dados de exemplo |
| `POST` | `/api/etl/ticketmaster` | Importa eventos do Ticketmaster |
| `GET` | `/playground` | Interface de chat do Agno |
| `GET` | `/docs` | Documentação interactiva |

### Filtros disponíveis para `/api/events`:

| Parâmetro | Valores possíveis |
|-----------|-------------------|
| `category` | `party`, `networking`, `academic`, `casual` |
| `price` | `free`, `cheap`, `paid` |
| `audience` | `student`, `general` |
| `limit` | número inteiro (padrão: 20) |

---

## 🐛 Problemas comuns

**"ModuleNotFoundError: No module named 'agno'"**
→ O ambiente virtual não está activo. Corre `source venv/bin/activate` (Mac/Linux) ou `venv\Scripts\activate` (Windows).

**"ANTHROPIC_API_KEY not found"**
→ Verifica se copiaste o ficheiro `.env.example` para `.env` e colocaste a chave correcta.

**"No events found"**
→ Corre primeiro `python etl/seed.py` para popular a base de dados.

**Porta 8000 já em uso**
→ `uvicorn main:app --reload --port 8001`

---

## 🤖 Nota sobre uso de IA

Este projecto foi desenvolvido com apoio do **Claude** (Anthropic):
- Geração da estrutura base do projecto e boilerplate
- Revisão da lógica do agente e do prompt do sistema
- Debugging e explicações dos erros

O código foi depois revisto, adaptado ao contexto de Lisboa e testado manualmente.

---

## 🚀 Melhorias possíveis (Extra Mile)

- **Scraping de sites portugueses** (Agenda Cultural de Lisboa, EGEAC, Time Out Lisboa)
- **Recomendações personalizadas** (guardar preferências do utilizador)
- **Pesquisa semântica** com embeddings (mais inteligente que filtros exactos)
- **Notificações** de novos eventos por email/Telegram
- **Frontend** em React/Vue com mapa de eventos
