import streamlit as st
from supabase import create_client

# Konfigurasi Halaman
st.set_page_config(page_title="Tutor AI Bimbel TPA", page_icon="📝")

# Inisialisasi Klien Supabase
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# Inisialisasi Memori Sesi
if 'sudah_masuk' not in st.session_state:
    st.session_state['sudah_masuk'] = False

# ==========================================
# PORTAL AKSES
# ==========================================
if not st.session_state['sudah_masuk']:
    st.title("Portal Akses Bimbingan Belajar TPA")
    
    tab_masuk, tab_daftar = st.tabs(["Masuk ke Sistem", "Pendaftaran Pengguna Baru"])
    
    with tab_masuk:
        nama_pengguna = st.text_input("Nama Pengguna (Username)", key="log_nama")
        kata_sandi = st.text_input("Kata Sandi", type="password", key="log_sandi")
        if st.button("Masuk"):
            try:
                # Menggunakan nama tabel huruf kecil
                respons = supabase.table('tabel_peserta').select("*").eq("nama_akun", nama_pengguna).execute()
                if respons.data and respons.data[0]['kata_sandi'] == kata_sandi:
                    st.session_state.update({'sudah_masuk': True, 'nama_aktif': respons.data[0]['nama_lengkap'], 'kategori_pendidikan': respons.data[0]['kategori_pendidikan']})
                    st.rerun()
                else:
                    st.error("Identitas atau kata sandi tidak valid.")
            except Exception as e:
                st.error(f"Koneksi gagal: {e}")

    with tab_daftar:
        nama_lengkap = st.text_input("Nama Lengkap")
        kategori = st.selectbox("Tingkat Pendidikan", ["SMP", "SMA", "Mahasiswa", "Umum"])
        institusi = st.text_input("Asal Sekolah / Universitas")
        nama_baru = st.text_input("Username Baru")
        sandi_baru = st.text_input("Kata Sandi Baru", type="password")
        
        if st.button("Daftar Sekarang"):
            try:
                # Menggunakan nama tabel huruf kecil
                supabase.table('tabel_peserta').insert({
                    "nama_lengkap": nama_lengkap,
                    "kategori_pendidikan": kategori,
                    "institusi_asal": institusi,
                    "nama_akun": nama_baru,
                    "kata_sandi": sandi_baru
                }).execute()
                st.success("Registrasi berhasil! Silakan masuk.")
            except Exception as e:
                st.error(f"Gagal daftar: {e}")

else:
    st.title("Tutor AI Bimbingan Belajar TPA")
    if st.button("Keluar"):
        st.session_state['sudah_masuk'] = False
        st.rerun()
    st.write(f"Selamat datang, {st.session_state['nama_aktif']}.")