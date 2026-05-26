"""
kajian_notes.py - Ekstrak subtitle YouTube dan generate ringkasan kajian Islam
menggunakan yt-dlp + OpenAI GPT-4o

Usage:
    python kajian_notes.py <URL_YOUTUBE>
    python kajian_notes.py <URL_YOUTUBE> --lang en
    python kajian_notes.py <URL_YOUTUBE> --output custom_output.txt

Requires:
    - yt-dlp (pip install yt-dlp)
    - openai (pip install openai)
    - Environment variable: OPENAI_API_KEY
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from openai import OpenAI


def extract_video_id(url: str) -> str:
    """Ekstrak video ID dari URL YouTube."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Tidak bisa ekstrak video ID dari: {url}")


def download_subtitle(url: str, lang: str = "id") -> str:
    """Download auto-generated subtitle dari YouTube via yt-dlp."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_template = os.path.join(tmpdir, "%(id)s")

        cmd = [
            "yt-dlp",
            "--write-auto-subs",
            "--sub-lang", lang,
            "--sub-format", "vtt",
            "--skip-download",
            "--output", output_template,
            url,
        ]

        print(f"Downloading subtitle ({lang})...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            # Coba fallback ke subtitle manual
            cmd_manual = [
                "yt-dlp",
                "--write-subs",
                "--sub-lang", lang,
                "--sub-format", "vtt",
                "--skip-download",
                "--output", output_template,
                url,
            ]
            result = subprocess.run(cmd_manual, capture_output=True, text=True)
            if result.returncode != 0:
                print("STDERR:", result.stderr)
                raise RuntimeError("Gagal download subtitle. Pastikan video memiliki subtitle/CC.")

        # Cari file subtitle yang didownload
        vtt_files = list(Path(tmpdir).glob("*.vtt"))
        if not vtt_files:
            raise RuntimeError(
                f"Subtitle tidak ditemukan untuk bahasa '{lang}'. "
                "Coba bahasa lain dengan --lang (misal: en)"
            )

        vtt_content = vtt_files[0].read_text(encoding="utf-8")
        return vtt_to_text(vtt_content)


def vtt_to_text(vtt: str) -> str:
    """Convert VTT subtitle ke plain text dengan timestamp."""
    lines = vtt.split("\n")
    result = []
    timestamp_pattern = re.compile(
        r'(\d{1,2}:\d{2}:\d{2})\.\d{3}\s*-->\s*\d{1,2}:\d{2}:\d{2}\.\d{3}'
    )
    tag_pattern = re.compile(r'<[^>]+>')

    current_time = None
    seen_lines = set()

    for line in lines:
        line = line.strip()

        # Skip VTT header dan metadata
        if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue

        # Cek timestamp
        match = timestamp_pattern.match(line)
        if match:
            current_time = match.group(1)
            # Hapus leading zero pada jam jika 0
            if current_time.startswith("0:"):
                current_time = current_time[2:]
            continue

        # Skip baris kosong dan nomor urut
        if not line or line.isdigit():
            continue

        # Bersihkan HTML tags
        clean_line = tag_pattern.sub("", line)
        clean_line = clean_line.strip()

        if not clean_line:
            continue

        # Deduplicate (auto-subs sering repeat)
        if clean_line in seen_lines:
            continue
        seen_lines.add(clean_line)

        if current_time:
            result.append(f"[{current_time}] {clean_line}")
        else:
            result.append(clean_line)

    return "\n".join(result)


def load_prompt() -> str:
    """Load prompt template dari PROMPT-YT-SAFE.md."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "PROMPT-YT-SAFE.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file tidak ditemukan: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def build_prompt(transcript: str) -> str:
    """Bangun prompt lengkap dengan transkrip."""
    template = load_prompt()
    # Ganti placeholder dengan transkrip actual
    prompt = template.replace("[PASTE TRANSKRIP DI SINI]", transcript)
    return prompt


def generate_notes(transcript: str) -> str:
    """Kirim transkrip ke OpenAI dan generate ringkasan."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY tidak ditemukan. Set environment variable terlebih dahulu.\n"
            "Windows: set OPENAI_API_KEY=sk-...\n"
            "Linux/Mac: export OPENAI_API_KEY=sk-..."
        )

    client = OpenAI(api_key=api_key)
    prompt = build_prompt(transcript)

    print("Generating ringkasan dengan GPT-4o...")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=4096,
    )

    return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Generate ringkasan kajian Islam dari video YouTube"
    )
    parser.add_argument("url", help="URL video YouTube")
    parser.add_argument("--lang", default="id", help="Bahasa subtitle (default: id)")
    parser.add_argument("--output", "-o", help="Path output file (opsional)")
    parser.add_argument(
        "--transcript-only", action="store_true",
        help="Hanya download dan tampilkan transkrip, tanpa generate ringkasan"
    )

    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.url)
        print(f"Video ID: {video_id}")

        # Download subtitle
        transcript = download_subtitle(args.url, args.lang)
        print(f"Transkrip berhasil didownload ({len(transcript)} karakter)\n")

        if args.transcript_only:
            print(transcript)
            return

        # Generate ringkasan
        notes = generate_notes(transcript)

        # Output
        print("=" * 60)
        print(notes)
        print("=" * 60)

        # Simpan ke file
        output_path = args.output
        if not output_path:
            output_dir = Path(__file__).parent.parent / "private" / "output"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{video_id}.txt"

        Path(output_path).write_text(notes, encoding="utf-8")
        print(f"\nDisimpan ke: {output_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
