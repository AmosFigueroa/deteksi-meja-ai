import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Deteksi Meja AI", layout="wide")

st.title("🕵️ Deteksi Ketersediaan Meja (Web Version)")
st.write("Arahkan kamera ke kursi/meja, atur kotak area, lalu lihat hasilnya!")

# --- 1. LOAD MODEL AI ---
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

try:
    model = load_model()
except Exception as e:
    st.error(f"Gagal memuat model: {e}")

# --- 2. SIDEBAR: PENGATURAN MEJA ---
st.sidebar.header("🛠️ Setting Area Meja")
st.sidebar.info("Geser slider di bawah ini untuk pasang kotak hijau di kursimu.")

# Menggunakan Slider sebagai pengganti mouse click
# Kita asumsikan resolusi kamera default web adalah 640x480
x_pos = st.sidebar.slider("Posisi Kiri-Kanan (X)", 0, 640, 150)
y_pos = st.sidebar.slider("Posisi Atas-Bawah (Y)", 0, 480, 200)
lebar = st.sidebar.slider("Lebar Kotak", 50, 400, 200)
tinggi = st.sidebar.slider("Tinggi Kotak", 50, 400, 200)

# Koordinat Meja [x1, y1, x2, y2]
meja_x1, meja_y1 = x_pos, y_pos
meja_x2, meja_y2 = x_pos + lebar, y_pos + tinggi

# --- 3. INPUT KAMERA ---
img_file = st.camera_input("Ambil Foto untuk Deteksi")

if img_file is not None:
    # Konversi gambar dari Browser ke format OpenCV
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)
    
    # --- 4. PROSES AI ---
    # Deteksi orang (class=0)
    results = model.predict(frame, classes=0, conf=0.4)
    
    orang_terdeteksi = []
    
    # Ambil data hasil deteksi
    for result in results:
        boxes = result.boxes
        for box in boxes:
            bx1, by1, bx2, by2 = map(int, box.xyxy[0])
            
            # Titik tengah kaki (agar akurat saat duduk)
            cx = (bx1 + bx2) // 2
            cy = by2 
            orang_terdeteksi.append((cx, cy))
            
            # Gambar kotak ungu di sekitar orang
            cv2.rectangle(frame, (bx1, by1), (bx2, by2), (255, 0, 255), 2)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 255), -1)

    # --- 5. LOGIKA STATUS MEJA ---
    status = "KOSONG"
    warna_kotak = (0, 255, 0) # Hijau
    
    # Cek apakah ada orang di dalam kotak meja yg kita buat di sidebar
    for orang in orang_terdeteksi:
        ox, oy = orang
        if meja_x1 < ox < meja_x2 and meja_y1 < oy < meja_y2:
            status = "TERISI"
            warna_kotak = (0, 0, 255) # Merah
            break
            
    # Gambar Kotak Meja
    cv2.rectangle(frame, (meja_x1, meja_y1), (meja_x2, meja_y2), warna_kotak, 3)
    cv2.putText(frame, f"Meja: {status}", (meja_x1, meja_y1 - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, warna_kotak, 2)

    # --- 6. TAMPILKAN HASIL ---
    # Ubah warna BGR (OpenCV) ke RGB (Streamlit) agar warnanya benar
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    st.image(frame_rgb, caption="Hasil Analisis AI", use_column_width=True)
    
    if status == "KOSONG":
        st.success("✅ Meja Kosong! Silakan duduk.")
    else:
        st.error("❌ Meja Terisi! Cari tempat lain.")

else:
    st.warning("Silakan izinkan akses kamera dan klik 'Take Photo'")