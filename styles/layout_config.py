import streamlit as st

def apply_layout():
    st.set_page_config(
        page_title="SupplyShield 2.0",
        layout="wide",
        page_icon="🚚",
        initial_sidebar_state="expanded"
    )

    # Inject light/dark style
    st.markdown("""
        <style>
        .reportview-container .main {
            background: linear-gradient(to right, #f8f9fa, #e0eafc);
            padding: 2rem;
        }
        .sidebar .sidebar-content {
            background: #f0f2f6;
        }
        .block-container {
            padding-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
