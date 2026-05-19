# yt-kajian-notes

Prompt untuk menghasilkan komentar YouTube berformat timestamp dari transkrip ceramah/kajian Islam. Bisa dipakai di ChatGPT, Claude, Gemini, atau LLM lainnya.

## Cocok Untuk

- Penonton kajian Islam yang ingin berbagi poin penting di komentar YouTube
- Admin channel dakwah yang ingin menambahkan timestamp di deskripsi/komentar video
- Pencatat ilmu yang ingin ringkasan terstruktur dari ceramah yang didengarkan
- Siapa saja yang sering menyimak kajian dan ingin memudahkan orang lain menavigasi video

## Fitur

- Timestamp clickable (M:SS / H:MM:SS)
- Pengelompokan per topik/pertanyaan dengan header
- Emoji tematik (📖 dalil, 💡 tips, ⚖️ hukum, ⚠️ klarifikasi)
- Mendukung format ceramah biasa maupun Q&A
- Guardrail: tidak mengarang dalil, setia pada transkrip

## Cara Pakai

### 1. Dapatkan Transkrip

Gunakan salah satu website berikut untuk generate transkrip dari video YouTube:

- [YouTubeTranscript.com](https://youtubetranscript.com)
- [TubeTranscript.com](https://tubetranscript.com)
- [Tactiq.io](https://tactiq.io/tools/youtube-transcript)
- [NoteGPT](https://notegpt.io/youtube-transcript-generator)

Cukup paste URL video, lalu copy hasil transkripnya.

> ⚠️ **Perhatian:** Website tersebut kadang menyimpan cache transkrip lama. Jika video pernah dipotong/diedit oleh pemilik channel, transkrip yang dihasilkan bisa tidak sinkron. **Pastikan timestamp terakhir di transkrip sesuai dengan durasi video** sebelum diproses.

### 2. Generate Komentar Timestamp

**Manual (LLM manapun):**

1. Buka file [`PROMPT.md`](PROMPT.md)
2. Ganti bagian `[PASTE TRANSKRIP DI SINI]` dengan transkrip kamu
3. Copy seluruh isi prompt, paste ke LLM pilihanmu (ChatGPT, Claude, Gemini, dll.)
4. Hasilnya langsung bisa di-copy-paste ke komentar YouTube

**Dengan AI Coding Agent:**

Project ini menyertakan skill definition di folder `.agents/skills/`. Jika kamu menggunakan AI coding agent yang mendukung custom skills/instructions (seperti Kiro, Cursor, Windsurf, dll.), cukup berikan transkrip dan agent akan otomatis memproses sesuai aturan yang sudah didefinisikan.

## Contoh Output

Lihat contoh lengkap (input & output) di folder [`example/`](example/) (dibuat menggunakan Claude Opus 4.6)

Video sumber: [247. INILAH SEPARUH IMAN MU | Tadzkiratus saami' | Ustadz Muhammad Nuzul Dzikri](https://youtu.be/bY3qthc5muw)

## Struktur Project

```
yt-kajian-notes/
├── README.md
├── LICENSE
├── PROMPT.md                         # Prompt utama
├── example/
│   ├── input.txt                     # Contoh transkrip input
│   └── output.txt                    # Contoh hasil output
└── .agents/
    └── skills/
        └── kajian-notes/
            └── SKILL.md              # Skill definition untuk AI agent
```

## Limitasi

- Dioptimalkan untuk kajian/ceramah Islam berbahasa Indonesia
- Kualitas output sangat bergantung pada kualitas transkrip (jika transkrip berantakan, output juga kurang akurat)
- Untuk video non-Islam atau bahasa lain, prompt perlu diadaptasi
- LLM bisa saja salah mengestimasi timestamp jika transkrip tidak punya penanda waktu yang jelas

## Tips

- Untuk transkrip yang tidak punya penanda waktu, prompt akan mengestimasi timestamp berdasarkan posisi teks.
- Cocok untuk video kajian 30 menit sampai 2 jam. Untuk video lebih panjang, bisa pecah transkrip per bagian.
- Hasil bisa langsung di-paste ke komentar YouTube tanpa edit tambahan.

## Kontribusi

Kontribusi terbuka untuk siapa saja! Beberapa hal yang bisa dikontribusikan:

- Improve prompt supaya output lebih akurat
- Tambah contoh output dari video yang berbeda
- Adaptasi prompt untuk bahasa/topik lain
- Perbaikan dokumentasi

Silakan buat Pull Request atau buka Issue jika ada saran.

## Lisensi

[Unlicense](LICENSE) — public domain, bebas dipakai tanpa syarat apapun.
