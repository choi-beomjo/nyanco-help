from sqlalchemy.ext.declarative import declarative_base
from db.crud.crud import engine


Base = declarative_base()

Base.metadata.create_all(bind=engine)