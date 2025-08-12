from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from util.crawl import get_webdriver, get_web_content
from util.gen_ai import get_stage_prompt, get_genai_response
from util.embedding import get_stage_embeddings, write_faiss_index, model
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urljoin, urlparse, unquote, urlunparse
import os
import re


# FastAPI 앱 초기화
app = FastAPI()

# Pydantic 모델 정의
class TextsToEmbed(BaseModel):
    texts: List[str]

# 모델 로딩
# 한국어 임베딩에 적합한 모델을 선택합니다.
# `distiluse-base-multilingual-cased-v1`은 다국어를 지원하며 비교적 가벼운 모델 중 하나입니다.


@app.post("/embed")
def embed_texts(texts_to_embed: TextsToEmbed):
    """
    주어진 텍스트 리스트를 벡터로 임베딩합니다.
    """
    embeddings = model.encode(texts_to_embed.texts, convert_to_tensor=False)
    # NumPy 배열을 Python 리스트로 변환하여 JSON 직렬화 가능하게 합니다.
    return {"embeddings": embeddings.tolist()}




@app.get("/namuwiki")
def get_namuwiki_selenium():
    url = "https://namu.wiki/w/악한%20자"

    driver = get_webdriver()
    
    try:
        extracted_text = get_web_content(driver, url, 'x7-L0tzH')
        
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        prompt = get_stage_prompt(extracted_text)

        stage_list = get_genai_response(client, prompt)

        embeddings, ids = get_stage_embeddings(stage_list)
        
        write_faiss_index(embeddings, ids)


        return {"message": "Faiss 인덱스가 성공적으로 저장되었습니다."}

        
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
        
    finally:
        driver.quit()


def write_prompt_to_file(prompt):
    with open("/app/prompt.txt", "a", encoding="utf-8") as f:
        f.write(prompt)


def extract_stage_links_from_story_html(html: str, base_url: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')

    def _emit(href: str, out: list):
        href = urljoin(base_url, href)
        href = canonicalize_url(href)
        if not any(k in href for k in ('edit','discuss','history','member')):
            out.append(href)

    # 1) '목록' 또는 '스테이지 목록' h2 찾기
    target_h2 = None
    for h2 in soup.find_all('h2'):
        if '목록' in h2.get_text(strip=True):  # '목록' / '스테이지 목록' 포함
            target_h2 = h2
            break

    chapter_urls: List[str] = []

    # 2) 섹션 범위(다음 h2 전까지) 1차 수집
    if target_h2:
        for sib in target_h2.next_siblings:
            if isinstance(sib, Tag) and sib.name == 'h2':
                break  # 섹션 종료
            if not isinstance(sib, Tag):
                continue

            # 2-1) 번호 앵커 바로 뒤의 문서 링크 (클래스 비의존)
            for a in sib.select('a[href^="#s-"][href*="."] + a[href^="/w/"]'):
                _emit(a['href'], chapter_urls)

            # 2-2) 같은 라인(span) 안의 번호 앵커 + 장 링크 (난수 클래스 폴백)
            for span in sib.select('span._8XwiLI7j'):
                idx_anchor = span.find('a', href=re.compile(r'^#s-\d+(?:\.\d+)+$'))
                if not idx_anchor:
                    continue
                link = span.find('a', class_='H3uoeNgK', href=True) or \
                       span.find('a', href=re.compile(r'^/w/'))
                if link and link.get('href'):
                    _emit(link['href'], chapter_urls)

    # 3) 폴백: 섹션에서 0건이면 문서 전역(TOC 블록 포함) 스캔
    if not chapter_urls:
        # 레전드/신 레전드 모두에서 실제로 쓰이는 구조 확인됨
        # (span._8XwiLI7j 내에 '#s-3.x' 또는 '#s-2.x'와 장 링크가 함께 존재)
        for span in soup.select('div.LuW3xQqz span._8XwiLI7j, span._8XwiLI7j'):
            idx_anchor = span.find('a', href=re.compile(r'^#s-\d+(?:\.\d+)+$'))
            if not idx_anchor:
                continue
            link = span.find('a', class_='H3uoeNgK', href=True) or \
                   span.find('a', href=re.compile(r'^/w/'))
            if link and link.get('href'):
                _emit(link['href'], chapter_urls)

    # 4) 중복 제거(원순서 보존)
    seen = set()
    unique = []
    for u in chapter_urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)
    return unique





def canonicalize_url(u: str) -> str:
    p = urlparse(u)
    # 쿼리/프래그먼트 제거 + 경로 디코딩으로 정규화
    path = unquote(p.path)
    return urlunparse((p.scheme, p.netloc, path, '', '', ''))




@app.get("/scrape-legend-story", tags=["Scraping and Indexing"])
def get_all_stories_and_index():
    base_url = "https://namu.wiki"
    stories_to_scrape = [
        {"name": "레전드 스토리", "url": f"{base_url}/w/냥코%20대전쟁/%EB%A0%88%EC%A0%84%EB%93%9C%20%EC%8A%A4%ED%86%A0%EB%A6%AC"},
        {"name": "신 레전드 스토리", "url": f"{base_url}/w/냥코%20대전쟁/%EC%8B%A0%20%EB%A0%88%EC%A0%84%EB%93%9C%20%EC%8A%A4%ED%86%A0%EB%A6%AC"},
    ]

    all_stages = []
    driver = get_webdriver()

    # 전역 중복 제거(정규화된 URL 기준)
    seen_urls = set()

    try:
        for story in stories_to_scrape:
            # 메인 페이지 HTML
            driver.get(story["url"])
            WebDriverWait(driver, 20).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            story_html = driver.page_source

            # 목차 기반으로 스테이지 링크 수집(중복 제거 포함)
            chapter_urls = extract_stage_links_from_story_html(story_html, base_url)
            print(f"[INFO] {story['name']} stages found (unique): {len(chapter_urls)}")

            # 각 스테이지 페이지 처리
            for chapter_url in chapter_urls:
                norm_url = canonicalize_url(chapter_url)
                if norm_url in seen_urls:
                    print(f"[SKIP] already seen: {chapter_url}")
                    continue
                seen_urls.add(norm_url)
                # 기존 get_web_content 시그니처 유지 시:
                # extracted_text = get_web_content(driver, chapter_url, 'x7-L0tzH')
                # 만약 HTML 전문이 필요하면 driver.get + driver.page_source 사용
                try:
                    extracted_text = get_web_content(driver, chapter_url, 'x7-L0tzH')
                    if not extracted_text:
                        print(f"[WARN] empty text: {chapter_url}")
                        continue

                    # 디버깅을 위해 URL과 함께 저장
                    write_prompt_to_file(f"\n\n=== {chapter_url} ===\n{extracted_text}\n")

                    # 아래 단계는 필요 시 해제
                    # client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
                    # prompt = get_stage_prompt(extracted_text)
                    # stage_list = get_genai_response(client, prompt)
                    # if isinstance(stage_list, list):
                    #     all_stages.extend(stage_list)
                    # elif isinstance(stage_list, dict):
                    #     all_stages.append(stage_list)

                except Exception as e:
                    print(f"[ERR] chapter fetch failed: {chapter_url}: {e}")
                    continue

        # if not all_stages:
        #     raise HTTPException(status_code=404, detail="No chapter content found for scraping.")
        # embeddings, ids = get_stage_embeddings(all_stages)
        # write_faiss_index(embeddings, ids)

        return {"message": f"Faiss index process finished. unique stage urls: {len(seen_urls)}"}

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch main page: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during pipeline execution: {e}")
    finally:
        driver.quit()