# etl/seed.py
# Popula a base de dados com eventos fictícios de Lisboa para testar sem API keys

from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import SessionLocal, init_db
from database.models import Event

def seed_mock_events():
    """Insere eventos de exemplo na base de dados."""
    init_db()
    now = datetime.now()

    mock_events = [
        # --- PARTIES ---
        {
            "title": "Erasmus Night Party @ Bairro Alto",
            "description": "A maior festa Erasmus de Lisboa! Música, drinks e estudantes de todo o mundo. Entry: 5€ com drink incluído.",
            "date": now + timedelta(hours=6),
            "location": "Bairro Alto, Lisboa",
            "category": "party",
            "price": "cheap",
            "audience": "student",
            "url": "https://www.facebook.com/events/erasmusnight",
            "source": "mock",
        },
        {
            "title": "Techno Night @ Lux Frágil",
            "description": "Uma das melhores discotecas de Lisboa com DJs internacionais de música electrónica.",
            "date": now + timedelta(days=1, hours=8),
            "location": "Lux Frágil, Santa Apolónia",
            "category": "party",
            "price": "paid",
            "audience": "general",
            "url": "https://luxfragil.com",
            "source": "mock",
        },
        {
            "title": "Rooftop Sunset Party – TOPO",
            "description": "Cocktails ao pôr-do-sol com vista para o Castelo. DJs a partir das 19h.",
            "date": now + timedelta(days=2, hours=5),
            "location": "TOPO Rooftop, Martim Moniz",
            "category": "party",
            "price": "cheap",
            "audience": "general",
            "url": "https://topo-lisbon.com",
            "source": "mock",
        },
        {
            "title": "Estudantes em Festa – Queima das Fitas",
            "description": "Celebração académica com concertos, arraial e muita animação. Gratuito para estudantes.",
            "date": now + timedelta(days=3),
            "location": "Alameda da Universidade, Lisboa",
            "category": "party",
            "price": "free",
            "audience": "student",
            "url": "https://queima2026.pt",
            "source": "mock",
        },

        # --- NETWORKING ---
        {
            "title": "Tech Networking Lisboa – Edição Maio",
            "description": "Evento mensal para developers, designers e empreendedores. Drinks incluídos. Traz cartões!",
            "date": now + timedelta(days=2),
            "location": "Startup Lisboa, Rua da Prata 80",
            "category": "networking",
            "price": "free",
            "audience": "general",
            "url": "https://startuplisboa.com/events",
            "source": "mock",
        },
        {
            "title": "Startup Pitch Night Lisboa",
            "description": "Startups em fase inicial apresentam as suas ideias a investidores. Óptimo para fazer networking.",
            "date": now + timedelta(days=6),
            "location": "Beta-i, Rua Alexandre Herculano, Lisboa",
            "category": "networking",
            "price": "free",
            "audience": "student",
            "url": "https://beta-i.com",
            "source": "mock",
        },
        {
            "title": "Language Exchange – Café Central",
            "description": "Troca de idiomas num ambiente descontraído. Português, Inglês, Espanhol e mais. Todos bem-vindos!",
            "date": now + timedelta(days=3),
            "location": "Café Central, Chiado",
            "category": "networking",
            "price": "free",
            "audience": "student",
            "url": "https://meetup.com/lisbon-language-exchange",
            "source": "mock",
        },

        # --- ACADEMIC ---
        {
            "title": "Career Fair – NOVA University",
            "description": "50+ empresas a recrutar estudantes de todas as faculdades. CV obrigatório!",
            "date": now + timedelta(days=5),
            "location": "NOVA University, Campus de Campolide",
            "category": "academic",
            "price": "free",
            "audience": "student",
            "url": "https://novacareerafair.pt",
            "source": "mock",
        },
        {
            "title": "Workshop de Machine Learning para Iniciantes",
            "description": "Aprende Python e ML na prática com projectos reais. Computador obrigatório.",
            "date": now + timedelta(days=7),
            "location": "Instituto Superior Técnico, Alameda",
            "category": "academic",
            "price": "free",
            "audience": "student",
            "url": "https://ist.ulisboa.pt/events",
            "source": "mock",
        },

        # --- CASUAL ---
        {
            "title": "Beach Volleyball @ Carcavelos",
            "description": "Jogo aberto de voleibol de praia ao fim de tarde. Todos os níveis bem-vindos. Óptimo para conhecer gente!",
            "date": now + timedelta(days=4),
            "location": "Praia de Carcavelos, Cascais",
            "category": "casual",
            "price": "free",
            "audience": "general",
            "url": "https://meetup.com/lisbon-volleyball",
            "source": "mock",
        },
        {
            "title": "Noite de Fado no Alfama",
            "description": "Experiência autêntica de Fado no bairro histórico de Alfama. Jantar opcional.",
            "date": now + timedelta(days=1),
            "location": "Tasca do Chico, Alfama",
            "category": "casual",
            "price": "paid",
            "audience": "general",
            "url": "https://tascadochico.pt",
            "source": "mock",
        },
        {
            "title": "Picnic Colectivo no Parque Eduardo VII",
            "description": "Encontro descontraído no maior parque do centro de Lisboa. Traz comida para partilhar!",
            "date": now + timedelta(days=5),
            "location": "Parque Eduardo VII, Lisboa",
            "category": "casual",
            "price": "free",
            "audience": "general",
            "url": "",
            "source": "mock",
        },
    ]

    db = SessionLocal()
    added = 0
    skipped = 0

    for data in mock_events:
        existing = db.query(Event).filter(Event.title == data["title"]).first()
        if not existing:
            db.add(Event(**data))
            added += 1
        else:
            skipped += 1

    db.commit()
    db.close()

    print(f"✅ Seed concluído: {added} eventos adicionados, {skipped} já existiam.")


if __name__ == "__main__":
    seed_mock_events()
