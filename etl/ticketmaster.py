# etl/ticketmaster.py
# ETL real: vai buscar eventos de Lisboa à API do Ticketmaster
# Precisas de uma API key GRATUITA em https://developer.ticketmaster.com

import os
import sys
import requests
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from database.database import SessionLocal, init_db
from database.models import Event

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


def categorize(event_data: dict) -> str:
    """Tenta adivinhar a categoria a partir do tipo de evento."""
    classifications = event_data.get("classifications", [{}])
    if classifications:
        segment = classifications[0].get("segment", {}).get("name", "").lower()
        genre   = classifications[0].get("genre",   {}).get("name", "").lower()

        if "music" in segment:
            return "party"
        if "arts" in segment or "theatre" in segment:
            return "casual"
        if "conference" in genre or "seminar" in genre:
            return "networking"
        if "education" in genre:
            return "academic"
    return "casual"


def get_price(event_data: dict) -> str:
    """Extrai o nível de preço."""
    ranges = event_data.get("priceRanges", [])
    if not ranges:
        return "free"
    min_price = ranges[0].get("min", 0)
    if min_price == 0:
        return "free"
    if min_price < 20:
        return "cheap"
    return "paid"


def fetch_and_store(pages: int = 3):
    """Vai buscar eventos e guarda-os na base de dados."""
    if not TICKETMASTER_API_KEY:
        print("⚠️  TICKETMASTER_API_KEY não definida no .env – a saltar ETL real.")
        return

    init_db()
    db = SessionLocal()
    total_added = 0

    for page in range(pages):
        params = {
            "apikey":      TICKETMASTER_API_KEY,
            "city":        "Lisbon",
            "countryCode": "PT",
            "size":        20,
            "page":        page,
            "sort":        "date,asc",
        }

        try:
            resp = requests.get(BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"❌ Erro na página {page}: {e}")
            continue

        data   = resp.json()
        events = data.get("_embedded", {}).get("events", [])

        for ev in events:
            # Data
            start    = ev.get("dates", {}).get("start", {})
            date_str = start.get("dateTime") or start.get("localDate", "")
            try:
                event_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except Exception:
                event_date = None

            # Local
            venues   = ev.get("_embedded", {}).get("venues", [{}])
            location = venues[0].get("name", "Lisboa") if venues else "Lisboa"

            # Descrição
            desc = (ev.get("info") or ev.get("pleaseNote") or "")[:500]

            event_obj = Event(
                title       = ev.get("name", "Evento sem nome"),
                description = desc,
                date        = event_date,
                location    = location,
                category    = categorize(ev),
                price       = get_price(ev),
                audience    = "general",
                url         = ev.get("url", ""),
                source      = "ticketmaster",
            )

            exists = db.query(Event).filter(Event.title == event_obj.title).first()
            if not exists:
                db.add(event_obj)
                total_added += 1

    db.commit()
    db.close()
    print(f"✅ Ticketmaster ETL: {total_added} novos eventos adicionados.")


if __name__ == "__main__":
    fetch_and_store()
