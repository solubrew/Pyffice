"""Test Video document generation and import."""
import pytest
from pyffice.media import video as video_doc


def test_extract_audio():
    """Test audio extraction from video."""
    doc = video_doc.PyfficeVideo()
    doc.extract_audio("input.mp4", "output.mp3")
    assert True


def test_trim_video():
    """Test video trimming."""
    doc = video_doc.PyfficeVideo()
    doc.trim_video("input.mp4", "output.mp4", 0, 10)
    assert True
