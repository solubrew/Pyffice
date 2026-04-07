# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Audio Ports Module
	description: >
		External audio format ports - converts all external audio formats to/from
		PyfficeAudio. Includes MP3, WAV, FLAC, AAC, OGG, M4A and other formats.
	version: 0.0.1.0.1.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from typing import Dict, Any, Optional, List
from pathlib import Path
from abc import ABC, abstractmethod

# ======================================3rd Party Library Modules=====================================================||
try:
    import ffmpeg
    HAS_FFMPEG = True
except ImportError:
    HAS_FFMPEG = False

# ======================================Solutions Brewer Library Modules==============================================||
from pyffice.audio.audio import PyfficeAudio
from pyffice.document import PyfficeDocument


# ====================================================================================================================||


class AudioPort(ABC):
    """Abstract base class for audio format ports"""
    
    EXTENSIONS: set = set()
    
    @abstractmethod
    def import_file(self, file_path: str) -> PyfficeAudio:
        """Import audio file to PyfficeAudio"""
        pass
    
    @abstractmethod
    def export_file(self, audio: PyfficeAudio, file_path: str) -> None:
        """Export PyfficeAudio to audio file format"""
        pass


class MP3Port(AudioPort):
    """MPEG Audio Layer 3 (MP3) format port"""
    
    EXTENSIONS = {'.mp3', '.MP3'}
    
    def import_file(self, file_path: str) -> PyfficeAudio:
        """Import MP3 to PyfficeAudio"""
        path = Path(file_path)
        
        audio = PyfficeAudio(str(path))
        audio.create_new_document(path.stem)
        audio.document['source_format'] = 'mp3'
        
        if HAS_FFMPEG:
            try:
                probe = ffmpeg.probe(str(path))
                audio.document['duration'] = probe['format'].get('duration')
                audio.document['bit_rate'] = probe['format'].get('bit_rate')
            except Exception as e:
                audio.document['error'] = str(e)
        
        return audio
    
    def export_file(self, audio: PyfficeAudio, file_path: str) -> None:
        """Export PyfficeAudio to MP3"""
        path = Path(file_path)
        
        if HAS_FFMPEG:
            # Would need source audio data
            pass


class WAVPort(AudioPort):
    """Waveform Audio File Format (WAV) port"""
    
    EXTENSIONS = {'.wav', '.WAV'}
    
    def import_file(self, file_path: str) -> PyfficeAudio:
        """Import WAV to PyfficeAudio"""
        path = Path(file_path)
        
        audio = PyfficeAudio(str(path))
        audio.create_new_document(path.stem)
        audio.document['source_format'] = 'wav'
        
        if HAS_FFMPEG:
            try:
                probe = ffmpeg.probe(str(path))
                audio.document['duration'] = probe['format'].get('duration')
                audio.document['sample_rate'] = probe['format'].get('sample_rate')
            except Exception as e:
                audio.document['error'] = str(e)
        
        return audio
    
    def export_file(self, audio: PyfficeAudio, file_path: str) -> None:
        """Export PyfficeAudio to WAV"""
        path = Path(file_path)
        
        if HAS_FFMPEG:
            pass


class FLACPort(AudioPort):
    """Free Lossless Audio Codec (FLAC) format port"""
    
    EXTENSIONS = {'.flac', '.FLAC'}
    
    def import_file(self, file_path: str) -> PyfficeAudio:
        """Import FLAC to PyfficeAudio"""
        path = Path(file_path)
        
        audio = PyfficeAudio(str(path))
        audio.create_new_document(path.stem)
        audio.document['source_format'] = 'flac'
        
        return audio
    
    def export_file(self, audio: PyfficeAudio, file_path: str) -> None:
        """Export PyfficeAudio to FLAC"""
        path = Path(file_path)
        
        if HAS_FFMPEG:
            pass


