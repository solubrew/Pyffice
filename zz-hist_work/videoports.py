# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Video Ports Module
	description: >
		External video format ports - converts all external video formats to/from
		PyfficeVideo. Includes MP4, AVI, MKV, MOV, WebM, FLV and other formats.
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
from pyffice.video.video import PyfficeVideo
from pyffice.document import PyfficeDocument


# ====================================================================================================================||


class VideoPort(ABC):
    """Abstract base class for video format ports"""
    
    EXTENSIONS: set = set()
    
    @abstractmethod
    def import_file(self, file_path: str) -> PyfficeVideo:
        """Import video file to PyfficeVideo"""
        pass
    
    @abstractmethod
    def export_file(self, video: PyfficeVideo, file_path: str) -> None:
        """Export PyfficeVideo to video file format"""
        pass


class MP4Port(VideoPort):
    """MPEG-4 Part 14 (MP4) format port"""
    
    EXTENSIONS = {'.mp4', '.MP4', '.m4v', '.M4V'}
    
    def import_file(self, file_path: str) -> PyfficeVideo:
        """Import MP4 to PyfficeVideo"""
        path = Path(file_path)
        
        video = PyfficeVideo()
        video.create_new_document(path.stem)
        video.document['source_format'] = 'mp4'
        
        if HAS_FFMPEG:
            try:
                probe = ffmpeg.probe(str(path))
                video.document['duration'] = probe['format'].get('duration')
                video.document['bit_rate'] = probe['format'].get('bit_rate')
                
                # Get video stream info
                for stream in probe['streams']:
                    if stream['codec_type'] == 'video':
                        video.document['width'] = stream.get('width')
                        video.document['height'] = stream.get('height')
                        video.document['codec'] = stream.get('codec_name')
                    elif stream['codec_type'] == 'audio':
                        video.document['has_audio'] = True
            except Exception as e:
                video.document['error'] = str(e)
        
        return video
    
    def export_file(self, video: PyfficeVideo, file_path: str) -> None:
        """Export PyfficeVideo to MP4"""
        path = Path(file_path)
        
        if HAS_FFMPEG:
            pass


class AVIPort(VideoPort):
    """Audio Video Interleave (AVI) format port"""
    
    EXTENSIONS = {'.avi', '.AVI'}
    
    def import_file(self, file_path: str) -> PyfficeVideo:
        """Import AVI to PyfficeVideo"""
        path = Path(file_path)
        
        video = PyfficeVideo()
        video.create_new_document(path.stem)
        video.document['source_format'] = 'avi'
        
        if HAS_FFMPEG:
            try:
                probe = ffmpeg.probe(str(path))
                video.document['duration'] = probe['format'].get('duration')
            except Exception as e:
                video.document['error'] = str(e)
        
        return video
    
    def export_file(self, video: PyfficeVideo, file_path: str) -> None:
        """Export PyfficeVideo to AVI"""
        path = Path(file_path)
        
        if HAS_FFMPEG:
            pass


class MKVPort(VideoPort):
    """Matroska Video (MKV) format port"""
    
    EXTENSIONS = {'.mkv', '.MKV'}
    
    def import_file(self, file_path: str) -> PyfficeVideo:
        """Import MKV to PyfficeVideo"""
        path = Path(file_path)
        
        video = PyfficeVideo()
        video.create_new_document(path.stem)
        video.document['source_format'] = 'mkv'
        
        return video
    
    def export_file(self, video: PyfficeVideo, file_path: str) -> None:
        """Export PyfficeVideo to MKV"""
        path = Path(file_path)
        
        if HAS_FFMPEG:
            pass


class MOVPort(VideoPort):
    """QuickTime File Format (MOV) port"""
    
    EXTENSIONS = {'.mov', '.MOV'}
    
    def import_file(self, file_path: str) -> PyfficeVideo:
        """Import MOV to PyfficeVideo"""
        path = Path(file_path)
        
        video = PyfficeVideo()
        video.create_new_document(path.stem)
        video.document['source_format'] = 'mov'
        
        return video
    
    def export_file(self, video: PyfficeVideo, file_path: str) -> None:
        """Export PyfficeVideo to MOV"""
        path = Path(file_path)
        
        if HAS_FFMPEG:
            pass


