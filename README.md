# EmberNote 🔥
Aplikasi **pesan dan foto rahasia** sekali baca (burn-after-reading) berbasis **AES-256-GCM**, satu algoritma saja.

## Struktur
```
EmberNote/
├── .streamlit/
│   └── config.toml      # tema warna Streamlit
├── images/
│   └── logo.png         # logo; taruh screenshot laporan (jpg) di sini
├── modules/
│   ├── __init__.py
│   ├── aes_gcm.py       # inti kriptografi: AES-256-GCM + AAD (teks dan byte)
│   ├── payload.py       # membungkus teks + foto jadi satu paket (validasi gambar)
│   ├── visual.py        # ciphertext -> gambar noise, entropi, pratinjau Base64
│   ├── storage.py       # penyimpanan SQLite (hanya ciphertext)
│   └── selftest.py      # 13 pengujian otomatis (bukti keamanan)
├── .gitignore
├── app.py               # aplikasi Streamlit (Beranda, Main, Bukti Keamanan, Tentang)
├── tema.py              # CSS dan komponen tampilan
├── laporan.ipynb        # notebook laporan: penjelasan, kode, pengujian, demo
├── README.md
└── requirements.txt
```

## Menjalankan lokal
```bash
pip install -r requirements.txt
streamlit run app.py
python -m modules.selftest     # opsional: jalankan 13 pengujian di terminal
```

## Deploy ke Streamlit Community Cloud
1. Upload seluruh isi folder ini ke repository GitHub (`.gitignore` sudah menyingkirkan file yang tidak perlu).
2. Buka https://share.streamlit.io, login dengan GitHub, klik **Create app**.
3. Pilih repository dan branch, isi **Main file path** dengan `app.py`, lalu **Deploy**.

Catatan: penyimpanan di Streamlit Cloud bersifat sementara; file `embernote.db` hilang saat aplikasi restart.

## Alur singkat
1. **Main · Buat Pesan**: teks dan/atau foto (maks 2 MB) dibungkus jadi satu paket, dienkripsi dengan kunci acak 256-bit; server menyimpan nonce + ciphertext. Detail ciphertext sebagai gambar noise tersedia lewat tombol **Lihat isi server**.
2. Bagikan **ID** dan **kunci** lewat dua jalur berbeda.
3. **Main · Baca Pesan**: dekripsi + verifikasi tag, foto dan teks tampil, lalu pesan dihapus (hanya satu pembaca yang berhasil).

## Batasan dan ancaman yang tidak ditangani
- Bukan E2EE murni: kunci dibuat dan dipakai di server saat pesan dibuat/dibuka.
- Siapa pun yang memegang ID + kunci dapat membuka pesan.
- Panjang pesan, ukuran foto, ID, dan waktu dibuat/kedaluwarsa tidak tersembunyi.
- Foto tidak dibersihkan dari metadata (EXIF/lokasi).
- Tidak ada pembatasan spam atau percobaan.
- Penyimpanan Streamlit Cloud sementara; plaintext tetap ada di sesi browser sampai pesan ditutup.
- Proyek pembelajaran, belum diaudit pihak independen.
