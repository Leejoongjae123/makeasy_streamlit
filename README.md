# 🚀 크롤마스터 (CrawlMaster) - 유니버셜 크롤링 대시보드

이 프로젝트는 **Streamlit**을 기반으로 구축된 현대적이고 세련된 디자인의 고성능 크롤링 매니지먼트 대시보드입니다. 다양한 소스에서 수집된 데이터를 통합 관리하고 분석할 수 있는 기능을 제공합니다.

## ✨ 주요 기능

- **📊 대시보드**: 전체 프로젝트의 활성 상태 및 핵심 지표 한눈에 파악
- **🔍 프로젝트 A (이슈 모니터링)**:
  - 상세 검색 필터 (발행일 범위, 유형, 정보원, 키워드)
  - 필터링된 결과의 **실시간 엑셀 다운로드** 지원
- **📈 프로젝트 B (데이터 분석)**: 수집된 데이터의 다각도 시각화 및 리포트 (개발 중)
- **🤖 프로젝트 C (자동화)**: 워크플로우 관리 및 수동 동기화 스케줄링 (베타)
- **🎨 프리미엄 UI/UX**:
  - `Inter` 폰트 및 커스텀 CSS 적용
  - 깔끔한 사이드바 네비게이션 및 미니멀 라이트 테마
  - `#1F2C5C` 메인 컬러 기반의 세련된 디자인 시스템

## 📂 프로젝트 구조

```text
206_2.universial_crwaling_streamlit/
├── main.py                 # 앱 엔트리 포인트 및 라우터
├── components/
│   └── sidebar.py          # 사이드바 공통 컴포넌트
├── pages/
│   ├── dashboard.py        # 대시보드 홈
│   ├── project_a.py        # 프로젝트 A (이슈 모니터링)
│   ├── project_b.py        # 프로젝트 B (데이터 분석)
│   └── project_c.py        # 프로젝트 C (자동화)
├── utils/
│   ├── styles.py           # 커스텀 테마 및 디자인 시스템
│   └── data_manager.py     # 데이터 로딩 및 관리 유틸리티
└── README.md
```

## 🛠️ 기술 스택

- **Core**: Python, Streamlit
- **Data**: Pandas
- **Export**: XlsxWriter
- **Styling**: Vanilla CSS (Streamlit Markdown)

## 🚀 빠른 시작

1. 저장소를 클론합니다.
   ```bash
   git clone https://github.com/Leejoongjae123/makeasy_streamlit.git
   cd makeasy_streamlit
   ```

2. 필수 라이브러리를 설치합니다.
   ```bash
   pip install streamlit pandas xlsxwriter
   ```

3. 애플리케이션을 실행합니다.
   ```bash
   streamlit run main.py
   ```

## 📝 라이선스

이 프로젝트는 개인/학습용 프로젝트로 자유롭게 수정 및 배포가 가능합니다.
