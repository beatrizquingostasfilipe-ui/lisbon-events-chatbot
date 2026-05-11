# api/routes.py
# Endpoints da API REST para gerir eventos

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from database.database import get_db
from database.models import Event

router = APIRouter(prefix="/api", tags=["Events"])


@router.get("/events", summary="Lista todos os eventos futuros")
def list_events(
    category: Optional[str] = None,
    price:    Optional[str] = None,
    audience: Optional[str] = None,
    limit:    int = 20,
    db: Session = Depends(get_db),
):
    """
    Devolve uma lista de eventos.
    Podes filtrar por category, price e audience.
    Exemplo: GET /api/events?category=party&price=free
    """
    query = db.query(Event).filter(Event.date >= datetime.now())

    if category:
        query = query.filter(Event.category == category)
    if price:
        query = query.filter(Event.price == price)
    if audience:
        query = query.filter(Event.audience == audience)

    events = query.order_by(Event.date.asc()).limit(limit).all()
    return [e.to_dict() for e in events]


@router.get("/events/{event_id}", summary="Detalhes de um evento")
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return event.to_dict()


@router.post("/etl/seed", summary="Popula a BD com eventos de exemplo")
def run_seed():
    """Corre o seed de dados mock (útil para testar)."""
    from etl.seed import seed_mock_events
    seed_mock_events()
    return {"message": "Seed concluído com sucesso!"}


@router.post("/etl/ticketmaster", summary="Importa eventos reais do Ticketmaster")
def run_ticketmaster_etl():
    """Corre o ETL do Ticketmaster (precisa de TICKETMASTER_API_KEY no .env)."""
    from etl.ticketmaster import fetch_and_store
    fetch_and_store()
    return {"message": "ETL Ticketmaster concluído!"}
