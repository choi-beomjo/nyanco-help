from .base import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey

class Post(Base):
    __tablename__ = 'POST'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    contents = Column(Text)
    #user_id = Column(Integer, ForeignKey("USER.id"), nullable=True)