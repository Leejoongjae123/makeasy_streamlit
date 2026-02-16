import streamlit as st

def show():
    st.title("프로젝트 B - 데이터 분석 에이전트")
    st.divider()
    
    st.info("💡 본 서비스는 초기 기획 단계이며, 곧 업데이트될 예정입니다.")
    
    st.markdown("""
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 400px; text-align: center;">
            <div style="font-size: 80px; margin-bottom: 20px;">🏗️</div>
            <h2 style="color: var(--text-muted);">서비스 준비 중</h2>
            <p style="color: var(--text-muted); font-size: 18px; max-width: 500px;">
                데이터를 다각도로 분석하고 시각화 리포트를 생성하는 에이전트 기능을 개발하고 있습니다. 
                더 나은 분석 환경을 위해 조금만 기다려 주세요!
            </p>
        </div>
    """, unsafe_allow_html=True)
