import streamlit as st
import cv2
import av
import numpy as np
from ultralytics import YOLO
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Realtime CCTV AI", layout="wide")
st.title("📹 Deteksi Meja Real-time")

# --- 2. LOAD MODEL AI ---
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")

# --- 3. CLASS PEMROSES VIDEO ---
# Class ini bertugas menerima frame video satu per satu dan memprosesnya
class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        # Default setting meja (akan diupdate dari slider)
        self.meja_coords = (100, 200, 300, 400) # x1, y1, x2, y2
        self.model = model

    def recv(self, frame):
        # 1. Konversi frame dari format Web ke OpenCV
        img = frame.to_ndarray(format="bgr24")
        
        # 2. Deteksi Orang dengan YOLO
        results = self.model.predict(img, classes=0, conf=0.5, verbose=False)
        
        orang_terdeteksi = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                bx1, by1, bx2, by2 = map(int, box.xyxy[0])
                cx, cy = (bx1 + bx2) // 2, by2  # Titik kaki
                orang_terdeteksi.append((cx, cy))
                
                # Gambar kotak ungu di orang
                cv2.rectangle(img, (bx1, by1), (bx2, by2), (255, 0, 255), 2)

        # 3. Logika Status Meja
        mx1, my1, mx2, my2 = self.meja_coords
        status = "KOSONG"
        warna_kotak = (0, 255, 0) # Hijau

        for orang in orang_terdeteksi:
            ox, oy = orang
            # Cek apakah kaki orang ada di dalam kotak meja
            if mx1 < ox < mx2 and my1 < oy < my2:
                status = "TERISI"
                warna_kotak = (0, 0, 255) # Merah
                break
        
        # 4. Gambar Kotak Meja & Status
        cv2.rectangle(img, (mx1, my1), (mx2, my2), warna_kotak, 3)
        cv2.putText(img, f"Status: {status}", (mx1, my1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, warna_kotak, 2)

        # 5. Kembalikan gambar yang sudah dicoret-coret ke layar
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- 4. TAMPILAN SIDEBAR ---
st.sidebar.header("🛠️ Setting Area")
x_pos = st.sidebar.slider("Posisi X (Kiri-Kanan)", 0, 640, 100)
y_pos = st.sidebar.slider("Posisi Y (Atas-Bawah)", 0, 480, 200)
lebar = st.sidebar.slider("Lebar", 50, 400, 200)
tinggi = st.sidebar.slider("Tinggi", 50, 400, 200)

# --- 5. MENJALANKAN STREAMING ---
st.write("Klik **START** di bawah untuk memulai kamera.")

# Menjalankan WebRTC
ctx = webrtc_streamer(
    key="example", 
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# --- 6. UPDATE POSISI MEJA REALTIME ---
# Kode ini mengirim nilai slider ke dalam proses video yang sedang berjalan
if ctx.video_transformer:
    ctx.video_transformer.meja_coords = (x_pos, y_pos, x_pos + lebar, y_pos + tinggi)