class WebMPort(VideoPort):
    """WebM format port"""
    
    EXTENSIONS = {'.webm', '.WEBM'}
    
    def import_file(self, file_path: str) -> PyfficeVideo:
        """Import WebM to PyfficeVideo"""
        path = Path(file_path)
        
        video = PyfficeVideo()
        video.create_new_document(path.stem)
        video.document['source_format'] = 'webm'
        
        return video
    
    def export_file(self, video: PyfficeVideo, file_path: str) -> None:
        """Export PyfficeVideo to WebM"""
        path = Path(file_path)
        
        if HAS_FFMPEG:
            pass


class FLVPort(VideoPort):
    """Flash Video format port"""
    
    EXTENSIONS = {'.flv', '.FLV'}
    
    def import_file(self, file_path: str) -> PyfficeVideo:
        """Import FLV to PyfficeVideo"""
        path = Path(file_path)
        
        video = PyfficeVideo()
        video.create_new_document(path.stem)
        video.document['source_format'] = 'flv'
        
        return video
    
    def export_file(self, video: PyfficeVideo, file_path: str) -> None:
        """Export PyfficeVideo to FLV"""
        path = Path(file_path)
        
        if HAS_FFMPEG:
            pass


class VideoPortsManager:
    """Manages all video format ports and conversions"""
    
    def __init__(self):
        self.ports: Dict[str, VideoPort] = {}
        self._register_default_ports()
    
    def _register_default_ports(self):
        """Register all default video ports"""
        self.ports['mp4'] = MP4Port()
        self.ports['m4v'] = MP4Port()
        self.ports['avi'] = AVIPort()
        self.ports['mkv'] = MKVPort()
        self.ports['mov'] = MOVPort()
        self.ports['webm'] = WebMPort()
        self.ports['flv'] = FLVPort()
    
    def register_port(self, format_name: str, port: VideoPort) -> None:
        """Register a new video format port"""
        self.ports[format_name] = port
    
    def get_port(self, format_name: str) -> Optional[VideoPort]:
        """Get port for a specific format"""
        return self.ports.get(format_name.lower())
    
    def import_file(self, file_path: str) -> PyfficeVideo:
        """Import any supported video file to PyfficeVideo"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        for port in self.ports.values():
            if ext in port.EXTENSIONS:
                return port.import_file(str(path))
        
        raise ValueError(f"Unsupported video format: {ext}")
    
    def export_file(self, video: PyfficeVideo, file_path: str, format_name: str = None) -> None:
        """Export PyfficeVideo to specified format"""
        path = Path(file_path)
        
        if format_name is None:
            format_name = path.suffix.lower().lstrip('.')
        
        port = self.ports.get(format_name.lower())
        if port is None:
            raise ValueError(f"Unsupported video format: {format_name}")
        
        port.export_file(video, str(path))
    
    def convert(self, input_path: str, output_path: str) -> PyfficeVideo:
        """Convert between video formats"""
        vid = self.import_file(input_path)
        self.export_file(vid, output_path)
        return vid
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported format extensions"""
        formats = set()
        for port in self.ports.values():
            formats.update(port.EXTENSIONS)
        return sorted(list(formats))


# Global port manager instance
_port_manager = None

def get_ports_manager() -> VideoPortsManager:
    """Get global video ports manager instance"""
    global _port_manager
    if _port_manager is None:
        _port_manager = VideoPortsManager()
    return _port_manager


def import_video(file_path: str) -> PyfficeVideo:
    """Convenience function to import video file"""
    return get_ports_manager().import_file(file_path)


def export_video(video: PyfficeVideo, file_path: str) -> None:
    """Convenience function to export video file"""
    get_ports_manager().export_file(video, file_path)


def convert_video(input_path: str, output_path: str) -> PyfficeVideo:
    """Convenience function to convert between video formats"""
    return get_ports_manager().convert(input_path, output_path)


# ====================================================================================================================||
