# 💰 Discord Catat Pengeluaran Bot (AI + Google Sheets)

Bot Discord untuk mencatat pengeluaran harian ke Google Spreadsheet, dibantu AI (via OpenRouter).  
Tanpa biaya, bisa dijalankan lokal 💻

---

## 🛠️ Fitur

- Perintah: `!catat <jumlah> <deskripsi>`
- Bot akan:
  - Memahami pengeluaran via AI
  - Klasifikasikan kategori otomatis (makanan, dll)
  - Simpan ke Google Sheets (format: tanggal, kategori, jumlah, deskripsi)

---

## 📦 Stack yang Digunakan

- Python
- discord.py
- OpenRouter (pakai model `mistral-7b-instruct`)
- Google Sheets API

---

## ✅ Langkah Setup

### 1. 📋 Siapkan Google Spreadsheet

1. Buat spreadsheet kosong di Google Drive.
2. Rename Sheet-nya menjadi `Sheet1` (default).
3. Copy `spreadsheetId` dari URL-nya:  
   `https://docs.google.com/spreadsheets/d/**SPREADSHEET_ID**/edit`
4. Aktifkan [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com).
5. Buat Service Account di Google Cloud.
6. Download `credentials.json` ke project ini.
7. Share akses **Editor** ke email service account (contoh: `bot-catatan@project-id.iam.gserviceaccount.com`).

---

### 2. 🤖 Buat Bot Discord

1. Kunjungi [Discord Developer Portal](https://discord.com/developers/applications)
2. Klik `New Application`
3. Masuk tab `Bot` > `Add Bot`
4. Centang permissions:
   - `MESSAGE CONTENT INTENT`
   - Bot permission: `Read Message History`, `Send Messages`, `Read Messages`
5. Invite bot ke server:  
   Gunakan URL format:


---

### 3. 🔑 Setup OpenRouter API

1. Daftar di https://openrouter.ai
2. Pergi ke [API Keys](https://openrouter.ai/account/keys)
3. Copy API key
4. Buat file `.env` di root folder:

env
Liat di .env copy

---

### 4. 💻 Jalankan di Lokal

git clone https://github.com/rsnonci/catat-pengeluaran.git

cd catat-pengeluaran-bot

python -m venv venv

source venv/Scripts/activate    # atau venv\Scripts\activate.bat untuk Windows CMD
# atau source venv/bin/activate untuk Mac/Linux

pip install -r requirements.txt

python bot.py

---

### 5. 📢 Contoh Penggunaan

Discord: !catat 15000 beli sabun

Respon Bot: ✅ Dicatat: 15000 untuk beli sabun