<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MediScan AI</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        :root {
            --primary-color: #06b6d4; /* Teal */
            --secondary-color: #1e3a8a; /* Dark Blue */
            --background-color: #0f172a; /* Darkest Blue */
            --card-bg: rgba(255, 255, 255, 0.05);
            --text-light: #f1f5f9;
            --text-subtle: #94a3b8;
            --border-color: rgba(255, 255, 255, 0.1);
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--background-color);
            color: var(--text-light);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem 1rem;
            position: relative;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at top left, #1e3a8a 0%, transparent 20%),
                        radial-gradient(circle at bottom right, #06b6d4 0%, transparent 20%);
            z-index: -1;
            opacity: 0.3;
        }

        .main-container {
            max-width: 900px;
            margin: auto;
            width: 100%;
            animation: fadeIn 0.8s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .glass-card {
            background-color: var(--card-bg);
            backdrop-filter: blur(15px);
            border-radius: 1.5rem;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }

        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
        }

        .main-header {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(45deg, var(--primary-color), var(--text-light));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }

        .sub-header {
            font-size: 1.2rem;
            color: var(--text-subtle);
            text-align: center;
            margin-top: 0.5rem;
        }

        .button-primary {
            background: linear-gradient(90deg, #10b981, var(--primary-color));
            color: var(--background-color);
            font-weight: 600;
            padding: 0.75rem 2.5rem;
            border-radius: 9999px;
            border: none;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
            transition: all 0.3s ease;
        }
        
        .button-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6);
        }

        .button-secondary {
            background-color: rgba(255, 255, 255, 0.1);
            color: var(--text-light);
            font-weight: 600;
            padding: 0.75rem 2.5rem;
            border-radius: 9999px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }

        .button-secondary:hover {
            background-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-1px);
        }
        
        .button-sm {
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
        }

        .result-type {
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--primary-color);
            text-align: center;
            padding: 0.5rem 1.5rem;
            background-color: rgba(6, 182, 212, 0.1);
            border: 1px solid var(--primary-color);
            border-radius: 1rem;
            display: inline-block;
        }
        
        .confidence-bar-container {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 9999px;
            height: 12px;
            width: 100%;
            margin-top: 0.5rem;
            overflow: hidden;
        }
        
        .confidence-bar {
            background: linear-gradient(90deg, #3b82f6, var(--primary-color));
            height: 100%;
            border-radius: 9999px;
            transition: width 1s ease-in-out;
            animation: progressAnimation 2s forwards;
        }
        
        @keyframes progressAnimation {
            from { width: 0; }
        }

        .spinner {
            border: 4px solid rgba(255, 255, 255, 0.5);
            border-left-color: var(--primary-color);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Modal styling */
        .modal {
            background-color: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(5px);
            z-index: 50;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }

        .modal.active {
            opacity: 1;
            visibility: visible;
        }

        .modal-content {
            transform: translateY(-20px);
            transition: all 0.3s ease;
        }

        .modal.active .modal-content {
            transform: translateY(0);
        }

        .icon-small {
            width: 24px;
            height: 24px;
        }

        .icon-large {
            width: 48px;
            height: 48px;
        }

        /* Toast Notification */
        .toast {
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            background-color: rgba(6, 182, 212, 0.95);
            color: white;
            padding: 1rem 2rem;
            border-radius: 9999px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease-in-out;
            z-index: 60;
        }
        .toast.show {
            opacity: 1;
            visibility: visible;
            transform: translateX(-50%) translateY(-10px);
        }
    </style>
</head>
<body>

    <div class="main-container">
        <!-- Header -->
        <h1 class="main-header">MediScan AI</h1>
        <p class="sub-header">Klasifikasi Otomatis Jenis Luka Luar</p>

        <!-- Main Content Area -->
        <div id="app-content" class="mt-12">
            <!-- Content will be rendered here by JavaScript -->
        </div>

        <!-- Footer -->
        <footer class="text-center text-gray-500 text-sm mt-16 py-4">
            Aplikasi Klasifikasi Luka Otomatis v5.0 | Dikembangkan oleh fath
        </footer>
    </div>

    <!-- Disclaimer Modal -->
    <div id="disclaimer-modal" class="modal fixed inset-0 flex items-center justify-center p-4">
        <div class="modal-content bg-slate-800 p-8 rounded-2xl shadow-xl w-full max-w-lg border border-slate-700">
            <div class="flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon-large text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
            </div>
            <h3 class="text-2xl font-bold text-white text-center mb-4">Disclaimer Penting</h3>
            <p class="text-gray-400 leading-relaxed text-center">
                Informasi ini adalah panduan awal dan bukan pengganti diagnosis atau perawatan medis profesional.
                Selalu konsultasi dengan tenaga medis profesional jika luka parah, tidak membaik, menunjukkan tanda infeksi, atau Anda ragu.
            </p>
            <div class="mt-6 text-center">
                <button id="accept-disclaimer" class="button-primary">Saya Mengerti</button>
            </div>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast-notification" class="toast"></div>

    <script>
        // Data rekomendasi luka
        const RECOMMENDATIONS = {
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
        };
        
        const CLASS_NAMES = ['Abrasion', 'Burn', 'Cut', 'Laceration'];

        // State management
        let appState = {
            page: 'upload',
            uploadedFile: null,
            predictionResult: null,
            scansHistory: JSON.parse(localStorage.getItem('mediscan_history')) || []
        };
        
        const appContent = document.getElementById('app-content');
        const disclaimerModal = document.getElementById('disclaimer-modal');
        const acceptDisclaimerButton = document.getElementById('accept-disclaimer');
        const toastNotification = document.getElementById('toast-notification');

        // Fungsi utilitas untuk notifikasi toast
        function showToast(message) {
            toastNotification.textContent = message;
            toastNotification.classList.add('show');
            setTimeout(() => {
                toastNotification.classList.remove('show');
            }, 3000);
        }

        // Fungsi untuk menampilkan/menyembunyikan modal
        function showModal() {
            disclaimerModal.classList.add('active');
        }

        function hideModal() {
            disclaimerModal.classList.remove('active');
        }

        // Fungsi untuk merender halaman 'upload'
        function renderUploadPage() {
            appContent.innerHTML = `
                <div class="glass-card p-8 md:p-12 text-center animate-fadeIn">
                    <h2 class="text-3xl font-bold text-white mb-2">Unggah Foto Luka Anda</h2>
                    <p class="text-gray-400 mb-6">Mulai analisis cepat dan dapatkan panduan pertolongan pertama.</p>
                    
                    <div id="drop-zone" class="relative border-2 border-dashed border-gray-600 rounded-2xl p-8 mb-8 hover:border-blue-500 transition-colors cursor-pointer">
                        <input type="file" id="file-upload" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" accept="image/jpeg, image/png">
                        <div id="upload-area" class="flex flex-col items-center justify-center">
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon-large text-gray-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                            </svg>
                            <p class="text-gray-400 font-medium">Seret dan letakkan gambar di sini atau</p>
                            <span class="text-blue-400 font-semibold mt-1">klik untuk mengunggah</span>
                        </div>
                    </div>

                    <div id="image-preview" class="hidden mb-6 text-left">
                        <p class="text-gray-300 font-semibold mb-2">Gambar yang Diunggah:</p>
                        <div class="relative">
                            <img id="preview-img" src="" alt="Gambar Luka Anda" class="rounded-xl w-full max-h-96 object-cover shadow-lg">
                        </div>
                    </div>
                    
                    <div class="flex flex-col sm:flex-row gap-4 justify-center">
                        <button id="analyze-button" class="button-primary w-full max-w-xs mt-4" disabled>
                            Mulai Analisis
                        </button>
                        <button id="view-history-button" class="button-secondary w-full max-w-xs mt-4" style="${appState.scansHistory.length === 0 ? 'display:none' : ''}">
                            Lihat Riwayat Scan
                        </button>
                    </div>
                </div>
            `;
            
            const fileUpload = document.getElementById('file-upload');
            const analyzeButton = document.getElementById('analyze-button');
            const imagePreview = document.getElementById('image-preview');
            const previewImg = document.getElementById('preview-img');
            const viewHistoryButton = document.getElementById('view-history-button');
            
            fileUpload.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    appState.uploadedFile = file;
                    previewImg.src = URL.createObjectURL(file);
                    imagePreview.classList.remove('hidden');
                    analyzeButton.disabled = false;
                } else {
                    appState.uploadedFile = null;
                    imagePreview.classList.add('hidden');
                    analyzeButton.disabled = true;
                }
            });

            analyzeButton.addEventListener('click', () => {
                if (appState.uploadedFile) {
                    appState.page = 'loading';
                    renderApp();
                }
            });

            viewHistoryButton.addEventListener('click', () => {
                appState.page = 'history';
                renderApp();
            });
        }

        // Fungsi untuk merender halaman 'loading'
        function renderLoadingPage() {
            appContent.innerHTML = `
                <div class="glass-card p-8 md:p-12 text-center flex flex-col items-center animate-fadeIn">
                    <div class="relative w-32 h-32 mb-8">
                        <img src="${URL.createObjectURL(appState.uploadedFile)}" alt="Luka yang diunggah" class="w-full h-full object-cover rounded-full shadow-lg border-4 border-slate-700">
                        <div class="absolute inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 rounded-full">
                            <div class="spinner"></div>
                        </div>
                    </div>
                    
                    <h2 class="text-3xl font-bold text-white mb-2">Menganalisis Luka Anda...</h2>
                    <p class="text-gray-400 mb-6">Harap tunggu sebentar, kami sedang memproses data...</p>

                    <div class="w-full max-w-sm">
                        <p class="text-gray-500 text-sm mb-2 text-left" id="progress-text">Menganalisis...</p>
                        <div class="confidence-bar-container">
                            <div id="loading-progress-bar" class="confidence-bar" style="width: 0%;"></div>
                        </div>
                    </div>
                </div>
            `;
            
            // Animasi bilah progres
            const progressBar = document.getElementById('loading-progress-bar');
            let progress = 0;
            const interval = setInterval(() => {
                progress += 1;
                progressBar.style.width = `${progress}%`;
                if (progress >= 100) {
                    clearInterval(interval);
                }
            }, 20); // Kecepatan animasi

            // Simulasikan prediksi setelah 3 detik
            setTimeout(() => {
                const randomClass = CLASS_NAMES[Math.floor(Math.random() * CLASS_NAMES.length)];
                const randomConfidence = (Math.random() * 20 + 80).toFixed(2); // Confidence between 80-100
                const prediction = {
                    name: randomClass,
                    confidence: parseFloat(randomConfidence),
                    imageUrl: URL.createObjectURL(appState.uploadedFile),
                    timestamp: new Date().toISOString()
                };

                // Simpan hasil scan ke riwayat
                appState.scansHistory.unshift(prediction);
                localStorage.setItem('mediscan_history', JSON.stringify(appState.scansHistory));

                appState.predictionResult = prediction;
                appState.page = 'result';
                renderApp();
            }, 3000);
        }
        
        // Fungsi untuk merender halaman 'result'
        function renderResultPage(scan = appState.predictionResult) {
            const recommendation = RECOMMENDATIONS[scan.name] || {
                title: "Jenis Luka Tidak Dikenal",
                guidance: ["Tidak ada rekomendasi spesifik untuk jenis luka ini. Segera cari pertolongan medis profesional."],
                when_to_seek_help: ["Segera cari pertolongan medis profesional."]
            };
            
            appContent.innerHTML = `
                <div class="glass-card p-8 md:p-12 text-left animate-fadeIn">
                    <h2 class="text-3xl font-bold text-white text-center mb-8">Analisis Selesai!</h2>

                    <div class="grid md:grid-cols-2 gap-8 mb-8 items-center">
                        <div class="flex justify-center">
                            <img src="${scan.imageUrl}" alt="Gambar Luka Anda" class="rounded-xl w-full max-w-sm shadow-lg border-2 border-slate-700">
                        </div>
                        <div class="flex flex-col justify-center text-center md:text-left">
                            <p class="text-gray-400 font-medium text-lg mb-1">Jenis Luka Teridentifikasi:</p>
                            <div class="result-type mx-auto md:mx-0">${recommendation.title}</div>
                            <p class="text-gray-500 font-medium text-lg mt-4 mb-2">Tingkat Kepercayaan Model:</p>
                            <div class="confidence-bar-container w-full max-w-xs md:mx-0 mx-auto">
                                <div class="confidence-bar" style="width: ${scan.confidence}%;"></div>
                            </div>
                            <p class="text-gray-500 text-sm mt-1 md:text-left text-center">${scan.confidence.toFixed(2)}% Akurasi</p>
                        </div>
                    </div>
                    
                    <div class="bg-slate-900 p-6 rounded-xl mt-8 border border-slate-700">
                        <div class="flex items-center gap-2 mb-4">
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon-small text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.111a1 1 0 011.025 1.342L18.066 11.2a2 2 0 01-.015 2.502l-4.437 5.485a2.5 2.5 0 01-3.79 0L3.957 13.702a2.5 2.5 0 01-1.04-1.745l.003-.507c.05-1.12.92-2.073 2.05-2.203.882-.102 1.77-.102 2.652 0 .53-.06.944-.455.944-.997s-.414-.937-.944-.997c-.882-.102-1.77-.102-2.652 0C2.92 7.747 1.05 9.68 1.05 12.399a3.5 3.5 0 001.04 2.457l3.792 3.754a1.5 1.5 0 002.136 0l4.437-5.485a2.5 2.5 0 01.015-2.502l-1.025-1.196a1 1 0 01-.025-1.342z" />
                            </svg>
                            <h3 class="text-xl font-bold text-white">Panduan Pertolongan Pertama</h3>
                        </div>
                        <ul class="list-disc list-inside space-y-3 text-gray-300">
                            ${recommendation.guidance.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    </div>

                    <div class="bg-slate-900 p-6 rounded-xl mt-4 border border-slate-700">
                        <div class="flex items-center gap-2 mb-4">
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon-small text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                            <h3 class="text-xl font-bold text-white">Kapan Harus Mencari Bantuan Medis</h3>
                        </div>
                        <ul class="list-disc list-inside space-y-3 text-gray-300">
                            ${recommendation.when_to_seek_help.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    </div>

                    <div class="flex flex-col sm:flex-row justify-center gap-4 mt-12">
                        <button id="scan-again-button" class="button-secondary w-full sm:w-auto flex-1 max-w-sm">
                            Scan Luka Lain
                        </button>
                        <button id="copy-button" class="button-secondary w-full sm:w-auto flex-1 max-w-sm flex items-center justify-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon-small" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                            </svg>
                            Salin Rekomendasi
                        </button>
                        <button id="save-button" class="button-primary w-full sm:w-auto flex-1 max-w-sm flex items-center justify-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="icon-small text-slate-900" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                            </svg>
                            Simpan Rekomendasi
                        </button>
                    </div>
                </div>
            `;
            
            document.getElementById('scan-again-button').addEventListener('click', () => {
                appState.page = 'upload';
                appState.uploadedFile = null;
                appState.predictionResult = null;
                renderApp();
            });

            document.getElementById('save-button').addEventListener('click', () => {
                const recommendationText = `
Hasil Analisis MediScan AI

Jenis Luka Teridentifikasi: ${recommendation.title}
Tingkat Kepercayaan Model: ${scan.confidence.toFixed(2)}%

---

Panduan Pertolongan Pertama:
${recommendation.guidance.map((item, index) => `${index + 1}. ${item}`).join('\n')}

---

Kapan Harus Mencari Bantuan Medis:
${recommendation.when_to_seek_help.map((item, index) => `${index + 1}. ${item}`).join('\n')}
                `;

                const blob = new Blob([recommendationText], { type: 'text/plain' });
                const a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = `rekomendasi_mediscan_${scan.name.toLowerCase()}_${Date.now()}.txt`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(a.href);
                showToast("Rekomendasi berhasil disimpan!");
            });

            document.getElementById('copy-button').addEventListener('click', () => {
                const recommendationText = `
Hasil Analisis MediScan AI

Jenis Luka Teridentifikasi: ${recommendation.title}
Tingkat Kepercayaan Model: ${scan.confidence.toFixed(2)}%

---

Panduan Pertolongan Pertama:
${recommendation.guidance.map((item, index) => `${index + 1}. ${item}`).join('\n')}

---

Kapan Harus Mencari Bantuan Medis:
${recommendation.when_to_seek_help.map((item, index) => `${index + 1}. ${item}`).join('\n')}
                `;
                
                const tempTextarea = document.createElement('textarea');
                tempTextarea.value = recommendationText;
                document.body.appendChild(tempTextarea);
                tempTextarea.select();
                document.execCommand('copy');
                document.body.removeChild(tempTextarea);
                showToast("Rekomendasi berhasil disalin!");
            });
        }

        // Fungsi untuk merender halaman 'history'
        function renderHistoryPage() {
            const history = appState.scansHistory;
            
            let historyContent;
            if (history.length === 0) {
                historyContent = `
                    <div class="p-8 text-center">
                        <p class="text-gray-400 mb-6">Anda belum memiliki riwayat pemindaian.</p>
                        <button id="back-to-upload" class="button-primary w-full max-w-xs mt-4">
                            Kembali ke Halaman Utama
                        </button>
                    </div>
                `;
            } else {
                const historyItems = history.map((scan, index) => {
                    const recommendation = RECOMMENDATIONS[scan.name] || { title: "Tidak Dikenal" };
                    return `
                        <div class="glass-card p-4 flex items-center gap-4 cursor-pointer hover:shadow-lg transition-all duration-200">
                            <img src="${scan.imageUrl}" alt="Scan" class="w-16 h-16 object-cover rounded-lg shadow-md">
                            <div class="flex-1">
                                <p class="font-bold text-white">${recommendation.title}</p>
                                <p class="text-sm text-gray-400">Akurasi: ${scan.confidence.toFixed(2)}%</p>
                                <p class="text-xs text-gray-500 mt-1">${new Date(scan.timestamp).toLocaleString()}</p>
                            </div>
                            <button class="text-blue-400 hover:text-blue-500 font-semibold text-sm" onclick="showHistoryDetail(${index})">Lihat Detail</button>
                        </div>
                    `;
                }).join('');

                historyContent = `
                    <div class="p-8">
                        <div id="history-list" class="space-y-4">
                            ${historyItems}
                        </div>
                        <div class="mt-8 text-center flex flex-col sm:flex-row justify-center gap-4">
                            <button id="back-to-upload" class="button-secondary w-full sm:w-auto">
                                Kembali ke Halaman Utama
                            </button>
                            <button id="clear-history-button" class="button-secondary w-full sm:w-auto text-red-400 border border-red-900 hover:bg-red-900 hover:text-white">
                                Bersihkan Riwayat
                            </button>
                        </div>
                    </div>
                `;
            }

            appContent.innerHTML = `
                <div class="glass-card p-0 md:p-0 animate-fadeIn">
                    <h2 class="text-3xl font-bold text-white mb-4 text-center p-8 border-b border-slate-700">Riwayat Pemindaian</h2>
                    ${historyContent}
                </div>
            `;
            
            if (history.length > 0) {
                document.getElementById('clear-history-button').addEventListener('click', () => {
                    // Custom confirmation for better UI
                    if (confirm("Apakah Anda yakin ingin menghapus semua riwayat scan?")) {
                        appState.scansHistory = [];
                        localStorage.removeItem('mediscan_history');
                        renderApp();
                        showToast("Riwayat berhasil dibersihkan!");
                    }
                });
            }

            document.getElementById('back-to-upload').addEventListener('click', () => {
                appState.page = 'upload';
                renderApp();
            });
        }
        
        // Fungsi untuk menampilkan detail dari riwayat
        window.showHistoryDetail = (index) => {
            appState.predictionResult = appState.scansHistory[index];
            appState.page = 'result';
            renderApp();
        };

        // Fungsi utama untuk merender aplikasi berdasarkan state
        function renderApp() {
            // Hapus URL objek lama untuk menghindari kebocoran memori
            if (appState.page !== 'loading' && appState.uploadedFile) {
                // Pastikan file yang diunggah sebelumnya masih ada
                const oldUrl = URL.createObjectURL(appState.uploadedFile);
                URL.revokeObjectURL(oldUrl);
            }
            if (appState.page === 'upload') {
                renderUploadPage();
            } else if (appState.page === 'loading') {
                renderLoadingPage();
            } else if (appState.page === 'result') {
                renderResultPage();
            } else if (appState.page === 'history') {
                renderHistoryPage();
            }
        }

        // Jalankan aplikasi saat halaman dimuat
        window.onload = () => {
            showModal();
        };

        acceptDisclaimerButton.addEventListener('click', () => {
            hideModal();
            renderApp();
        });

    </script>
</body>
</html>
