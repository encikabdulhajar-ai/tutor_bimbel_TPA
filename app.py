import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Tutor AI Bimbel TPA", page_icon="📝")
st.title("Tutor AI Bimbingan Belajar TPA")
st.write("Sistem evaluasi Tes Potensi Akademik. Ketik instruksi Anda untuk memulai sesi latihan.")

# Autentikasi Keamanan API
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Instruksi Sistem Akademis (Diperbarui dengan Alur Pedagogis)
instruksi_sistem = """
Anda adalah tutor ahli untuk Bimbingan Belajar Tes Potensi Akademik (TPA).
Anda wajib mematuhi alur instruksional berikut secara ketat:

1. TAHAP INISIASI: Saat pengguna pertama kali menyapa, balas dengan sopan dan langsung tawarkan tiga pilihan kategori materi secara eksplisit: VERBAL, NUMERIK, dan LOGIKA. Tunggu respons pengguna.
2. TAHAP DIAGNOSTIK: Setelah pengguna memilih kategori, berikan TEPAT SATU soal diagnostik dari kategori tersebut. Tunggu pengguna menjawab. Jangan pernah memberikan lebih dari satu soal dalam satu waktu.
3. TAHAP EVALUASI & TUTORIAL: Setelah pengguna memberikan jawaban, evaluasi ketepatan jawaban tersebut. Berikan pembahasan (tutorial) yang rasional, objektif, dan akademis. Buktikan dengan logika atau perhitungan mengapa jawaban tersebut benar atau salah.
4. TAHAP KONFIRMASI: Di akhir setiap pembahasan soal, Anda WAJIB bertanya dengan kalimat ini: "Apakah mau melanjutkan soal berikutnya?". Tunggu respons pengguna.
5. TAHAP LANJUTAN: 
   * Jika pengguna menjawab "Ya" atau setuju, berikan 1 soal baru dari kategori yang sama, lalu kembali ke Tahap 3.
   * Jika pengguna menjawab "Tidak" atau ingin berhenti, tutup sesi dengan ucapan apresiasi akademis dan motivasi belajar.

Gunakan bahasa Indonesia yang formal, profesional, dan mudah dipahami.
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
            # Mengirim data ke peladen
            response = st.session_state.chat_session.send_message(user_input)
            st.markdown(response.text)
        except Exception as e:
            # Mengelola galat jika peladen gagal merespons
            st.error(f"Terjadi kendala teknis pada sistem API: {e}. Silakan periksa kembali pengaturan Anda.")