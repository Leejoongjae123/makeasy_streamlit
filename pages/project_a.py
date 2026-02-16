import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.data_manager import get_sample_data

def show():
    st.title("프로젝트 A - 이슈 모니터링")
    st.markdown("수집된 항목들을 검색하고 분석합니다.")
    

    # 1. 검색 필터 섹션
    with st.container(border=True):
        st.markdown("### 검색 필터")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 유형 (Type)
            type_options = st.multiselect(
                "유형",
                ["뉴스", "블로그", "소셜미디어", "보고서"],
                default=["뉴스", "블로그"]
            )
            
            # 정보원 (Source)
            source_options = st.multiselect(
                "정보원",
                ["네이버", "다음", "구글", "트위터"],
                default=["네이버", "다음"]
            )

        with col2:
            # 발행일 범위 (Start Date & End Date)
            st.markdown("<p style='font-size: 14px; font-weight: 500; margin-bottom: 2px;'>발행일 범위</p>", unsafe_allow_html=True)
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                start_date = st.date_input(
                    "시작일",
                    value=datetime.now() - timedelta(days=7),
                    label_visibility="collapsed"
                )
            with d_col2:
                end_date = st.date_input(
                    "종료일",
                    value=datetime.now(),
                    label_visibility="collapsed"
                )
            
            # 키워드 (Keyword)
            keyword = st.text_input(
                "키워드",
                placeholder="검색할 키워드를 입력하세요..."
            )
        
        search_btn = st.button("검색 실행", type="primary", use_container_width=True)

    st.divider()

    # 2. 데이터 필터링 로직
    df = get_sample_data()
    
    # 발행일 기간 필터링
    df["발행일_dt"] = pd.to_datetime(df["발행일"]).dt.date
    df = df[(df["발행일_dt"] >= start_date) & (df["발행일_dt"] <= end_date)]

    # 유형 필터링
    if type_options:
        df = df[df["유형"].isin(type_options)]

    # 정보원 필터링
    if source_options:
        df = df[df["정보원"].isin(source_options)]

    # 키워드 필터링
    if keyword:
        df = df[
            df["제목"].str.contains(keyword, case=False) | 
            df["내용"].str.contains(keyword, case=False) |
            df["키워드"].str.contains(keyword, case=False)
        ]

    # 기본 정렬 (최신순)
    df = df.sort_values("발행일", ascending=False)

    # 3. 결과 표시
    col_res1, col_res2 = st.columns([3, 1])
    with col_res1:
        st.markdown(f"총 **{len(df)}**개의 결과가 검색되었습니다.")
    
    with col_res2:
        if not df.empty:
            import io
            # 엑셀 파일 생성을 위한 버퍼
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                # 필터링된 데이터에서 불필요한 보조 컬럼 제외하고 저장
                export_df = df.drop(columns=["발행일_dt"]) if "발행일_dt" in df.columns else df
                export_df.to_excel(writer, index=False, sheet_name='Sheet1')
            
            st.download_button(
                label="엑셀 다운로드",
                data=buffer.getvalue(),
                file_name=f"issue_monitoring_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="download_excel"
            )
    
    if not df.empty:
        st.dataframe(
            df[["ID", "제목", "유형", "정보원", "발행일", "키워드"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "제목": st.column_config.TextColumn("제목", width="large"),
                "유형": st.column_config.TextColumn("유형"),
                "발행일": st.column_config.DateColumn("발행일"),
            }
        )
    else:
        st.info("검색 조건에 맞는 데이터가 없습니다.")
