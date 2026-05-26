"""
extract_transcript.py - Download dan parse subtitle YouTube jadi plain text

Usage:
    python extract_transcript.py <URL_YOUTUBE> [--lang id]

Output: private/temp/<VIDEO_ID>.txt (transkrip bersih dengan timestamp)
Stdout: path file yang dihasilkan
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

TEMP_DIR = Path(__file__).parent.parent / "private" / "temp"


def extract_video_id(url: str) -> str:
    patterns = [
        r'(?:v=|/v/|youtu\.be/|/live/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Cannot extract video ID from: {url}")


def download_vtt(url: str, lang: str, video_id: str) -> Path:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    output_template = str(TEMP_DIR / "%(id)s")

    # Try auto-subs first, then manual subs
    attempts = [
        ["python", "-m", "yt_dlp", "--write-auto-subs", "--sub-lang", lang,
         "--sub-format", "vtt", "--skip-download", "--output", output_template, url],
        ["python", "-m", "yt_dlp", "--write-subs", "--sub-lang", lang,
         "--sub-format", "vtt", "--skip-download", "--output", output_template, url],
    ]

    for cmd in attempts:
        result = subprocess.run(cmd, capture_output=True, text=True)
        vtt_files = list(TEMP_DIR.glob(f"{video_id}*.vtt"))
        if vtt_files:
            return vtt_files[0]

    # Try English as last resort
    if lang != "en":
        cmd = ["python", "-m", "yt_dlp", "--write-auto-subs", "--sub-lang", "en",
               "--sub-format", "vtt", "--skip-download", "--output", output_template, url]
        subprocess.run(cmd, capture_output=True, text=True)
        vtt_files = list(TEMP_DIR.glob(f"{video_id}*.vtt"))
        if vtt_files:
            return vtt_files[0]

    print("ERROR: No subtitle found", file=sys.stderr)
    sys.exit(1)


def vtt_to_transcript(vtt_path: Path) -> str:
    vtt = vtt_path.read_text(encoding="utf-8")
    lines = vtt.split("\n")
    timestamp_re = re.compile(
        r'(\d{1,2}):(\d{2}):(\d{2})\.\d{3}\s*-->'
    )
    tag_re = re.compile(r'<[^>]+>')

    result = []
    current_time = None
    prev_text = ""

    for line in lines:
        line = line.strip()

        if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or \
           line.startswith("Language:") or line.isdigit() or "align:" in line:
            match = timestamp_re.search(line)
            if match:
                h, m, s = int(match.group(1)), int(match.group(2)), int(match.group(3))
                current_time = f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m}:{s:02d}"
            continue

        match = timestamp_re.match(line)
        if match:
            h, m, s = int(match.group(1)), int(match.group(2)), int(match.group(3))
            current_time = f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m}:{s:02d}"
            continue

        clean = tag_re.sub("", line).strip()
        if not clean or clean == prev_text:
            continue
        prev_text = clean

        if current_time:
            result.append(f"[{current_time}] {clean}")

    return "\n".join(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--lang", default="id")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    vtt_path = download_vtt(args.url, args.lang, video_id)
    transcript = vtt_to_transcript(vtt_path)

    # Save transcript
    out_path = TEMP_DIR / f"{video_id}.txt"
    out_path.write_text(transcript, encoding="utf-8")

    # Cleanup VTT
    vtt_path.unlink(missing_ok=True)

    # Output path to stdout for Kiro to read
    print(str(out_path))


if __name__ == "__main__":
    main()
