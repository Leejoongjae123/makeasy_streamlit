import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.data_manager import get_sample_data

def show():
    st.title("프로젝트 A - 이슈 모니터링 에이전트")
    st.markdown("이슈 수집 및 정밀 분석을 수행합니다.")
    st.divider()

    # 세션 상태 초기화 및 탭 제어 로직
    if "project_a_tab" not in st.session_state:
        st.session_state.project_a_tab = "이슈 수집"
    if "is_analyzing" not in st.session_state:
        st.session_state.is_analyzing = False

    # 풀스크린 로더 오버레이 구현
    if st.session_state.is_analyzing:
        st.markdown("""
            <style>
                .loader-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    background-color: rgba(255, 255, 255, 0.8);
                    z-index: 9999;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }
                .spinner {
                    width: 50px;
                    height: 50px;
                    border: 5px solid #E2E8F0;
                    border-top: 5px solid #1F2C5C;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                .loader-text {
                    margin-top: 20px;
                    font-size: 18px;
                    font-weight: 600;
                    color: #1F2C5C;
                    font-family: 'Inter', sans-serif;
                }
            </style>
            <div class="loader-overlay">
                <div class="spinner"></div>
                <div class="loader-text">AI 분석 중</div>
            </div>
        """, unsafe_allow_html=True)
        
        import time
        time.sleep(2.5) # 로딩 효과 시뮬레이션
        st.session_state.project_a_tab = "이슈 분석"
        st.session_state.is_analyzing = False
        st.rerun()

    # 상단 커스텀 탭 (언더라인 스타일)
    st.markdown("""
        <style>
            .tab-container {
                display: flex;
                gap: 20px;
                border-bottom: 2px solid #E2E8F0;
                margin-bottom: 25px;
            }
            .stButton > button.custom-tab {
                background-color: transparent !important;
                border: none !important;
                border-radius: 0 !important;
                padding: 10px 20px !important;
                font-size: 18px !important;
                font-weight: 500 !important;
                color: #64748B !important;
                border-bottom: 3px solid transparent !important;
                height: auto !important;
            }
            .stButton > button.custom-tab-active {
                background-color: transparent !important;
                border: none !important;
                border-radius: 0 !important;
                padding: 10px 20px !important;
                font-size: 18px !important;
                font-weight: 700 !important;
                color: #1F2C5C !important;
                border-bottom: 3px solid #1F2C5C !important;
                height: auto !important;
            }
            .stButton > button.custom-tab:hover {
                color: #1F2C5C !important;
            }
        </style>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 5])
    with c1:
        if st.button("이슈 수집", key="btn_tab1", use_container_width=True, 
                     type="secondary", help=None):
            st.session_state.project_a_tab = "이슈 수집"
            st.rerun()
        # 활성화 시 스타일 적용을 위한 HTML/CSS 주입 (버튼 클래스 제어가 어려우므로 수동 스타일링)
        if st.session_state.project_a_tab == "이슈 수집":
            st.markdown('<style>#btn_tab1 { border-bottom: 3px solid #1F2C5C !important; color: #1F2C5C !important; font-weight: 700 !important; }</style>', unsafe_allow_html=True)
            
    with c2:
        if st.button("이슈 분석", key="btn_tab2", use_container_width=True,
                     type="secondary", help=None):
            st.session_state.project_a_tab = "이슈 분석"
            st.rerun()
        if st.session_state.project_a_tab == "이슈 분석":
            st.markdown('<style>#btn_tab2 { border-bottom: 3px solid #1F2C5C !important; color: #1F2C5C !important; font-weight: 700 !important; }</style>', unsafe_allow_html=True)

    # 모든 버튼에 공통 스타일 적용을 위한 ID 기반 CSS
    st.markdown(f"""
        <style>
            div[data-testid="stColumn"]:nth-child(1) button {{
                border: none !important;
                background: transparent !important;
                border-bottom: 3px solid {"#1F2C5C" if st.session_state.project_a_tab == "이슈 수집" else "transparent"} !important;
                color: {"#1F2C5C" if st.session_state.project_a_tab == "이슈 수집" else "#64748B"} !important;
                font-size: 18px !important;
                font-weight: {"700" if st.session_state.project_a_tab == "이슈 수집" else "500"} !important;
                border-radius: 0px !important;
            }}
            div[data-testid="stColumn"]:nth-child(2) button {{
                border: none !important;
                background: transparent !important;
                border-bottom: 3px solid {"#1F2C5C" if st.session_state.project_a_tab == "이슈 분석" else "transparent"} !important;
                color: {"#1F2C5C" if st.session_state.project_a_tab == "이슈 분석" else "#64748B"} !important;
                font-size: 18px !important;
                font-weight: {"700" if st.session_state.project_a_tab == "이슈 분석" else "500"} !important;
                border-radius: 0px !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.project_a_tab == "이슈 수집":
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
                    placeholder="검색할 키워드를 입력하세요...",
                    key="keyword_input"
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
        
        if "df_with_selection" not in st.session_state:
            df.insert(0, "선택", False)
            st.session_state.df_with_selection = df
        if "selected_idx_history" not in st.session_state:
            st.session_state.selected_idx_history = []

        # 3. 결과 표시 및 버튼 영역
        col_res_text, col_res_btn1, col_res_btn2 = st.columns([2, 1, 1])
        with col_res_text:
            st.markdown(f"총 **{len(st.session_state.df_with_selection)}**개의 결과가 검색되었습니다.")
        
        with col_res_btn1:
            if not st.session_state.df_with_selection.empty:
                import io
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    export_df = st.session_state.df_with_selection.drop(columns=["발행일_dt"]) if "발행일_dt" in st.session_state.df_with_selection.columns else st.session_state.df_with_selection
                    export_df.to_excel(writer, index=False, sheet_name='Sheet1')
                
                st.download_button(
                    label="엑셀 다운로드",
                    data=buffer.getvalue(),
                    file_name=f"issue_monitoring_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="download_excel"
                )
        
        with col_res_btn2:
            if st.button("🚀 분석 실행", type="primary", use_container_width=True):
                st.session_state.is_analyzing = True
                st.rerun()

        if not st.session_state.df_with_selection.empty:
            # st.data_editor를 사용하여 체크박스 선택 구현
            edited_df = st.data_editor(
                st.session_state.df_with_selection[["선택", "ID", "제목", "유형", "정보원", "발행일"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "선택": st.column_config.CheckboxColumn("선택", default=False, width="small"),
                    "ID": st.column_config.NumberColumn("ID", width="small", disabled=True),
                    "제목": st.column_config.TextColumn("제목", width="large", disabled=True),
                    "유형": st.column_config.TextColumn("유형", disabled=True),
                    "발행일": st.column_config.DateColumn("발행일", disabled=True),
                },
                key="issue_selection_table"
            )

            # 선택 제한 로직 (최대 3개, 초과 시 경고 및 무시)
            if st.session_state.issue_selection_table["edited_rows"]:
                changes = st.session_state.issue_selection_table["edited_rows"]
                
                # 현재 이미 선택된 갯수 확인
                current_selected_count = st.session_state.df_with_selection["선택"].sum()
                
                for idx_str, change in changes.items():
                    idx = int(idx_str)
                    is_trying_to_select = change.get("선택", False)
                    
                    # 새로 선택하려는 경우
                    if is_trying_to_select:
                        # 이미 3개인 상태에서 추가 선택 시도 시
                        if current_selected_count >= 3:
                            st.warning("⚠️ 최대 3개까지만 선택 가능합니다.")
                            # 변경 사항 반영하지 않고 패스 (세션 상태 유지)
                        else:
                            st.session_state.df_with_selection.at[idx, "선택"] = True
                            st.session_state.selected_idx_history.append(idx)
                    # 선택 해제하려는 경우
                    elif "선택" in change and not change["선택"]:
                        st.session_state.df_with_selection.at[idx, "선택"] = False
                        if idx in st.session_state.selected_idx_history:
                            st.session_state.selected_idx_history.remove(idx)
                
                # 강제 리렌더링하여 체크박스 상태 업데이트
                st.rerun()
        else:
            st.info("검색 조건에 맞는 데이터가 없습니다.")

    else:
        st.subheader("이슈 분석 리포트")
        st.markdown("수집된 데이터에 대한 AI 정밀 분석 결과입니다.")
        
        # 테이블 스타일 커스텀 CSS 적용
        st.markdown("""
        <style>
            .issue-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                border: 1px solid #E2E8F0;
                font-family: 'Inter', sans-serif;
            }
            .issue-table th {
                background-color: var(--primary-color);
                color: white;
                padding: 15px;
                text-align: center;
                border: 1px solid var(--primary-color);
                font-size: 18px;
            }
            .issue-table td {
                padding: 20px;
                border: 1px solid #E2E8F0;
                vertical-align: top;
            }
            .label-cell {
                background-color: #F1F5F9;
                color: #1E293B;
                font-weight: 700;
                width: 120px;
                text-align: center;
                vertical-align: middle !important;
            }
            .summary-text {
                line-height: 1.6;
                color: #334155;
                white-space: pre-wrap;
            }
            .url-text {
                color: #2563EB;
                word-break: break-all;
                text-decoration: none;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <table class="issue-table">
            <thead>
                <tr>
                    <th class="label-cell">제목</th>
                    <th>인도 델리, 대기오염 악화로 재택근무 조치 시행</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="label-cell">요약</td>
                    <td class="summary-text">
<strong>□ 델리, 심각한 대기오염으로 재택근무 정책 시행</strong>
- 델리(Delhi)의 대기오염 문제가 지속됨에 따라, 델리 지방정부는 12월 17일부로 민간 및 정부 기관의 50%에 대해 재택근무 조치를 시행함.
- 델리의 대기질 지수(AQI: Air Quality Index)는 '심각(severe)' 수준을 유지하고 있으며, 가시거리 및 항공·철도 교통에 영향을 미치고 있음.

<strong>□ 대기오염 대응 조치 및 피해 노동자 지원</strong>
- 델리 정부는 환경 기준 미달 차량을 금지하고 있으며, 일부 건설 활동을 중단함.
- 카필 미슈라(Kapil Mishra) 델리 지방정부 장관은 금지 조치로 피해를 입은 건설 노동자들에게 1만 루피(약 16만 원)의 보상금을 지급한다고 발표함.

<strong>□ 정부, 대기질 개선 의지 표명</strong>
- 만진더 싱 시르사(Manjinder Singh Sirsa) 델리 환경부장관은 청정한 공기를 제공하겠다는 정부의 의지를 강조함.
- 델리와 인근 지역의 대기오염 문제는 특히 겨울철에 악화되는 것으로 알려져 있으며, 다수 주민들의 호흡기 질환을 초래하고 있음.
                    </td>
                </tr>
                <tr>
                    <td class="label-cell">출처</td>
                    <td><a href="#" class="url-text">https://www.ittefaq.com.bd/766469/E0%A6%AD%E0%A6%AD%E0%A6%AD%E0%A6%AD%E0%A6%AD...</a></td>
                </tr>
            </tbody>
        </table>
        <br>
        """, unsafe_allow_html=True)
