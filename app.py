import streamlit as st
import google.generativeai as genai
from datetime import date

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================
st.set_page_config(
    page_title="KreatifHub",
    page_icon="🎨",
    layout="wide"
)

# ==================================================
# GEMINI AI CONFIGURATION
# ==================================================
# Membaca API Key dari Secrets Streamlit Cloud
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("❌ API Key Gemini tidak ditemukan pada Secrets Streamlit Cloud!")
    st.info("Silakan ke Dashboard Streamlit -> Settings -> Secrets, lalu masukkan API Key Anda.")
    st.stop()

try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Menggunakan gemini-1.5-flash sebagai standar produksi yang stabil
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Gagal menghubungkan ke Google AI: {str(e)}")
    st.stop()

# ==================================================
# HEADER
# ==================================================
st.title("🎨 KreatifHub")
st.subheader("Asisten Freelancer Kreatif Berbasis AI")

st.markdown("""
KreatifHub membantu freelancer untuk:
✅ Menghitung biaya proyek | ✅ Membuat Creative Brief | ✅ Konsultasi dengan AI
""")

# ==================================================
# TABS
# ==================================================
tab1, tab2, tab3 = st.tabs([
    "💰 Kalkulator Biaya",
    "📝 Creative Brief",
    "🤖 AI Assistant"
])

# ==================================================
# TAB 1: KALKULATOR BIAYA
# ==================================================
with tab1:
    st.header("💰 Kalkulator Estimasi Biaya")
    col1, col2 = st.columns(2)

    with col1:
        layanan = st.selectbox(
            "Jenis Layanan",
            ["Desain Grafis", "Copywriting", "Video Editing", "UI/UX Design", "Social Media Management"]
        )
        tarif_per_jam = st.number_input("Tarif Per Jam (Rp)", min_value=10000, value=100000, step=10000)

    with col2:
        jam_kerja = st.number_input("Estimasi Jam Kerja", min_value=1, value=15)
        kompleksitas = st.selectbox("Kompleksitas", ["Rendah", "Sedang", "Tinggi"])

    revisi = st.slider("Jumlah Revisi Gratis", 0, 5, 2)
    biaya_revisi = st.number_input("Biaya Revisi Tambahan", min_value=0, value=75000)

    if st.button("Hitung Biaya"):
        faktor = {"Rendah": 1.0, "Sedang": 1.2, "Tinggi": 1.5}
        total = (tarif_per_jam * jam_kerja * faktor[kompleksitas])
        st.success(f"Estimasi Biaya: Rp {total:,.0f}")
        st.info(f"Layanan: {layanan} | Jam Kerja: {jam_kerja} jam | Kompleksitas: {kompleksitas}")

# ==================================================
# TAB 2: CREATIVE BRIEF
# ==================================================
with tab2:
    st.header("📝 Generator Creative Brief")
    nama_klien = st.text_input("Nama Klien")
    nama_proyek = st.text_input("Nama Proyek")
    deskripsi = st.text_area("Tujuan dan Deskripsi Proyek")
    target = st.text_area("Target Audiens")
    gaya = st.text_input("Gaya Visual")
    deadline = st.date_input("Deadline", date.today())

    if st.button("Buat Brief"):
        if not nama_klien or not nama_proyek:
            st.warning("Lengkapi data terlebih dahulu.")
        else:
            brief = f"# CREATIVE BRIEF\n\nNama Klien: {nama_klien}\nNama Proyek: {nama_proyek}\nDeadline: {deadline}\n\n## Tujuan Proyek\n{deskripsi}\n\n## Target Audiens\n{target}\n\n## Gaya Visual\n{gaya}"
            st.markdown(brief)
            st.download_button("⬇ Download Brief", brief, file_name=f"{nama_proyek}.txt")

# ==================================================
# TAB 3: AI CHATBOT
# ==================================================
with tab3:
    st.header("🤖 AI Freelancer Assistant")
    st.write("Tanyakan apa saja seputar freelance, desain, branding, UI/UX, dan bisnis kreatif.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Halo 👋\n\nSaya AI Freelancer Assistant. Ada yang bisa saya bantu hari ini?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Tulis pertanyaan...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Gemini sedang berpikir..."):
            try:
                response = model.generate_content(
                    f"Kamu adalah AI Freelancer Assistant profesional. Jawablah pertanyaan ini dengan Bahasa Indonesia yang ringkas, jelas, dan profesional: {prompt}"
                )
                jawaban = response.text
            except Exception as e:
                jawaban = f"Terjadi kesalahan pada sistem Google API: {str(e)}"

        with st.chat_message("assistant"):
            st.markdown(jawaban)

        st.session_state.messages.append({"role": "assistant", "content": jawaban})

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")
st.caption("KreatifHub v3.0 | Gemini AI Powered")
