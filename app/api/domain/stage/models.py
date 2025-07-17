from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import relationship


class StageEnemy(Base):
    __tablename__ = 'stage_enemies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_id = Column(String(10), ForeignKey('stages.id'), nullable=False)
    enemy_id = Column(Integer, ForeignKey('enemies.id'), nullable=False)
    spawn_count = Column(Integer, nullable=False)
    first_spawn = Column(Integer, nullable=False)
    respawn1 = Column(Integer, nullable=False)
    respawn2 = Column(Integer, nullable=False)
    health = Column(Integer, nullable=False)

    stage = relationship("Stage", back_populates="enemies")
    enemy = relationship("Enemy", back_populates="stages")


class Stage(Base):
    __tablename__ = "stages"

    id = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=False)
    stage_hp = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    max_enemies = Column(Integer, nullable=False)
    min_spawn = Column(Integer, nullable=False)
    difficulty = Column(Float, nullable=False)

    enemies = relationship("StageEnemy", back_populates="stage")
    user_experiences = relationship("UserExperience", back_populates="stage")
