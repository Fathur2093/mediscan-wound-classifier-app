import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import time # Untuk simulasi loading

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(
    page_title="Klasifikasi Otomatis Jenis Luka Luar",
    page_icon="🩹", # Ikon halaman
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Judul dan Sub-judul Aplikasi ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [class*="st-emotion-cache"]  {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #007bff; /* Biru primer */
        text-align: center;
        margin-bottom: 0.5em;
    }
    .sub-header {
        font-size: 1.2em;
        color: #555;
        text-align: center;
        margin-bottom: 2em;
    }
    .stButton>button {
        background-color: #007bff; /* Biru primer */
        color: white;
        font-weight: bold;
        padding: 0.75em 1.5em;
        border-radius: 2em;
        border: none;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0056b3; /* Biru lebih gelap saat hover */
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
    }
    .accent-green-button>button {
        background-color: #28a745; /* Hijau aksen positif */
    }
    .accent-green-button>button:hover {
        background-color: #218838; /* Hijau lebih gelap saat hover */
    }
    .warning-box {
        background-color: #fff3cd; /* Kuning peringatan */
        border-left: 5px solid #ffc107; /* Border kuning */
        padding: 1em;
        border-radius: 0.5em;
        color: #856404; /* Teks gelap */
        margin-top: 1.5em;
        margin-bottom: 1.5em;
    }
    .card-container {
        background-color: white;
        padding: 2em;
        border-radius: 1em;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 2em;
    }
    .result-type {
        font-size: 2em;
        font-weight: bold;
        color: #28a745; /* Hijau untuk hasil positif */
        background-color: #e6ffe6; /* Latar belakang hijau muda */
        padding: 0.5em 1em;
        border-radius: 0.5em;
        display: inline-block;
        margin-bottom: 1em;
    }
    .confidence-bar-container {
        background-color: #e0e0e0;
        border-radius: 0.5em;
        height: 15px;
        width: 100%;
        margin-top: 0.5em;
    }
    .confidence-bar {
        background-color: #007bff;
        height: 100%;
        border-radius: 0.5em;
    }
    .recommendation-section {
        text-align: left;
        margin-top: 1.5em;
    }
    .recommendation-section h3 {
        font-size: 1.3em;
        font-weight: bold;
        color: #333;
        margin-bottom: 1em;
    }
    .recommendation-section ul {
        list-style-type: disc;
        margin-left: 1.5em;
    }
    .recommendation-section li {
        margin-bottom: 0.5em;
    }
    .spinner {
        border: 4px solid rgba(0, 123, 255, 0.2);
        border-left-color: #007bff;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 0 auto 1.5em;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-header">Klasifikasi Otomatis Jenis Luka Luar</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Menggunakan Transfer Learning dengan Arsitektur MobileNetV2</div>', unsafe_allow_html=True)

# --- Disclaimer Global ---
st.markdown(
    """
    <div class="warning-box">
        <p><strong>Disclaimer Penting:</strong> Informasi ini adalah panduan awal dan bukan pengganti diagnosis atau perawatan medis profesional. Selalu konsultasi dengan tenaga medis profesional jika luka parah, tidak membaik, menunjukkan tanda infeksi, atau Anda ragu.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Muat Model (Ganti dengan path model Anda) ---
# Pastikan file model Anda (misal: 'wound_classification_model.h5') ada di direktori yang sama
# dengan file app.py ini, atau di lokasi yang bisa diakses oleh Streamlit.
@st.cache_resource # Cache model agar tidak dimuat ulang setiap interaksi
def load_wound_model():
    try:
        # Nama file model harus persis sama dengan yang Anda simpan di Langkah 4
        model = tf.keras.models.load_model('wound_classification_model.h5')
        return model
    except Exception as e:
        st.error(f"Gagal memuat model. Pastikan file 'wound_classification_model.h5' ada di direktori yang sama. Error: {e}")
        return None

model = load_wound_model()

# --- Definisi Kelas Luka (Harus sesuai dengan urutan saat pelatihan model) ---
# PASTIKAN URUTAN DAN NAMA KELAS INI SAMA PERSIS DENGAN train_generator.class_indices ANDA
# Contoh: Jika train_generator.class_indices adalah {'Abrasion': 0, 'Burn': 1, 'Cut': 2, 'Laceration': 3}
CLASS_NAMES = ['Abrasion', 'Burn', 'Cut', 'Laceration'] # <--- SESUAIKAN INI DENGAN KELAS ANDA!

# --- Basis Pengetahuan Rekomendasi Penanganan ---
RECOMMENDATIONS = {
    "Abrasion": {
        "title": "Luka Lecet (Ringan)",
        "guidance": [
            "Bersihkan luka dengan air mengalir dan sabun lembut untuk menghilangkan kotoran dan kuman.",
            "Oleskan antiseptik ringan (misalnya povidone-iodine atau larutan antiseptik bebas alkohol).",
            "Biarkan luka terbuka agar kering, atau tutup dengan perban non-lengket jika area bergesekan atau kotor.",
            "Ganti perban secara teratur dan jaga kebersihan."
        ],
        "when_to_seek_help": [
            "Luka sangat dalam atau luas.",
            "Terdapat banyak kotoran yang sulit dibersihkan.",
            "Tanda-tanda infeksi (kemerahan bertambah, bengkak, nyeri, nanah).",
            "Jika Anda tidak yakin tentang tingkat keparahan luka."
        ]
    },
    "Burn": {
        "title": "Luka Bakar (Tingkat 1)",
        "guidance": [
            "Segera dinginkan area luka dengan air mengalir (bukan air es) selama 10-20 menit.",
            "Lepaskan perhiasan atau pakaian ketat sebelum bengkak terjadi.",
            "Lindungi luka dengan perban steril longgar atau kain bersih.",
            "Hindari memecahkan lepuh yang mungkin terbentuk.",
            "Konsumsi pereda nyeri yang dijual bebas jika diperlukan."
        ],
        "when_to_seek_help": [
            "Luka bakar lebih dari 7.5 cm persegi.",
            "Luka bakar di wajah, tangan, kaki, atau area sendi utama.",
            "Luka bakar tingkat 2 (ada lepuh besar) atau 3 (kulit hangus/hitam).",
            "Tanda-tanda infeksi (kemerahan bertambah, bengkak, nyeri parah, nanah).",
            "Jika Anda ragu atau kondisi tidak membaik setelah penanganan awal."
        ]
    },
    "Cut": {
        "title": "Luka Sayatan (Ringan)",
        "guidance": [
            "Bersihkan luka dengan air mengalir dan sabun lembut.",
            "Berikan tekanan langsung dengan kain bersih untuk menghentikan pendarahan.",
            "Setelah pendarahan berhenti, tutup luka dengan perban steril.",
            "Ganti perban setiap hari dan jaga kebersihan luka."
        ],
        "when_to_seek_help": [
            "Pendarahan tidak berhenti setelah 10-15 menit tekanan langsung.",
            "Luka sangat dalam, lebar, atau memperlihatkan otot/tulang.",
            "Luka disebabkan oleh benda kotor atau berkarat (risiko tetanus).",
            "Luka di area wajah atau sendi.",
            "Tanda-tanda infeksi (merah, bengkak, nyeri, nanah)."
        ]
    },
    "Laceration": {
        "title": "Luka Robek",
        "guidance": [
            "Bersihkan luka dengan air dan sabun lembut untuk menghilangkan kotoran.",
            "Hentikan pendarahan dengan memberikan tekanan langsung menggunakan kain bersih.",
            "Tutup luka dengan perban steril setelah pendarahan terkontrol.",
            "Jangan mencoba membersihkan luka yang dalam atau memasukkan jari ke dalamnya."
        ],
        "when_to_seek_help": [
            "Luka sangat dalam, lebar, atau tepi luka tidak menyatu.",
            "Pendarahan hebat yang tidak berhenti dengan tekanan.",
            "Terdapat benda asing yang tertanam dalam luka.",
            "Luka disebabkan oleh gigitan hewan atau manusia.",
            "Tanda-tanda infeksi (merah, bengkak, nyeri, nanah)."
        ]
    }
    # Tambahkan jenis luka lain sesuai dengan kelas model Anda
}

# --- Fungsi Pra-pemrosesan Gambar ---
def preprocess_image(img_file):
    img = Image.open(img_file).convert('RGB') # Pastikan format RGB
    img = img.resize((224, 224)) # Sesuaikan dengan IMAGE_SIZE model Anda (224, 224)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) # Tambahkan dimensi batch
    img_array /= 255.0 # Normalisasi piksel
    return img_array

# --- Fungsi untuk Mendapatkan Rekomendasi ---
def get_recommendation(wound_type):
    return RECOMMENDATIONS.get(wound_type, {
        "title": "Jenis Luka Tidak Dikenal",
        "guidance": ["Tidak ada rekomendasi spesifik untuk jenis luka ini."],
        "when_to_seek_help": ["Segera cari pertolongan medis profesional."]
    })

# --- Alur Aplikasi Streamlit ---
st.write("---")

# Menggunakan session_state untuk mengelola tampilan halaman
if 'page' not in st.session_state:
    st.session_state.page = 'upload'
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

# Halaman Unggah
if st.session_state.page == 'upload':
    st.markdown(
        """
        <div class="card-container">
            <h2 style="font-size: 1.8em; font-weight: bold; color: #333;">Selamat Datang!</h2>
            <p style="color: #666; margin-top: 0.5em;">Dapatkan analisis cepat jenis luka Anda untuk panduan pertolongan pertama yang akurat dan tepat.</p>
            <img src="https://placehold.co/400x200/E0F2F7/007bff?text=Ilustrasi+Deteksi+Luka" alt="Ilustrasi Deteksi Luka" style="margin-top: 1.5em; border-radius: 0.5em;">
            <p style="color: #555; margin-top: 1em; font-size: 0.9em;">Tips: Ambil gambar luka dalam pencahayaan cukup dan fokus pada area luka.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Unggah Gambar Luka Anda",
        type=["jpg", "jpeg", "png"],
        help="Pastikan gambar luka jelas, fokus, dan pencahayaan cukup."
    )

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.image(uploaded_file, caption='Gambar Luka Anda', use_column_width=True)
        st.write("")
        if st.button("Mulai Analisis Sekarang", key="analyze_button"):
            st.session_state.page = 'loading'
            st.rerun() # Rerun untuk pindah ke halaman loading
    else:
        st.info("Silakan unggah gambar luka untuk memulai analisis.")

# Halaman Loading
elif st.session_state.page == 'loading':
    st.markdown(
        """
        <div style="text-align: center; padding: 2em;">
            <img src="https://placehold.co/150x150/E0F2F7/007bff?text=Gambar+Luka" alt="Luka yang diunggah" style="width: 150px; height: 150px; object-fit: cover; border-radius: 0.5em; margin-bottom: 1.5em; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <div class="spinner"></div>
            <h2 style="font-size: 2em; font-weight: bold; color: #333; margin-bottom: 0.5em;">Menganalisis Luka Anda...</h2>
            <p style="color: #666; margin-bottom: 1em;">Harap tunggu sebentar, kami sedang memproses data...</p>
            <p style="color: #777; font-size: 0.8em;">Ini mungkin membutuhkan waktu beberapa detik tergantung koneksi internet dan ukuran gambar.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Lakukan prediksi di sini setelah penundaan simulasi
    if model is not None and st.session_state.uploaded_file is not None:
        time.sleep(3) # Simulasi waktu proses
        processed_img = preprocess_image(st.session_state.uploaded_file)
        predictions = model.predict(processed_img)
        predicted_class_idx = np.argmax(predictions[0])
        predicted_class_name = CLASS_NAMES[predicted_class_idx]
        confidence = np.max(predictions[0]) * 100

        st.session_state.prediction_result = {
            "name": predicted_class_name,
            "confidence": confidence
        }
        st.session_state.page = 'result'
        st.rerun() # Rerun untuk pindah ke halaman hasil
    else:
        st.warning("Terjadi masalah saat memuat file atau model. Silakan coba lagi.")
        st.session_state.page = 'upload' # Kembali ke unggah jika ada masalah
        st.rerun()

# Halaman Hasil
elif st.session_state.page == 'result':
    result = st.session_state.prediction_result
    if result:
        st.markdown("---")
        st.markdown('<div class="main-header" style="color: #333; font-size: 2em;">Analisis Selesai!</div>', unsafe_allow_html=True)

        st.image(st.session_state.uploaded_file, caption='Gambar Luka Anda', use_column_width=True)

        st.markdown(f'<p style="font-size: 1.1em; color: #666; margin-bottom: 0.5em;">Jenis Luka Teridentifikasi:</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-type">{result["name"]}</div>', unsafe_allow_html=True)

        st.markdown(f'<p style="font-size: 1.1em; color: #666; margin-top: 1em; margin-bottom: 0.5em;">Tingkat Kepercayaan Model:</p>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="confidence-bar-container">
                <div class="confidence-bar" style="width: {result["confidence"]:.2f}%;"></div>
            </div>
            <p style="font-size: 0.9em; color: #555; margin-top: 0.2em; font-weight: 500;">{result["confidence"]:.2f}% Akurasi</p>
            """,
            unsafe_allow_html=True
        )

        # Tampilkan rekomendasi
        recommendation_data = get_recommendation(result["name"])
        st.markdown('<div class="recommendation-section">', unsafe_allow_html=True)
        st.markdown(f'<h3>Rekomendasi Pertolongan Pertama:</h3>', unsafe_allow_html=True)
        st.markdown(f'<p class="font-bold mb-2">{recommendation_data["title"]}:</p>', unsafe_allow_html=True)
        for item in recommendation_data["guidance"]:
            st.markdown(f'- {item}')

        st.markdown(f'<h3 style="margin-top: 1.5em;">Kapan Harus Mencari Bantuan Medis (Segera):</h3>', unsafe_allow_html=True)
        for item in recommendation_data["when_to_seek_help"]:
            st.markdown(f'- {item}')
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Scan Luka Lain", key="scan_again_button", help="Unggah gambar luka lain untuk analisis baru.", type="secondary"):
                st.session_state.clear() # Hapus state sesi untuk reset aplikasi
                st.rerun() # Rerun aplikasi untuk kembali ke awal
        with col2:
            st.button("Simpan Rekomendasi", key="save_recommendation_button", help="Fitur ini belum diimplementasikan.", type="secondary") # Placeholder

    else:
        st.warning("Tidak ada hasil prediksi yang ditemukan. Silakan unggah gambar lagi.")
        st.session_state.page = 'upload'
        st.rerun()

# --- Footer ---
st.markdown(
    """
    <div style="text-align: center; margin-top: 3em; color: #777; font-size: 0.8em;">
        Aplikasi Klasifikasi Luka Otomatis v1.0 | Dikembangkan oleh [Nama/Tim Anda]
    </div>
    """,
    unsafe_allow_html=True
)
