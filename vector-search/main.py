from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sentence_transformers import SentenceTransformer
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
from google.genai import types
from google import genai
import json
import numpy as np
import faiss

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


def get_webdriver():

    selenium_url = os.getenv("SELENIUM_URL")
    # WebDriver 옵션 설정
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # selenium/python 이미지에는 이미 드라이버가 준비되어 있으므로, Service 객체는 필요 없습니다.
    driver = webdriver.Remote(command_executor=selenium_url, options=options)

    return driver


def get_web_content(driver, url, class_name):

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        main_content_div = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        )

        extracted_text = "\n".join([div.text for div in main_content_div])
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
    
    return extracted_text


def get_stage_prompt(extracted_text):

    return  f"""
        아래 텍스트는 냥코대전쟁의 공략집 내용이야. 스테이지별로 분석해서 다음 JSON 형식으로 정리해줘.


JSON 형식:

{{

"stage_name": "[스테이지 이름]",

"summary": "[전체 공략 요약]",

"main_enemy": "[주요 보스 적 이름]",

"enemy_traits": "[주요 적의 특성, 쉼표로 구분]",

"strategy": "[구체적인 공략법]",

"recommended_units": "[추천 캐릭터 이름, 쉼표로 구분]"

}}


텍스트:

{extracted_text}
        """


def get_genai_response(client: genai.Client, prompt):
    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        result = response.text.replace("```json", "").replace("```", "")
        return json.loads(result)
    except Exception as e:
        return {"error": f"An error occurred: {e}"}


def write_faiss_index(stage_list):
    try:

        embeddings = []
        ids = []

        for stage in stage_list:
            ids.append(stage['stage_name'])
            full_text = (
                f"스테이지: {stage['stage_name']}. 요약: {stage['summary']}. "
                f"주요 적: {stage['main_enemy']}. 적 특성: {stage['enemy_traits']}. "
                f"공략: {stage['strategy']}. 추천 유닛: {stage['recommended_units']}"
                "타입: stage"
            )
            embedding = model.encode(full_text)
            embeddings.append(embedding)
        
        embeddings = np.array(embeddings)

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


@app.get("/namuwiki")
def get_namuwiki_selenium():
    url = "https://namu.wiki/w/악한%20자"

    driver = get_webdriver()
    
    try:
        extracted_text = get_web_content(driver, url, 'x7-L0tzH')
        

        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        prompt = get_stage_prompt(extracted_text)

        stage_list = get_genai_response(client, prompt)
        
        write_faiss_index(stage_list)


        return {"message": "Faiss 인덱스가 성공적으로 저장되었습니다."}

        
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
        
    finally:
        driver.quit()