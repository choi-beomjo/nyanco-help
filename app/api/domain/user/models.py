from model.base import Base
from sqlalchemy import Column, Integer, String, Boolean


class User(Base):
    __tablename__ = 'USER'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)