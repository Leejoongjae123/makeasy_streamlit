import streamlit as st

def sidebar_menu_btn(label, page_key, current_page):
    is_active = current_page == page_key
    btn_type = "primary" if is_active else "secondary"
    if st.button(label, key=f"nav_{page_key}", use_container_width=True, type=btn_type):
        st.session_state.current_page = page_key
        st.rerun()

def render_sidebar():
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-header">
                <h3 style='margin: 0; color: #1E293B; font-size: 18px; letter-spacing: -0.5px;'>
                    정보 분석 에이전트
                </h3>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin: 20px 0 10px 4px; color: #94A3B8; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>메인 메뉴</div>", unsafe_allow_html=True)
        sidebar_menu_btn("대시보드", "dashboard", st.session_state.current_page)
        
        st.markdown("<div style='margin: 20px 0 10px 4px; color: #94A3B8; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>프로젝트</div>", unsafe_allow_html=True)
        sidebar_menu_btn("프로젝트 A", "project_a", st.session_state.current_page)
        sidebar_menu_btn("프로젝트 B", "project_b", st.session_state.current_page)
        sidebar_menu_btn("프로젝트 C", "project_c", st.session_state.current_page)

        st.markdown("<div style='margin-top: 60px; padding-left: 4px; color: #94A3B8; font-size: 11px;'>v1.2.0 • 안정화 버전</div>", unsafe_allow_html=True)
