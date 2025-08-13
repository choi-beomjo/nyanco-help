from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from util.crawl import get_webdriver, get_web_content
from util.gen_ai import get_stage_prompt, get_genai_response
from util.embedding import get_stage_embeddings, write_faiss_index, model
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urljoin, urlparse, unquote, urlunparse
import os
import re
import json

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


def extract_stage_content(html: str) -> List[Dict[str, Any]]:
    """
    HTML에서 광란 스테이지의 제목과 공략 텍스트를 추출합니다.
    """
    soup = BeautifulSoup(html, 'html.parser')
    stages: List[Dict[str, Any]] = []

    # 1) 스테이지 헤더 수집
    header_anchors = soup.select('h3 > a[id^="s-2."], h3 > a[id^="s-3."]')
    header_re = re.compile(r'^s-(2|3)\.\d+$')

    for a in header_anchors:
        h3 = a.find_parent('h3')
        if not h3:
            continue

        # "2.1. 광란의 고양이 강림 [편집]" -> "광란의 고양이 강림"
        raw_stage_name = h3.get_text(" ", strip=True).replace('[편집]', '')
        clean_stage_name = re.sub(r'^\d+\.\d+\.\s*', '', raw_stage_name).strip()

        stage_item: Dict[str, Any] = {
            "stage_name": clean_stage_name,
            "text": "",
            "type": "special_stage",
            "metadata": {}
        }

        text_parts: List[str] = []
        captured_info_table = False

        # 2) 현재 h3 이후의 요소들을 문서 순서로 순회
        for node in h3.next_elements:
            # 2-1) 다음 스테이지 h3를 만나면 종료
            if isinstance(node, Tag) and node.name == 'h3':
                na = node.find('a', id=header_re)
                if na:
                    break

            if not isinstance(node, Tag):
                continue

            # 2-2) 정보 테이블(있을 경우 최초 1회)
            if not captured_info_table and node.name == 'table':
                try:
                    # 표 구조가 문서마다 조금 달라서, 가장 단순한 1행을 우선 파싱
                    rows = node.select('tbody tr')
                    if rows:
                        cells = rows[0].find_all('td')
                        if len(cells) >= 3:
                            stage_item['metadata']['info_table'] = {
                                # 필요 시 필드명은 조정하세요
                                "col1": cells[0].get_text(" ", strip=True),
                                "col2": cells[1].get_text(" ", strip=True),
                                "col3": cells[2].get_text(" ", strip=True),
                            }
                            # 가끔 4번째 셀에 보스명이 있기도 함
                            if len(cells) >= 4:
                                stage_item['metadata']['info_table']["col4"] = cells[3].get_text(" ", strip=True)
                            captured_info_table = True
                except Exception:
                    pass

            # 2-3) 보스 스탯(블록 인용)
            if node.name == 'blockquote':
                btxt = node.get_text("\n", strip=True)
                if btxt:
                    lines = [ln for ln in btxt.splitlines() if ln.strip()]
                    # 첫 줄이 대개 보스명
                    if lines:
                        stage_item['metadata'].setdefault('boss_stats', {})
                        if 'boss_name' not in stage_item['metadata']:
                            stage_item['metadata']['boss_name'] = re.sub(r'[:：]\s*$', '', lines[0])

                    # 대표 스탯 숫자 파싱
                    for k, pat in [
                        ('체력', r'체력[:：]?\s*([0-9,]+)'),
                        ('공격력', r'공격력[:：]?\s*([0-9,]+)'),
                        ('사거리', r'사거리[:：]?\s*([0-9,]+)'),
                        ('히트백', r'히트백[:：]?\s*([0-9,]+)'),
                    ]:
                        m = re.search(pat, btxt)
                        if m:
                            stage_item['metadata']['boss_stats'][k] = m.group(1)

                    # 특징 한 줄(예: 100% 파동, 떠있는 적 등)도 같이 기록
                    m2 = re.search(r'(100%[^,\n]+파동|떠있는 적|좀비|흑|메탈|천사)', btxt)
                    if m2:
                        stage_item['metadata']['boss_stats']['trait_or_note'] = m2.group(1)

                # 블록 인용 내부 텍스트는 본문에서 제외(중복 방지)
                continue

            # 2-4) 본문 텍스트 수집: 문단 컨테이너(가장 흔한 x7-L0tzH) 위주
            if ('x7-L0tzH' in (node.get('class') or [])) and \
               (node.find_parent('blockquote') is None) and \
               (node.find_parent('table') is None):
                t = node.get_text(" ", strip=True)
                if t and '월간 일정' not in t:
                    text_parts.append(t)

        # 3) 클린업 & 결과 반영
        full_text = "\n".join(text_parts).strip()
        # 방어적 삭제(만약 꼬리표가 섞였을 경우)
        full_text = re.sub(r'한국판 냥코 대전쟁 월간 일정.*', '', full_text, flags=re.DOTALL)

        stage_item["text"] = full_text
        stages.append(stage_item)

    return stages




@app.get("/except-legend-story", tags=["Scraping and Indexing"])
def get_except_legend_story():
    base_url = "https://namu.wiki"

    stories_to_scrape = [
        {"name": "사이클론", "url": f"{base_url}/w/냥코%20대전쟁/스페셜%20스테이지/사이클론"},
        {"name": "광란", "url": f"{base_url}/w/냥코%20대전쟁/스페셜%20스테이지/광란"},
        {"name": "각성", "url": f"{base_url}/w/냥코%20대전쟁/스페셜%20스테이지/각성"},
        {"name": "강습", "url": f"{base_url}/w/냥코%20대전쟁/스페셜%20스테이지/강습"},
        {"name": "풍운냥코탑", "url": f"{base_url}/w/풍운%20냥코탑"},
        {"name": "이계냥코탑", "url": f"{base_url}/w/이계%20냥코탑"},
    ]

    all_stages = []
    driver = get_webdriver()

    for story in stories_to_scrape:
            # 메인 페이지 HTML
        driver.get(story["url"])
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        story_html = driver.page_source

        # story_html을 /app/{story['name']}_raw.html 저장
        #with open(f"/app/{story['name']}_raw.html", "w", encoding="utf-8") as f:
        #    f.write(story_html)
        
        extracted_data = extract_stage_content(story_html)   
        # 추출된 데이터를 파일로 저장 (디버깅 목적)
        with open(f"/app/{story['name']}_extracted.json", "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False)

    return {"message": "Scraping finished."}





