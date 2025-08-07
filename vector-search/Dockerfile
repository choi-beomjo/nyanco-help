# 파이썬 3.10-slim-bullseye 이미지를 사용하면 용량을 줄일 수 있습니다.
FROM python:3.10-slim-bullseye

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 앱 코드 복사
COPY . .

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]