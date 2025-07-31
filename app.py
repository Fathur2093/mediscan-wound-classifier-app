import streamlit as st
import time
import random
from io import BytesIO

# --- Konfigurasi Halaman dan Tema ---
st.set_page_config(
    page_title="MediScan AI",
    page_icon="�",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS Kustom untuk Tampilan Profesional ---
# Menggunakan Markdown dengan HTML untuk menyuntikkan CSS.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* Palet Warna & Latar Belakang */
    :root {
        --primary-blue: #007bff;
        --secondary-green: #28a745;
        --light-bg: #f8f9fa;
        --card-bg: #ffffff;
        --text-dark: #212529;
        --text-subtle: #6c757d;
        --border-color: #dee2e6;
        --shadow-soft: rgba(0, 0, 0, 0.05);
    }
    
    body {
        background-color: var(--light-bg);
        color: var(--text-dark);
    }
    
    .stApp {
        background-color: var(--light-bg);
    }

    /* Kartu UI yang Lebih Bersih */
    .clean-card {
        background-color: var(--card-bg);
        border-radius: 1rem;
        box-shadow: 0 4px 12px var(--shadow-soft);
        border: 1px solid var(--border-color);
        padding: 2.5rem;
        margin-top: 2rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .clean-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Judul Utama */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        color: var(--primary-blue);
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* Sub-header */
    .sub-header {
        color: var(--text-subtle);
        text-align: center;
        font-size: 1.2rem;
        font-weight: 400;
    }

    /* Styling tombol utama (Primary) */
    .stButton > button {
        background-color: var(--primary-blue);
        color: white;
        font-weight: 700;
        padding: 0.75rem 2.5rem;
        border-radius: 9999px;
        border: none;
        box-shadow: 0 4px 10px rgba(0, 123, 255, 0.3);
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #0069d9;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 123, 255, 0.4);
    }
    .stButton > button:disabled {
        background-color: #e9ecef;
        color: #adb5bd;
        box-shadow: none;
        cursor: not-allowed;
    }

    /* Styling tombol sekunder */
    .stDownloadButton > button, 
    .stButton:not(.stButton[data-testid*="primary"]) > button {
        background-color: var(--card-bg);
        color: var(--text-dark);
        font-weight: 600;
        padding: 0.75rem 2.5rem;
        border-radius: 9999px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 5px var(--shadow-soft);
        transition: all 0.2s ease-in-out;
    }
    .stDownloadButton > button:hover, 
    .stButton:not(.stButton[data-testid*="primary"]) > button:hover {
        background-color: #e9ecef;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }

    /* Judul Hasil */
    .result-type {
        font-size: 2.25rem;
        font-weight: 800;
        color: var(--secondary-green);
        text-align: center;
        padding: 0.5rem 1.5rem;
        background-color: rgba(40, 167, 69, 0.1);
        border-radius: 1rem;
        display: inline-block;
    }
    
    /* Styling peringatan dan informasi */
    div[data-testid="stAlert"] {
        border-radius: 0.75rem;
    }
    
    /* Tombol ikon kembali */
    .back-btn-container {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Rekomendasi Luka ---
RECOMMENDATIONS = {
    "Abrasion": {
        "title": "Luka Lecet (Ringan)",
        "guidance": [
            "Bersihkan area luka dengan hati-hati menggunakan air mengalir dan sabun yang lembut untuk menghilangkan kotoran, debu, atau kuman. Hindari menggosok terlalu keras.",
            "Setelah bersih, keringkan area dengan menepuk-nepuk menggunakan kain bersih atau kassa steril. Oleskan krim antiseptik untuk mencegah infeksi.",
            "Tutup luka dengan perban non-lengket jika area tersebut sering bergesekan atau rawan kotor. Jika tidak, biarkan terbuka agar cepat kering dan sembuh.",
            "Ganti perban setiap hari atau jika kotor dan basah. Pantau tanda-tanda infeksi seperti kemerahan, bengkak, atau nyeri."
        ],
        "when_to_seek_help": [
            "Luka sangat dalam atau luas.",
            "Terdapat banyak kotoran yang sulit dibersihkan.",
            "Ada tanda-tanda infeksi seperti kemerahan yang meluas, bengkak, nyeri bertambah, atau keluar nanah.",
            "Jika Anda tidak yakin tentang tingkat keparahan luka atau luka tidak kunjung membaik setelah beberapa hari."
        ]
    },
    "Burn": {
        "title": "Luka Bakar (Tingkat 1 - Ringan)",
        "guidance": [
            "Segera dinginkan area luka dengan air mengalir biasa (bukan air es) selama 10-20 menit. Ini akan meredakan nyeri dan mengurangi kerusakan jaringan.",
            "Lepaskan perhiasan atau pakaian ketat di sekitar area luka sebelum bengkak terjadi.",
            "Lindungi luka dengan perban steril longgar atau kain bersih. Jangan gunakan kapas karena bisa menempel pada luka.",
            "Hindari memecahkan lepuh yang mungkin terbentuk, karena ini adalah pelindung alami tubuh terhadap infeksi.",
            "Konsumsi pereda nyeri yang dijual bebas seperti ibuprofen atau parasetamol jika diperlukan."
        ],
        "when_to_seek_help": [
            "Luka bakar lebih dari 7.5 cm persegi.",
            "Luka bakar di area wajah, tangan, kaki, sendi utama, atau alat kelamin.",
            "Luka bakar yang menyebabkan lepuh besar atau hangus (kulit hitam/putih).",
            "Terdapat tanda-tanda infeksi (kemerahan, bengkak, nyeri parah, nanah).",
            "Jika luka bakar disebabkan oleh zat kimia atau listrik.",
            "Jika Anda ragu atau kondisi tidak membaik setelah penanganan awal."
        ]
    },
    "Cut": {
        "title": "Luka Sayatan (Ringan)",
        "guidance": [
            "Bersihkan luka dengan air mengalir dan sabun lembut untuk menghilangkan kuman dan partikel asing.",
            "Berikan tekanan langsung pada luka dengan kain bersih atau kassa steril selama 5-10 menit untuk menghentikan pendarahan.",
            "Setelah pendarahan berhenti, oleskan krim antibiotik dan tutup luka dengan perban steril untuk menjaga kebersihannya.",
            "Ganti perban setiap hari atau jika basah. Pastikan luka tetap kering."
        ],
        "when_to_seek_help": [
            "Pendarahan tidak berhenti setelah 10-15 menit tekanan langsung.",
            "Luka sangat dalam, lebar, atau tepi luka tidak bisa disatukan.",
            "Luka disebabkan oleh benda kotor, berkarat, atau gigitan hewan.",
            "Luka di area wajah, sendi, atau dekat mata.",
            "Ada tanda-tanda infeksi seperti demam, kemerahan, bengkak, atau nanah."
        ]
    },
    "Laceration": {
        "title": "Luka Robek",
        "guidance": [
            "Bersihkan luka secara perlahan dengan air bersih. Jangan mencoba membersihkan luka yang sangat dalam atau menyingkirkan benda asing yang tertanam.",
            "Hentikan pendarahan dengan memberikan tekanan langsung dan elevasi (angkat) bagian yang terluka jika memungkinkan.",
            "Setelah pendarahan terkontrol, lindungi luka dengan perban steril longgar.",
            "Jangan mencoba menjahit luka sendiri atau menempelkan plester pada luka yang lebar."
        ],
        "when_to_seek_help": [
            "Luka sangat dalam atau lebar dan memerlukan jahitan.",
            "Pendarahan hebat yang tidak terkontrol.",
            "Ada benda asing (misalnya serpihan kaca) yang tertanam dalam luka.",
            "Luka disebabkan oleh gigitan hewan atau manusia.",
            "Terdapat tanda-tanda infeksi (merah, bengkak, nyeri, demam)."
        ]
    }
}
CLASS_NAMES = list(RECOMMENDATIONS.keys())

# --- Manajemen State Sesi ---
if 'page' not in st.session_state:
    st.session_state.page = 'disclaimer'
if 'scans_history' not in st.session_state:
    st.session_state.scans_history = []
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

# --- Fungsi Halaman ---

def disclaimer_page():
    """Halaman disclaimer dan persetujuan."""
    st.markdown("<h1 class='main-header'>MediScan AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Klasifikasi Otomatis Jenis Luka Luar</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
        st.info("⚠️ **Disclaimer Penting**")
        st.markdown("""
        Informasi ini adalah panduan awal dan bukan pengganti diagnosis atau perawatan medis profesional. 
        Selalu konsultasi dengan tenaga medis profesional jika luka parah, tidak membaik, menunjukkan tanda infeksi, atau Anda ragu.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Saya Mengerti", use_container_width=True):
                st.session_state.page = 'upload'
                st.rerun() # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()

def upload_page():
    """Halaman unggah file utama."""
    st.markdown("<h1 class='main-header'>MediScan AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Klasifikasi Otomatis Jenis Luka Luar</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
        st.subheader("Unggah Foto Luka Anda")
        st.write("Mulai analisis cepat dan dapatkan panduan pertolongan pertama.")
        
        uploaded_file = st.file_uploader(
            "Pilih gambar luka Anda",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            st.image(st.session_state.uploaded_file, caption="Gambar yang Diunggah", use_column_width=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Mulai Analisis", disabled=not uploaded_file, use_container_width=True):
                st.session_state.page = 'loading'
                st.rerun() # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
        with col2:
            if st.session_state.scans_history:
                if st.button("Lihat Riwayat Scan", use_container_width=True):
                    st.session_state.page = 'history'
                    st.rerun() # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

def loading_page():
    """Halaman simulasi loading."""
    st.markdown("<h1 class='main-header'>Menganalisis Luka Anda...</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Harap tunggu sebentar, kami sedang memproses data...</p>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
        
        if st.session_state.uploaded_file:
            st.image(st.session_state.uploaded_file, width=150)
        
        st.write("")
        with st.spinner("Model sedang berjalan..."):
            time.sleep(3) # Simulasi waktu prediksi
        
        st.success("Analisis selesai!")
        
        # Simulasi hasil prediksi
        random_class = random.choice(CLASS_NAMES)
        random_confidence = random.uniform(80.0, 99.9)
        
        prediction = {
            "name": random_class,
            "confidence": random_confidence,
            "image_data": st.session_state.uploaded_file.getvalue(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Simpan hasil ke riwayat
        st.session_state.scans_history.insert(0, prediction)
        
        st.session_state.prediction_result = prediction
        st.session_state.page = 'result'
        st.rerun() # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)


def result_page():
    """Halaman menampilkan hasil dan rekomendasi."""
    st.markdown("<div class='back-btn-container'>", unsafe_allow_html=True)
    if st.button("← Kembali", key="back_from_result"):
        st.session_state.page = 'upload'
        st.rerun() # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h1 class='main-header'>Analisis Selesai!</h1>", unsafe_allow_html=True)
    
    prediction = st.session_state.prediction_result
    if not prediction:
        st.warning("Tidak ada hasil yang ditemukan.")
        st.session_state.page = 'upload'
        st.rerun() # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
        return

    recommendation = RECOMMENDATIONS.get(prediction['name'], {
        "title": "Jenis Luka Tidak Dikenal",
        "guidance": ["Tidak ada rekomendasi spesifik untuk jenis luka ini. Segera cari pertolongan medis profesional."],
        "when_to_seek_help": ["Segera cari pertolongan medis profesional."]
    })

    with st.container():
        st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(BytesIO(prediction['image_data']), caption="Gambar Luka Anda", use_column_width=True)
            
        with col2:
            st.markdown("<p style='color: var(--text-subtle);'>Jenis Luka Teridentifikasi:</p>", unsafe_allow_html=True)
            st.markdown(f"<div class='result-type'>{recommendation['title']}</div>", unsafe_allow_html=True)
            
            st.markdown("<p style='color: var(--text-subtle); margin-top: 1rem;'>Tingkat Kepercayaan Model:</p>", unsafe_allow_html=True)
            st.progress(prediction['confidence'] / 100)
            st.markdown(f"<p style='color: var(--text-subtle); font-size: 0.875rem;'>{prediction['confidence']:.2f}% Akurasi</p>", unsafe_allow_html=True)
            
        st.markdown("<h3 style='color: var(--primary-blue); font-weight: 600; margin-top: 2rem;'>Panduan Pertolongan Pertama</h3>", unsafe_allow_html=True)
        for item in recommendation['guidance']:
            st.markdown(f"✅ {item}")
        
        st.markdown("<h3 style='color: #dc3545; font-weight: 600; margin-top: 2rem;'>Kapan Harus Mencari Bantuan Medis</h3>", unsafe_allow_html=True)
        for item in recommendation['when_to_seek_help']:
            st.markdown(f"🚨 {item}")
            
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Scan Luka Lain", use_container_width=True):
                st.session_state.page = 'upload'
                st.rerun() # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()

        with col_btn2:
            download_text = f"""
Hasil Analisis MediScan AI
Jenis Luka Teridentifikasi: {recommendation['title']}
Tingkat Kepercayaan Model: {prediction['confidence']:.2f}%

---

Panduan Pertolongan Pertama:
{'\n'.join([f"{idx+1}. {item}" for idx, item in enumerate(recommendation['guidance'])])}

---

Kapan Harus Mencari Bantuan Medis:
{'\n'.join([f"{idx+1}. {item}" for idx, item in enumerate(recommendation['when_to_seek_help'])])}
"""
            st.download_button(
                label="Simpan Rekomendasi",
                data=download_text,
                file_name=f"rekomendasi_mediscan_{prediction['name']}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)


def history_page():
    """Halaman riwayat pemindaian."""
    st.markdown("<div class='back-btn-container'>", unsafe_allow_html=True)
    if st.button("← Kembali", key="back_from_history"):
        st.session_state.page = 'upload'
        st.rerun() # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h1 class='main-header'>Riwayat Pemindaian</h1>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='clean-card'>", unsafe_allow_html=True)

        if not st.session_state.scans_history:
            st.warning("Anda belum memiliki riwayat pemindaian.")
        else:
            for i, scan in enumerate(st.session_state.scans_history):
                recommendation = RECOMMENDATIONS.get(scan['name'], {"title": "Tidak Dikenal"})
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.image(BytesIO(scan['image_data']), width=75)
                with col2:
                    st.markdown(f"**{recommendation['title']}**")
                    st.markdown(f"<p style='font-size: 0.875rem; color: var(--text-subtle);'>Akurasi: {scan['confidence']:.2f}%</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 0.75rem; color: var(--text-subtle);'>{scan['timestamp']}</p>", unsafe_allow_html=True)
                with col3:
                    if st.button("Lihat Detail", key=f"history_btn_{i}", use_container_width=True):
                        st.session_state.prediction_result = scan
                        st.session_state.page = 'result'
                        st.rerun() # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
                st.markdown("---")
                
            # Tombol aksi riwayat
            if len(st.session_state.scans_history) > 1:
                if st.button("Bersihkan Riwayat", key="clear_history", use_container_width=True):
                    st.session_state.scans_history = []
                    st.session_state.page = 'history'
                    st.rerun() # PERBAIKAN: Mengganti st.experimental_rerun() dengan st.rerun()
                    st.toast("Riwayat berhasil dibersihkan!")

        st.markdown("</div>", unsafe_allow_html=True)

# --- Routing Logika Aplikasi ---
if st.session_state.page == 'disclaimer':
    disclaimer_page()
elif st.session_state.page == 'upload':
    upload_page()
elif st.session_state.page == 'loading':
    loading_page()
elif st.session_state.page == 'result':
    result_page()
elif st.session_state.page == 'history':
    history_page()

# --- Footer ---
st.markdown("<p style='text-align: center; color: var(--text-subtle); font-size: 0.875rem; margin-top: 3rem;'>Aplikasi Klasifikasi Luka Otomatis v5.0 | Dikembangkan oleh fath</p>", unsafe_allow_html=True)
