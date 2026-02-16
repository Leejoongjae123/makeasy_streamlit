import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

@st.cache_data
def get_sample_data():
    data = []
    base_date = datetime.now()
    for i in range(50):
        data.append({
            "ID": i + 1,
            "제목": f"이슈 항목 {i + 1}",
            "유형": ["뉴스", "블로그", "소셜미디어", "보고서"][i % 4],
            "정보원": ["네이버", "다음", "구글", "트위터"][i % 4],
            "발행일": (base_date - timedelta(days=i)).strftime("%Y-%m-%d"),
            "키워드": ["AI", "빅데이터", "클라우드", "보안"][i % 4],
            "내용": f"이것은 샘플 이슈 내용입니다. 항목 {i + 1}에 대한 상세 설명입니다."
        })
    return pd.DataFrame(data)
