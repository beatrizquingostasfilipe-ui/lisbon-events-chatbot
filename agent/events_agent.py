# agent/events_agent.py
# O agente principal: recebe a mensagem do utilizador, chama a ferramenta
# de pesquisa de eventos e devolve uma resposta amigável.

import os
import json
import logging
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

from database.database import SessionLocal, init_db
from database.models import Event

# ─── Logging (guarda num ficheiro para o extra mile do desafio) ──────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/agent.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


# ─── Ferramenta de pesquisa ───────────────────────────────────────────────────

def search_events(
    category: Optional[str] = None,
    price: Optional[str] = None,
    audience: Optional[str] = None,
    date_start: Optional[str] = None,
    date_end: Optional[str] = None,
    keywords: Optional[str] = None,
    limit: Optional[int] = 5,
) -> str:
    if isinstance(limit, str):
        limit = int(limit)
    if limit is None:
        limit = 5

    """
    Procura eventos locais em Lisboa na base de dados.

    Args:
        category:   Categoria do evento: party | networking | academic | casual
        price:      Preço: free | cheap | paid
        audience:   Público: student | general
        date_start: Data de início em formato ISO (ex: 2026-05-07T20:00:00)
        date_end:   Data de fim em formato ISO
        keywords:   Palavras-chave para pesquisar no título/descrição (separadas por vírgula)
        limit:      Número máximo de resultados (padrão: 5)
    """
    init_db()
    db = SessionLocal()

    try:
        query = db.query(Event)

        # Filtrar apenas eventos futuros
        query = query.filter(Event.date >= datetime.now())

        if date_start:
            query = query.filter(Event.date >= datetime.fromisoformat(date_start))
        if date_end:
            query = query.filter(Event.date <= datetime.fromisoformat(date_end))
        if category:
            query = query.filter(Event.category == category)
        if price == "free":
            query = query.filter(Event.price == "free")
        elif price == "cheap":
            query = query.filter(Event.price.in_(["free", "cheap"]))
        elif price == "paid":
            query = query.filter(Event.price == "paid")
        if audience:
            query = query.filter(Event.audience == audience)
        if keywords:
            for kw in keywords.split(","):
                kw = kw.strip()
                query = query.filter(
                    Event.title.ilike(f"%{kw}%") |
                    Event.description.ilike(f"%{kw}%")
                )

        events = query.order_by(Event.date.asc()).limit(limit).all()

        # Log para o ficheiro
        logger.info(json.dumps({
            "filters": {
                "category": category, "price": price, "audience": audience,
                "date_start": date_start, "date_end": date_end, "keywords": keywords
            },
            "results_count": len(events),
            "titles": [e.title for e in events],
        }))

        if not events:
            return json.dumps({
                "found": 0,
                "message": "Nenhum evento encontrado com esses filtros.",
                "events": [],
            })

        return json.dumps({
            "found": len(events),
            "events": [e.to_dict() for e in events],
        })

    finally:
        db.close()


# ─── Criar o agente Agno ─────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are a helpful local assistant that recommends events in Lisbon, especially for students.
IMPORTANT: Always respond in European Portuguese only. Never use any other language.

Your job:
1. Understand what the user wants (party, networking, free events, etc.)
2. Always call the search_events tool before responding
3. Give a short, friendly, conversational answer in Portuguese

Rules:
- NEVER respond without calling search_events first
- Suggest at most 3-5 events
- If nothing found, suggest alternatives (different day or category)
- Casual friendly tone, like a local friend in Lisbon
- Use emojis sparingly
""".strip()


def create_agent():
    from agno.agent import Agent
    from agno.models.groq import Groq

    agent = Agent(
        name="Lisbon Events Bot",
        model=Groq(id="qwen/qwen3-32b"),
        tools=[search_events],
        instructions=SYSTEM_PROMPT,
        show_tool_calls=True,
        markdown=True,
        tool_choice="auto",
    )
    return agent
