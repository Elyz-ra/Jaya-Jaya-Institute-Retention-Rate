# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding
Jaya Jaya Institute adalah sebuah lembaga pendidikan berbasis teknologi (edutech) yang berfokus pada peningkatan kualitas akademik dan retensi mahasiswa. Salah satu tantangan utama yang dihadapi adalah tingginya angka dropout mahasiswa yang dapat berdampak pada reputasi institusi dan efisiensi operasional. Untuk itu, diperlukan sistem yang mampu memprediksi risiko mahasiswa putus studi agar tindakan preventif dapat diambil lebih awal.

### Permasalahan Bisnis
- Tingginya angka dropout mahasiswa tanpa indikasi awal.
- Kurangnya alat bantu untuk mengidentifikasi mahasiswa berisiko tinggi.
- Belum adanya visualisasi data yang memadai bagi pihak manajemen untuk memahami pola dropout.

### Cakupan Proyek
1. Melakukan eksplorasi dan analisis data mahasiswa yang dikumpulkan dari database internal Supabase.
2. Mengembangkan business dashboard interaktif untuk menunjukkan distribusi status mahasiswa, gender, dan korelasi nilai awal dengan risiko dropout.
3. Membangun sistem machine learning berbasis XGBoost untuk memprediksi kemungkinan mahasiswa mengalami dropout.
4. Menyediakan antarmuka prediksi yang dapat digunakan oleh pihak manajemen akademik.

### Persiapan

