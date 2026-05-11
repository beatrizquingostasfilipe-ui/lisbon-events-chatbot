# database/models.py
# Define como os eventos ficam guardados na base de dados

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Event(Base):
    __tablename__ = "events"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(255), nullable=False)
    description = Column(Text, default="")
    date        = Column(DateTime)
    location    = Column(String(255), default="Lisbon")
    category    = Column(String(100))   # party | networking | academic | casual
    price       = Column(String(50))    # free | cheap | paid
    audience    = Column(String(100))   # student | general
    url         = Column(String(500), default="")
    source      = Column(String(100), default="manual")  # ticketmaster | mock | manual

    def to_dict(self):
        return {
            "id":          self.id,
            "title":       self.title,
            "description": self.description,
            "date":        self.date.strftime("%A, %d %B às %H:%M") if self.date else "TBD",
            "location":    self.location,
            "category":    self.category,
            "price":       self.price,
            "audience":    self.audience,
            "url":         self.url,
        }
