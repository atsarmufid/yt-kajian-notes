---
inclusion: auto
---

# Kajian Notes - Auto Timestamp Generator

Ketika user mengirimkan teks berupa transkrip ceramah/kajian Islam (ditandai dengan timestamp seperti `(00:00)` atau `[00:00:00]` di awal baris), maka:

1. Langsung gunakan prompt dari `#[[file:PROMPT-YT-SAFE.md]]` untuk memproses transkrip tersebut.

2. Jika ada URL YouTube di teks transkrip, fetch judul asli video dari URL tersebut menggunakan web_fetch. Judul ini digunakan untuk:
   - Nama file output (slug dari judul, contoh: `keutamaan-sabar.txt`)
   - Konteks tambahan untuk memahami topik kajian

3. Simpan output ke folder `private/output/` dengan nama file berdasarkan prioritas:
   - Jika berhasil fetch judul YouTube: gunakan slug dari judul (contoh: `keutamaan-sabar.txt`)
   - Jika ada judul video di teks transkrip (manual): gunakan slug dari judul tersebut
   - Jika fetch gagal dan ada URL YouTube: gunakan video ID (contoh: `hU93hHJk1rA.txt`)
   - Jika tidak ada keduanya: gunakan `output-1.txt`, `output-2.txt`, dst increment dari yang sudah ada

4. Langsung proses tanpa bertanya — user sudah paham bahwa mengirimkan transkrip = minta dibuatkan ringkasan timestamp.

5. Setelah selesai, tampilkan path file output yang dibuat beserta judul video (jika berhasil di-fetch).
