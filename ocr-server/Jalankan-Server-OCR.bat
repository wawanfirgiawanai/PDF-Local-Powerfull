@echo off
setlocal
title Server OCR - PDF Combine
rem Peluncur sekali klik untuk server OCR Unlimited-OCR 2.
rem Memakai lingkungan Python yang sudah terpasang di %USERPROFILE%\.venvs\unlimited-ocr

set "VENV=%USERPROFILE%\.venvs\unlimited-ocr"
set "PY=%VENV%\Scripts\python.exe"

if not exist "%PY%" (
  echo [!] Lingkungan Python OCR tidak ditemukan di:
  echo     %VENV%
  echo     Lihat bagian "Menjalankan Server OCR" di README.md untuk memasangnya.
  pause
  exit /b 1
)

rem Model sudah tersimpan di cache: jalankan tanpa internet dan tanpa mengunduh ulang kode model
set HF_HUB_OFFLINE=1
set PYTHONIOENCODING=utf-8

cd /d "%~dp0"
echo ============================================================
echo  Server OCR PDF Combine
echo  - Tunggu sampai muncul tulisan "Server transformers berjalan"
echo  - Biarkan jendela ini terbuka selama memakai fitur OCR
echo  - Tutup jendela ini (atau tekan Ctrl+C) untuk mematikan server
echo ============================================================
echo.

rem Buka aplikasi di browser
start "" "%~dp0..\index.html"

"%PY%" server.py %*

echo.
echo Server berhenti.
pause
