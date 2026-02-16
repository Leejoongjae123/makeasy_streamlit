import streamlit as st
from utils.styles import apply_custom_css
from components.sidebar import render_sidebar
from views import dashboard, project_a, project_b, project_c

# Basic Page Config
st.set_page_config(
    page_title="CrawlMaster Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Styles
apply_custom_css()

# Session State Initialization
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

# Render Sidebar
render_sidebar()

# Main Router
def main():
    if st.session_state.current_page == "dashboard":
        dashboard.show()
    elif st.session_state.current_page == "project_a":
        project_a.show()
    elif st.session_state.current_page == "project_b":
        project_b.show()
    elif st.session_state.current_page == "project_c":
        project_c.show()

if __name__ == "__main__":
    main()
