import streamlit as st
import pandas as pd
import altair as alt
import random

st.set_page_config(page_title="Owner Dashboard", layout="wide")

st.title("📊 Owner Dashboard")

# --- PASSWORD PROTECTION ---
pwd = st.text_input("🔑 Masukkan Password Owner", type="password")

if pwd == "admin123":
    # --- DATA DUMMY (SIMULASI) ---
    st.success("Login Berhasil!")
    
    # 1. Ringkasan
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Pengunjung", "128", "+10%")
    c2.metric("Total Omset", "Rp 3.200.000", "+5%")
    c3.metric("Rating Layanan", "4.8/5.0", "⭐")
    
    st.divider()
    
    # 2. Grafik
    st.subheader("Tren Keramaian")
    data = pd.DataFrame({
        'Jam': [f'{i}:00' for i in range(10, 22)],
        'Pengunjung': [random.randint(10, 60) for _ in range(12)]
    })
    
    chart = alt.Chart(data).mark_area(color='lightblue').encode(
        x='Jam', y='Pengunjung'
    )
    st.altair_chart(chart, use_container_width=True)
    
    # 3. Absensi
    st.subheader("Daftar Pegawai")
    pegawai = pd.DataFrame({
        "Nama": ["Ali", "Budi", "Citra"],
        "Shift": ["Pagi", "Siang", "Malam"],
        "Status": ["Hadir", "Hadir", "Izin"]
    })
    st.dataframe(pegawai, use_container_width=True)

else:
    if pwd != "admin123":
        st.error("Password Salah!")