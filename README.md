# Automation Test Chatbot LUNA

## Deskripsi
Project ini bertujuan untuk melakukan automation testing pada chatbot LUNA. Proses automation meliputi:
1. Membaca daftar pertanyaan dari file CSV.
2. Membuka website LUNA menggunakan Playwright.
3. Mengucapkan setiap pertanyaan menggunakan Text-to-Speech (TTS).
4. Merekam jawaban audio dari LUNA.
5. Mengubah jawaban audio menjadi teks menggunakan Speech-to-Text (STT).
6. Menyimpan hasil percakapan ke dalam file CSV baru.

## Metode Perekaman Audio Baru (PENTING!)
Versi terbaru ini **tidak lagi menggunakan microphone** untuk merekam jawaban LUNA. Sebagai gantinya, program ini merekam **audio output langsung dari sistem** melalui perangkat virtual bernama **"Stereo Mix"** atau "Wave Out".

**Keuntungan:**
- **Kualitas audio jernih**: Tidak ada lagi suara bising dari luar atau gema ruangan.
- **Akurasi STT lebih tinggi**: Transkripsi menjadi jauh lebih akurat.
- **Tidak perlu microphone fisik**: Proses berjalan sepenuhnya secara internal.

**Syarat Wajib:**
- **Perangkat perekam loopback audio** harus diaktifkan. Anda bisa memilih salah satu:
  1.  **Stereo Mix**: Biasanya sudah tersedia di Windows, hanya perlu diaktifkan.
  2.  **VB-Audio Virtual Cable**: Alternatif gratis jika "Stereo Mix" tidak ada. Perlu di-download dan di-install.

## Setup Awal (Hanya sekali)
Sebelum menjalankan program, Anda wajib melakukan setup berikut:

### 1. Aktifkan Perangkat Perekam Loopback
- Jalankan file `setup.bat` yang sudah disediakan.
- Ikuti instruksi yang muncul di layar untuk mengaktifkan "Stereo Mix" atau "CABLE Output" (dari VB-Cable).
- Jika Anda tidak memiliki "Stereo Mix", Anda bisa menginstall **VB-Audio Virtual Cable** dari [https://vb-audio.com/Cable/](https://vb-audio.com/Cable/).

### 2. Install FFmpeg (Untuk Playback Audio)
- **Download FFmpeg:** Kunjungi [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/) dan download `ffmpeg-release-essentials.zip`.
- **Ekstrak File:** Ekstrak file zip yang sudah di-download ke lokasi yang mudah diakses (contoh: `C:\ffmpeg`).
- **Tambahkan ke PATH:**
    1. Buka Start Menu, ketik "Edit the system environment variables", dan buka.
    2. Klik tombol "Environment Variables...".
    3. Di bagian "System variables", cari dan pilih variabel `Path`, lalu klik "Edit".
    4. Klik "New" dan tambahkan path ke folder `bin` di dalam folder FFmpeg Anda (contoh: `C:\ffmpeg\bin`).
    5. Klik OK di semua jendela untuk menyimpan.
- **Verifikasi:** Buka Command Prompt baru dan ketik `ffmpeg -version`. Jika instalasi berhasil, Anda akan melihat informasi versi FFmpeg.

### 3. Install Dependencies Python
- Jalankan `pip install -r requirements.txt` untuk menginstall semua library Python yang dibutuhkan.

## Cara Menjalankan
1. Pastikan `Stereo Mix` sudah aktif (lihat setup di atas).
2. Isi file `data/input.csv` dengan daftar pertanyaan yang ingin diuji.
3. Jalankan `run.bat` atau `python main.py`.
4. Program akan membuka browser Chrome, mengunjungi website LUNA, dan memulai proses tanya-jawab.
5. Setelah selesai, hasil akan tersimpan di `data/output.csv`.

## Konfigurasi
Anda bisa mengubah beberapa pengaturan di file `config.py`:
- `CHROME_PATH`: Lokasi file `chrome.exe` di komputer Anda.
- `LUNA_URL`: URL dari chatbot LUNA.
- `INPUT_CSV` dan `OUTPUT_CSV`: Lokasi file input dan output.
- `WAKE_WORD`: Kata sapaan untuk memulai percakapan (misal: "halo erva").
- `SILENCE_THRESHOLD`: Batas waktu (detik) program akan berhenti merekam jika tidak ada suara.

## Deployment on Free Hosting Platforms (e.g., Vercel, Railway)

This application can be deployed to a free hosting platform, but with some limitations. These platforms are designed for web applications and do not provide the necessary hardware or drivers for the audio recording and speech-to-text features to work.

### Limitations

*   **Audio Recording and Speech-to-Text:** The audio-related features of this application will not work on free hosting platforms. The application will gracefully skip these steps and only perform the text-based part of the test.
*   **Headless Browser:** The browser will always run in headless mode. You will not see a "pop-up" of the Chrome browser.

### Instructions

1.  **Fork this repository.**
2.  **Create a new project on your hosting platform and connect it to your forked repository.**
3.  **Configure the following environment variables:**
    *   `REDIS_URL`: The URL of your Redis instance. Most hosting platforms provide this as a service.
    *   `SECRET_KEY`: A long, random string to secure your application.
4.  **Deploy the application.** The hosting platform should automatically detect the `Procfile` and start the web server and Celery worker.
