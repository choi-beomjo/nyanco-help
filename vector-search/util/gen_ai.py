from google import genai
import json


def get_stage_prompt(extracted_text):
    """
    Genimi API에 전달할 프롬프트를 생성합니다.
    """
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
    """
    Genimi API를 호출하여 구조화된 JSON 응답을 받습니다.
    """
    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        result = response.text.replace("```json", "").replace("```", "")
        
        return json.loads(result)
    
    except Exception as e:
        print(f"GenAI 응답 생성 중 오류 발생: {e}")
        return []