import streamlit as st

def show():
    st.title("프로젝트 C - 자동화")
    st.markdown("워크플로우 관리 및 작업 스케줄링을 담당합니다.")
    st.divider()

    st.warning("자동화 시스템은 현재 베타 버전입니다.")

    with st.expander("활성 워크플로우", expanded=True):
        st.write("1. 데일리 웹 크롤링 - **실행 중**")
        st.write("2. AI 키워드 추출 - **대기**")
        st.write("3. 데이터베이스 동기화 - **예약됨**")

    if st.button("수동 동기화 실행", type="primary"):
        st.success("수동 동기화가 성공적으로 시작되었습니다.")
