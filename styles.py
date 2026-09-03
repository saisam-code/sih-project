import streamlit as st

def apply_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: #eee; }
        h1, h2, h3 { color: #ff4b4b; }
        </style>
    """, unsafe_allow_html=True)