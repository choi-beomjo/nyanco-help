# Python 3.10 이미지 사용
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 앱 코드 복사
COPY . .
