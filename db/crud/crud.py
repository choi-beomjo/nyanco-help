from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session


engine = create_engine(
    "sqlite:///./myapi.db",
    pool_recycle=500, pool_size=5, max_overflow=20, echo=False, echo_pool=True 
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

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

# 예제 모델 클래스
class User(Base):
    __tablename__ = 'USER'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

# 예제 사용법
if __name__ == "__main__":
    crud = CRUD(session=SessionLocal)

    # 사용자 생성
    new_user = User(name="John Doe", email="john.doe@example.com")
    created_user = crud.create(new_user)
    print(f"Created User: {created_user.id}, {created_user.name}, {created_user.email}")

    # 사용자 읽기
    read_user = crud.read(User, created_user.id)
    print(f"Read User: {read_user.id}, {read_user.name}, {read_user.email}")

    # 사용자 업데이트
    updated_user = crud.update(User, read_user.id, name="Jane Doe", email="jane.doe@example.com")
    print(f"Updated User: {updated_user.id}, {updated_user.name}, {updated_user.email}")

    # 사용자 삭제
    #deleted_user = crud.delete(User, updated_user.id)
    #print(f"Deleted User: {deleted_user.id if deleted_user else 'User not found'}")
