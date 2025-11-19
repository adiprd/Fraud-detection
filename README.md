# Aplikasi Deteksi Penipuan AI

## Gambaran Umum

Aplikasi web berbasis Flask yang komprehensif untuk mendeteksi transaksi keuangan mencurigakan secara real-time. Sistem ini menggunakan pengenalan pola berbasis aturan dan teknik machine learning untuk mengidentifikasi aktivitas mencurigakan.

## Fitur Utama

- **Monitoring Transaksi Real-time**: Analisis berkelanjutan terhadap transaksi keuangan
- **Deteksi Penipuan Cerdas**: Multiple aturan deteksi dan pengenalan pola
- **Penilaian Risiko**: Scoring risiko otomatis dan klasifikasi
- **Analisis Visual**: Dashboard dan chart interaktif
- **Sistem Peringatan**: Notifikasi langsung untuk transaksi berisiko tinggi
- **Monitoring Karyawan**: Pelacakan pola transaksi per karyawan

## Persyaratan Teknis

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Dependencies
- Flask==2.3.3
- pandas==2.1.4
- numpy==1.26.0
- scikit-learn==1.3.2
- matplotlib==3.8.2
- faker==21.0.0
- werkzeug==2.3.7

## Struktur Proyek

```
fraud_detection_ai/
├── app.py                 # Aplikasi utama Flask
├── requirements.txt       # Dependencies Python
├── data/
│   ├── transactions.csv   # Data transaksi sample
│   └── fraud_rules.csv    # Aturan deteksi penipuan
├── templates/
│   ├── index.html        # Halaman utama
│   ├── dashboard.html    # Dashboard monitoring
│   └── error.html        # Halaman error
└── static/
    └── css/              # File stylesheet
```

## Aturan Deteksi Penipuan

Sistem menggunakan beberapa aturan untuk mendeteksi transaksi mencurigakan:

1. **Transaksi Amount Tinggi**: Amount melebihi 3x rata-rata transaksi
2. **Waktu Tidak Biasa**: Transaksi di luar jam kerja (23:00-05:00)
3. **Vendor Baru**: Transaksi dengan vendor yang belum pernah digunakan
4. **Frekuensi Tinggi**: Multiple transaksi dalam waktu singkat
5. **Transaksi Weekend**: Biaya bisnis di akhir pekan

## Instalasi dan Menjalankan

### 1. Setup Environment
```bash
cd fraud_detection_ai
pip install -r requirements.txt
```

### 2. Menjalankan Aplikasi
```bash
python app.py
```

### 3. Akses Aplikasi
Buka browser dan akses: http://localhost:5000

## Penggunaan

### Halaman Utama
- Tampilan overview fitur aplikasi
- Tombol untuk masuk ke dashboard

### Dashboard Monitoring
- **Statistik Utama**: Total transaksi, risiko tinggi, transaksi terflag
- **Distribusi Risiko**: Chart pie distribusi level risiko
- **Alert Kritis**: Daftar transaksi berisiko tinggi yang memerlukan tindakan
- **Distribusi Skor Penipuan**: Histogram skor penipuan
- **Karyawan Berisiko**: Daftar karyawan dengan skor risiko tertinggi
- **Dampak Keuangan**: Analisis dampak finansial transaksi mencurigakan

### API Endpoints
- `GET /` - Halaman utama
- `GET /dashboard` - Dashboard monitoring
- `POST /api/check_transaction` - API untuk mengecek transaksi individual
- `GET /api/transactions` - API untuk mendapatkan data transaksi

## Data Sample

Aplikasi dilengkapi dengan data sample yang meliputi:
- 500 transaksi simulasi
- 5 karyawan sample dari berbagai departemen
- Multiple vendor dan kategori transaksi
- Pattern transaksi mencurigakan yang sengaja disisipkan

## Skoring Risiko

Sistem memberikan skor risiko berdasarkan aturan yang dilanggar:

- **Risiko Rendah (0-39)**: Monitor saja
- **Risiko Menengah (40-59)**: Perlu review
- **Risiko Tinggi (60-100)**: Blokir dan alert security

## Pengembangan

### Menambah Aturan Deteksi Baru
Edit file `app.py` pada class `FraudDetector` method `detect_fraud_patterns`

### Modifikasi Data Sample
Edit function `generate_sample_data` untuk menyesuaikan pattern data

### Customisasi Tampilan
Edit file HTML di folder `templates` dan CSS di folder `static/css`

## Troubleshooting

### Data Tidak Terload
- Pastikan file CSV ada di folder `data/`
- Check permission akses file

### Dependencies Error
- Update pip: `python -m pip install --upgrade pip`
- Install ulang requirements: `pip install -r requirements.txt`

### Port Already in Use
- Ganti port di `app.run(port=5001)`
- Kill process yang menggunakan port 5000

## Keamanan

Aplikasi ini ditujukan untuk demonstrasi dan pengembangan. Untuk environment production, pertimbangkan:
- Autentikasi dan autorisasi
- Enkripsi data sensitif
- Secure database connection
- Input validation yang ketat

## Kontribusi

Untuk pengembangan lebih lanjut, silakan:
1. Fork repository
2. Buat feature branch
3. Commit changes
4. Push ke branch
5. Buat Pull Request

## Support

Untuk issues dan pertanyaan teknis, buka ticket di sistem issue tracking project.
