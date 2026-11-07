# Panduan Fitur PDF → Markdown (OCR)

Panduan ini untuk komputer yang **sudah terpasang** semua kebutuhannya. Anda tidak perlu memasang apa pun lagi.

| Komponen | Lokasi / versi |
|---|---|
| Lingkungan Python | `%USERPROFILE%\.venvs\unlimited-ocr` (Python 3.11, PyTorch 2.11 CUDA 12.8, triton-windows 3.7) |
| Model Unlimited-OCR 2 (±6,5 GB) | `%USERPROFILE%\.cache\huggingface\hub\models--baidu--Unlimited-OCR-2` |
| GPU yang diuji | NVIDIA GeForce RTX 5050 Laptop 8 GB (model memakai ±6,6 GB) |

---

## Langkah Singkat

1. **Nyalakan server OCR** — buka folder `ocr-server`, lalu klik dua kali **`Jalankan-Server-OCR.bat`**.
2. **Tunggu** sampai jendela hitam menampilkan:
   ```
   [ocr] Server transformers berjalan di http://127.0.0.1:8000
   ```
   Memuat model ke GPU memakan waktu sekitar 15–30 detik. Aplikasi PDF Combine otomatis terbuka di browser. Server berjalan **tanpa internet**.
3. Di aplikasi, buka tab **PDF → Markdown**.
4. **Unggah PDF** (klik kotak unggah atau seret berkas ke halaman).
5. Klik **Cek koneksi** — harus muncul titik hijau *Terhubung · baidu/Unlimited-OCR-2*.
6. Klik **Mulai OCR**, lalu tunggu bilah kemajuan sampai selesai. Di RTX 5050 setiap halaman butuh sekitar **10–20 detik**; halaman **pertama** setelah server dinyalakan lebih lama (±35 detik) karena GPU sedang menyiapkan kernel.
7. Periksa hasilnya, lalu klik **Unduh .md**.
8. Selesai memakai OCR? **Tutup jendela hitam** server agar memori GPU dilepas.

> Jangan tutup jendela hitam selama OCR berjalan — itulah server yang menjalankan model.

Selama OCR berjalan, jendela hitam hanya menampilkan baris singkat seperti:

```
[ocr] Memproses 1 halaman ...
[ocr] 1 halaman selesai dalam 18.4 dtk
```

Butuh log teknis lengkap dari model (untuk mencari kesalahan)? Jalankan `Jalankan-Server-OCR.bat --verbose` dari Command Prompt. Baris seperti `[PageRope]`, `[DASH]`, atau `ok=False` di log itu adalah catatan diagnostik bawaan model, **bukan** galat.

---

## Pengaturan

| Pengaturan | Pilihan | Saran |
|---|---|---|
| **Halaman** | Semua · Terpilih (dari tab *Gabung & Atur*) · Rentang (mis. `1-3, 5`) | Coba beberapa halaman dulu sebelum seluruh dokumen. |
| **Mode model** | Otomatis · Gundam · Base | *Otomatis*. Pakai *Base* jika muncul galat kehabisan memori (*out of memory*). |
| **Resolusi render** | 150 · 200 · 300 DPI | *200 DPI*. Pakai 300 DPI untuk teks yang sangat kecil. |
| **Halaman per permintaan** | 1–20 | *1* (aman). *2* sudah diuji dan muat di RTX 5050 8 GB; cocok bila ada tabel/paragraf yang bersambung ke halaman berikutnya. Angka lebih besar butuh memori GPU lebih besar. |
| **Sisipkan gambar ke dalam .md** | centang / tidak | Dicentang: gambar & grafik ikut tersimpan di dalam berkas `.md`. Tidak dicentang: berkas lebih kecil, gambar hanya berupa nama berkas. |

## Membaca Hasil

- **Pratinjau** — tampilan hasil seperti dokumen: judul, paragraf, tabel, rumus, dan potongan gambar.
- **Markdown** — teks Markdown yang bisa **disunting langsung** sebelum diunduh.
- **Mentah** — keluaran asli model (berguna untuk memeriksa bila hasil terlihat aneh).
- **Salin** menyalin Markdown ke papan klip; **Unduh .md** menyimpannya sebagai berkas.

Tabel ditulis dalam format HTML di dalam Markdown — tampil dengan benar di VS Code, GitHub, Obsidian, dan Typora.

---

## Jika Ada Masalah

| Gejala | Penyebab & solusi |
|---|---|
| *Server tidak dapat dihubungi* | Server belum menyala atau masih memuat model. Pastikan jendela hitam sudah menampilkan "Server transformers berjalan", lalu klik **Cek koneksi** lagi. |
| Galat `CUDA out of memory` | Memori GPU penuh. Ubah **Mode model** ke *Base*, **Halaman per permintaan** ke *1*, atau turunkan **Resolusi render**. Tutup aplikasi lain yang memakai GPU (game, editor video). |
| Galat `CompilationError` / `Block pointers have been removed` | Versi Triton terlalu baru. Jalankan: `%USERPROFILE%\.venvs\unlimited-ocr\Scripts\python -m pip install "triton-windows<3.8"` |
| Jendela hitam langsung tertutup / galat "Lingkungan Python OCR tidak ditemukan" | Folder `%USERPROFILE%\.venvs\unlimited-ocr` terhapus. Pasang ulang mengikuti bagian *Menjalankan Server OCR* di `README.md`. |
| Hasil OCR berulang-ulang atau aneh | Coba mode *Gundam* atau resolusi lebih tinggi untuk halaman tersebut saja (pilih *Rentang*). |
| OCR terasa lambat | Normal untuk GPU laptop: setiap halaman diproses satu per satu. Klik **Hentikan** kapan saja; halaman yang sudah selesai tetap tersimpan di hasil. |

## Catatan

- Semua proses berjalan **di komputer Anda sendiri** — PDF tidak dikirim ke internet.
- Hasil OCR bisa keliru; periksa kembali angka, nama, dan rumus sebelum dipakai.
- Ingin mencoba tampilan tanpa GPU? Jalankan `Jalankan-Server-OCR.bat --backend demo` dari Command Prompt.
