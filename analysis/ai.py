from google import genai
from google.genai import types

from config.settings import AI_API_KEY


def generate_ai_summary(contents):
    # 이 함수는 재사용 가능하게 유지
    client = genai.Client(api_key=AI_API_KEY)  # 생성 위치 이동!
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        config=types.GenerateContentConfig(
            system_instruction="""
        다음은 사용자의 거래 내역입니다. 이 내역을 기반으로 아래 내용을 요약해 주세요:
        
        1. 총 수입과 총 지출
        2. 카테고리별 지출 금액 및 비율
        3. 가장 지출이 많은 항목 (날짜, 카테고리, 금액)
        4. 지출 습관 분석 및 간단한 조언
        """
        ),
        contents=contents,
    )
    return response.text
