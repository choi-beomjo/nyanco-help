from fastapi import HTTPException
from .models import Property
from db.crud.crud import CRUD


def get_properties_from_db(crud: CRUD, property_info={}):
    filters = {key: value for key, value in property_info if value}

    properties = crud.list(Property, filters=filters)

    return properties

def get_property_from_db(crud: CRUD, property_info={}):

    properties = crud.get(Property, obj_id=property_info['id'])

    return properties


def add_property_to_db(property_data, crud: CRUD):

    crud.create(Property(**property_data))
