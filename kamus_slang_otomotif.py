"""
Kamus normalisasi slang, istilah jual-beli, dan singkatan otomotif OLX.
Dipakai untuk mengubah kata tidak baku -> kata baku sebelum ekstraksi fitur/NLP.

Perbaikan: key 'km' sebelumnya didefinisikan dua kali ('kilometer' lalu
'kamu' menimpanya) sehingga 'km' selalu diterjemahkan jadi 'kamu', padahal
di konteks otomotif hampir selalu berarti 'kilometer'. Sekarang 'km' tetap
'kilometer', dan 'kamu' dipakai sebagai kata sendiri.
"""

KAMUS_SLANG_OTOMOTIF = {
    # --- Transmisi & Mesin ---
    "mt": "manual", "m/t": "manual", "mnl": "manual",
    "at": "otomatis", "a/t": "otomatis", "matic": "otomatis", "matict": "otomatis", "metuk": "otomatis",
    "cc": "kapasitas mesin", "silinder": "kapasitas mesin",
    "bensin": "bensin", "bsn": "bensin", "solar": "diesel", "dsl": "diesel",

    # --- Surat & Pajak ---
    "pjk": "pajak", "pajak": "pajak", "pjkny": "pajak",
    "on": "hidup", "off": "mati", "pnjg": "panjang", "puanjang": "panjang",
    "stnk": "stnk", "bpkb": "bpkb", "faktur": "faktur",
    "komplit": "lengkap", "kmplit": "lengkap", "komplit2": "lengkap", "lkp": "lengkap",
    "tgn": "tangan", "tgn1": "tangan pertama", "tgn2": "tangan kedua",
    "plat": "plat nomor", "kaleng": "masa berlaku plat",

    # --- Kondisi Fisik & Interior ---
    "km": "kilometer", "odo": "odometer", "low": "rendah", "anteng": "stabil",
    "ori": "orisinil", "orisinil": "orisinil", "orisinal": "orisinil", "ors": "orisinil",
    "cat": "cat bodi", "mulus": "mulus", "mlus": "mulus", "kinclong": "bersih",
    "ac": "pendingin kabin", "dngn": "dingin", "nyess": "dingin", "menggigil": "sangat dingin",
    "kaki": "suspensi", "kaki2": "suspensi", "senyap": "hening",
    "ban": "ban", "tebel": "tebal", "tbl": "tebal",
    "siap": "siap", "siap2": "siap", "pke": "pakai", "pakai": "pakai", "gas": "jalan",

    # --- Istilah Jual Beli & Negosiasi ---
    "nego": "negosiasi", "nggo": "negosiasi", "nett": "harga pas", "net": "harga pas",
    "dijual": "jual", "djual": "jual", "bu": "butuh uang", "b.u": "butuh uang",
    "tt": "tukar tambah", "bt": "barter", "kredit": "kredit", "krdt": "kredit",
    "cash": "tunai", "csh": "tunai", "dp": "uang muka", "angs": "angsuran", "angsrn": "angsuran",

    # --- Kata Penghubung / Slang Umum ---
    "yg": "yang", "dgn": "dengan", "dg": "dengan", "utk": "untuk", "untk": "untuk",
    "tp": "tapi", "krn": "karena", "karna": "karena", "jd": "jadi", "jgn": "jangan",
    "udh": "sudah", "udah": "sudah", "dah": "sudah", "sdh": "sudah",
    "blm": "belum", "trs": "terus", "sy": "saya", "kamu": "kamu",
    "bs": "bisa", "gk": "tidak", "ga": "tidak", "gak": "tidak", "tdk": "tidak",
    "bgt": "banget", "bener": "benar", "aja": "saja", "kalo": "kalau", "lok": "lokasi",
}
