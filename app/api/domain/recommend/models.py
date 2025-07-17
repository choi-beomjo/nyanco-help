from model.base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import json


class UserExperience(Base):
    __tablename__ = "user_experiences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stage_id = Column(String(10), ForeignKey('stages.id'), nullable=False)
    characters_data = Column(Text, nullable=False)  # JSON 형태로 캐릭터 사용 데이터 저장
    result = Column(String(20), nullable=False)  # 'win', 'lose', 'draw' - 필수 필드
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    # 추천 모델 학습을 위한 추가 필드들
    clear_time = Column(Integer, nullable=True)  # 클리어 시간 (초)
    difficulty_rating = Column(Integer, nullable=True)  # 사용자가 평가한 난이도 (1-5)

    # 관계 정의
    stage = relationship("Stage", back_populates="user_experiences")

    def get_characters_data(self):
        """JSON 문자열을 파싱하여 캐릭터 데이터 반환"""
        if self.characters_data:
            return json.loads(self.characters_data)
        return []

    def set_characters_data(self, characters_data):
        """캐릭터 데이터를 JSON 문자열로 저장"""
        self.characters_data = json.dumps(characters_data) 