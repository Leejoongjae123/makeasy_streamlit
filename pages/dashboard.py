import streamlit as st

def show():
    st.title("대시보드")
    st.markdown("프로젝트 현황 및 시스템 상태 개요입니다.")
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### 프로젝트 A")
            st.markdown("이슈 모니터링 에이전트")
            st.markdown("상태: **활성**")
            if st.button("프로젝트 A 열기", key="go_a", use_container_width=True, type="primary"):
                st.session_state.current_page = "project_a"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 프로젝트 B")
            st.markdown("데이터 분석 리포트")
            st.markdown("상태: **개발 중**")
            if st.button("프로젝트 B 열기", key="go_b", use_container_width=True, type="primary"):
                st.session_state.current_page = "project_b"
                st.rerun()

    with col3:
        with st.container(border=True):
            st.markdown("### 프로젝트 C")
            st.markdown("자동화 워크플로우")
            st.markdown("상태: **대기**")
            if st.button("프로젝트 C 열기", key="go_c", use_container_width=True, type="primary"):
                st.session_state.current_page = "project_c"
                st.rerun()
