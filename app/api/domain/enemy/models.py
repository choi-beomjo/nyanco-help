from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from api.domain.stage.models import StageEnemy  # 정확한 경로로 import


# 중간 테이블 정의
enemy_skills = Table(
    'enemy_skills', Base.metadata,
    Column('enemy_id', Integer, ForeignKey('enemies.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

enemy_properties = Table(
    'enemy_properties', Base.metadata,
    Column('enemy_id', Integer, ForeignKey('enemies.id'), primary_key=True),
    Column('property_id', Integer, ForeignKey('properties.id'), primary_key=True)
)

# 메인 테이블 정의
class Enemy(Base):
    __tablename__ = "enemies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    atk = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    range = Column(Integer, nullable=False)
    kb = Column(Integer, nullable=False)
    dps = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    tba = Column(Integer, nullable=False)
    target = Column(String(50), nullable=False) 
    atk_sec = Column(Integer, nullable=False) 

    # 관계 정의
    skills = relationship("Skill", secondary=enemy_skills, back_populates="enemies")
    properties = relationship("Property", secondary=enemy_properties, back_populates="enemies")


    stages = relationship(StageEnemy, back_populates="enemy")  # ✅ 직접 참조