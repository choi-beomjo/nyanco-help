from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

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
    atk = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    range = Column(Integer, nullable=False)

    # 관계 정의
    skills = relationship("Skill", secondary=enemy_skills, back_populates="enemies")
    properties = relationship("Property", secondary=enemy_properties, back_populates="enemies")


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    enemies = relationship("Enemy", secondary=enemy_skills, back_populates="skills")


class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    enemies = relationship("Enemy", secondary=enemy_properties, back_populates="properties")
