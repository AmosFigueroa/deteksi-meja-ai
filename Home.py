import streamlit as st

st.set_page_config(
    page_title="Sistem Resto AI",
    page_icon="🤖",
)

st.title("👋 Selamat Datang di Smart Resto AI")

st.markdown(
    """
    Aplikasi ini menggunakan Kecerdasan Buatan (AI) untuk memantau restoran secara otomatis.
    
    **Silakan pilih menu di sebelah kiri:**
    * **📹 CCTV Monitor:** Untuk layar monitor di kasir/ruang staff (Real-time Deteksi).
    * **📊 Owner Dashboard:** Untuk pemilik melihat statistik & kinerja pegawai.
    """
)

st.info("👈 Pilih menu di Sidebar untuk memulai.")