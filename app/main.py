import pickle

import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_globals import GlobalsMiddleware, g
import uvicorn
import torch
from api.api import api
from utils.infer.set_model import *


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 보안 강화를 위해 특정 도메인으로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GlobalsMiddleware)

app.include_router(api, prefix="/api")

@app.on_event('startup')
def load_model():
    model, embedidngs, node_mapping, scaler, char_stat_dict = load_model_files()
    set_request_data()




if __name__ == "__main__":
    uvicorn.run(app, port=8080)