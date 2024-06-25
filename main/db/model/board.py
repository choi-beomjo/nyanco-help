from .base import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'POST'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    contents = Column(Text)
    user_id = Column(Integer, ForeignKey("USER.id"), nullable=True)
    user = relationship("User", backref="question_users")