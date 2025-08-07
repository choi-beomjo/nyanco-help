from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sentence_transformers import SentenceTransformer

# FastAPI 앱 초기화
app = FastAPI()

# Pydantic 모델 정의
class TextsToEmbed(BaseModel):
    texts: List[str]

# 모델 로딩
# 한국어 임베딩에 적합한 모델을 선택합니다.
# `distiluse-base-multilingual-cased-v1`은 다국어를 지원하며 비교적 가벼운 모델 중 하나입니다.
model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

@app.post("/embed")
def embed_texts(texts_to_embed: TextsToEmbed):
    """
    주어진 텍스트 리스트를 벡터로 임베딩합니다.
    """
    embeddings = model.encode(texts_to_embed.texts, convert_to_tensor=False)
    # NumPy 배열을 Python 리스트로 변환하여 JSON 직렬화 가능하게 합니다.
    return {"embeddings": embeddings.tolist()}