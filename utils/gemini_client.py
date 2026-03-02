import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Gemini API 설정
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ============================================================
# 요약 프롬프트 설정 (이 부분을 수정하면 요약 형태가 변경됩니다)
# ============================================================
SUMMARY_PROMPT_PREFIX = """당신은 전문 이슈 분석가입니다. 다음 여러 이슈들의 본문 내용을 종합적으로 분석하여 하나의 통합된 요약 리포트를 작성해주세요.

## 작성 가이드라인:
1. **통합 제목**: 모든 이슈를 아우르는 핵심 주제를 한 줄로 요약
2. **핵심 요약**: 주요 내용을 3-5개의 불렛포인트로 정리
3. **세부 내용**: 각 이슈의 중요한 세부사항을 논리적으로 구성
4. **영향 및 시사점**: 이 이슈들이 가지는 의미와 향후 전망

## 출력 형식:
- 각 섹션은 **굵은 글씨**로 제목 표시
- 불렛포인트는 '-' 기호 사용
- 간결하고 명확한 문장 사용
- 한국어로 작성

---

## 분석할 이슈 내용:

"""

def get_gemini_client():
    """Gemini 클라이언트 초기화"""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-3-flash-preview')
    return model

def summarize_issues(issues_data):
    """
    여러 이슈의 내용을 받아서 통합 요약을 생성합니다.

    Args:
        issues_data: 이슈 데이터 리스트 [{'title': str, 'content': str, 'source_url': str}, ...]

    Returns:
        dict: {'title': str, 'summary': str, 'sources': list}
    """
    try:
        model = get_gemini_client()

        # 이슈 내용을 프롬프트에 포함
        issues_text = ""
        for i, issue in enumerate(issues_data, 1):
            issues_text += f"\n### 이슈 {i}: {issue['title']}\n"
            issues_text += f"본문: {issue['content']}\n"
            issues_text += "-" * 50 + "\n"

        full_prompt = SUMMARY_PROMPT_PREFIX + issues_text

        # Gemini API 호출
        response = model.generate_content(full_prompt)

        # 소스 URL 수집
        sources = [issue['source_url'] for issue in issues_data if issue.get('source_url')]

        # 통합 제목 생성 (첫 번째 이슈 제목 또는 기본값)
        if issues_data:
            combined_title = f"통합 분석: {issues_data[0]['title']}"
            if len(issues_data) > 1:
                combined_title += f" 외 {len(issues_data)-1}건"
        else:
            combined_title = "이슈 분석 리포트"

        return {
            'title': combined_title,
            'summary': response.text,
            'sources': sources
        }

    except Exception as e:
        raise Exception(f"Gemini API 호출 실패: {e}")

def update_summary_prompt(new_prompt):
    """
    요약 프롬프트 프리픽스를 업데이트합니다.

    Args:
        new_prompt: 새로운 프롬프트 문자열
    """
    global SUMMARY_PROMPT_PREFIX
    SUMMARY_PROMPT_PREFIX = new_prompt
