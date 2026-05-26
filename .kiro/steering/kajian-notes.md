---
inclusion: auto
---

# Kajian Notes - Auto Timestamp Generator

Ketika user memberikan URL YouTube atau teks transkrip, langsung proses TANPA bertanya.

## Input: URL YouTube

Jika input mengandung youtube.com, youtu.be, /live/, atau video ID 11 karakter:

1. **Ekstrak transkrip** — jalankan:
   ```
   python scripts/extract_transcript.py "<URL>"
   ```
   Output: path file transkrip di stdout, tersimpan di `private/temp/<VIDEO_ID>.txt`

2. **Baca file transkrip** yang dihasilkan

3. **Generate ringkasan** sesuai format di `#[[file:prompts/PROMPT-YT-SAFE.md]]`. Keluarkan HANYA teks komentar YouTube tanpa penjelasan tambahan.

4. **Simpan output** ke `private/output/<VIDEO_ID>.txt`

5. **Cleanup** — hapus file di `private/temp/`

## Input: Teks Transkrip

Jika user mengirimkan teks berupa transkrip (ditandai timestamp seperti `(00:00)` atau `[00:00:00]` di awal baris):

1. Langsung gunakan prompt dari `#[[file:prompts/PROMPT-YT-SAFE.md]]` untuk memproses transkrip tersebut.

2. Simpan output ke folder `private/output/` dengan nama file:
   - Jika ada URL YouTube: gunakan video ID (contoh: `hU93hHJk1rA.txt`)
   - Jika ada judul video: gunakan slug dari judul
   - Jika tidak ada keduanya: gunakan `output-1.txt`, `output-2.txt`, dst

3. Tampilkan path file output yang dibuat.

## Catatan Penting

- Jangan tanya konfirmasi, langsung jalankan semua langkah
- Jika transkrip terlalu panjang untuk context, fokus pada poin-poin utama yang terlihat
- Video ID: setelah `v=`, `youtu.be/`, atau `/live/` (11 karakter)
- Output TIDAK ditampilkan di chat. Cukup tampilkan path file yang tersimpan saja.
