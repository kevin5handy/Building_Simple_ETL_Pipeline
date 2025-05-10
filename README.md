
# 🧵 Web Scraping & Data Pipeline Produk Fashion

Proyek ini merupakan pipeline ETL (Extract-Transform-Load) berbasis Python yang digunakan untuk melakukan scraping data produk fashion dari website e-commerce fiktif. Data hasil scraping kemudian dibersihkan, ditransformasi, dan disimpan ke tiga media: file CSV, PostgreSQL, dan Google Sheets.

## 🗂️ Struktur Proyek

```
.
├── main.py                         # Main runner
├── requirements.txt               # Daftar dependency
├── products.csv                   # Output data (CSV)
├── submission.txt                 # Catatan tugas (opsional)
├── google-sheets-api.json        # Kredensial Google Sheets API
├── utils/
│   ├── extract.py                 # Fungsi scraping dan ekstraksi data
│   ├── transform.py              # Pembersihan dan transformasi data
│   └── load.py                   # Simpan ke CSV, PostgreSQL, dan Google Sheets
├── tests/
│   ├── test_extract.py           # Unit test untuk extract.py
│   ├── test_transform.py         # Unit test untuk transform.py
│   └── test_load.py              # Unit test untuk load.py
```

## 🚀 Cara Menjalankan Proyek

1. **Install semua dependency**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan pipeline**:
   ```bash
   python main.py
   ```

3. **Hasil akan disimpan ke**:
   - `products.csv`
   - Tabel `bookstoscrape` di PostgreSQL
   - Google Sheets (akses via Spreadsheet ID)

## ⚙️ Konfigurasi yang Diperlukan

### ✅ PostgreSQL
Pastikan kamu sudah membuat database dan mengganti URL koneksi pada `main.py`:
```python
db_url = 'postgresql+psycopg2://username:password@localhost:5432/namadb'
```

### ✅ Google Sheets API
1. Aktifkan Google Sheets API dari Google Cloud Console.
2. Buat `Service Account` dan unduh file `client_secret.json` (ganti namanya jadi `google-sheets-api.json`).
3. Share spreadsheet ke email service account agar bisa menulis.

## 🧪 Menjalankan Unit Test

**Jalankan semua unit test:**
```bash
python -m pytest tests/
```

**Dengan coverage report:**
```bash
pytest --cov=utils tests/
```

## ✅ Fitur Utama
- Scraping multi halaman dari e-commerce fiktif
- Ekstraksi detail produk: nama, harga, rating, warna, ukuran, gender
- Data cleaning & transformasi (regex, konversi numerik, konversi mata uang)
- Penyimpanan data ke:
  - `.csv` lokal
  - PostgreSQL
  - Google Sheets
- > 80% test coverage untuk semua fungsi utama

## 🛠️ Teknologi yang Digunakan
- Python 3
- `requests`, `BeautifulSoup` untuk scraping
- `pandas` untuk transformasi data
- `sqlalchemy` untuk koneksi ke PostgreSQL
- `google-api-python-client` untuk Google Sheets
- `pytest` dan `unittest.mock` untuk testing

## 👨‍💻 Kontributor
- Kevin M. Shandy

## 📄 Lisensi
Proyek ini dapat digunakan bebas untuk keperluan edukasi dan non-komersial.
