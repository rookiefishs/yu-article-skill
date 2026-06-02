#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Xiaomi MiMo TTS audio with the Bingtang voice.

The script keeps the existing Azure/Microsoft TTS workflow untouched and offers
a separate Xiaomi MiMo path for short-video narration.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1"
DEFAULT_MODEL = "mimo-v2.5-tts"
DEFAULT_VOICE = "\u51b0\u7cd6"
DEFAULT_STYLE = (
    "\u4e2d\u6587\u79d1\u6280\u77ed\u89c6\u9891\u65c1\u767d\uff0c"
    "\u6e05\u6670\u3001\u81ea\u7136\u3001\u53e3\u8bed\u5316\uff0c"
    "\u8bed\u901f\u7565\u5feb\u4f46\u4e0d\u8981\u6025\uff0c"
    "\u907f\u514d\u64ad\u97f3\u8154\u3002"
)


def read_user_env_on_windows(name: str) -> str | None:
    if os.name != "nt":
        return None
    try:
        import winreg  # type: ignore

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
            return value
    except Exception:
        return None


def get_api_key() -> str:
    api_key = os.environ.get("MIMO_API_KEY") or read_user_env_on_windows("MIMO_API_KEY")
    if not api_key:
        raise SystemExit("MIMO_API_KEY is not set")
    return api_key


def extract_narration(markdown: str) -> str:
    markers = [
        "## \u6574\u6761\u8fde\u8d2f\u7248",
        "## \u5b8c\u6574\u6587\u6848",
    ]
    for marker in markers:
        if marker in markdown:
            return clean_text(markdown.split(marker, 1)[1])
    return clean_text(markdown)


def clean_text(text: str) -> str:
    lines: list[str] = []
    skip_fence = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            skip_fence = not skip_fence
            continue
        if skip_fence:
            continue
        if not line or line == "---":
            continue
        if line.startswith("#"):
            continue
        line = re.sub(r"^\[[\d:]+\]\s*", "", line)
        line = re.sub(r"^\*\*(.*?)\*\*\s*", r"\1", line)
        line = re.sub(r"^>\s*", "", line)
        line = re.sub(r"<break\s+time=\"[^\"]+\"\s*/?>", " ", line, flags=re.IGNORECASE)
        line = re.sub(r"<phoneme\b[^>]*>(.*?)</phoneme>", r"\1", line, flags=re.IGNORECASE)
        line = re.sub(r"<[^>]+>", " ", line)
        line = line.replace("`", "")
        lines.append(line)
    return normalize_plain_narration(" ".join(lines))


def normalize_plain_narration(text: str) -> str:
    text = convert_digits_for_tts(text)
    text = re.sub(r"[，。！？、；：,.!?;:\"'“”‘’（）()【】\[\]{}《》<>「」『』—–_\-+*=#/@\\|~￥$%^&]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def convert_digits_for_tts(text: str) -> str:
    digits = {
        "0": "零",
        "1": "一",
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "七",
        "8": "八",
        "9": "九",
    }
    return re.sub(r"\d+", lambda match: "".join(digits[ch] for ch in match.group(0)), text)


def read_input(args: argparse.Namespace) -> str:
    if args.text:
        return args.text.strip()
    if not args.input:
        raise SystemExit("Please provide --input <file> or --text <text>")
    content = Path(args.input).read_text(encoding="utf-8")
    text = extract_narration(content)
    if not text:
        raise SystemExit("No narration text extracted")
    return text


def default_output_path(args: argparse.Namespace) -> Path:
    if args.output:
        return Path(args.output)
    if args.input:
        input_path = Path(args.input)
        return input_path.with_name(f"{input_path.stem}-\u5c0f\u7c73TTS-\u51b0\u7cd6.wav")
    return Path("mimo-tts-bingtang.wav")


def request_tts(
    *,
    api_key: str,
    base_url: str,
    model: str,
    voice: str,
    audio_format: str,
    style: str,
    text: str,
) -> bytes:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": style},
            {"role": "assistant", "content": text},
        ],
        "audio": {"format": audio_format, "voice": voice},
        "stream": False,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=240) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"MiMo TTS request failed: HTTP {exc.code}: {detail}") from exc

    data = json.loads(body)
    message = data["choices"][0]["message"]
    audio = message.get("audio") or {}
    audio_data = audio.get("data")
    if not audio_data:
        raise SystemExit("MiMo TTS response did not include audio data")
    return base64.b64decode(audio_data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Xiaomi MiMo Bingtang TTS audio.")
    parser.add_argument("--input", "-i", help="Input narration markdown/text file")
    parser.add_argument("--text", "-t", help="Direct narration text")
    parser.add_argument("--output", "-o", help="Output audio path, defaults to *-小米TTS-冰糖.wav")
    parser.add_argument("--style", default=DEFAULT_STYLE, help="Natural language style instruction")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="MiMo voice, default: 冰糖")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="MiMo TTS model")
    parser.add_argument("--format", default="wav", choices=["wav", "pcm16"], help="Output audio format")
    parser.add_argument("--base-url", default=os.environ.get("MIMO_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--save-text", help="Optional path to save extracted narration text")
    args = parser.parse_args()

    text = read_input(args)
    output = default_output_path(args)
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.save_text:
        Path(args.save_text).write_text(text, encoding="utf-8")

    audio_bytes = request_tts(
        api_key=get_api_key(),
        base_url=args.base_url,
        model=args.model,
        voice=args.voice,
        audio_format=args.format,
        style=args.style,
        text=text,
    )
    output.write_bytes(audio_bytes)
    print(json.dumps({"output": str(output), "voice": args.voice, "model": args.model}, ensure_ascii=False))


if __name__ == "__main__":
    main()
