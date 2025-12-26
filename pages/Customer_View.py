import streamlit as st
import time
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Selamat Datang", 
    page_icon="🍴",
    layout="centered" # Tampilan HP lebih cocok centered
)

# --- CSS CUSTOM (Agar tampilan lebih cantik) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
    }
    .status-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🍴 Resto Pintar")
st.write("Selamat datang! Silakan cek meja dan menu favoritmu.")

# --- NAVIGASI TAB (PILIHAN MENU) ---
tab1, tab2, tab3 = st.tabs(["🪑 Cari Meja", "🍔 Menu", "🎉 Promo"])

# ===========================
# TAB 1: STATUS MEJA (DENAH)
# ===========================
with tab1:
    st.header("Denah Ketersediaan Meja")
    st.caption("Data diperbarui secara real-time dari CCTV.")
    
    if st.button("🔄 Refresh Status Meja"):
        st.toast("Memuat data terbaru...")
        time.sleep(1)

    # --- SIMULASI KONEKSI DATA ---
    # Catatan: Nanti ini kita sambungkan ke Database agar sinkron dengan CCTV
    # Sekarang kita pakai random dulu untuk contoh tampilan
    status_meja_1 = random.choice(["KOSONG", "TERISI"])
    status_meja_2 = random.choice(["KOSONG", "TERISI"])
    status_meja_3 = "KOSONG" # Ceritanya meja 3 selalu kosong

    # Layout Grid 2 Kolom
    col1, col2 = st.columns(2)

    with col1:
        # MEJA 1
        warna = "green" if status_meja_1 == "KOSONG" else "red"
        st.markdown(f"""
            <div class="status-box" style="background-color: {warna};">
                <h3>MEJA 1</h3>
                <p>{status_meja_1}</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # MEJA 2
        warna = "green" if status_meja_2 == "KOSONG" else "red"
        st.markdown(f"""
            <div class="status-box" style="background-color: {warna};">
                <h3>MEJA 2</h3>
                <p>{status_meja_2}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # MEJA 3 (Baris Baru)
    st.markdown(f"""
        <div class="status-box" style="background-color: green;">
            <h3>MEJA 3 (VIP)</h3>
            <p>KOSONG</p>
        </div>
    """, unsafe_allow_html=True)

    st.info("🟢 Hijau = Silakan Duduk | 🔴 Merah = Penuh")

# ===========================
# TAB 2: MENU MAKANAN
# ===========================
with tab2:
    st.header("Daftar Menu Favorit")
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.image("https://source.unsplash.com/200x200/?fried-rice", caption="Nasi Goreng Spesial")
        st.write("**Rp 25.000**")
        st.button("Pesan", key="btn1")
        
    with col_m2:
        st.image("https://source.unsplash.com/200x200/?ice-tea", caption="Es Teh Manis Jumbo")
        st.write("**Rp 5.000**")
        st.button("Pesan", key="btn2")

    st.divider()
    with col_m1:
        st.image("https://source.unsplash.com/200x200/?satay", caption="Sate Ayam Madura")
        st.write("**Rp 30.000**")
        st.button("Pesan", key="btn3")

# ===========================
# TAB 3: PROMO
# ===========================
with tab3:
    st.image("https://source.unsplash.com/600x300/?restaurant-promotion", use_column_width=True)
    st.subheader("Promo Jumat Berkah!")
    st.write("Diskon 50% untuk pembelian kedua Nasi Goreng.")
    st.success("Kode Voucher: JUMAT50")