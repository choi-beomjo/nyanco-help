# 파이썬 3.10-slim-bullseye 이미지를 사용하면 용량을 줄일 수 있습니다.
FROM python:3.10-slim-bullseye

# 작업 디렉토리 설정
WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-pip \
    build-essential \
    libnss3 \
    libxss1 \
    libappindicator1 \
    libasound2 \
    libatk1.0-0 \
    libgtk-3-0 \
    libcups2 \
    libdrm2 \
    libgconf-2-4 \
    libgdk-pixbuf2.0-0 \
    libgl1 \
    libnspr4 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    mesa-utils \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 앱 코드 복사
COPY . .

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]