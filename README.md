# PDF Combine

**Aplikasi web untuk menggabungkan, mengatur, menandatangani, memberi highlight, dan meng-OCR PDF menjadi Markdown — langsung di browser, tanpa mengunggah berkas ke server pihak ketiga.**

![HTML5](https://img.shields.io/badge/HTML5-single%20file-E34F26?logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-vanilla-F7DF1E?logo=javascript&logoColor=black)
![No Backend](https://img.shields.io/badge/backend-tidak%20perlu-2f6fde)
![Privacy](https://img.shields.io/badge/privasi-100%25%20lokal-1f9d55)

PDF Combine adalah aplikasi satu berkas (`index.html`) yang berjalan sepenuhnya di sisi klien. Semua pemrosesan dokumen terjadi di browser Anda, sehingga cocok untuk dokumen akademik, administrasi, maupun dokumen yang bersifat rahasia.

---

## Daftar Isi

- [Fitur](#fitur)
- [Cara Menjalankan](#cara-menjalankan)
- [Menjalankan Server OCR](#menjalankan-server-ocr)
- [Panduan Penggunaan](#panduan-penggunaan)
- [Teknologi](#teknologi)
- [Privasi & Keamanan](#privasi--keamanan)
- [Keterbatasan](#keterbatasan)
- [Struktur Proyek](#struktur-proyek)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

---

## Fitur

### 1. Gabung & Atur Halaman
- Gabungkan banyak **PDF, JPG, dan PNG** menjadi satu dokumen (gambar otomatis disesuaikan ke halaman A4).
- Ubah urutan halaman dengan **seret-dan-lepas** atau tombol geser ◀ ▶.
- **Putar**, **hapus**, atau **sisipkan halaman kosong**.
- Pilih beberapa halaman sekaligus untuk diputar, dihapus, atau **diunduh sebagai PDF terpisah**.
- Berkas baru disisipkan setelah halaman yang dipilih, atau di akhir dokumen.

### 2. Tanda Tangan
- **Gambar** tanda tangan langsung dengan mouse, stylus, atau jari (pilihan warna tinta dan ketebalan).
- **Unggah** gambar tanda tangan atau stempel, dengan opsi menghapus latar putih secara otomatis.
- **Tempel teks** multi-baris (misalnya tempat & tanggal, nama, NIP) dengan ukuran dan warna yang dapat diatur.
- Tanda tangan dapat digeser dan diubah ukurannya di halaman.
- Tanda tangan yang pernah dibuat **tersimpan di browser** untuk dipakai ulang.
- **Tanda tangan digital berbasis sertifikat (PKCS#7)** dari berkas `.p12` / `.pfx` yang dapat diverifikasi di Adobe Acrobat Reader. Tersedia juga pembuat sertifikat uji coba (self-signed).

### 3. Highlight
- Tujuh warna siap pakai — **Kuning, Hijau, Biru, Merah muda, Oranye, Ungu, Merah** — ditambah pemilih warna bebas.
- Tiga mode penandaan:
  | Mode | Kegunaan |
  |---|---|
  | **Blok teks** | Seret di atas teks seperti memblok biasa; highlight menempel saat mouse dilepas. |
  | **Kotak** | Gambar area bebas — cocok untuk PDF hasil scan, gambar, atau tabel. |
  | **Hapus** | Klik highlight untuk menghapusnya. |
- Batalkan (**Ctrl+Z**) dan hapus semua highlight di satu halaman.
- Highlight disimpan ke PDF dengan *blend mode multiply*, sehingga teks di bawahnya tetap jelas terbaca.

### 4. PDF → Markdown (OCR)
- Ubah halaman PDF — termasuk **PDF hasil scan** — menjadi **Markdown** dengan model [Unlimited-OCR 2](https://github.com/baidu/Unlimited-OCR) dari Baidu.
- Mengenali **judul bertingkat**, paragraf, **tabel** (sebagai HTML, tabel lintas halaman digabung otomatis), rumus, dan **gambar/grafik** (dipotong otomatis dari halaman).
- Pilih halaman: semua, yang terpilih di tab *Gabung & Atur*, atau rentang (mis. `1-3, 5`).
- Pilihan mode model (*Otomatis*, *Gundam*, *Base*), resolusi render, dan jumlah halaman per permintaan.
- Lihat hasil sebagai **Pratinjau**, sunting **Markdown**-nya, atau periksa keluaran **Mentah** model; lalu **Salin** atau **Unduh .md** (gambar bisa disisipkan langsung ke dalam berkas).
- Model dijalankan oleh **server OCR lokal** (`ocr-server/server.py`) di komputer Anda sendiri — lihat [Menjalankan Server OCR](#menjalankan-server-ocr).

### Lainnya
- Tempat unggah tersedia di **setiap tab**; semua fitur bekerja pada dokumen yang sama.
- Navigasi halaman dengan tombol **← →**, serta perbesar/perkecil tampilan.
- Mendukung **mode gelap** otomatis dan tampilan **responsif** untuk ponsel.

---

## Cara Menjalankan

Tidak ada proses instalasi atau *build*. Aplikasi membutuhkan koneksi internet untuk memuat pustaka dari CDN.

**Opsi A — Buka langsung**

Klik dua kali `index.html` untuk membukanya di browser (Chrome, Edge, Firefox, atau Safari versi terbaru).

**Opsi B — Server lokal (disarankan)**

```bash
python -m http.server 8765
```

Lalu buka <http://localhost:8765> di browser.

**Opsi C — GitHub Pages**

1. Unggah repositori ini ke GitHub.
2. Buka **Settings → Pages**.
3. Pada **Source**, pilih branch `main` dan folder `/ (root)`, lalu **Save**.
4. Aplikasi akan tersedia di `https://<username>.github.io/<nama-repo>/`.

---

## Menjalankan Server OCR

Fitur **PDF → Markdown** membutuhkan model Unlimited-OCR 2 (3 miliar parameter, ±6,7 GB) yang berjalan di komputer dengan **GPU NVIDIA**. Browser merender halaman menjadi gambar lalu mengirimkannya ke server lokal ini; konversi keluaran model ke Markdown dilakukan di browser.

**1. Pasang PyTorch versi CUDA** sesuai GPU Anda dari <https://pytorch.org/get-started/locally/> (RTX seri 50xx membutuhkan build CUDA 12.8 atau lebih baru), misalnya:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

**2. Pasang dependensi lainnya:**

```bash
pip install -r ocr-server/requirements.txt
```

**3. Jalankan server** (unduhan model ±6,7 GB dari Hugging Face terjadi saat pertama kali):

```bash
python ocr-server/server.py
```

Di Windows, cukup klik dua kali **`ocr-server/Jalankan-Server-OCR.bat`** (memakai lingkungan Python di `%USERPROFILE%\.venvs\unlimited-ocr`). Panduan langkah demi langkah ada di [`PANDUAN-OCR.md`](PANDUAN-OCR.md).

Server berjalan di `http://127.0.0.1:8000`. Buka tab **PDF → Markdown**, klik **Cek koneksi**, lalu **Mulai OCR**.

| Pilihan | Kegunaan |
|---|---|
| `--backend transformers` | (bawaan) memuat model langsung di GPU. Bobot bf16 ±6,7 GB, jadi GPU 8 GB berada di batas minimum — gunakan 1 halaman per permintaan dan mode *Base* bila kehabisan memori. |
| `--backend sglang --sglang-url http://host:10000` | meneruskan ke server SGLang resmi (Linux, GPU besar) sesuai [README Unlimited-OCR](https://github.com/baidu/Unlimited-OCR). Cocok untuk dokumen panjang. |
| `--backend demo` | tanpa model dan tanpa GPU — mengembalikan contoh keluaran untuk mencoba antarmuka. |
| `--host`, `--port` | alamat server (bawaan `127.0.0.1:8000`). Isi alamat yang sama di kolom *Alamat server* pada aplikasi. |
| `--model` | ID model Hugging Face atau folder lokal (bawaan `baidu/Unlimited-OCR-2`). |
| `--verbose` | tampilkan log debug bawaan kode model (`[PageRope]`, `[DASH]`, …). Tanpa opsi ini log disembunyikan agar jendela server tetap ringkas. |

> Server dapat dijalankan di komputer lain (mis. server lab ber-GPU) dengan `--host 0.0.0.0`; isi alamat IP komputer tersebut di aplikasi. Lakukan ini hanya di jaringan yang tepercaya.

---

## Panduan Penggunaan

1. **Unggah berkas** — klik kotak unggah atau seret berkas PDF/gambar ke halaman.
2. **Atur halaman** di tab *Gabung & Atur*: urutkan, putar, atau hapus halaman.
3. **Tanda tangani** di tab *Tanda Tangan*: buat tanda tangan, klik untuk menempel, lalu geser ke posisi yang diinginkan.
4. **Beri highlight** di tab *Highlight*: pilih warna dan mode, lalu tandai teks.
5. **Unduh** — isi nama berkas di pojok kanan atas, lalu klik **Unduh PDF**.
6. **Ubah ke Markdown** di tab *PDF → Markdown*: jalankan server OCR, pilih halaman, klik **Mulai OCR**, lalu unduh berkas `.md`.

> **Tips:** Pada mode *Blok teks*, mulailah menyeret tepat di atas tulisan, bukan di area kosong di sampingnya.

---

## Teknologi

| Pustaka | Versi | Kegunaan |
|---|---|---|
| [pdf-lib](https://pdf-lib.js.org/) | 1.17.1 | Membuat, menggabungkan, dan menyunting PDF |
| [PDF.js](https://mozilla.github.io/pdf.js/) | 3.11.174 | Menampilkan halaman PDF dan lapisan teks |
| [node-forge](https://github.com/digitalbazaar/forge) | 1.3.1 | Membaca sertifikat PKCS#12 dan membuat tanda tangan PKCS#7 |
| [marked](https://marked.js.org/) | 12.0.2 | Menampilkan pratinjau Markdown hasil OCR |
| [DOMPurify](https://github.com/cure53/DOMPurify) | 3.1.6 | Membersihkan HTML pratinjau |
| [Unlimited-OCR 2](https://github.com/baidu/Unlimited-OCR) | — | Model OCR dokumen (MIT); logika konversi ke Markdown di-*port* dari `utils/process_unlimitedOCR2.py` |

Antarmuka dibangun dengan HTML, CSS, dan JavaScript murni tanpa *framework*.

---

## Privasi & Keamanan

- **Tidak ada berkas yang dikirim ke server pihak ketiga.** Seluruh proses berlangsung di browser, kecuali fitur OCR yang mengirim gambar halaman **hanya ke alamat server OCR yang Anda isi** (bawaan: komputer Anda sendiri, `127.0.0.1`).
- Satu-satunya data yang disimpan adalah tanda tangan tersimpan dan pilihan warna highlight, di `localStorage` browser Anda sendiri.
- Kata sandi dan kunci privat sertifikat hanya berada di memori selama halaman terbuka dan tidak pernah disimpan.

---

## Keterbatasan

- Highlight, tanda tangan gambar, dan teks **menyatu dengan isi halaman** (bukan anotasi), sehingga tidak dapat disunting satu per satu di pembaca PDF lain.
- Memutar halaman akan menghapus tanda tangan dan highlight yang sudah ditempel pada halaman tersebut.
- PDF yang terkunci kata sandi tidak dapat dibuka.
- Tanda tangan digital hanya mendukung sertifikat **RSA**. Sertifikat uji coba akan ditampilkan sebagai "identitas tidak dikenal" oleh Adobe Reader.
- Mode *Blok teks* hanya bekerja pada PDF yang memiliki lapisan teks; untuk PDF hasil scan gunakan mode *Kotak*.
- OCR membutuhkan GPU NVIDIA (model tidak berjalan di CPU). Keluaran model bisa keliru — periksa kembali hasil Markdown sebelum digunakan.

---

## Struktur Proyek

```
PDF-Combine/
├── index.html   # Seluruh aplikasi (HTML, CSS, JavaScript)
├── ocr-server/
│   ├── server.py         # Server OCR lokal (Unlimited-OCR 2)
│   ├── Jalankan-Server-OCR.bat  # Peluncur sekali klik (Windows)
│   └── requirements.txt  # Dependensi Python server OCR
├── PANDUAN-OCR.md  # Panduan pemakaian fitur OCR
├── LICENSE      # Lisensi MIT
└── README.md
```

---

## Kontribusi

Saran dan perbaikan sangat diterima.

1. *Fork* repositori ini.
2. Buat branch baru: `git checkout -b fitur/nama-fitur`.
3. *Commit* perubahan: `git commit -m "Tambah fitur ..."`.
4. *Push* ke branch: `git push origin fitur/nama-fitur`.
5. Buka **Pull Request**.

Untuk melaporkan bug, silakan buka *Issue* dengan langkah-langkah untuk mereproduksinya.

---

## Lisensi

Didistribusikan di bawah Lisensi MIT. Lihat berkas [`LICENSE`](LICENSE) untuk detailnya.

---

<p align="center">Dibuat oleh <b>Wawan Firgiawan</b> · Universitas Sulawesi Barat</p>
