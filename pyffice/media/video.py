"""
Pyffice Video Handler
"""

import subprocess
from pathlib import Path
from typing import Optional, Tuple


def extract_audio(video_path: str, audio_path: str, codec: str = "libmp3lame") -> None:
    """Extract audio from video file."""
    cmd = ["ffmpeg", "-i", video_path, "-vn", "-acodec", codec, "-y", audio_path]
    subprocess.run(cmd, check=True, capture_output=True)


def trim(video_path: str, output_path: str, start: str = "0", duration: Optional[str] = None) -> None:
    """Trim video file."""
    cmd = ["ffmpeg", "-i", video_path, "-ss", start, "-y"]
    if duration:
        cmd.extend(["-t", duration])
    cmd.append(output_path)
    subprocess.run(cmd, check=True, capture_output=True)


def get_duration(video_path: str) -> float:
    """Get video duration in seconds using ffprobe."""
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def get_resolution(video_path: str) -> Tuple[int, int]:
    """Get video resolution (width, height)."""
    cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    w, h = result.stdout.strip().split("x")
    return int(w), int(h)


def convert(video_path: str, output_path: str, codec: str = "libx264", crf: int = 23) -> None:
    """Convert video to different format/codec."""
    cmd = ["ffmpeg", "-i", video_path, "-c:v", codec, "-crf", str(crf), "-y", output_path]
    subprocess.run(cmd, check=True, capture_output=True)
