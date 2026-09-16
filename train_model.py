"""
Script Training Model Prediksi Harga Mobil OLX (Versi Lengkap)
Alur:
1. Load dataset bersih
2. Ekstraksi tipe/seri mobil (model) dari teks 'judul'
3. Split train-test (80:20)
4. Pipeline Preprocessing (OneHotEncoder untuk kategorikal, Passthrough untuk numerik)
5. Komparasi performa model regresi:
   - Linear / Ridge Regression (Baseline)
   - Gradient Boosting Regressor
   - Random Forest Regressor
6. Simpan model terbaik ke 'model_prediksi_mobil.pkl'
"""

import pandas as pd
import numpy as np
import pickle
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# ============================================================
# 1. DAFTAR SERI MOBIL UNTUK EKSTRAKSI DARI JUDUL
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
    "ertiga", "xl7", "ignis", "baleno", "jimny", "karimun", "sx4", "s-presso", "grand vitara",
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
# 2. LOAD DATA & PERSIAPAN FITUR
# ============================================================
print("Membaca data bersih...")
df = pd.read_csv("dataset_olx_bersih.csv")

# Ekstraksi tipe/seri mobil ke kolom 'model'
df['model'] = df['judul'].apply(ekstrak_model)

# Atribut yang digunakan untuk memprediksi harga
fitur = ['merek', 'model', 'tahun', 'transmisi', 'jarak_tempuh']
target = 'harga'

df_model = df.dropna(subset=fitur + [target]).copy()

X = df_model[fitur]
y = df_model[target]

print(f"Total data siap training: {len(df_model)} baris")
print(f"Fitur: {fitur}")

# Split 80% data latih dan 20% data uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ============================================================
# 3. PIPELINE PREPROCESSING
# ============================================================
categorical_cols = ['merek', 'model', 'transmisi']
numerical_cols = ['tahun', 'jarak_tempuh']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
        ('num', 'passthrough', numerical_cols)
    ]
)

# ============================================================
# 4. TRAINING & EVALUASI KOMPARASI MODEL
# ============================================================
models = {
    "Ridge Regression (Baseline)": Ridge(),
    "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=150, random_state=42),
    "Random Forest Regressor": RandomForestRegressor(n_estimators=200, random_state=42)
}

print("\n" + "="*50)
print("HASIL EVALUASI KOMPARASI MODEL")
print("="*50)

best_model_name = None
best_model_pipeline = None
best_r2 = -np.inf

for nama_model, regressor in models.items():
    pipeline = Pipeline(steps=[
        ('prep', preprocessor),
        ('reg', regressor)
    ])
    
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"\nModel: {nama_model}")
    print(f"- R2 Score (Akurasi Variansi): {r2:.4f}")
    print(f"- MAE (Rata-rata Error)       : Rp {mae:,.0f}")
    print(f"- RMSE                       : Rp {rmse:,.0f}")
    
    if r2 > best_r2:
        best_r2 = r2
        best_model_name = nama_model
        best_model_pipeline = pipeline

print("\n" + "="*50)
print(f"Model Pemenang Terpilih: {best_model_name} (R2: {best_r2:.4f})")
print("="*50)

# ============================================================
# 5. SIMPAN MODEL FINAL
# ============================================================
with open("model_prediksi_mobil.pkl", "wb") as f:
    pickle.dump(best_model_pipeline, f)

print("\nModel terbaik berhasil disimpan ke 'model_prediksi_mobil.pkl'!")