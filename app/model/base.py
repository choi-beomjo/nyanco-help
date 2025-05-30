from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from db.crud.crud import engine
from api.domain.character.models import Character
from api.domain.skill.models import Skill
from api.domain.property.models import Property
from api.domain.enemy.models import Enemy
from api.domain.character.models import Character
from api.domain.stage.models import StageEnemy, Stage
from api.domain.user.models import User
from api.domain.board.models import Post

Base = declarative_base()

Base.metadata.create_all(bind=engine)