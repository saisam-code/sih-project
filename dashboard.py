import pandas as pd
import streamlit as st
from datetime import datetime

def init_log():
    if "log" not in st.session_state:
        st.session_state.log = pd.DataFrame(
            columns=["timestamp", "type", "track_id", "class", "night", "confidence"])

def add_alerts(alerts):
    if not alerts:
        return
    rows = [{**a, "timestamp": datetime.now().strftime("%H:%M:%S")} for a in alerts]
    st.session_state.log = pd.concat([st.session_state.log, pd.DataFrame(rows)], ignore_index=True)

def render_log_panel():
    st.subheader("🚨 Alerts")
    st.metric("Total Violations", len(st.session_state.log))
    st.dataframe(st.session_state.log.tail(10), use_container_width=True)
    csv = st.session_state.log.to_csv(index=False).encode()
    st.download_button("Export CSV", csv, "ibvap_events.csv", "text/csv")