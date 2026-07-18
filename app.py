import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Tutor AI Bimbel TPA", page_icon="📝")
st.title("Tutor AI Bimbingan Belajar TPA")
st.write("Sistem evaluasi Tes Potensi Akademik. Ketik instruksi Anda untuk memulai sesi latihan.")

# Autentikasi Keamanan API
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Instruksi Sistem Akademis
instruksi_sistem = """
Anda adalah tutor ahli untuk Bimbingan Belajar Tes Potensi Akademik (TPA).
Tugas Anda adalah memberikan soal latihan, mengevaluasi jawaban, dan memberikan pembahasan akademis yang akurat untuk materi logika, verbal, dan numerik.
Gunakan bahasa yang formal, objektif, dan jelas. Berikan umpan balik yang konstruktif dan berikan contoh konkret bila diperlukan.
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