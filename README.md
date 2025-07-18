# Nyanco Help API

게임 데이터 관리를 위한 FastAPI 기반 백엔드 API 서비스입니다.

## 🚀 프로젝트 개요

이 프로젝트는 게임 내 다양한 데이터(캐릭터, 적, 스킬, 스테이지 등)를 관리하는 RESTful API를 제공합니다.

## 📋 주요 기능

- **게임 데이터 관리**: 캐릭터, 적, 스킬, 속성, 스테이지 정보 관리
- **사용자 관리**: 사용자 정보 및 인증
- **게시판 시스템**: 커뮤니티 기능
- **추천 시스템**: 게임 내 추천 기능
- **RESTful API**: 표준 HTTP 메서드를 사용한 API 제공

## 🛠 기술 스택

- **Framework**: FastAPI 0.111.0
- **Database**: SQLAlchemy 2.0.36
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **Database Migration**: Alembic
- **Server**: Uvicorn
- **Containerization**: Docker

## 📁 프로젝트 구조

```
nyanco-help-api/
├── app/
│   ├── api/
│   │   ├── domain/
│   │   │   ├── board/          # 게시판 API
│   │   │   ├── character/      # 캐릭터 API
│   │   │   ├── enemy/          # 적 API
│   │   │   ├── property/       # 속성 API
│   │   │   ├── recommend/      # 추천 API
│   │   │   ├── skill/          # 스킬 API
│   │   │   ├── stage/          # 스테이지 API
│   │   │   └── user/           # 사용자 API
│   │   ├── api.py
│   │   └── deps.py
│   ├── core/
│   │   └── security.py         # 보안 관련 설정
│   ├── db/
│   │   ├── crud/              # 데이터베이스 CRUD 작업
│   │   └── init_db.py         # 데이터베이스 초기화
│   ├── model/
│   │   └── base.py            # 기본 모델
│   ├── utils/
│   │   └── msg/               # 메시지 유틸리티
│   └── main.py                # 애플리케이션 진입점
├── tests/                     # 테스트 코드
├── docker-compose.yml         # Docker Compose 설정
├── Dockerfile                 # Docker 이미지 설정
└── requirements.txt           # Python 의존성
```

## 🚀 설치 및 실행

### 1. 로컬 환경에서 실행

```bash
# 저장소 클론
git clone <repository-url>
cd nyanco-help-api

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
cd app
alembic upgrade head

# 애플리케이션 실행
python main.py
```

### 2. Docker를 사용한 실행

```bash
# Docker Compose로 실행
docker-compose up --build

# 백그라운드에서 실행
docker-compose up -d --build
```

## 📡 API 엔드포인트

서버가 실행되면 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 주요 API 경로

- `/api/user` - 사용자 관리
- `/api/character` - 캐릭터 정보
- `/api/enemy` - 적 정보
- `/api/skill` - 스킬 정보
- `/api/property` - 속성 정보
- `/api/stage` - 스테이지 정보
- `/api/board` - 게시판
- `/api/recommend` - 추천 시스템

## 🧪 테스트

```bash
# 테스트 실행
pytest

# 커버리지와 함께 테스트 실행
pytest --cov=app
```

## 🔧 개발 환경 설정

### 환경 변수

`.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
DATABASE_URL=sqlite:///./myapi.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 데이터베이스 마이그레이션

```bash
# 새로운 마이그레이션 생성
alembic revision --autogenerate -m "description"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 되돌리기
alembic downgrade -1
```

## 🐳 Docker 설정

### Docker Compose 서비스

- **포트**: 8000
- **볼륨**: 로컬 코드 변경사항 자동 반영
- **네트워크**: Jenkins 네트워크와 연결

### Docker 명령어

```bash
# 이미지 빌드
docker build -t nyanco-help-api .

# 컨테이너 실행
docker run -p 8000:8000 nyanco-help-api

# Docker Compose로 전체 스택 실행
docker-compose up
```

## 📝 API 문서

API 문서는 FastAPI의 자동 문서 생성 기능을 사용합니다:

- **개발 환경**: http://localhost:8000/docs
- **프로덕션 환경**: http://your-domain/docs (도메인은 추후 업데이트 예정)

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.
