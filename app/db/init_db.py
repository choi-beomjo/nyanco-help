from db.crud.crud import engine
from model.base import Base

# ❗ 여기서 모델들 import
from api.domain.character.models import Character
from api.domain.skill.models import Skill
from api.domain.property.models import Property
from api.domain.enemy.models import Enemy
from api.domain.stage.models import Stage, StageEnemy
from api.domain.user.models import User
from api.domain.board.models import Post

def init_db():
    Base.metadata.create_all(bind=engine)
