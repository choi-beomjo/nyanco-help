from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


class StageEnemy(Base):
    __tablename__ = 'stage_enemies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_id = Column(Integer, ForeignKey('stages.id'), nullable=False)
    enemy_id = Column(Integer, ForeignKey('enemies.id'), nullable=False)

    stage = relationship("Stage", back_populates="enemies")
    enemy = relationship("Enemy", back_populates="stages")


class Stage(Base):
    __tablename__ = "stage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    enemies = relationship("StageEnemy", back_populates="stage")
