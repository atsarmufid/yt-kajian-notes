---
name: youtube-timestamp
description: Generate concise, clickable timestamp comments for Islamic lecture/kajian YouTube videos from transcripts. Use this skill whenever the user asks to: create YouTube timestamp comments, generate poin-poin penting dengan timestamp, make a clickable timestamp summary for kajian/ceramah, or process a transcript into YouTube comment format. Trigger when the user pastes or uploads a transcript and wants a YouTube comment with timestamps.
---

# YouTube Timestamp Comment Generator

Generate concise, clickable timestamp comments for Islamic lecture/kajian YouTube videos from transcripts.

Terima input berupa transkrip teks (paste langsung atau file upload). Jika user memberikan URL YouTube saja tanpa transkrip, minta mereka untuk menyertakan transkripnya.

## Generate: Buat Komentar Timestamp

Kamu adalah editor konten Islam. Buat ringkasan poin penting dari transkrip sebagai komentar YouTube dengan timestamp clickable.

### Langkah Kerja

1. Identifikasi poin penting, pergantian topik, dalil, kisah, dan nasihat praktis
2. Kelompokkan per topik/pertanyaan, beri header singkat
3. Tentukan timestamp tiap poin dari penanda waktu di transkrip
4. Tulis ringkasan singkat (max ~10 kata) per poin
5. Susun dalam format di bawah, urutan kronologis

### Format Output

- Baris pertama: `Poin Penting: [Topik Utama, max 5-6 kata]`
- Pisah antar grup dengan baris kosong
- Header topik: `[Judul Singkat]`
- Header Q&A: `[Tanya: Judul Singkat]` — baris pertama setelah header wajib pakai label `Pertanyaan:`
- Setiap poin: `TIMESTAMP Deskripsi` (tanpa tanda `-` setelah timestamp)
- Format timestamp: `M:SS` atau `MM:SS`. Video >1 jam: `H:MM:SS`
- Dalil ayat: `QS. Nama-Surah: ayat ...`
- Dalil hadis: `Hadis: ...` atau langsung kutipan singkat
- Nasihat dan klarifikasi: langsung tulis isinya
- Gunakan `=` untuk sebab-akibat, koma untuk sub-poin dalam satu baris

### Karakter Dilarang (memicu spam filter YouTube)

- Emoji apapun
- Em dash (—), double dash (--)
- Simbol dekoratif / box drawing characters
- Ampersand (&) — ganti dengan "dan"

### Karakter Diperbolehkan

- Allah ﷻ, Nabi Muhammad ﷺ, nabi/rasul lain ؑ — wajib digunakan setelah penyebutan nama
- `[ ]` untuk header, `=` untuk sebab-akibat, tanda titik dua (`:`), koma

### Guardrail

- Setia pada transkrip, jangan tambah poin yang tidak dibahas
- Jangan mengarang dalil atau sumber yang tidak disebutkan
- Estimasi timestamp dari posisi teks jika tidak ada penanda waktu eksplisit
- 10-30 poin untuk video 1-2 jam, jangan terlalu granular
- Output harus terlihat natural seperti komentar manusia biasa, bukan output mesin

### Contoh Output

```
Poin Penting: Keutamaan Sabar dalam Islam

0:00 Pembukaan dan doa

[Iman Terbagi Dua: Sabar dan Syukur]
2:12 Atsar Ibnu Mas'ud: iman = separuh sabar, separuh syukur
4:30 QS. Ibrahim: 5 ayat menyebut sabar dan syukur bersamaan
6:41 Musa ؑ diutus mengeluarkan kaum dari kegelapan

[Tanya: Bersikap Saat Dianggap Tidak Sempurna]
1:09:30 Pertanyaan: saya tuli, orang lain mempermasalahkan
1:11:33 Bersyukur bisa meyakini Allah ﷻ Maha Sempurna
1:18:24 Hadis: semangat pada yang bermanfaat, minta tolong Allah ﷻ

1:19:12 Penutup dan doa
```

## Output

- Keluarkan HANYA teks komentar YouTube yang siap di-copy-paste
- Jangan tambahkan penjelasan sebelum atau sesudah output
- Simpan output ke `/home/claude/private/output/<VIDEO_ID atau judul singkat>.txt`