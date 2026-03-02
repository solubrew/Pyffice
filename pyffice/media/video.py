"""
Pyffice Video Module - Handle video files
"""

import os
from typing import Dict, Any, Optional, List
from pathlib import Path


class PyfficeVideo:
    """Handle video file operations"""
    
    SUPPORTED_EXTENSIONS = [
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', 
        '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.ogv'
    ]
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    # Configurable size limits per extension
    SIZE_LIMITS = {
        '.mp4': 256 * 1024 * 1024,
        '.avi': 256 * 1024 * 1024,
        '.mkv': 256 * 1024 * 1024,
        '.mov': 256 * 1024 * 1024,
        '.webm': 256 * 1024 * 1024,
        '.wmv': 256 * 1024 * 1024,
        '.flv': 256 * 1024 * 1024,
    }
    
    def __init__(self, file_path: str, limit: Optional[int] = None):
        self.file_path = Path(file_path)
        self.limit = limit or self.SIZE_LIMITS.get(self.file_path.suffix.lower(), self.MAX_SIZE)
        self._validate()
    
    def _validate(self):
        if self.file_path.stat().st_size > self.limit:
            raise ValueError(f"File exceeds {self.limit}MB limit for {self.file_path.suffix}")
    
    def get_info(self) -> Dict[str, Any]:
        """Get video file info"""
        stat = self.file_path.stat()
        return {
            'path': str(self.file_path),
            'name': self.file_path.name,
            'extension': self.file_path.suffix,
            'size': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'modified': stat.st_mtime,
        }
    
    def extract_frame(self, timestamp: float, output_path: str) -> str:
        """Extract a frame at timestamp (requires ffmpeg)"""
        import subprocess
        output = Path(output_path)
        cmd = [
            'ffmpeg', '-y', '-ss', str(timestamp),
            '-i', str(self.file_path),
            '-vframes', '1', str(output)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return str(output)
    
    def convert(self, output_path: str, codec: str = 'libx264', bitrate: str = '1M'):
        """Convert video (requires ffmpeg)"""
        import subprocess
        cmd = [
            'ffmpeg', '-y', '-i', str(self.file_path),
            '-c:v', codec, '-b:v', bitrate, str(output_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    
    def get_thumbnail(self, timestamp: float = 1.0) -> bytes:
        """Get thumbnail as bytes (requires ffmpeg)"""
        import subprocess
        import io
        cmd = [
            'ffmpeg', '-y', '-ss', str(timestamp),
            '-i', str(self.file_path),
            '-vframes', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'
        ]
        result = subprocess.run(cmd, check=True, capture_output=True)
        return result.stdout
    
    @classmethod
    def configure_limit(cls, extension: str, limit_mb: int):
        """Configure size limit for specific extension"""
        ext = extension.lower()
        if not ext.startswith('.'):
            ext = '.' + ext
        cls.SIZE_LIMITS[ext] = limit_mb * 1024 * 1024


def get_video_info(file_path: str) -> Dict[str, Any]:
    """Convenience function to get video info"""
    return PyfficeVideo(file_path).get_info()


def extract_video_frame(file_path: str, timestamp: float, output_path: str) -> str:
    """Convenience function to extract video frame"""
    return PyfficeVideo(file_path).extract_frame(timestamp, output_path)
