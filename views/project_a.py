import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.data_manager import get_sample_data, get_supabase_data, get_categories, get_sources
from utils.gemini_client import summarize_issues

def show():
    st.title("프로젝트 A - 이슈 모니터링 에이전트")
    st.markdown("이슈 수집 및 정밀 분석을 수행합니다.")
    st.divider()

    # 세션 상태 초기화 및 탭 제어 로직
    if "project_a_tab" not in st.session_state:
        st.session_state.project_a_tab = "이슈 수집"
    if "is_analyzing" not in st.session_state:
        st.session_state.is_analyzing = False
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None

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

        # 선택된 항목 수집
        selected_df = st.session_state.df_with_selection[st.session_state.df_with_selection["선택"] == True]

        if len(selected_df) > 0:
            issues_data = []
            for _, row in selected_df.iterrows():
                issues_data.append({
                    'title': row['제목'],
                    'content': row['내용'],
                    'source_url': row.get('source_url', '')
                })

            try:
                # Gemini API 호출
                result = summarize_issues(issues_data)
                st.session_state.analysis_result = result
            except Exception as e:
                st.session_state.analysis_result = {
                    'title': '분석 실패',
                    'summary': f'AI 분석 중 오류가 발생했습니다: {str(e)}',
                    'sources': []
                }

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
        # Supabase에서 동적으로 카테고리와 정보원 로드
        categories = get_categories()
        sources_dict, source_names, _ = get_sources()

        # 1. 검색 필터 섹션
        with st.container(border=True):
            st.markdown("### 검색 필터")

            col1, col2 = st.columns(2)

            with col1:
                # 유형 (Type) - Supabase에서 가져온 카테고리 사용
                type_options = st.multiselect(
                    "유형",
                    categories,
                    default=[]  # 기본값 없음 - 모든 유형 표시
                )

                # 정보원 (Source) - Supabase에서 가져온 정보원 사용
                source_options = st.multiselect(
                    "정보원",
                    source_names,
                    default=[]  # 기본값 없음 - 모든 정보원 표시
                )

            with col2:
                # 수집일 범위 (Start Date & End Date)
                st.markdown("<p style='font-size: 14px; font-weight: 500; margin-bottom: 2px;'>수집일 범위</p>", unsafe_allow_html=True)
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

                # 제목 검색
                title_search = st.text_input(
                    "제목 검색",
                    placeholder="검색할 제목을 입력하세요...",
                    key="title_search_input"
                )

            search_btn = st.button("검색 실행", type="primary", use_container_width=True)

        st.divider()

        # 2. Supabase에서 필터링된 데이터 가져오기
        df = get_supabase_data(
            type_filters=type_options if type_options else None,
            source_filters=source_options if source_options else None,
            start_date=start_date,
            end_date=end_date,
            title_search=title_search if title_search else None
        )

        # 검색 버튼을 눌렀을 때 세션 상태 업데이트
        if search_btn or "df_with_selection" not in st.session_state:
            df.insert(0, "선택", False)
            st.session_state.df_with_selection = df
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
            selected_count = st.session_state.df_with_selection["선택"].sum() if not st.session_state.df_with_selection.empty else 0
            if selected_count == 0:
                st.button("🚀 분석 실행", type="primary", use_container_width=True, disabled=True)
                st.caption("⚠️ 분석할 항목을 선택하세요 (최대 3개)")
            elif selected_count > 3:
                st.button("🚀 분석 실행", type="primary", use_container_width=True, disabled=True)
                st.caption("⚠️ 최대 3개까지만 선택 가능합니다")
            else:
                if st.button("🚀 분석 실행", type="primary", use_container_width=True):
                    st.session_state.is_analyzing = True
                    st.rerun()

        if not st.session_state.df_with_selection.empty:
            # st.data_editor를 사용하여 체크박스 선택 구현
            edited_df = st.data_editor(
                st.session_state.df_with_selection[["선택", "ID", "제목", "유형", "정보원", "수집일"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "선택": st.column_config.CheckboxColumn("선택", default=False, width="small"),
                    "ID": st.column_config.NumberColumn("ID", width="small", disabled=True),
                    "제목": st.column_config.TextColumn("제목", width="large", disabled=True),
                    "유형": st.column_config.TextColumn("유형", disabled=True),
                    "수집일": st.column_config.DateColumn("수집일", disabled=True),
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
                        else:
                            st.session_state.df_with_selection.at[idx, "선택"] = True
                            st.session_state.selected_idx_history.append(idx)
                    # 선택 해제하려는 경우
                    elif "선택" in change and not change["선택"]:
                        st.session_state.df_with_selection.at[idx, "선택"] = False
                        if idx in st.session_state.selected_idx_history:
                            st.session_state.selected_idx_history.remove(idx)

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
                border: 1px solid rgba(128, 128, 128, 0.2);
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
                border: 1px solid rgba(128, 128, 128, 0.2);
                vertical-align: top;
            }
            .label-cell {
                background-color: var(--secondary-background-color);
                color: var(--text-color);
                font-weight: 700;
                width: 120px;
                text-align: center;
                vertical-align: middle !important;
            }
            .summary-text {
                line-height: 1.6;
                color: var(--text-color);
                white-space: pre-wrap;
            }
            .url-text {
                color: #3B82F6;
                word-break: break-all;
                text-decoration: none;
            }
            .source-list {
                line-height: 1.8;
            }
        </style>
        """, unsafe_allow_html=True)

        # 분석 결과가 있으면 표시
        if st.session_state.analysis_result:
            result = st.session_state.analysis_result
            title = result.get('title', '분석 결과')
            summary = result.get('summary', '요약 내용이 없습니다.')
            sources = result.get('sources', [])

            # 출처 URL 포맷팅
            sources_html = ""
            if sources:
                for url in sources:
                    if url:
                        sources_html += f'<a href="{url}" class="url-text" target="_blank">{url}</a><br>'
            else:
                sources_html = '<span style="color: var(--text-color); opacity: 0.6;">출처 정보가 없습니다.</span>'

            st.markdown(f"""
            <table class="issue-table">
                <thead>
                    <tr>
                        <th class="label-cell">제목</th>
                        <th>{title}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="label-cell">요약</td>
                        <td class="summary-text">{summary}</td>
                    </tr>
                    <tr>
                        <td class="label-cell">출처</td>
                        <td class="source-list">{sources_html}</td>
                    </tr>
                </tbody>
            </table>
            <br>
            """, unsafe_allow_html=True)
        else:
            st.info("분석할 이슈를 선택하고 '분석 실행' 버튼을 클릭하세요.")
            st.markdown("""
            <table class="issue-table">
                <thead>
                    <tr>
                        <th class="label-cell">제목</th>
                        <th>분석 대기 중</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="label-cell">요약</td>
                        <td class="summary-text" style="color: var(--text-color); opacity: 0.6;">
                            이슈 수집 탭에서 분석할 항목을 선택(최대 3개)한 후,
                            '🚀 분석 실행' 버튼을 클릭하면 AI가 자동으로 요약합니다.
                        </td>
                    </tr>
                    <tr>
                        <td class="label-cell">출처</td>
                        <td><span style="color: var(--text-color); opacity: 0.6;">분석 후 출처 URL이 표시됩니다.</span></td>
                    </tr>
                </tbody>
            </table>
            <br>
            """, unsafe_allow_html=True)
