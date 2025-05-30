from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from db.crud.crud import engine
from . import *

Base = declarative_base()

Base.metadata.create_all(bind=engine)