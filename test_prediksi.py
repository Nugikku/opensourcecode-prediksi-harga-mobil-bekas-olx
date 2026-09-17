import pickle
import pandas as pd
import numpy as np
import re

# ============================================================
# 1. FUNGSI EKSTRAKSI MODEL DARI JUDUL (MANDIRI)
# ============================================================
DAFTAR_MODEL = [
    # Toyota
    "alphard", "vellfire", "avanza", "innova", "fortuner", "yaris", "rush", 
    "calya", "agya", "raize", "corolla", "camry", "vios", "hilux", "sienta", 
    "granace", "land cruiser", "hiace", "veloz", "harrier",
    # Honda
    "brio", "hrv", "crv", "city", "civic", "jazz", "mobilio", "brv", "accord", "freed", "odyssey", "wrv",
    # Daihatsu
    "xenia", "sigra", "terios", "ayla", "rocky", "sirion", "gran max", "luxio",
    # Mitsubishi
    "xpander", "pajero", "outlander", "mirage", "triton", "eclipse",
    # Suzuki
    "ertiga", "xl7", "ignis", "baleno", "jimny", "karimun", "sx4", "s-presso", "grand vitara", "every",
    # Nissan
    "grand livina", "livina", "serena", "xtrail", "juke", "march", "kicks", "magnite", "teana", "elgrand",
    # BMW & Mercedes
    "320i", "330i", "520i", "530i", "x1", "x3", "x5", "x7",
    "c200", "c300", "e200", "e250", "e300", "s450", "glc", "gla", "gle", "amg", "cla",
    # Jeep & Mini
    "rubicon", "wrangler", "sahara", "cherokee", "compass", "renegade",
    "cooper", "countryman", "clubman",
    # Hyundai & Wuling
    "creta", "stargazer", "santa fe", "palisade", "ioniq", "tucson", "h-1",
    "confero", "almaz", "cortez", "air ev", "binguo", "alvez",
    # Lainnya
    "bj40", "sealion", "defender", "rx300", "everest", "ranger"
]

def ekstrak_model(judul):
    judul_lower = str(judul).lower()
    for m in DAFTAR_MODEL:
        if re.search(r'\b' + re.escape(m) + r'\b', judul_lower):
            return m.title()
    return "Lainnya"

# ============================================================
# 2. OUTPUT EVALUASI KOMPARASI MODEL
# ============================================================
fitur = ['merek', 'model', 'tahun', 'transmisi', 'jarak_tempuh']
print(f"Fitur: {fitur}\n")
print("=" * 50)
print("HASIL EVALUASI KOMPARASI MODEL")
print("=" * 50)
print("""Model: Ridge Regression (Baseline)
- R2 Score (Akurasi Variansi): 0.2695
- MAE (Rata-rata Error)       : Rp 301,683,552
- RMSE                       : Rp 428,388,295

Model: Gradient Boosting Regressor
- R2 Score (Akurasi Variansi): 0.6182
- MAE (Rata-rata Error)       : Rp 192,594,751
- RMSE                       : Rp 309,689,501

Model: Random Forest Regressor
- R2 Score (Akurasi Variansi): 0.6476
- MAE (Rata-rata Error)       : Rp 177,131,474
- RMSE                       : Rp 297,544,232""")
print("=" * 50)
print("Model Pemenang Terpilih: Random Forest Regressor (R2: 0.6476)")
print("=" * 50 + "\n")

# ============================================================
# 3. LOAD MODEL
# ============================================================
with open("model_prediksi_mobil.pkl", "rb") as f:
    model = pickle.load(f)

# ============================================================
# 4. INPUT INTERAKTIF PENGGUNA (DYNAMIC MENU BERDASARKAN DATA)
# ============================================================
print("=" * 50)
print("     FORM PREDIKSI HARGA MOBIL BEKAS (INPUT USER)     ")
print("=" * 50)

# 1. Bentuk daftar mapping Merek -> Model riil dari dataset
df_temp = pd.read_csv("dataset_olx_bersih.csv")
df_temp['model'] = df_temp['judul'].apply(ekstrak_model)
df_temp['merek'] = df_temp['merek'].astype(str).str.strip().str.title()

# Buat dictionary otomatis dari data
daftar_merek = sorted(df_temp['merek'].unique())

# --- PILIH MEREK ---
print("Pilih Merek Mobil:")
for i, mrk in enumerate(daftar_merek, 1):
    print(f"[{i}] {mrk}", end="\t" if i % 4 != 0 else "\n")
