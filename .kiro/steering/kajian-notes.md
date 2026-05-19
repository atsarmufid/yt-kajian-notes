---
inclusion: auto
---

# Kajian Notes - Auto Timestamp Generator

Ketika user mengirimkan teks berupa transkrip ceramah/kajian Islam (ditandai dengan timestamp seperti `(00:00)` atau `[00:00:00]` di awal baris), maka:

1. Langsung gunakan skill dari `#[[file:.agents/skills/kajian-notes/SKILL.md]]` untuk memproses transkrip tersebut.

2. Simpan output ke folder `private/output/` dengan nama file berdasarkan:
   - Jika ada judul video di teks: gunakan slug dari judul (contoh: `keutamaan-sabar.txt`)
   - Jika ada URL YouTube: gunakan video ID (contoh: `hU93hHJk1rA.txt`)
   - Jika tidak ada keduanya: gunakan timestamp saat ini (contoh: `output-1.txt`, `output-2.txt`, dst increment dari yang sudah ada)

3. Langsung proses tanpa bertanya — user sudah paham bahwa mengirimkan transkrip = minta dibuatkan ringkasan timestamp.

4. Setelah selesai, tampilkan path file output yang dibuat.
