from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Boolean
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150))
    email = Column(String(150))
    password = Column(String(150))
    full_name = Column(String(150))
    disabled = Column(Boolean)# Create tables based on the models
