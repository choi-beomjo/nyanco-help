from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

# 중간 테이블 정의
character_skills = Table(
    'character_skills', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

character_properties = Table(
    'character_properties', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id'), primary_key=True),
    Column('property_id', Integer, ForeignKey('properties.id'), primary_key=True)
)

# 메인 테이블 정의
class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    atk = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    range = Column(Integer, nullable=False)
    grade = Column(String, nullable=False)

    # 관계 정의
    skills = relationship("Skill", secondary=character_skills, back_populates="characters")
    properties = relationship("Property", secondary=character_properties, back_populates="characters")

