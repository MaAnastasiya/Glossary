from sqlalchemy import Column, Integer, String
from src.database import Base

class TermModel(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)