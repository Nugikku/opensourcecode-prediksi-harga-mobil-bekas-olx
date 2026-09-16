import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import re

async def scrape_olx(target_data=600):
    all_cars = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        # Menetapkan ukuran layar standar agar tombol tidak tersembunyi
        context = await browser.new_context(
            viewport={'width': 1366, 'height': 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # --- LOGIKA BARU: Tangkap Data Tanpa Memperdulikan Nama URL-nya ---
        async def tangkap_response(response):
            # Hanya periksa respons yang merupakan paket data JSON
            if "application/json" in response.headers.get("content-type", ""):
                try:
                    res_json = await response.json()
                    # Pastikan paket data ini berisi daftar/list informasi (bukan data analitik)
                    if isinstance(res_json, dict) and "data" in res_json and isinstance(res_json["data"], list):
                        items = res_json.get("data", [])
                        for item in items:
                            # Ciri-ciri iklan mobil asli di OLX: punya atribut 'parameters' dan 'price'
                            if "parameters" in item and "price" in item:
                                param_dict = {}
                                for param in item.get("parameters", []):
                                    param_dict[param.get("key")] = param.get("value_name", param.get("value"))
                                
                                car = {
                                    "id_iklan": item.get("id"),
                                    "judul": item.get("title"),
                                    "deskripsi": item.get("description"),
                                    "merek": param_dict.get("make", "Lainnya"),
                                    "model": param_dict.get("model", "Lainnya"),
                                    "tahun": param_dict.get("year"),
                                    "transmisi": param_dict.get("transmission", "Lainnya"),
                                    "jarak_tempuh": param_dict.get("mileage"),
                                    "harga": item.get("price", {}).get("value", {}).get("raw")
                                }
                                
                                if car["id_iklan"] and car["id_iklan"] not in [c["id_iklan"] for c in all_cars]:
                                    all_cars.append(car)
                except Exception:
                    pass

        page.on("response", tangkap_response)

        print("Membuka halaman OLX Mobil Bekas...")
        await page.goto("https://www.olx.co.id/mobil-bekas_c198", wait_until="domcontentloaded")
        await asyncio.sleep(5)  # Beri waktu elemen halaman agar termuat sempurna

        # Loop scrolling menggunakan tombol keyboard (lebih stabil)
        percobaan_kosong = 0
        while len(all_cars) < target_data and percobaan_kosong < 10:
            jumlah_sebelum = len(all_cars)
            
            # Tekan tombol 'Page Down' berkali-kali untuk meniru manusia membaca
            for _ in range(6):
                await page.keyboard.press("PageDown")
                await asyncio.sleep(1.5)

            # Cari dan klik tombol "Muat lainnya" / "Load more"
            try:
                tombol = page.locator("button", has_text=re.compile(r"muat|load", re.IGNORECASE)).first
                if await tombol.is_visible():
                    await tombol.click()
                    await asyncio.sleep(3)
            except Exception:
                pass

            print(f"Terkumpul: {len(all_cars)} data mobil...")

            # Evaluasi apakah ada data baru yang masuk
            if len(all_cars) == jumlah_sebelum:
                percobaan_kosong += 1
            else:
                percobaan_kosong = 0

        await browser.close()

    return all_cars[:target_data]

if __name__ == "__main__":
    print("Memulai scraping OLX via Browser...")
    hasil = asyncio.run(scrape_olx(target_data=600))
    
    if not hasil:
        print("\nData masih kosong. Sistem keamanan OLX mungkin sedang sangat ketat di IP jaringan Anda.")
    else:
        df = pd.DataFrame(hasil)
        df = df.drop_duplicates(subset=["id_iklan"]).reset_index(drop=True)
        
        df.to_csv("dataset_olx_mentah.csv", index=False, encoding="utf-8-sig")
        print(f"\nSelesai! Berhasil menyimpan {len(df)} baris ke 'dataset_olx_mentah.csv'")
        print(df[["judul", "merek", "tahun", "transmisi", "harga"]].head())