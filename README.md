# 🚗 Prediksi Harga Mobil Bekas OLX

Proyek Data Mining untuk memprediksi harga mobil bekas menggunakan data yang di-scraping dari OLX Indonesia. Model machine learning dilatih menggunakan algoritma **Random Forest**, **Gradient Boosting**, dan **Ridge Regression**, lalu dipilih model dengan performa terbaik.

---

## 📁 Struktur File

```
scripts_prediksi/
│
├── scraping.py               # Scraping data iklan mobil dari OLX
├── kamus_slang_otomotif.py   # Kamus normalisasi teks otomotif
├── processing.py             # Preprocessing & pembersihan data
├── train_model.py            # Training & komparasi model ML
├── test_prediksi.py          # Pengujian prediksi menggunakan data riil
│
├── dataset_olx_mentah.csv    # Output scraping (data mentah)
├── dataset_olx_bersih.csv    # Output preprocessing (data bersih)
└── model_prediksi_mobil.pkl  # Model ML terbaik yang sudah dilatih
```

---

## ⚙️ Instalasi

### 1. Install library Python yang dibutuhkan

```bash
pip install pandas scikit-learn playwright
```

### 2. Install browser Chromium untuk Playwright (khusus scraping)

```bash
playwright install chromium
```

---

## 🔄 Urutan Langkah Pengolahan Data

### Langkah 1 — Scraping Data dari OLX (`scraping.py`)

Script ini membuka browser Chromium secara otomatis dan mengambil data iklan mobil bekas dari OLX Indonesia.

```bash
python scraping.py
```

**Output:** `dataset_olx_mentah.csv`

Kolom yang dikumpulkan:
- `id_iklan`, `judul`, `deskripsi`, `merek`, `model`, `tahun`, `transmisi`, `jarak_tempuh`, `harga`

> **Catatan:** Target default adalah **600 data**. Pastikan koneksi internet stabil saat menjalankan script ini.

---

### Langkah 2 — Preprocessing Data (`processing.py`)

Script ini membersihkan dan mempersiapkan data mentah agar siap dilatih oleh model.

```bash
python processing.py
```

**Input:** `dataset_olx_mentah.csv`  
**Output:** `dataset_olx_bersih.csv`

Proses yang dilakukan:
- ✅ Ekstraksi tahun dari kolom `judul` jika kolom `tahun` kosong
- ✅ Deteksi transmisi (otomatis/manual) dari teks judul
- ✅ Pembersihan format angka harga & jarak tempuh (termasuk rentang seperti `65.000-70.000`)
- ✅ Penghapusan data duplikat
- ✅ Pengisian nilai jarak tempuh yang kosong dengan nilai median
- ✅ Filter outlier (harga Rp 25 juta – Rp 2,5 miliar, tahun 1995–2026)
- ✅ Normalisasi teks menggunakan `kamus_slang_otomotif.py`

---

### Langkah 3 — Training Model (`train_model.py`)

Script ini melatih dan membandingkan 3 model machine learning, lalu menyimpan model terbaik.

```bash
python train_model.py
```

**Input:** `dataset_olx_bersih.csv`  
**Output:** `model_prediksi_mobil.pkl`

Fitur yang digunakan untuk prediksi:
- `merek`, `model` (seri mobil), `tahun`, `transmisi`, `jarak_tempuh`

Model yang dibandingkan:
| Model | Keterangan |
|-------|-----------|
| Ridge Regression | Baseline / model sederhana |
| Gradient Boosting Regressor | Boosting ensemble |
| Random Forest Regressor | Bagging ensemble (200 estimators) |

Metrik evaluasi: **R² Score**, **MAE**, **RMSE**

---

### Langkah 4 — Pengujian Prediksi (`test_prediksi.py`)

Script ini menguji model yang sudah dilatih menggunakan 5 sampel data riil dari dataset bersih.

```bash
python test_prediksi.py
```

**Input:** `dataset_olx_bersih.csv`, `model_prediksi_mobil.pkl`

Contoh output:
```
Unit [1]: Toyota Avanza 2019 Matic
- Input Model   : Toyota Avanza | 2019 | otomatis | 45,000 km
- Harga Asli OLX: Rp 155,000,000
- Prediksi Model: Rp 148,500,000
- Selisih/Error : Rp 6,500,000
```

---

## 🛠️ Teknologi yang Digunakan

- **Python 3.x**
- **Pandas** — manipulasi & analisis data
- **Scikit-learn** — machine learning pipeline & evaluasi model
- **Playwright** — web scraping berbasis browser

---

## 📊 Alur Sistem

```
OLX.co.id
    │
    ▼
[scraping.py] ──────────────► dataset_olx_mentah.csv
                                        │
                                        ▼
                             [processing.py] ─────────► dataset_olx_bersih.csv
                                                                  │
                                                                  ▼
                                                       [train_model.py] ──────► model_prediksi_mobil.pkl
                                                                                          │
                                                                                          ▼
                                                                              [test_prediksi.py]
```

---

## 📝 Catatan

- Pastikan menjalankan script **sesuai urutan** (scraping → processing → training → testing).
- File `model_prediksi_mobil.pkl` sudah tersedia di repository sehingga Anda bisa langsung menjalankan `test_prediksi.py` tanpa perlu scraping ulang.
- Jika ingin memperbarui data, jalankan ulang dari langkah 1.

---

## ⚠️ Disclaimer

Dataset yang digunakan dalam proyek ini diperoleh melalui web scraping dari OLX Indonesia semata-mata untuk keperluan **akademis dan edukasi**.
Proyek ini tidak berafiliasi dengan OLX dan tidak digunakan untuk tujuan komersial.