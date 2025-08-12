from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json

model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

        
def get_stage_full_text(stage):
    """
    스테이지 정보를 조합하여 전체 텍스트를 생성합니다.
    """
    return (
        f"스테이지: {stage['stage_name']}. 요약: {stage['summary']}. "
        f"주요 적: {stage['main_enemy']}. 적 특성: {stage['enemy_traits']}. "
        f"공략: {stage['strategy']}. 추천 유닛: {stage['recommended_units']}"
        "타입: stage"
    )


def get_stage_embeddings(stage_list):
    """
    스테이지 리스트를 받아 임베딩 벡터와 ID 리스트를 생성합니다.
    """
    if model is None:
        raise RuntimeError("임베딩 모델이 로드되지 않았습니다.")

    embeddings = []
    ids = []

    for stage in stage_list:
        ids.append(stage['stage_name'])
        full_text = get_stage_full_text(stage)
        embedding = model.encode(full_text)
        embeddings.append(embedding)
        
    embeddings = np.array(embeddings)

    return embeddings, ids


def write_faiss_index(embeddings, ids):
    """
    생성된 임베딩과 ID를 Faiss 인덱스 파일로 저장합니다.
    """
    try:

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension) # L2 유클리드 거리를 사용하는 인덱스 생성
        index.add(embeddings)
        print(f"Faiss 인덱스에 {index.ntotal}개 벡터가 추가되었습니다.")

        # 6. Faiss 인덱스 파일과 ID 매핑 파일 저장
        faiss.write_index(index, "/app/data/my_faiss_index.faiss")
        with open("/app/data/id_mapping.json", "w", encoding="utf-8") as f:
            json.dump(ids, f, ensure_ascii=False, indent=2)

        
    except Exception as e:
        return {"error": f"An error occurred: {e}"}