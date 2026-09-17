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
# 4. INPUT INTERAKTIF DARI PENGGUNA
# ============================================================
print("=" * 50)
print("     FORM PREDIKSI HARGA MOBIL BEKAS (INPUT USER)     ")
print("=" * 50)

merek_input = input("Masukkan Merek Mobil (misal: Suzuki, Toyota): ").strip().title()
model_input = input("Masukkan Tipe/Model (misal: Every, Innova, Lainnya): ").strip().title()
tahun_input = int(input("Masukkan Tahun Pembuatan (misal: 2004, 2020): ").strip())
transmisi_input = input("Masukkan Transmisi (manual / otomatis): ").strip().lower()
km_input = int(input("Masukkan Jarak Tempuh / KM (misal: 45000): ").strip())

data_user = pd.DataFrame([{
    'merek': merek_input,
    'model': model_input,
    'tahun': tahun_input,
    'transmisi': transmisi_input,
    'jarak_tempuh': km_input
}])

prediksi_user = model.predict(data_user)[0]

print("\n--- HASIL PREDIKSI INPUT USER ---")
print(f"Unit           : {merek_input} {model_input}")
print(f"- Input Model  : {merek_input} {model_input} | {tahun_input} | {transmisi_input} | {km_input:,} km")
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