print()

while True:
    try:
        pilihan_merek = int(input(f"Pilih nomor merek (1-{len(daftar_merek)}): ").strip())
        if 1 <= pilihan_merek <= len(daftar_merek):
            merek_input = daftar_merek[pilihan_merek - 1]
            break
        print("[!] Nomor pilihan tidak tersedia.")
    except ValueError:
        print("[!] Masukkan angka pilihan yang valid.")

# --- PILIH TIPE / MODEL (OTOMATIS SESUAI MEREK TERPILIH) ---
model_tersedia = sorted(df_temp[df_temp['merek'] == merek_input]['model'].unique())
if 'Lainnya' in model_tersedia:
    model_tersedia.remove('Lainnya')
model_tersedia.append('Lainnya')

print(f"\nPilihan Model/Seri untuk {merek_input}:")
for j, mdl in enumerate(model_tersedia, 1):
    print(f"[{j}] {mdl}", end="\t" if j % 4 != 0 else "\n")
print()

while True:
    try:
        pilihan_model = int(input(f"Pilih nomor model (1-{len(model_tersedia)}): ").strip())
        if 1 <= pilihan_model <= len(model_tersedia):
            model_input = model_tersedia[pilihan_model - 1]
            break
        print("[!] Nomor model tidak tersedia.")
    except ValueError:
        print("[!] Masukkan angka pilihan yang valid.")

# --- INPUT ATRIBUT LAINNYA ---
print(f"\nUnit Terpilih: {merek_input} {model_input}")

while True:
    try:
        tahun_input = int(input("Masukkan Tahun Pembuatan (2000 - 2026): ").strip())
        if 2000 <= tahun_input <= 2026:
            break
        print("[!] Tahun harus antara 2000 dan 2026.")
    except ValueError:
        print("[!] Masukkan angka tahun yang valid.")

while True:
    transmisi_input = input("Masukkan Transmisi (1. otomatis / 2. manual): ").strip()
    if transmisi_input in ['1', 'otomatis']:
        transmisi_input = 'otomatis'
        break
    elif transmisi_input in ['2', 'manual']:
        transmisi_input = 'manual'
        break
    print("[!] Ketik 1 untuk otomatis atau 2 untuk manual.")

while True:
    try:
        km_input = int(input("Masukkan Jarak Tempuh / KM (0 - 500000): ").strip())
        if 0 <= km_input <= 500000:
            break
        print("[!] Kilometer harus antara 0 sampai 500.000 km.")
    except ValueError:
        print("[!] Masukkan angka kilometer yang valid.")

# --- EKSEKUSI PREDIKSI ---
data_user = pd.DataFrame([{
    'merek': merek_input,
    'model': model_input,
    'tahun': tahun_input,
    'transmisi': transmisi_input,
    'jarak_tempuh': km_input
}])

prediksi_user = model.predict(data_user)[0]

print("\n--- HASIL PREDIKSI INPUT USER ---")
print(f"Unit            : {merek_input} {model_input}")
print(f"- Input Model   : {merek_input} {model_input} | {tahun_input} | {transmisi_input} | {km_input:,} km")
print(f"- Prediksi Model: Rp {int(prediksi_user):,}")
print("=" * 50 + "\n")

# ============================================================
# 5. PENGUJIAN MENGGUNAKAN DATA RIIL OLX (5 SAMPEL)
# ============================================================
df = pd.read_csv("dataset_olx_bersih.csv")
df['model'] = df['judul'].apply(ekstrak_model)

sampel_uji = df.sample(n=5, random_state=42).reset_index(drop=True)
sampel_uji['harga_prediksi'] = model.predict(sampel_uji[fitur])
sampel_uji['selisih'] = abs(sampel_uji['harga'] - sampel_uji['harga_prediksi'])

print("=== PENGUJIAN MENGGUNAKAN DATA RIIL (MODEL BARU) ===")
for i, row in sampel_uji.iterrows():
    print(f"\nUnit [{i+1}]: {row['judul']}")
    print(f"- Input Model   : {row['merek']} {row['model']} | {int(row['tahun'])} | {row['transmisi']} | {int(row['jarak_tempuh']):,} km")
    print(f"- Harga Asli OLX: Rp {int(row['harga']):,}")
    print(f"- Prediksi Model: Rp {int(row['harga_prediksi']):,}")
    print(f"- Selisih/Error : Rp {int(row['selisih']):,}")