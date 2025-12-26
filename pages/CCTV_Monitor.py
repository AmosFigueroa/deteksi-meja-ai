import streamlit as st
import cv2
import av
import numpy as np
from ultralytics import YOLO
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.set_page_config(page_title="CCTV Monitor", layout="wide")

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

try:
    model = load_model()
except Exception as e:
    st.error(f"Error: {e}")

# --- PROCESSOR CLASS ---
class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.meja_coords = (100, 200, 300, 400)
        self.model = model

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Deteksi
        results = self.model.predict(img, classes=0, conf=0.5, verbose=False)
        orang_terdeteksi = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                bx1, by1, bx2, by2 = map(int, box.xyxy[0])
                cx, cy = (bx1 + bx2) // 2, by2
                orang_terdeteksi.append((cx, cy))
                cv2.rectangle(img, (bx1, by1), (bx2, by2), (255, 0, 255), 2)

        # Logika Meja
        mx1, my1, mx2, my2 = self.meja_coords
        status = "KOSONG"
        warna = (0, 255, 0)
        
        for orang in orang_terdeteksi:
            if mx1 < orang[0] < mx2 and my1 < orang[1] < my2:
                status = "TERISI"
                warna = (0, 0, 255)
                break
        
        cv2.rectangle(img, (mx1, my1), (mx2, my2), warna, 3)
        cv2.putText(img, f"Status: {status}", (mx1, my1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, warna, 2)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- UI HALAMAN ---
st.title("📹 CCTV Live Monitor")
col1, col2 = st.columns([3, 1])

with col1:
    ctx = webrtc_streamer(
        key="cctv", 
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

with col2:
    st.write("### ⚙️ Setting Area")
    x = st.slider("X", 0, 640, 100)
    y = st.slider("Y", 0, 480, 200)
    w = st.slider("Lebar", 50, 400, 200)
    h = st.slider("Tinggi", 50, 400, 200)
    
    if ctx.video_transformer:
        ctx.video_transformer.meja_coords = (x, y, x+w, y+h)