import numpy as np
import pandas as pd
import torch
from fastapi_globals import g


def recommend_characters(stage_id, top_k=5):
    stage_id_to_idx = g.node_mapping["stage_id_to_idx"]
    char_id_to_idx = g.node_mapping["character_id_to_idx"]

    character_df = pd.read_csv('../models/characters.csv')

    stage_vec = g.embeddings[stage_id_to_idx[stage_id]].numpy()  # (64,)

    candidates = []
    for char_id in character_df["id"]:
        if char_id not in char_id_to_idx or char_id not in g.char_stat_dict:
            continue

        char_vec = g.embeddings[char_id_to_idx[char_id]].numpy()         # (64,)
        stat_vec = g.char_stat_dict[char_id]                             # (16,)
        input_vec = np.concatenate([stage_vec, char_vec, stat_vec])    # (144,)

        with torch.no_grad():
            pred = g.model(torch.tensor(input_vec, dtype=torch.float32).unsqueeze(0)).item()

        candidates.append((char_id, pred))

    # 정렬 후 Top-K 추출
    top_k_chars = sorted(candidates, key=lambda x: x[1], reverse=True)[:top_k]

    char_name = character_df.set_index("id")["name"].to_dict()

    ret = [
        dict(
            rank=rank,
            character_id=char_id,
            character_name=char_name[char_id],
            score=score
        )
        for rank, (char_id, score) in enumerate(top_k_chars, 1)
    ]

    return ret