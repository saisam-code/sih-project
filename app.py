import streamlit as st
import cv2
import tempfile
from detector import Detector
from dashboard import init_log, add_alerts, render_log_panel
from charts import render_charts
from styles import apply_style

st.set_page_config(page_title="IBVAP", layout="wide")
apply_style()
init_log()

st.title("🛰 IBVAP — Intelligent Border Video Analytics Platform")

source = st.sidebar.radio("Video Source", ["Sample Video", "Upload Video", "Webcam"])
run = st.sidebar.toggle("Start Analysis")

if "detector" not in st.session_state:
    st.session_state.detector = Detector()

video_path = "sample.mp4"
if source == "Upload Video":
    f = st.sidebar.file_uploader("Upload", type=["mp4", "avi", "mov"])
    if f:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tmp.write(f.read())
        video_path = tmp.name
elif source == "Webcam":
    video_path = 0

col1, col2 = st.columns([2, 1])
frame_slot = col1.empty()
with col2:
    render_log_panel()

if run:
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        frame, alerts, night = st.session_state.detector.process(frame)
        add_alerts(alerts)
        frame_slot.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
    cap.release()

st.divider()
render_charts()