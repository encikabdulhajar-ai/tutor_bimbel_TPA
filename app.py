import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Halaman Aplikasi
st.set_page_config(page_title="Tutor AI", page_icon="book")
st.title("Tutor AI Bimbel TPA")

# 2. Pengaturan Keamanan API Key
# Kunci diambil dari fail konfigurasi rahasia Streamlit
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 3. Penyusunan Instruksi Sistem
# Teks ini menggantikan pengaturan instruksi pada GEMS Bapak
instruksi_sistem = """
Anda adalah asisten akademik ahli yang membantu penyusunan materi pendidikan.
Fokus utama Anda adalah integrasi metode STEAM (Science, Technology, Engineering, Arts, and Mathematics) 
dan pengembangan kurikulum muatan lokal budaya Melayu Kepulauan Riau.
Berikan informasi yang akurat, terstruktur, dan gunakan bahasa yang formal serta mudah dipahami.
"""

# 4. Inisialisasi Model Bahasa
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instruksi_sistem
)

# 5. Manajemen Memori Percakapan (Session State)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Menampilkan riwayat percakapan sebelumnya di layar
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 6. Kolom Masukan Pengguna
user_input = st.chat_input("Ketik pertanyaan atau instruksi tugas di sini...")

if user_input:
    # Menampilkan teks yang diketik pengguna
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Mengirim teks ke server Google dan menampilkan hasil analisis
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(user_input)
        st.markdown(response.text)