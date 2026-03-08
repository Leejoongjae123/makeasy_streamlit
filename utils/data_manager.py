import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.supabase_client import get_supabase_client

@st.cache_data(ttl=300)
def get_categories():
    """Supabase categories 테이블에서 카테고리 목록을 가져옵니다."""
    try:
        supabase = get_supabase_client()
        response = supabase.table("categories").select("id, name").execute()

        categories = [item["name"] for item in response.data]
        return sorted(categories)
    except Exception as e:
        st.error(f"카테고리 로드 실패: {e}")
        return ["뉴스", "커뮤니티", "SNS블로그", "카페", "기타", "미디어"]

@st.cache_data(ttl=300)
def get_sources():
    """Supabase에서 모든 정보원 목록을 가져옵니다."""
    try:
        supabase = get_supabase_client()
        response = supabase.table("sources").select("id, name, category").execute()

        sources = {}
        source_categories = {}
        for item in response.data:
            sources[item["id"]] = item["name"]
            source_categories[item["id"]] = item.get("category", [])

        source_names = list(sources.values())
        return sources, sorted(source_names), source_categories
    except Exception as e:
        st.error(f"정보원 로드 실패: {e}")
        return {}, [], {}

def get_supabase_data(type_filters=None, source_filters=None, start_date=None, end_date=None, title_search=None):
    """
    Supabase에서 필터링된 데이터를 가져옵니다.

    Args:
        type_filters: 유형 필터 리스트 (sources.category 기반)
        source_filters: 정보원 필터 리스트
        start_date: 시작일 (date 객체) - 수집일 기준
        end_date: 종료일 (date 객체) - 수집일 기준
        title_search: 제목 검색어

    Returns:
        DataFrame: 필터링된 데이터
    """
    try:
        supabase = get_supabase_client()

        # 기본 쿼리 - sources와 JOIN
        query = supabase.table("datas").select("*, sources(id, name, country, category)")

        # 수집일 필터 적용 (created_at 기준)
        if start_date:
            query = query.gte("created_at", start_date.isoformat())
        if end_date:
            end_datetime = datetime.combine(end_date, datetime.max.time())
            query = query.lte("created_at", end_datetime.isoformat())

        # 데이터 가져오기
        response = query.execute()
        data = response.data

        # DataFrame으로 변환
        df = pd.DataFrame(data)

        if df.empty:
            return pd.DataFrame(columns=["ID", "제목", "유형", "정보원", "수집일", "내용", "source_url"])

        # 컬럼 매핑 및 변환
        df["ID"] = df["id"]
        df["제목"] = df["title"]
        df["내용"] = df["content"]
        df["source_url"] = df["source_url"]

        # 수집일 변환 (created_at 사용)
        df["수집일"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d")

        # 정보원 추출 (sources 관계 데이터에서)
        df["정보원"] = df["sources"].apply(lambda x: x.get("name", "알 수 없음") if x else "알 수 없음")

        # 유형 추출 (sources.category에서 - jsonb 배열을 콤마로 구분된 문자열로 변환)
        df["유형"] = df["sources"].apply(
            lambda x: ", ".join(x.get("category", [])) if x and x.get("category") else "기타"
        )

        # 유형 필터 적용 - "유형" 컬럼에 필터 값이 포함되어 있는지 확인
        if type_filters:
            mask = df["유형"].apply(
                lambda x: any(t in x for t in type_filters) if x else False
            )
            df = df[mask]

        # 정보원 필터 적용
        if source_filters:
            df = df[df["정보원"].isin(source_filters)]

        # 제목 검색 필터 적용
        if title_search:
            title_search_lower = title_search.lower()
            mask = df["제목"].str.lower().str.contains(title_search_lower, na=False)
            df = df[mask]

        # 최종 컬럼 선택 및 정렬
        result_df = df[["ID", "제목", "유형", "정보원", "수집일", "내용", "source_url"]].copy()
        result_df = result_df.sort_values("수집일", ascending=False).reset_index(drop=True)

        return result_df

    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return pd.DataFrame(columns=["ID", "제목", "유형", "정보원", "수집일", "내용", "source_url"])

@st.cache_data
def get_sample_data():
    """
    기존 호환성을 위해 유지. 실제로는 Supabase 데이터를 반환합니다.
    """
    return get_supabase_data()
