"""
Pyffice Audio Handler
"""

import subprocess
from pathlib import Path
from typing import Optional


def extract(audio_path: str, output_path: str, format: str = "mp3", bitrate: str = "192k") -> None:
    """Extract audio from file or convert format."""
    cmd = ["ffmpeg", "-i", audio_path, "-acodec", "libmp3lame" if format == "mp3" else "aac", 
           "-b:a", bitrate, "-y", output_path]
    subprocess.run(cmd, check=True, capture_output=True)


def convert(input_path: str, output_path: str, codec: str = "libmp3lame", bitrate: str = "192k") -> None:
    """Convert audio to different format."""
    cmd = ["ffmpeg", "-i", input_path, "-acodec", codec, "-b:a", bitrate, "-y", output_path]
    subprocess.run(cmd, check=True, capture_output=True)


def get_duration(audio_path: str) -> float:
    """Get audio duration in seconds."""
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def get_info(audio_path: str) -> dict:
    """Get audio file info."""
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", audio_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    import json
    return json.loads(result.stdout)


def trim(audio_path: str, output_path: str, start: float = 0, duration: Optional[float] = None) -> None:
    """Trim audio file."""
    cmd = ["ffmpeg", "-i", audio_path, "-ss", str(start), "-y"]
    if duration:
        cmd.extend(["-t", str(duration)])
    cmd.append(output_path)
    subprocess.run(cmd, check=True, capture_output=True)