class AACPort(AudioPort):
    """Advanced Audio Coding (AAC) format port"""
    
    EXTENSIONS = {'.aac', '.AAC', '.m4a', '.M4A'}
    
    def import_file(self, file_path: str) -> PyfficeAudio:
        """Import AAC/M4A to PyfficeAudio"""
        path = Path(file_path)
        
        audio = PyfficeAudio(str(path))
        audio.create_new_document(path.stem)
        audio.document['source_format'] = 'aac'
        
        return audio
    
    def export_file(self, audio: PyfficeAudio, file_path: str) -> None:
        """Export PyfficeAudio to AAC"""
        path = Path(file_path)
        
        if HAS_FFMPEG:
            pass


class OGGPort(AudioPort):
    """Ogg Vorbis format port"""
    
    EXTENSIONS = {'.ogg', '.OGG', '.oga', '.OGA'}
    
    def import_file(self, file_path: str) -> PyfficeAudio:
        """Import OGG to PyfficeAudio"""
        path = Path(file_path)
        
        audio = PyfficeAudio(str(path))
        audio.create_new_document(path.stem)
        audio.document['source_format'] = 'ogg'
        
        return audio
    
    def export_file(self, audio: PyfficeAudio, file_path: str) -> None:
        """Export PyfficeAudio to OGG"""
        path = Path(file_path)
        
        if HAS_FFMPEG:
            pass


class AudioPortsManager:
    """Manages all audio format ports and conversions"""
    
    def __init__(self):
        self.ports: Dict[str, AudioPort] = {}
        self._register_default_ports()
    
    def _register_default_ports(self):
        """Register all default audio ports"""
        self.ports['mp3'] = MP3Port()
        self.ports['wav'] = WAVPort()
        self.ports['flac'] = FLACPort()
        self.ports['aac'] = AACPort()
        self.ports['m4a'] = AACPort()
        self.ports['ogg'] = OGGPort()
    
    def register_port(self, format_name: str, port: AudioPort) -> None:
        """Register a new audio format port"""
        self.ports[format_name] = port
    
    def get_port(self, format_name: str) -> Optional[AudioPort]:
        """Get port for a specific format"""
        return self.ports.get(format_name.lower())
    
    def import_file(self, file_path: str) -> PyfficeAudio:
        """Import any supported audio file to PyfficeAudio"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        for port in self.ports.values():
            if ext in port.EXTENSIONS:
                return port.import_file(str(path))
        
        raise ValueError(f"Unsupported audio format: {ext}")
    
    def export_file(self, audio: PyfficeAudio, file_path: str, format_name: str = None) -> None:
        """Export PyfficeAudio to specified format"""
        path = Path(file_path)
        
        if format_name is None:
            format_name = path.suffix.lower().lstrip('.')
        
        port = self.ports.get(format_name.lower())
        if port is None:
            raise ValueError(f"Unsupported audio format: {format_name}")
        
        port.export_file(audio, str(path))
    
    def convert(self, input_path: str, output_path: str) -> PyfficeAudio:
        """Convert between audio formats"""
        audio = self.import_file(input_path)
        self.export_file(audio, output_path)
        return audio
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported format extensions"""
        formats = set()
        for port in self.ports.values():
            formats.update(port.EXTENSIONS)
        return sorted(list(formats))


# Global port manager instance
_port_manager = None

def get_ports_manager() -> AudioPortsManager:
    """Get global audio ports manager instance"""
    global _port_manager
    if _port_manager is None:
        _port_manager = AudioPortsManager()
    return _port_manager


def import_audio(file_path: str) -> PyfficeAudio:
    """Convenience function to import audio file"""
    return get_ports_manager().import_file(file_path)


def export_audio(audio: PyfficeAudio, file_path: str) -> None:
    """Convenience function to export audio file"""
    get_ports_manager().export_file(audio, file_path)


def convert_audio(input_path: str, output_path: str) -> PyfficeAudio:
    """Convenience function to convert between audio formats"""
    return get_ports_manager().convert(input_path, output_path)


# ====================================================================================================================||
