from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.orm import joinedload, subqueryload
from fastapi import Depends


engine = create_engine(
    "sqlite:///./myapi.db",
    pool_recycle=500, pool_size=5, max_overflow=20, echo=False, echo_pool=True 
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


class CRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, obj):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def read(self, model, filters=None,  # 필터 조건
        relationships=None,  # 로드할 관계 목록
        single=True  # 단일 객체 반환 여부
    ):
        query = self.session.query(model)

        # 관계 로드 처리
        if relationships:
            for rel in relationships:
                query = query.options(joinedload(getattr(model, rel)))

        # 필터 적용
        if filters:
            for key, value in filters.items():
                column = getattr(model, key)
                query = query.filter(column == value)

        # 결과 반환
        return query.first() if single else query.all()

    def read_all(self, model, **kwargs):
        query = self.session.query(model)
        for key, value in kwargs.items():
            column = getattr(model, key)

            # 관계 필드 처리
            if hasattr(column, "property") and hasattr(column.property, "mapper"):
                if isinstance(value, (list, set, tuple)):
                    # 관계된 모델의 id 컬렉션 생성
                    related_ids = [v.id for v in value]
                    query = query.filter(column.any(column.property.mapper.class_.id.in_(related_ids)))
                else:
                    # 단일 값인 경우
                    query = query.filter(column.any(column.property.mapper.class_.id == value.id))
            else:
                # 기본 컬렉션 또는 단일 값 처리
                if isinstance(value, (list, set, tuple)):
                    query = query.filter(column.in_(value))
                else:
                    query = query.filter(column == value)
        return query.all()

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

