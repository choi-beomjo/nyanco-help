from fastapi import APIRouter, Depends
from ...tags import Tags
from utils.msg.msg import Msg
from ...deps import get_current_user, get_crud, CRUD, admin_required