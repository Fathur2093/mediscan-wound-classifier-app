# app.py
# File ini adalah kode untuk membuat aplikasi web menggunakan Streamlit
import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import os
import sys

# Fungsi untuk memuat model dan membuat prediksi
# Menggunakan @st.cache_data agar model hanya dimuat sekali
@st.cache_data
def load_model():
    """Memuat model HDF5 yang sudah dilatih."""
    try:
        # Nama file model
        model_name = "wound_classification_model.h5"
        # Path absolut ke file model di direktori yang sama dengan app.py
        model_path = os.path.join(os.path.dirname(__file__), model_name)
        
        # Tambahkan pernyataan print untuk debugging
        st.write(f"Memuat model dari: {model_path}")
        
        # Cek apakah file model ada
        if not os.path.exists(model_path):
            st.error(f"ERROR: File model tidak ditemukan di: {model_path}")
            st.info("Pastikan file model .h5 berada di folder yang sama dengan app.py.")
            return None
            
        model = tf.keras.models.load_model(model_path, compile=False)
        return model
    except Exception as e:
        st.error(f"Gagal memuat model. Error: {e}")
        return None

def predict_wound(image, model):
    """
    Membuat prediksi jenis luka dari gambar yang diunggah.
    
    Args:
        image (PIL.Image): Gambar yang diunggah oleh pengguna.
        model (tf.keras.Model): Model TensorFlow yang sudah dilatih.
        
    Returns:
        tuple: (predicted_class, confidence_score)
    """
    # Mengatur ukuran gambar sesuai dengan input model
    img_size = (224, 224)
    image = ImageOps.fit(image, img_size, Image.LANCZOS)
    
    # Mengubah gambar menjadi array numpy
    image_array = np.asarray(image)
    
    # Normalisasi gambar
    normalized_image_array = (image_array.astype(np.float32) / 255.0)
    
    # Membuat batch
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    
    # Membuat prediksi
    prediction = model.predict(data)
    
    # Mendapatkan kelas dan confidence score
    class_labels = ['Abrasions', 'Bruises', 'Burns', 'Cut', 'Ingrown_nails', 'Laceration', 'Stab_wound']
    predicted_class_index = np.argmax(prediction)
    predicted_class = class_labels[predicted_class_index]
    confidence_score = float(prediction[0][predicted_class_index])
    
    return predicted_class, confidence_score

# --- UI Aplikasi Streamlit ---
st.set_page_config(
    page_title="Wound Classifier",
    page_icon="🩹",
    layout="centered"
)

st.title("Aplikasi Klasifikasi Jenis Luka")
st.markdown("Unggah gambar luka untuk memprediksi jenisnya.")

# Muat model saat aplikasi dijalankan
model = load_model()

if model is not None:
    # Komponen untuk mengunggah file
    uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Tampilkan gambar yang diunggah
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption='Gambar yang Diunggah', use_column_width=True)
        st.write("")
        st.markdown("### Prediksi:")

        # Buat prediksi
        predicted_class, confidence = predict_wound(image, model)
        
        st.write(f"Jenis Luka: **{predicted_class}**")
        st.write(f"Confidence: **{confidence:.2%}**")

        st.info("Catatan: Akurasi model mungkin dipengaruhi oleh ketidakseimbangan data. Hasil ini hanya untuk tujuan demonstrasi.")

else:
    st.error("Model gagal dimuat. Harap periksa path model dan coba lagi.")
