from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..enemy.models import enemy_skills
from ..character.models import character_skills


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    identify = Column(String(100), nullable=True)
    parse_fields = Column(String(500), nullable=True)

    effects = relationship("SkillEffect", back_populates="skills")
    enemies = relationship("Enemy", secondary=enemy_skills, back_populates="skills")
    characters = relationship("Character", secondary=character_skills, back_populates="skills")
    effects_enemy = relationship("SkillEffectEnemy", back_populates="skills")


class SkillEffect(Base):
    __tablename__ = 'skill_effects_cha'
    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey('characters.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    effect_type = Column(String(100), nullable=False)
    effect_value = Column(Integer, nullable=False)

    skills = relationship("Skill", back_populates="effects")
    characters = relationship("Character", back_populates="skill_effects_cha")


class SkillEffectEnemy(Base):
    __tablename__ = 'skill_effects_enemy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    enemy_id = Column(Integer, ForeignKey('enemies.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    effect_type = Column(String(100), nullable=False)
    effect_value = Column(Integer, nullable=False)

    skills = relationship("Skill", back_populates="effects_enemy")
    enemies = relationship("Enemy", back_populates="skill_effects_enemy")