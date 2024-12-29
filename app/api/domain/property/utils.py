from fastapi import HTTPException
from .models import Property
from db.crud.crud import CRUD


def get_properties_from_db(crud: CRUD, property_info={}):
    filters = {key: value for key, value in property_info if value}

    properties = crud.read_all(Property)

    return properties


def add_property_to_db(property_data, crud: CRUD):

    crud.create(Property(name=property_data['name']))
