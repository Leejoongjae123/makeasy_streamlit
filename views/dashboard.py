import streamlit as st

def show():
    st.title("대시보드")
    st.markdown("프로젝트 현황 및 시스템 상태 개요입니다.")
    st.divider()

    # 모든 카드의 높이를 강제로 통일하기 위한 CSS
    st.markdown("""
        <style>
            /* 컨테이너 자체의 높이를 통일 */
            div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorder"] {
                min-height: 280px !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: space-between !important;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown(f"""
                <div style="padding: 5px; font-family: 'Inter', sans-serif;">
                    <h3 style="color: var(--primary-color); font-size: 20px; margin-bottom: 15px;">이슈 모니터링 에이전트</h3>
                    <ul style="list-style-type: none; padding-left: 0; font-size: 15px; line-height: 1.8; color: var(--text-main);">
                        <li>• <b>(목적)</b> 글로벌 이슈 조사</li>
                        <li>• <b>(정보원)</b> 미디어, 정부공지</li>
                        <li>• <b>(상태)</b> 동작중</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("프로젝트 A 열기", key="go_a", use_container_width=True, type="primary"):
                st.session_state.current_page = "project_a"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown(f"""
                <div style="padding: 5px; font-family: 'Inter', sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
                    <h3 style="color: var(--text-muted); font-size: 20px; margin-bottom: 10px; margin-top: 20px;">데이터 분석 에이전트</h3>
                    <p style="color: var(--text-muted); font-size: 15px;">서비스 준비 중입니다.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.button("프로젝트 B 열기", key="go_b", use_container_width=True, type="secondary", disabled=True)

    with col3:
        with st.container(border=True):
            st.markdown(f"""
                <div style="padding: 5px; font-family: 'Inter', sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
                    <h3 style="color: var(--text-muted); font-size: 20px; margin-bottom: 10px; margin-top: 20px;">자동화 워크플로우</h3>
                    <p style="color: var(--text-muted); font-size: 15px;">서비스 준비 중입니다.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.button("프로젝트 C 열기", key="go_c", use_container_width=True, type="secondary", disabled=True)
