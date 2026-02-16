import streamlit as st

def show():
    st.title("프로젝트 C - 자동화 워크플로우")
    st.divider()
    
    st.info("💡 본 서비스는 초기 기획 단계이며, 곧 업데이트될 예정입니다.")
    
    st.markdown("""
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 400px; text-align: center;">
            <div style="font-size: 80px; margin-bottom: 20px;">🏗️</div>
            <h2 style="color: var(--text-muted);">서비스 준비 중</h2>
            <p style="color: var(--text-muted); font-size: 18px; max-width: 500px;">
                복잡한 수집 환경을 자동화하고 관리하는 통합 워크플로우 시스템을 준비하고 있습니다. 
                보다 안정적인 스케줄링을 위해 개선 작업 중입니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
