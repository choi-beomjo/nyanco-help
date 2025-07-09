from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
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

character_immunities = Table(
    'character_immunities', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id'), primary_key=True),
    Column('immunity_id', Integer, ForeignKey('immunities.id'), primary_key=True)
)

class Instinct(Base):
    __tablename__ = 'instincts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    instinct_type = Column(String(100), nullable=False)
    target_id = Column(Integer, nullable=False)

    character_instincts = relationship("CharacterInstinct", back_populates="instinct")


class CharacterInstinct(Base):
    __tablename__ = 'character_instincts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_id = Column(Integer, nullable=False)
    instinct_id = Column(Integer, ForeignKey('instincts.id'), nullable=False)

    instinct = relationship("Instinct", back_populates="character_instincts")


# 메인 테이블 정의
class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    atk1 = Column(Integer, nullable=False)
    atk2 = Column(Integer, nullable=False)
    atk3 = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    range = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    kb = Column(Integer, nullable=False)
    tba = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    spawn = Column(Integer, nullable=False)
    base_id = Column(Integer, nullable=False)
    form = Column(Integer, nullable=False)
    pre_atk1 = Column(Integer, nullable=False)
    pre_atk2 = Column(Integer, nullable=False)
    pre_atk3 = Column(Integer, nullable=False)
    back_atk = Column(Integer, nullable=False)
    atk_type = Column(Integer, nullable=False)
    trait = Column(Integer, nullable=False)
    long_distance1 = Column(Integer, nullable=False)
    long_distance2 = Column(Integer, nullable=False)
    immunity = Column(Integer, nullable=False)
    atk_freq = Column(Integer, nullable=False)
    ability_enabled = Column(Integer, nullable=False)


    # 관계 정의
    skills = relationship("Skill", secondary=character_skills, back_populates="characters")
    properties = relationship("Property", secondary=character_properties, back_populates="characters")

    skill_effects_cha = relationship("SkillEffect", back_populates="characters")
    immunities = relationship("Immunity", secondary=character_immunities, back_populates="characters")