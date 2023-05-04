import streamlit as st


def app_base_config():
    st.set_page_config(
        page_title="Talk Business",
        initial_sidebar_state="expanded",
        layout="wide",
        page_icon="talk_business/assets/favicon.png",
    )


def load_css(file_name: str) -> None:
    """Import a CSS file into the Streamlit app."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)