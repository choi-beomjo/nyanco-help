from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from fastapi import Depends


engine = create_engine(
    "sqlite:///./myapi.db",
    pool_recycle=500, pool_size=5, max_overflow=20, echo=False, echo_pool=True 
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_crud(db: Session = Depends(get_db)):
    return CRUD(db)


class CRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, obj):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def read(self, model, obj_id):
        return self.session.query(model).filter(model.id == obj_id).first()

    def update(self, model, obj_id, **kwargs):
        obj = self.session.query(model).filter(model.id == obj_id).first()
        if not obj:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, model, obj_id):
        obj = self.session.query(model).filter(model.id == obj_id).first()
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj

