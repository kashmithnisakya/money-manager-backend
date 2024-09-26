from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime, timezone

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), nullable=False)


class Expense(Base):
    __tablename__ = "expanses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer)
    description = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), nullable=False)
    user = relationship("User")
