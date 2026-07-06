"""Test Audio document generation and import."""
import pytest
from pyffice.media import audio as audio_doc


def test_extract_audio():
    """Test audio extraction."""
    doc = audio_doc.PyfficeAudio()
    doc.extract_audio("input.mp4", "output.mp3")
    assert True


def test_convert_audio():
    """Test audio conversion."""
    doc = audio_doc.PyfficeAudio()
    doc.convert_audio("input.mp3", "output.wav")
    assert True
