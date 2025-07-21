import torch
import joblib
import pickle
from fastapi_globals import g


def load_model_files():
    model = torch.load("../models/deeprec_model.pt", weights_only=False)
    model.eval()

    embeddings = torch.load("../models/full_embeddings.pt")
    node_mapping = torch.load(("../models/node_mapping_full.pt"))

    scaler = joblib.load("../models/stat_scaler.pkl")

    with open("../models/char_stat_dict.pkl", "rb") as f:
        char_stat_dict = pickle.load(f)

    return model, embeddings, node_mapping, scaler, char_stat_dict


async def set_request_data():
    model, embeddings, node_mapping, scaler, char_stat_dict = load_model_files()

    g.model = model
    g.embeddings = embeddings
    g.node_mapping = node_mapping
    g.scaler = scaler
    g.char_stat_dict = char_stat_dict


