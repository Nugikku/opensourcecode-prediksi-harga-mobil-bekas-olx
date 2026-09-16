import pickle
import pandas as pd
import re

# 1. Load Model
with open("model_prediksi_mobil.pkl", "rb") as f:
    model = pickle.load(f)

# 2. Fungsi pembantu ekstraksi model dari judul
from train_model import ekstrak_model

# 3. Load Data Uji
df = pd.read_csv("dataset_olx_bersih.csv")
df['model'] = df['judul'].apply(ekstrak_model)

sampel_uji = df.sample(n=5, random_state=42).reset_index(drop=True)

fitur = ['merek', 'model', 'tahun', 'transmisi', 'jarak_tempuh']
sampel_uji['harga_prediksi'] = model.predict(sampel_uji[fitur])
sampel_uji['selisih'] = abs(sampel_uji['harga'] - sampel_uji['harga_prediksi'])

print("=== PENGUJIAN MENGGUNAKAN DATA RIIL (MODEL BARU) ===")
for i, row in sampel_uji.iterrows():
    print(f"\nUnit [{i+1}]: {row['judul']}")
    print(f"- Input Model   : {row['merek']} {row['model']} | {int(row['tahun'])} | {row['transmisi']} | {int(row['jarak_tempuh']):,} km")
    print(f"- Harga Asli OLX: Rp {int(row['harga']):,}")
    print(f"- Prediksi Model: Rp {int(row['harga_prediksi']):,}")
    print(f"- Selisih/Error : Rp {int(row['selisih']):,}")