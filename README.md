# PDF Combine

**Aplikasi web untuk menggabungkan, mengatur, menandatangani, dan memberi highlight pada PDF — langsung di browser, tanpa mengunggah berkas ke server mana pun.**

![HTML5](https://img.shields.io/badge/HTML5-single%20file-E34F26?logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-vanilla-F7DF1E?logo=javascript&logoColor=black)
![No Backend](https://img.shields.io/badge/backend-tidak%20perlu-2f6fde)
![Privacy](https://img.shields.io/badge/privasi-100%25%20lokal-1f9d55)

PDF Combine adalah aplikasi satu berkas (`index.html`) yang berjalan sepenuhnya di sisi klien. Semua pemrosesan dokumen terjadi di browser Anda, sehingga cocok untuk dokumen akademik, administrasi, maupun dokumen yang bersifat rahasia.

---

## Daftar Isi

- [Fitur](#fitur)
- [Cara Menjalankan](#cara-menjalankan)
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

### Lainnya
- Tempat unggah tersedia di **setiap tab**; ketiga fitur bekerja pada dokumen yang sama.
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

## Panduan Penggunaan

1. **Unggah berkas** — klik kotak unggah atau seret berkas PDF/gambar ke halaman.
2. **Atur halaman** di tab *Gabung & Atur*: urutkan, putar, atau hapus halaman.
3. **Tanda tangani** di tab *Tanda Tangan*: buat tanda tangan, klik untuk menempel, lalu geser ke posisi yang diinginkan.
4. **Beri highlight** di tab *Highlight*: pilih warna dan mode, lalu tandai teks.
5. **Unduh** — isi nama berkas di pojok kanan atas, lalu klik **Unduh PDF**.

> **Tips:** Pada mode *Blok teks*, mulailah menyeret tepat di atas tulisan, bukan di area kosong di sampingnya.

---

## Teknologi

| Pustaka | Versi | Kegunaan |
|---|---|---|
| [pdf-lib](https://pdf-lib.js.org/) | 1.17.1 | Membuat, menggabungkan, dan menyunting PDF |
| [PDF.js](https://mozilla.github.io/pdf.js/) | 3.11.174 | Menampilkan halaman PDF dan lapisan teks |
| [node-forge](https://github.com/digitalbazaar/forge) | 1.3.1 | Membaca sertifikat PKCS#12 dan membuat tanda tangan PKCS#7 |

Antarmuka dibangun dengan HTML, CSS, dan JavaScript murni tanpa *framework*.

---

## Privasi & Keamanan

- **Tidak ada berkas yang dikirim ke server.** Seluruh proses berlangsung di browser.
- Satu-satunya data yang disimpan adalah tanda tangan tersimpan dan pilihan warna highlight, di `localStorage` browser Anda sendiri.
- Kata sandi dan kunci privat sertifikat hanya berada di memori selama halaman terbuka dan tidak pernah disimpan.

---

## Keterbatasan

- Highlight, tanda tangan gambar, dan teks **menyatu dengan isi halaman** (bukan anotasi), sehingga tidak dapat disunting satu per satu di pembaca PDF lain.
- Memutar halaman akan menghapus tanda tangan dan highlight yang sudah ditempel pada halaman tersebut.
- PDF yang terkunci kata sandi tidak dapat dibuka.
- Tanda tangan digital hanya mendukung sertifikat **RSA**. Sertifikat uji coba akan ditampilkan sebagai "identitas tidak dikenal" oleh Adobe Reader.
- Mode *Blok teks* hanya bekerja pada PDF yang memiliki lapisan teks; untuk PDF hasil scan gunakan mode *Kotak*.

---

## Struktur Proyek

```
PDF-Combine/
├── index.html   # Seluruh aplikasi (HTML, CSS, JavaScript)
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
