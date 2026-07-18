import streamlit as st
import google.generativeai as genai
from supabase import create_client, Client

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
# TAHAP 1: PORTAL AKSES (Sistem Login/Daftar)
# ==========================================
if not st.session_state['sudah_masuk']:
    st.title("Portal Akses Bimbingan Belajar TPA")
    st.write("Silakan masuk atau buat akun baru untuk memulai sesi evaluasi akademis.")
    
    tab_masuk, tab_daftar = st.tabs(["Masuk ke Sistem", "Pendaftaran Pengguna Baru"])
    
    with tab_masuk:
        st.subheader("Masuk ke Akun Anda")
        nama_pengguna = st.text_input("Nama Pengguna (Username)", key="input_masuk_nama")
        kata_sandi = st.text_input("Kata Sandi", type="password", key="input_masuk_sandi")
        
        if st.button("Masuk"):
            if nama_pengguna and kata_sandi:
                try:
                    # Mencocokkan data dengan pangkalan data Supabase
                    respons = supabase.table('Tabel_Peserta').select("*").eq("nama_akun", nama_pengguna).execute()
                    if len(respons.data) > 0:
                        data_pengguna = respons.data[0]
                        if data_pengguna['kata_sandi'] == kata_sandi:
                            st.session_state['sudah_masuk'] = True
                            st.session_state['nama_aktif'] = data_pengguna['nama_lengkap']
                            st.session_state['kategori_pendidikan'] = data_pengguna['kategori_pendidikan']
                            st.rerun()
                        else:
                            st.error("Kredensial tidak valid. Kata sandi keliru.")
                    else:
                        st.error("Identitas tidak ditemukan dalam sistem.")
                except Exception as e:
                    st.error(f"Terjadi galat komunikasi dengan pangkalan data: {e}")
            else:
                st.warning("Mohon lengkapi seluruh kolom pengisian.")
                
    with tab_daftar:
        st.subheader("Formulir Pendaftaran")
        nama_lengkap = st.text_input("Nama Lengkap")
        kategori = st.selectbox("Tingkat Pendidikan", ["SMP", "SMA", "Mahasiswa", "Umum"])
        institusi = st.text_input("Asal Sekolah / Universitas / Instansi")
        nama_pengguna_baru = st.text_input("Pilih Nama Pengguna (Username)", key="input_daftar_nama")
        kata_sandi_baru = st.text_input("Buat Kata Sandi", type="password", key="input_daftar_sandi")
        
        if st.button("Daftar Sekarang"):
            if nama_lengkap and institusi and nama_pengguna_baru and kata_sandi_baru:
                try:
                    # Mengirim data pendaftar baru ke Supabase
                    supabase.table('Tabel_Peserta').insert({
                        "nama_lengkap": nama_lengkap,
                        "kategori_pendidikan": kategori,
                        "institusi_asal": institusi,
                        "nama_akun": nama_pengguna_baru,
                        "kata_sandi": kata_sandi_baru
                    }).execute()
                    st.success("Registrasi akademis berhasil! Silakan beralih ke tab 'Masuk ke Sistem'.")
                except Exception as e:
                    st.error("Registrasi gagal. Nama pengguna mungkin telah digunakan oleh pihak lain.")
            else:
                st.warning("Seluruh parameter pendaftaran wajib diisi secara komprehensif.")

# ==========================================
# TAHAP 2: RUANG EVALUASI AI (Setelah Masuk)
# ==========================================
else:
    st.title("Tutor AI Bimbingan Belajar TPA")
    
    pengguna_aktif = st.session_state['nama_aktif']
    kategori_pendidikan = st.session_state['kategori_pendidikan']
    
    kolom1, kolom2 = st.columns([3, 1])
    with kolom1:
        st.write(f"Selamat datang, **{pengguna_aktif}** (Kategori: {kategori_pendidikan}).")
    with kolom2:
        if st.button("Keluar (Log Out)"):
            st.session_state['sudah_masuk'] = False
            st.rerun()
        
    st.divider()

    # Autentikasi Keamanan API Gemini
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    # Instruksi Sistem Akademis Dinamis
    instruksi_sistem = f"""
    Anda adalah tutor ahli untuk Bimbingan Belajar Tes Potensi Akademik (TPA).
    Peserta didik Anda saat ini berada pada tingkat pendidikan: {kategori_pendidikan}.
    Tugas utama Anda: Sesuaikan tingkat kesulitan soal dan kompleksitas bahasa pembahasan secara presisi dengan taraf kognitif {kategori_pendidikan}.
    
    Anda wajib mematuhi alur instruksional berikut secara ketat:
    1. TAHAP INISIASI: Saat pengguna pertama kali menyapa, balas dengan sopan dan langsung tawarkan tiga pilihan kategori materi secara eksplisit: VERBAL, NUMERIK, dan LOGIKA. Tunggu respons pengguna.
    2. TAHAP DIAGNOSTIK: Setelah pengguna memilih kategori, berikan TEPAT SATU soal diagnostik dari kategori tersebut. Tunggu pengguna menjawab. Jangan pernah memberikan lebih dari satu soal dalam satu waktu.
    3. TAHAP EVALUASI & TUTORIAL: Setelah pengguna memberikan jawaban, evaluasi ketepatan jawaban tersebut. Berikan pembahasan (tutorial) yang rasional, objektif, dan akademis. 
    4. TAHAP KONFIRMASI: Di akhir setiap pembahasan soal, Anda WAJIB bertanya dengan kalimat ini: "Apakah mau melanjutkan soal berikutnya?". Tunggu respons pengguna.
    5. TAHAP LANJUTAN: 
       * Jika pengguna menjawab "Ya", berikan 1 soal baru dari kategori yang sama, lalu kembali ke Tahap 3.
       * Jika pengguna menjawab "Tidak", tutup sesi dengan ucapan apresiasi akademis dan motivasi belajar.

    Gunakan bahasa Indonesia yang formal, profesional, dan memberikan semangat.
    """

    # Inisialisasi Model AI
    model = genai.GenerativeModel(
        model_name="gemini-3.5-flash",
        system_instruction=instruksi_sistem
    )

    # Manajemen Memori Percakapan
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    for message in st.session_state.chat_session.history:
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # Interaksi Pengguna
    user_input = st.chat_input("Ketik 'Saya ingin belajar' atau ajukan pertanyaan di sini...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            try:
                response = st.session_state.chat_session.send_message(user_input)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Terjadi kendala teknis pada sistem API: {e}.")