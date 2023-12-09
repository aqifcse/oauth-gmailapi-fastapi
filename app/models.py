from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Boolean
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    password = Column(String(150), nullable=False)
    full_name = Column(String(150), nullable=False)
    disabled = Column(Boolean, nullable=False)# Create tables based on the models
