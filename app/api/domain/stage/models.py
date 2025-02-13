from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


class StageEnemy(Base):
    __tablename__ = 'stage_enemies'

    stage_id = Column(Integer, ForeignKey('stages.id'), primary_key=True)
    enemy_id = Column(Integer, ForeignKey('enemies.id'), primary_key=True)

    stage = relationship("Stage", back_populates="enemies")
    enemy = relationship("Enemy", back_populates="stages")


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    enemies = relationship("StageEnemy", back_populates="stage")
