import pickle

import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import torch
from api.api import api


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 보안 강화를 위해 특정 도메인으로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api, prefix="/api")

@app.on_event('startup')
def load_model():
    global model
    model = torch.load("../models/deeprec_model.pt", weights_only=False)
    model.eval()

    global node_mapping
    global scaler
    global embeddings
    global char_stat_dict

    embeddings = torch.load("../models/full_embeddings.pt")
    node_mapping = torch.load(("../models/node_mapping_full.pt"))

    scaler = joblib.load("../models/stat_scaler.pkl")

    with open("../models/char_stat_dict.pkl", "rb") as f:
        char_stat_dict = pickle.load(f)




if __name__ == "__main__":
    uvicorn.run(app, port=8080)