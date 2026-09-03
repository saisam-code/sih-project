import plotly.express as px
import streamlit as st

def render_charts():
    df = st.session_state.log
    if df.empty:
        st.info("No events yet.")
        return
    fig1 = px.histogram(df, x="type", color="night", title="Alerts by Type")
    fig2 = px.histogram(df, x="timestamp", title="Alerts Over Time")
    c1, c2 = st.columns(2)
    c1.plotly_chart(fig1, use_container_width=True)
    c2.plotly_chart(fig2, use_container_width=True)