Sumber data: Github (https://github.com/dicodingacademy/dicoding_dataset/tree/main/students_performance)  

1. **Setup Environment - Anaconda:**
    - Buat environment baru
    `conda create --name student-dashboard python=3.9`
    `conda activate student-dashboard`
    - Install library yang diperlukan
    `pip install -r requirements.txt`

2. **Setup Environment - Shell/Terminal:**
    - Install pipenv terlebih dahulu
    `pip install pipenv`
    - Buat dan masuk ke virtual environment
    `pipenv install`
    `pipenv shell`
    - Install dependensi
    `pip install -r requirements.txt`

3. **Install Docker Desktop**  
   - Download dan install Docker Desktop dari [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).  
   - Pastikan Docker Desktop sudah berjalan.

4. **Mempersiapkan Database**

    - Pastikan file dataset `data.csv` berada di direktori proyek ini.  
    - Jalankan kode berikut untuk memasukkan data ke Supabase:
    `pip install sqlalchemy psycopg2 pandas`

    ```python
    import pandas as pd
    from sqlalchemy import create_engine

    file_path = 'data.csv'
    data = pd.read_csv(file_path)

    URL = "postgresql://postgres.csfaqojfluduffilprnd:elyzSupabase00@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"
 
    engine = create_engine(URL)
    df.to_sql('Student', engine)
    ```

5. **Menjalankan Metabase di Docker Desktop:**
    - Buka Docker Desktop, lalu buka terminal (Command Prompt/PowerShell/Terminal).
    - Jalankan perintah berikut untuk menarik image Metabase:
    `docker pull metabase/metabase:latest`
    - Jalankan container Metabase:
    `docker run -d -p 3000:3000 --name jayajayainstitute metabase/metabase` atau klik tombol play di docker desktop
    - Buka `http://localhost:3000` di browser
    - email : elyziajanarakhansa@gmail.com
    - password : elyzMetabase00

6. Akses Database di Metabase:
    - Lakukan konfigurasi Metabase:
    - Database Type: PostgreSQL
    - Host: aws-0-ap-southeast-1.pooler.supabase.com
    - Port: 5432
    - Database Name: postgres
    - Username: postgres.csfaqojfluduffilprnd
    - Password: elyzSupabase00
    - SSL: Yes

## Business Dashboard
Pada proyek ini, data scientist membuat business dashboard di Metabase untuk membantu departemen HR dalam memahami faktor-faktor yang mempengaruhi attrition rate.

### Informasi Akses Dashboard :
email : elyziajanarakhansa@gmail.com
pass : elyzMetabase00

### Deskripsi Dashboard

![Business Dashboard](Elyzia_Janara-dashboard.png)

1. Distribusi Status Siswa
    - Mayoritas mahasiswa berstatus Enrolled (terdaftar), diikuti oleh Graduate (lulus), dan Dropout (keluar).
    - Jumlah dropout cukup signifikan, menunjukkan perlunya intervensi untuk mengurangi angka ini.

2. Dropout Berdasarkan Gender
    - Male (pria) memiliki angka dropout lebih tinggi dibandingkan Female (wanita).
    - Perlu diteliti faktor penyebabnya, seperti motivasi, dukungan finansial, atau lingkungan akademik.

3. Dropout berdasarkan Marital Status
    - Mahasiswa dengan status Single (lajang) mendominasi jumlah dropout.
    - Status pernikahan seperti Married (menikah) atau Legally Separated (cerai) juga berkontribusi, tetapi lebih rendah.
    - Kemungkinan mahasiswa single kurang memiliki tanggung jawab atau dukungan keluarga yang mendorong kelulusan.

4. Dropout berdasarkan umur
    - Kelompok usia 17-20 dan 21-24 memiliki angka dropout tertinggi.
    - Ini mungkin karena masa transisi dari sekolah menengah ke perguruan tinggi atau ketidakstabilan dalam memilih jurusan.
    - Kelompok usia 31+ memiliki dropout terendah, mungkin karena lebih matang dan fokus.

5. Rata Rata GPA per Semester berdasarkan Status Siswa
    - Mahasiswa yang Graduate memiliki IPK lebih tinggi secara konsisten di setiap semester.
    - Mahasiswa Dropout menunjukkan penurunan atau stagnasi IPK sebelum keluar.
    - Ini bisa menjadi indikator awal untuk mengidentifikasi mahasiswa berisiko dropout berdasarkan kinerja akademik.

## Menjalankan Sistem Machine Learning
1. Persiapan
    - Menginstall Python (≥3.9) dan library yang diperlukan (pip install -r requirements.txt).
    - Dataset atau koneksi database (misalnya Supabase) sudah terkonfigurasi.

2. Menjalankan Aplikasi
    - Aktifkan Environment (jika menggunakan virtual env):
    `conda activate student-dashboard  # Untuk Anaconda`
    `pipenv shell                     # Untuk Pipenv`
    
    - Jalankan Streamlit:
    `streamlit run app.py`
    Aplikasi akan berjalan di http://localhost:8501 dan otomatis terbuka di browser.

3. Link Deployment dapat diakses pada :
    https://jaya-jaya-institute-retention-rate.streamlit.app


## Conclusion
Berdasarkan analisis dashboard retensi mahasiswa, dapat teridentifikasi tiga masalah utama beserta solusi terpadu:

1. Penanganan Angka Dropout Tinggi
    Insight menunjukkan mahasiswa pria usia 17-24 tahun dengan status single paling rentan dropout, dengan indikator penurunan IPK yang konsisten. Solusinya kami tawarkan sistem early warning berbasis IPK dan data demografis, didukung program mentoring dan konseling akademik khusus untuk kelompok berisiko ini.

2. Sistem Identifikasi Risiko Terpadu
    Temuan utama mengungkap gender, usia, dan status pernikahan sebagai faktor risiko kunci. Untuk mengatasinya, kami rekomendasikan pembangunan model prediktif machine learning yang mengintegrasikan IPK, kehadiran, dan data demografis, dengan dukungan dashboard real-time Metabase untuk pemantauan berkala.

3. Visualisasi Data Strategis
    Dashboard telah berhasil memetakan pola dropout melalui berbagai dimensi. Kami mengusulkan pengembangan dashboard interaktif Streamlit/Metabase yang memungkinkan manajemen melakukan analisis tren secara visual dan penyaringan data multidimensi (jurusan/semester).

**Rencana Aksi Implementasi:**
1. Teknologi: Integrasi Streamlit (prediksi) dan Metabase (monitoring)
2. Kebijakan: Wajibkan konseling & tingkatkan kapasitas dosen
3. Pengembangan: Sistem integrasi data real-time

**Target Kinerja:**
1. Penurunan dropout 20-30% dalam 1 tahun
2. Peningkatan kualitas keputusan berbasis data

Solusi terintegrasi ini dirancang untuk memberikan dampak signifikan dalam meningkatkan retensi mahasiswa melalui pendekatan data-driven yang komprehensif.

### Rekomendasi Action Items
1. Program pendampingan untuk mahasiswa baru (usia 17-24) dan mahasiswa pria.
2. Monitoring IPK secara berkala untuk mendeteksi mahasiswa berisiko.
3. Dukungan finansial atau psikologis bagi mahasiswa yang memiliki tantangan personal.
4. Intervensi dini bagi mahasiswa dengan penurunan IPK untuk mencegah dropout.