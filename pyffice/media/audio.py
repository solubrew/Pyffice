"""
Pyffice Audio Module - Handle audio files
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path


class PyfficeAudio:
    """Handle audio file operations"""
    
    SUPPORTED_EXTENSIONS = [
        '.mp3', '.wav', '.flac', '.ogg', '.aac', '.m4a',
        '.wma', '.ape', '.opus', '.webm', '.3gp'
    ]
    MAX_SIZE = 256 * 1024 * 1024  # 256MB
    
    # Configurable size limits per extension
    SIZE_LIMITS = {
        '.mp3': 256 * 1024 * 1024,
        '.wav': 256 * 1024 * 1024,
        '.flac': 256 * 1024 * 1024,
        '.ogg': 256 * 1024 * 1024,
        '.aac': 256 * 1024 * 1024,
        '.m4a': 256 * 1024 * 1024,
    }
    
    def __init__(self, file_path: str, limit: Optional[int] = None):
        self.file_path = Path(file_path)
        self.limit = limit or self.SIZE_LIMITS.get(self.file_path.suffix.lower(), self.MAX_SIZE)
        self._validate()
    
    def _validate(self):
        if self.file_path.stat().st_size > self.limit:
            raise ValueError(f"File exceeds {self.limit}MB limit for {self.file_path.suffix}")
    
    def get_info(self) -> Dict[str, Any]:
        """Get audio file info"""
        stat = self.file_path.stat()
        return {
            'path': str(self.file_path),
            'name': self.file_path.name,
            'extension': self.file_path.suffix,
            'size': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'modified': stat.st_mtime,
        }
    
    def convert(self, output_path: str, format: str = 'mp3', bitrate: str = '192k'):
        """Convert audio (requires ffmpeg)"""
        import subprocess
        cmd = [
            'ffmpeg', '-y', '-i', str(self.file_path),
            '-ab', bitrate, str(output_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    
    def extract_waveform(self, samples: int = 1000) -> list:
        """Extract waveform data (requires ffmpeg)"""
        import subprocess
        import numpy as np
        cmd = [
            'ffmpeg', '-i', str(self.file_path),
            '-ac', '1', '-filter:a', f'aresample=8000',
            '-map', '0:a', '-c:a', 'pcm_s16le',
            '-f', 's16le', '-'
        ]
        result = subprocess.run(cmd, capture_output=True)
        data = np.frombuffer(result.stdout, dtype=np.int16)
        if len(data) > samples:
            indices = np.linspace(0, len(data) - 1, samples)
            data = data[indices]
        return data.tolist()
    
    @classmethod
    def configure_limit(cls, extension: str, limit_mb: int):
        """Configure size limit for specific extension"""
        ext = extension.lower()
        if not ext.startswith('.'):
            ext = '.' + ext
        cls.SIZE_LIMITS[ext] = limit_mb * 1024 * 1024


def get_audio_info(file_path: str) -> Dict[str, Any]:
    """Convenience function to get audio info"""
    return PyfficeAudio(file_path).get_info()


def convert_audio(file_path: str, output_path: str, **kwargs) -> str:
    """Convenience function to convert audio"""
    return PyfficeAudio(file_path).convert(output_path, **kwargs)
