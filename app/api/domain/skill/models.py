from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..enemy.models import enemy_skills
from ..character.models import character_skills


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    enemies = relationship("Enemy", secondary=enemy_skills, back_populates="skills")
    characters = relationship("Character", secondary=character_skills, back_populates="skills")