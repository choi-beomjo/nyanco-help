from fastapi import APIRouter, Depends
from ...tags import Tags
from utils.msg.msg import Msg
from .utils import *
from .schemas import *
from ...deps import get_current_user, get_crud, CRUD, admin_required


router = APIRouter(tags=[Tags.property])


@router.get("/list")
def get_property_list(crud: CRUD = Depends(get_crud)):
    properties = get_properties_from_db(crud=crud)
    return [PropertyInfo.from_orm(property) for property in properties]


@router.post("")
def post_enemy(property_info: PropertyPost, crud: CRUD = Depends(get_crud), current_user=Depends(admin_required)):
    
    property_data = property_info.dict()
    add_property_to_db(property_data=property_data, crud=crud)

    return Msg(msg="success")