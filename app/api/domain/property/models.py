from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..enemy.models import enemy_properties
from ..character.models import character_properties



class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    enemies = relationship("Enemy", secondary=enemy_properties, back_populates="properties")
    characters = relationship("Character", secondary=character_properties, back_populates="properties")
