from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.api import api

from db.init_db import init_db

init_db()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 보안 강화를 위해 특정 도메인으로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api, prefix="/api")



if __name__ == "__main__":
    uvicorn.run(app, port=8080)