import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --primary-color: #1F2C5C;
            --background-light: #F8FAFC;
            --border-color: #E2E8F0;
            --text-main: #1E293B;
            --text-muted: #64748B;
        }

        /* 전역 글꼴 설정 */
        .main .block-container {
            font-family: 'Inter', sans-serif;
        }

        /* 사이드바 스타일 */
        [data-testid="stSidebar"] {
            background-color: var(--background-light);
            border-right: 1px solid var(--border-color);
        }

        /* 사이드바 내의 마크다운 텍스트 */
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #475569 !important;
        }

        /* 사이드바 내의 버튼 스타일 재정의 */
        [data-testid="stSidebar"] .stButton button {
            background-color: transparent;
            color: var(--text-muted);
            border: none;
            border-radius: 6px;
            padding: 8px 12px;
            text-align: left;
            font-weight: 500;
            font-size: 15px;
            transition: all 0.2s ease;
            margin-bottom: 2px;
            display: block;
            width: 100%;
        }

        [data-testid="stSidebar"] .stButton button:hover {
            background-color: #F1F5F9;
            color: var(--text-main);
        }

        /* 활성화된 버튼 스타일 (Primary) */
        [data-testid="stSidebar"] .stButton button[kind="primary"] {
            background-color: #F1F5F9 !important;
            color: var(--primary-color) !important;
            font-weight: 600;
            border-left: 3px solid var(--primary-color) !important;
            border-radius: 0 6px 6px 0;
        }

        /* 로고 영역 스타일 */
        .sidebar-header {
            padding: 10px 0 20px 0;
            margin-bottom: 10px;
            border-bottom: 1px solid var(--border-color);
        }

        /* 카드 스타일 */
        .stElementContainer div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: white;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        .stElementContainer div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.05);
            border-color: var(--primary-color) !important;
        }

        /* 버튼 스타일 */
        .stButton > button[kind="primary"] {
            background-color: var(--primary-color);
            color: white;
            border-radius: 6px;
            border: none;
        }

        h1, h2, h3 {
            color: var(--text-main);
            font-weight: 700 !important;
        }

        /* 엑셀 다운로드 버튼 전용 스타일 */
        div[data-testid="stDownloadButton"] > button {
            border: 1px solid #10B981 !important;
            color: #10B981 !important;
            background-color: white !important;
            transition: all 0.2s ease;
        }

        div[data-testid="stDownloadButton"] > button:hover {
            background-color: #F0FDF4 !important;
            border-color: #059669 !important;
            color: #059669 !important;
            transform: translateY(-1px);
        }

        /* 기본 사이드바 내비게이션 숨기기 */
        [data-testid="stSidebarNav"] {
            display: none;
        }

        /* 탭 스타일 개선 */
        [data-testid="stTabs"] {
            margin-bottom: 20px;
        }

        button[data-testid="stTab"] {
            height: 50px;
            padding: 0 30px !important;
            background-color: transparent !important;
            border: none !important;
            transition: all 0.3s ease;
        }

        /* 탭 아래의 기본 붉은 선 및 강조선 제거/수정 */
        div[data-baseweb="tab-highlight"] {
            background-color: var(--primary-color) !important;
        }

        button[data-testid="stTab"] p {
            font-size: 18px !important;
            font-weight: 500 !important;
            color: var(--text-muted) !important;
        }

        /* 선택된 탭 스타일 */
        button[data-testid="stTab"][aria-selected="true"] {
            border-bottom: 3px solid var(--primary-color) !important;
        }

        button[data-testid="stTab"][aria-selected="true"] p {
            color: var(--primary-color) !important;
            font-weight: 700 !important;
        }

        /* 호버 시 스타일 */
        button[data-testid="stTab"]:hover p {
            color: var(--primary-color) !important;
        }

        /* 멀티셀렉트(Multiselect) 배지 스타일 - 아웃라인 스타일 커스텀 */
        span[data-baseweb="tag"] {
            background-color: white !important;
            color: var(--primary-color) !important;
            border: 1px solid var(--primary-color) !important;
            border-radius: 4px !important;
        }

        span[data-baseweb="tag"] [data-testid="stIcon"] {
            color: var(--primary-color) !important;
        }

        /* 메인 콘텐츠 상단 패딩 축소 */
        .block-container {
            padding-top: 3rem !important;
            padding-bottom: 2rem !important;
        }

        /* 탭 포커스 시 나타나는 붉은 아웃라인 제거 */
        button[data-testid="stTab"]:focus {
            box-shadow: none !important;
            color: var(--primary-color) !important;
        }
    </style>
    """, unsafe_allow_html=True)
