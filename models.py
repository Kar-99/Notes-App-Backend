from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


shared_notes = Table(
    "shared_notes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("note_id", Integer, ForeignKey("notes.id"))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    notes = relationship("Note", back_populates="owner")
    shared_with_me = relationship(
    "Note",
    secondary=shared_notes,
    back_populates="shared_users"
)

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="notes")

    shared_users = relationship(
    "User",
    secondary=shared_notes,
    back_populates="shared_with_me"
)